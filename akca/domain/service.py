from akca.db import store
import click

class Service():
    def __init__(self, store: store.Store):
        self.store = store
    def create_account(self, name: str, currency: str) -> int:
        click.echo(f"new acc created: {name=}, {currency=}")
    def edit_account(self, id: int, name: str, currency: str) -> int:
        pass
    def delete_account(self, id: int):
        pass
    def list_account(self):
        pass