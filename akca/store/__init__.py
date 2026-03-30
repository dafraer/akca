import sqlite3

from akca.store import account, backup, category, purchase, stats
 
STORE_PATH = "/Users/kamil/Downloads/projects/akca-cli/akca.db"

class Store():
    def __init__(self, path=STORE_PATH):
        self.conn = sqlite3.connect(path) 
        cur = self.conn.cursor()
        cur.execute("""
                        create table if not exists accounts (
                            id integer primary key autoincrement,
                            name text not null,
                            currency text not null
                        );
                    """)
        cur.execute("""
                        create table if not exists categories (
                            id integer primary key autoincrement,
                            name text not null,
                            parent_id integer not null,
                            foreign key (parent_id) references categories(id)
                        );
                    """)
        cur.execute("""
                        create table if not exists purchases ( 
                            id integer primary key autoincrement,
                            amount integer not null,
                            item_name text not null,
                            description text,
                            purchased_at integer,
                            category_id integer,
                            account_id integer not null,
                            foreign key (category_id) references categories(id),
                            foreign key (account_id) references accounts(id)
                        );
                    """)
         

    create_account = account.create
    edit_account = account.edit
    delete_account = account.delete
    list_accounts = account.list
    backup = backup.backup
    create_category = category.create
    edit_category = category.edit
    delete_category = category.delete
    category_tree = category.tree
    list_categories = category.list
    create_purchase = purchase.create
    edit_purchase = purchase.edit
    delete_purchase = purchase.delete
    list_purchases = purchase.list
    stats = stats.stats
        