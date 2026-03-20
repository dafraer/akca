import click


@click.command
def account():
    click.echo("account command called")

@click.command
def category():
    click.echo("category command has been called")

@click.command
def purchase():
    click.echo("purchase command has been called")