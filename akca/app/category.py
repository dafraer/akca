import click


@click.group
def category():
    pass

@category.command
@click.option("-n", "--name", type=str, required=True)
@click.option("-p", "--parent", type=int)
def new(name: str, parent: int):
    click.echo(f"new category created: {name=}, {parent=}")

@category.command
@click.option("--id", type=int, required=True)
def rm(id: int):
    click.echo(f"removed category with {id=}")

@category.command
@click.option("--id", type=int, required=True)
@click.option("-n", "--name", type=str)
@click.option("-p", "--parent", type=int)
def edit(id: int, name: str, parent: str):
    click.echo(f"edited category with {id=}, {name=}, {parent=}")

@category.command
def tree():
    click.echo("Showing category tree with spending")

@category.command
def ls():
    click.echo("Listing all categories")
