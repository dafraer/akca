from datetime import date

import click

from akca.app.helpers import format_table
from akca.domain.purchase import CreatePurchaseParams, EditPurchaseParams, ListPurchasesParams

TODAY = str(date.today())
FROM_DATE = "2001-01-01"
ROWS_LIMIT = 100
DATE_FORMATS = ["%Y-%m-%d", "%Y%m%d"]

@click.group
def purchase():
    pass


@purchase.command
@click.option("-n", "--name", type=str, required=True)
@click.option("-a", "--amount", type=float, required=True)
@click.option("-d", "--date", "date_", type=click.DateTime(formats=DATE_FORMATS), default=TODAY)
@click.option("-desc", "--desc", type=str)
@click.option("-m", "--merchant", type=str, default=None)
@click.option("-c", "--category", type=str, required=True)
@click.option("-acc", "--account", type=str, required=True)
@click.pass_context
def new(ctx, name: str, amount: float, date_: date, desc: str, merchant: str, category: str, account: str):
    try:
        id_ = ctx.obj.create_purchase(CreatePurchaseParams(name, amount, desc, category, date_.date(), account, merchant))
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
@click.option("-desc", "--description", type=str)
@click.option("-m", "--merchant", type=str, default=None)
@click.option("-c", "--category", type=str)
@click.option("-d", "--date", "date_", type=click.DateTime(formats=DATE_FORMATS), default=None)
@click.option("-acc", "--account", type=str)
@click.pass_context
def edit(ctx, id: int, name: str, amount: float, description: str, merchant: str, category: str, date_: date, account: str):
    try:
        ctx.obj.edit_purchase(EditPurchaseParams(id, name, amount, description, category, date_.date() if date_ else None, account, merchant))
    except Exception as e:
        ctx.obj.logger.error(f"Error editing a purchase: {e}")
        raise SystemExit(1)
    click.echo(f"Purchase has been edited successfully: {id=} {name=} {amount=} {description=} {category=}")


@purchase.command
@click.option("-n", "--name", type=str)
@click.option("-from", "--from_date", type=click.DateTime(formats=DATE_FORMATS), default=FROM_DATE)
@click.option("-to", "--to_date", type=click.DateTime(formats=DATE_FORMATS), default=TODAY)
@click.option("-m", "--merchant", type=str, default=None)
@click.option("-c", "--category", type=str)
@click.option("-s", "--sort", type=click.Choice(["date", "amount", "alphabet"]))
@click.option("-l", "--limit", type=click.IntRange(min=1, max=ROWS_LIMIT), default=10)
@click.pass_context
def ls(ctx, name: str, from_date, to_date, merchant: str, category: str, sort: str, limit: int):
    from_date = from_date.date()
    to_date = to_date.date()
    if from_date > to_date:
        raise click.UsageError("to_date must be after from_date")
    try:
        purchases = ctx.obj.list_purchases(ListPurchasesParams(name, from_date, to_date, category, sort, limit, merchant))
    except Exception as e:
        ctx.obj.logger.error(f"Error listing purchases: {e}")
        raise SystemExit(1)
    click.echo(format_table(["id", "amount", "item_name", "description", "merchant", "date", "category_id", "account_id"], purchases))
