import click

@click.command
@click.argument("directory")
@click.pass_context
def backup(ctx, directory: str):
    ctx.obj.backup(directory)
