from akca.db import store
from akca.domain import account
from akca.domain import backup 
from akca.domain import category 
from akca.domain import purchase 
from akca.domain import stats 

import click

class Service():
    def __init__(self, store: store.Store):
        self.store = store
    create_account = account.create
    edit_account = account.edit
    delete_account = account.delete
    list_accounts = account.list
