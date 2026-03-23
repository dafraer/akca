import click


@click.group
def category():
    pass

@category.command
@click.option("-n", "--name", type=str, required=True)
@click.option("-p", "--parent", type=int)
@click.pass_context
def new(ctx, name: str, parent: int):
    ctx.obj.create_category(name, parent)

@category.command
@click.option("--id", type=int, required=True)
@click.pass_context
def rm(ctx, id: int):
    ctx.obj.delete_category(id)

@category.command
@click.option("--id", type=int, required=True)
@click.option("-n", "--name", type=str)
@click.option("-p", "--parent", type=int)
@click.pass_context
def edit(ctx, id: int, name: str, parent: str):
    ctx.obj.edit_category(id, name, parent)

@category.command
@click.pass_context
def tree(ctx):
    ctx.obj.category_tree()

@category.command
@click.pass_context
def ls(ctx):
    ctx.obj.list_categories()
