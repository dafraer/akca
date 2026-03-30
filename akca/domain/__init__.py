from akca.store import Store 
from akca.domain import account, backup, category, purchase, stats


class Service():
    def __init__(self, store: Store):
        self.store = store
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
