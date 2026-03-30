import click

def create(self, name: str, currency: str) -> int:
    click.echo(f"new acc created: {name=}, {currency=}")


def edit(self, id: int, name: str, currency: str) -> int:
    click.echo(f"acc edited: {id=} {name=}, {currency=}")


def delete(self, id: int) -> int:
    click.echo(f"acc deleted: {id=}")


def list(self):
    click.echo(f"accounts listed")