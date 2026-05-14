import logging

from akca.store import Store 
from akca.domain import account, backup, category, merchant, purchase, stats


class Service:
    def __init__(self, store: Store, logger: logging.Logger):
        self.store = store
        self.logger = logger
        logger.info("Initialized service")
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
    create_merchant = merchant.create
    delete_merchant = merchant.delete
    list_merchants = merchant.list_
    create_purchase = purchase.create
    edit_purchase = purchase.edit
    delete_purchase = purchase.delete
    list_purchases = purchase.list_
    trends_stats = stats.trends
    general_stats = stats.general
