import click

@click.group
def category():
    click.echo("category command has been called")

