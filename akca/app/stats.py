from datetime import date, datetime

import click

from akca.domain.stats import Stats
from akca.app.helpers import format_table

FROM_DATE = date(2001, 1, 1)
TODAY = date.today()
DATE_FORMATS = ["%Y-%m-%d", "%Y%m%d"]

@click.group
def stats():
    pass

@stats.command
@click.option("-gb", "--group_by", type=click.Choice(["month", "day", "year"]), default="month")
@click.option("-c", "--category", type=str)
@click.option("-from", "--from_date", type=click.DateTime(formats=DATE_FORMATS), default=None)
@click.option("-to", "--to_date", type=click.DateTime(formats=DATE_FORMATS), default=None)
@click.option("-acc", "--account", required=True)
@click.pass_context
def trends(group_by: str, category: str, account: str, from_date: datetime, to_date: datetime):
    pass 

@stats.command
@click.option("-from", "--from_date", type=click.DateTime(formats=DATE_FORMATS), default=None)
@click.option("-to", "--to_date", type=click.DateTime(formats=DATE_FORMATS), default=None)
@click.option("-p", "--period", type=click.Choice(["month", "year"]), default=None)
@click.option("-acc", "--account", type=str, required=True)
@click.pass_context
def general(ctx, from_date: datetime, to_date: datetime, account: str, period: str):
    if period and (from_date or to_date):
        raise click.UsageError("Use either --period OR --from/--to, not both.")
    if period:
        p1 = f"this {period}"
        if period == "month":
            from_date = TODAY.replace(day=1)
            to_date = TODAY
        else:
            from_date = TODAY.replace(day=1, month=1)
            to_date = TODAY
    elif from_date and to_date:
        from_date = from_date.date()
        to_date = to_date.date()
        p1 = f"from {from_date} to {to_date}"
    else:
        from_date = FROM_DATE
        to_date = TODAY
        p1 = "all time"

    if from_date >= to_date:
        raise click.UsageError("to_date must be after from_date")

    try:
        data: Stats = ctx.obj.general_stats(from_date, to_date, account)
    except Exception as e:
        ctx.obj.logger.error(f"Error getting stats: {e}")
        raise SystemExit(1)

    header = [f"Stats for {account} account"]
    rows = [
        [f"Total spent {p1}: {data.total} {data.currency}"], [""],
        [f"Number of purchases: {data.purchase_quantity}"], [""],
        [f"Average daily spending: {data.avg_daily_spending} {data.currency}"], [""],
        [f"Average monthly spending: {data.avg_monthly_spending} {data.currency}"], [""],
        [f"Largest purchase: {data.largest_purchase.name} {data.largest_purchase.amount} {data.currency}"], [""],
        [f"Smallest purchase: {data.smallest_purchase.name} {data.smallest_purchase.amount} {data.currency}"], [""],
        [f"Most expensive day: {data.max_day[0]}, spent: {data.max_day[1]} {data.currency}"], [""],
        [f"Cheapest day: {data.min_day[0]}, spent: {data.min_day[1]} {data.currency}"], [""],
        [f"Most expensive month: {data.max_month[0]}, spent: {data.max_month[1]} {data.currency}"], [""],
        [f"Cheapest month: {data.min_month[0]}, spent: {data.min_month[1]} {data.currency}"], [""],
    ]
    res = format_table(header, rows)
    res += "\nSpending by category:\n"
    headers = ["Name", f"Amount ({data.currency})"]
    res += format_table(headers, data.categories)
    click.echo(res)
