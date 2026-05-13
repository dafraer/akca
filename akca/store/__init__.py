import sqlite3
import logging
import os

from akca.store import account, backup, category, purchase, stats

def store_path() -> str:
    base = os.environ.get("XDG_DATA_HOME") or os.path.expanduser("~/.local/share")
    return os.path.join(base, "akca", "akca.db")

class Store:
    def __init__(self, logger: logging.Logger, path=store_path()):
        self.logger = logger
        self.path = path

        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        logger.info(f"Connected to {path}")

        cur = self.conn.cursor()

        cur.execute("""
                        create table if not exists accounts (
                            id integer primary key autoincrement,
                            name text not null,
                            currency text not null
                        );
                    """)

        logger.info("Initialized accounts table")

        cur.execute("""
                        create table if not exists categories (
                            id integer primary key autoincrement,
                            name text not null unique,
                            parent_id integer,
                            foreign key (parent_id) references categories(id)
                        );
                    """)

        logger.info("Initialized categories table")

        cur.execute("""
                        create table if not exists purchases ( 
                            id integer primary key autoincrement,
                            amount integer not null,
                            item_name text not null,
                            description text,
                            date integer,
                            category_id integer not null,
                            account_id integer not null,
                            foreign key (category_id) references categories(id),
                            foreign key (account_id) references accounts(id)
                        );
                    """)

        logger.info("Initialized purchases table")

        cur.execute("create index if not exists idx_purchases_account_id on purchases(account_id);")
        cur.execute("create index if not exists idx_purchases_category_id on purchases(category_id);")
        cur.execute("create index if not exists idx_purchases_date on purchases(date);")
        cur.execute("create index if not exists idx_categories_parent_id on categories(parent_id);")
        cur.execute("create index if not exists idx_categories_name on categories(name);")

        logger.info("Initialized indexes")

    create_account = account.create
    edit_account = account.edit
    delete_account = account.delete
    list_accounts = account.list_
    backup = backup.backup
    create_category = category.create
    edit_category = category.edit
    delete_category = category.delete
    category_tree = category.tree
    list_categories = category.list_
    check_category_cycle = category.check_cycle
    create_purchase = purchase.create
    edit_purchase = purchase.edit
    delete_purchase = purchase.delete
    list_purchases = purchase.list_
    trends_stats = stats.trends
    general_stats = stats.general
