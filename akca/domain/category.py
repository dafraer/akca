import click

def create(self, name: str, parent: int):
    click.echo(f"new category created: {name=}, {parent=}")
def edit(self, id: int, name: str, parent: int):
    click.echo(f"category edited: {id=}, {name=}, {parent=}")
def delete(self, id: int):
    click.echo(f"category deleted: {id=}")
def tree(self):
    click.echo(f"category tree shown")
def list(self):
    click.echo(f"categories listed")
