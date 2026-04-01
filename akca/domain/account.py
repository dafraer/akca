import click

def create(self, name: str, currency: str) -> int:
    return self.store.create_account(name, currency)

def edit(self, id_: int, name: str, currency: str):
    self.store.edit_account(id_, name, currency)


def delete(self, id_: int):
    self.store.delete_account(id_)


def list_(self, limit: int, order_by: str) -> list[tuple]:
    return self.store.list_accounts(limit, order_by)