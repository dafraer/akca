import click


@click.group
def account():
    pass

@account.command
@click.option("-n", "--name", type=str, required=True)
@click.option("-c", "--currency", type=str, required=True)
@click.pass_context
def new(ctx, name: str, currency: str):
   ctx.obj.create_account(name, currency) 

@account.command
@click.option("--id", type=int, required=True)
@click.pass_context
def rm(ctx, id: int):
    click.echo(f"removed account with {id=}")

@account.command
@click.option("--id", type=int, required=True)
@click.option("-n", "--name", type=str)
@click.option("-c", "--currency", type=str)
@click.pass_context
def edit(ctx, id: int, name: str, currency: str):
    click.echo(f"edited account with {id=}, {name=}, {currency=}")

@account.command
@click.pass_context
def ls(ctx):
    click.echo("Listing all accounts")




