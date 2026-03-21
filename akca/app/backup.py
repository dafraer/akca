import click


@click.group
def backup():
    pass

@backup.command
@click.argument("directory")
def directory(directory: str):
    click.echo(f"backup to {directory=}")
