import click

from akca.app.helpers import format_table
ROWS_LIMIT = 100

@click.group
def merchant():
    pass

@merchant.command
@click.option("--name", type=str, required=True)
@click.pass_context
def new(ctx, name: str):
    try:
        id_ = ctx.obj.create_merchant(name)
    except Exception as e:
        ctx.obj.logger.error(f"Error creating merchant: {e}")
        raise SystemExit(1)
    click.echo(f"New merchant has been created successfully: id={id_}")


@merchant.command
@click.option("--name", type=str, required=True)
@click.pass_context
def rm(ctx, name: str):
    try:
        ctx.obj.delete_merchant(name)
    except Exception as e:
        ctx.obj.logger.error(f"Error deleting merchant: {e}")
        raise SystemExit(1)
    click.echo(f"Merchant has been deleted successfully: {name=}")


@merchant.command
@click.option("--limit", type=click.IntRange(min=1, max=ROWS_LIMIT), default=ROWS_LIMIT)
@click.option("--order_by",
              type=click.Choice(["id", "name"], case_sensitive=True),
              default="id")
@click.pass_context
def ls(ctx, limit: int, order_by: str):
    try:
        merchants = ctx.obj.list_merchants(limit, order_by)
    except Exception as e:
        ctx.obj.logger.error(f"Error listing merchants: {e}")
        raise SystemExit(1)
    output = format_table(["id", "name"], merchants)
    click.echo(output)
