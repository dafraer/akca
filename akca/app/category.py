import click


@click.group
def category():
    pass

@category.command
@click.option("-n", "--name", type=str, required=True)
@click.option("-p", "--parent", type=int)
@click.pass_context
def new(ctx, name: str, parent: int):
    click.echo(f"new category created: {name=}, {parent=}")

@category.command
@click.option("--id", type=int, required=True)
@click.pass_context
def rm(ctx, id: int):
    click.echo(f"removed category with {id=}")

@category.command
@click.option("--id", type=int, required=True)
@click.option("-n", "--name", type=str)
@click.option("-p", "--parent", type=int)
@click.pass_context
def edit(ctx, id: int, name: str, parent: str):
    click.echo(f"edited category with {id=}, {name=}, {parent=}")

@category.command
@click.pass_context
def tree(ctx):
    click.echo("Showing category tree with spending")

@category.command
@click.pass_context
def ls(ctx):
    click.echo("Listing all categories")
