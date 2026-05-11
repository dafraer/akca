from datetime import datetime

import click

from akca.app.helpers import format_table
from akca.domain.purchase import CreatePurchaseParams, EditPurchaseParams, ListPurchasesParams

TIME=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
FROM_DATE="01/01/2001"
TO_DATE=datetime.today().strftime("%d/%m/%Y")
ROWS_LIMIT=100

@click.group
def purchase():
    pass


@purchase.command
@click.option("-n", "--name", type=str, required=True)
@click.option("-a", "--amount", type=float, required=True)
@click.option("-d", "--desc", type=str)
@click.option("-c", "--category", type=str, required=True)
@click.option("-t", "--time", type=str, default=TIME)
@click.option("-acc", "--account", type=str, required=True)
@click.pass_context
def new(ctx, name: str, amount: float, desc: str, category: str, time: str, account: str):
    try:
        id_ = ctx.obj.create_purchase(CreatePurchaseParams(name, amount, desc, category, time, account))
    except Exception as e:
        ctx.obj.logger.error(f"Error adding a purchase: {e}")
        raise SystemExit(1)
    click.echo(f"New purchase has been added successfully: {id_=}")


@purchase.command
@click.option("--id", type=int, required=True)
@click.pass_context
def rm(ctx, id: int):
    try:
        ctx.obj.delete_purchase(id)
    except Exception as e:
        ctx.obj.logger.error(f"Error deleting a purchase: {e}")
        raise SystemExit(1)
    click.echo(f"Purchase has been deleted successfully: {id=}")


@purchase.command
@click.option("--id", type=int, required=True)
@click.option("-n", "--name", type=str)
@click.option("-a", "--amount", type=float)
@click.option("-d", "--description", type=str)
@click.option("-c", "--category", type=str)
@click.option("-t", "--time", type=str)
@click.option("-acc", "--account", type=str)
@click.pass_context
def edit(ctx, id: int, name: str, amount: float, description: str, category: str, time: str, account: str):
    try:
        ctx.obj.edit_purchase(EditPurchaseParams(id, name, amount, description, category, time, account))
    except Exception as e:
        ctx.obj.logger.error(f"Error editing a purchase: {e}")
        raise SystemExit(1)
    click.echo(f"Purchase has been edited successfully: {id=} {name=} {amount=} {description=} {category=} {time=}")


@purchase.command
@click.option("-n", "--name", type=str)
@click.option("-from", "--from_date", type=str, default=FROM_DATE)
@click.option("-to", "--to_date", type=str, default=TO_DATE)
@click.option("-c", "--category", type=str)
@click.option("-s", "--sort", type=click.Choice(["time", "amount", "alphabet"]))
@click.option("-l", "--limit", type=click.IntRange(min=1, max=ROWS_LIMIT), default=10 )
@click.pass_context
def ls(ctx, name: str, from_date: str, to_date: str, category: str, sort: str, limit: int):
    try:
        purchases = ctx.obj.list_purchases(ListPurchasesParams(name, from_date, to_date, category, sort, limit))
    except Exception as e:
        ctx.obj.logger.error(f"Error listing purchases: {e}")
        raise SystemExit(1)
    click.echo(format_table(["id", "amount", "item_name", "description", "purchased_at", "category_id", "account_id"], purchases))