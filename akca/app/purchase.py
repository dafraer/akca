import click 

@click.group
def purchase():
    click.echo("purchase command has been called")