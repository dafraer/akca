import click


@click.group
def backup():
    pass

@backup.command
@click.argument("directory")
@click.pass_context
def directory(ctx, directory: str):
    click.echo(f"backup to {directory=}")
