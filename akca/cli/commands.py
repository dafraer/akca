import click

@click.group()
def root():
    pass

@root.group()
def root():
    pass

@root.command() 
def ahaha():
    click.echo("hello boxb")