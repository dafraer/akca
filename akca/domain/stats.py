import click

def stats(self, from_date: str, to_date: str):
    click.echo(f"showing stats: {from_date=}, {to_date=}")
