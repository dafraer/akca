import os

import click

MAX_LIMIT = 100

@click.group
def account():
    pass

@account.command
@click.option("--name", type=str, required=True)
@click.option("--currency", type=str, required=True)
@click.pass_context
def new(ctx, name: str, currency: str):
    try:
        id_ = ctx.obj.create_account(name, currency)
    except Exception as e:
        ctx.obj.logger.error(f"Error creating account: {e}")
        raise SystemExit(1)
    click.echo(f"New account has been created successfully: id={id_}")


@account.command
@click.option("--id", type=click.IntRange(min=1), required=True)
@click.pass_context
def rm(ctx, id: int):
    try:
        ctx.obj.delete_account(id)
    except Exception as e:
        ctx.obj.logger.error(f"Error deleting account: {e}")
        raise SystemExit(1)
    click.echo(f"Account has been deleted successfully")

@account.command
@click.option("--id", type=click.IntRange(min=1), required=True)
@click.option("-n", "--name", type=str)
@click.option("-c", "--currency", type=str)
@click.pass_context
def edit(ctx, id: int, name: str, currency: str):
    try:
        ctx.obj.edit_account(id, name, currency)
    except Exception as e:
        ctx.obj.logger.error(f"Error updating account: {e}")
        raise SystemExit(1)
    click.echo("Account has been updated successfully")


@account.command
@click.option("--limit", type=click.IntRange(min=1, max=MAX_LIMIT), default=10)
@click.option("--order_by",
              type=click.Choice(["id", "name", "currency"], case_sensitive=True),
              default="id")
@click.pass_context
def ls(ctx, limit: int, order_by: str):
    try:
        accounts = ctx.obj.list_accounts(limit, order_by)
    except Exception as e:
        ctx.obj.logger.error(f"Error listing accounts: {e}")
        raise SystemExit(1)
    columns, rows = os.get_terminal_size()

    #TODO: Remake into a separate function
    output = "+" + "-" * (columns - 2) + "+"
    section_width = (columns - 4)//3
    output = "\n".join([output, "| id" + (" " * (section_width-3)) + "| name" + (" " * (section_width-5)) + "| currency" + (" " * (section_width-9))])
    click.echo(output)




