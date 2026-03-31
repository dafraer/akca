import click

@click.group
def account():
    pass

@account.command
@click.option("-n", "--name", type=str, required=True)
@click.option("-c", "--currency", type=str, required=True)
@click.pass_context
def new(ctx, name: str, currency: str):
    try:
        id = ctx.obj.create_account(name, currency) 
    except:
        click.echo("Error creating new account")
        raise SystemExit(1)
    else:
        click.echo(f"New account has been created successfully, {id=}")


@account.command
@click.option("--id", type=int, required=True)
@click.pass_context
def rm(ctx, id: int):
    ctx.obj.delete_account(id)


@account.command
@click.option("--id", type=int, required=True)
@click.option("-n", "--name", type=str)
@click.option("-c", "--currency", type=str)
@click.pass_context
def edit(ctx, id: int, name: str, currency: str):
    ctx.obj.edit_account(id, name, currency)


@account.command
@click.pass_context
def ls(ctx):
    accounts = ctx.obj.list_accounts()
    click.echo(accounts)




