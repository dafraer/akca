import click


@click.group
def account():
    pass

@account.command
@click.option("-n", "--name", type=str, required=True)
@click.option("-c", "--currency", type=str, required=True)
def new(name: str, currency: str):
    click.echo(f"new acc created: {name=}, {currency=}")

@account.command
@click.option("--id", type=int, required=True)
def rm(id: int):
    click.echo(f"removed account with {id=}")

@account.command
@click.option("--id", type=int, required=True)
@click.option("-n", "--name", type=str)
@click.option("-c", "--currency", type=str)
def edit(id: int, name: str, currency: str):
    click.echo(f"edited account with {id=}, {name=}, {currency=}")

@account.command
def ls():
    click.echo("Listing all accounts")




