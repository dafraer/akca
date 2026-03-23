import click
from datetime import datetime

FROM_DATE="01/01/2001"
TO_DATE=datetime.today().strftime("%d/%m/%Y")

@click.command
@click.option("-from","--from_date", type=str, default=FROM_DATE)
@click.option("-to","--to_date", type=str, default=TO_DATE)
@click.pass_context
def stats(ctx, from_date: str, to_date: str):
    ctx.obj.stats(from_date, to_date)