import click

from akca.app.helpers import format_tree, format_table

ROWS_LIMIT = 100

@click.group
def category():
    pass

@category.command
@click.option("-n", "--name", type=str, required=True)
@click.option("-p", "--parent", type=str)
@click.pass_context
def new(ctx, name: str, parent: str):
    try:
        id_ = ctx.obj.create_category(name, parent)
    except Exception as e:
        ctx.obj.logger.error(f"Error creating a category: {e}")
        raise SystemExit(1)
    click.echo(f"New category has been created successfully: id={id_}")

@category.command
@click.option("--name", type=str, required=True)
@click.pass_context
def rm(ctx, name: str):
    try:
        ctx.obj.delete_category(name)
    except Exception as e:
        ctx.obj.logger.error(f"Error deleting a category: {e}")
        raise SystemExit(1)
    click.echo(f"Category has been deleted successfully: {name=}")

@category.command
@click.option("--id", type=int, required=True)
@click.option("-n", "--name", type=str)
@click.option("-p", "--parent", type=str)
@click.pass_context
def edit(ctx, id: int, name: str, parent: str):
    try:
        ctx.obj.edit_category(id, name, parent)
    except Exception as e:
        ctx.obj.logger.error(f"Error editing a category: {e}")
        raise SystemExit(1)
    click.echo(f"Category has been edited successfully: {id=}, {name=}, {parent=}")


@category.command
@click.pass_context
def tree(ctx):
    try:
        nodes = ctx.obj.category_tree()
    except Exception as e:
        ctx.obj.logger.error(f"Error getting categories tree: {e}")
        raise SystemExit(1)
    click.echo(format_tree(nodes))


@category.command
@click.option("--limit", type=click.IntRange(min=1, max=ROWS_LIMIT), default=10)
@click.option("--order_by",
              type=click.Choice(["id", "name", "parent_id"], case_sensitive=True),
              default="id")
@click.pass_context
def ls(ctx, limit: int, order_by: str):
    try:
        categories = ctx.obj.list_categories(limit, order_by)
    except Exception as e:
        ctx.obj.logger.error(f"Error listing categories: {e}")
        raise SystemExit(1)
    click.echo(format_table(["id", "name", "parent_id"], categories))
