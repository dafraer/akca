import click

def create(self, name: str, amount: int, desc: str, category: int, time: str):
    click.echo(f"new purchase created: {name=}, {amount=}, {desc=}, {category=}, {time=}")
def edit(self, id: int, name: str, amount: int, description: str, category: str, time: str):
    click.echo(f"purchase edited: {id=}, {name=}, {amount=}, {description=}, {category=}, {time=}")
def delete(self, id: int):
    click.echo(f"purchase deleted: {id=}")
def list(self, name: str, from_date: str, to_date: str, category: str, sort: str, max: int):
    click.echo(f"purchases listed: {name=}, {from_date=}, {to_date=}, {category=}, {sort=}, {max=}")
