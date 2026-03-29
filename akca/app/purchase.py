from datetime import datetime

import click

TIME=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
FROM_DATE="01/01/2001"
TO_DATE=datetime.today().strftime("%d/%m/%Y")


@click.group
def purchase():
    pass


@purchase.command
@click.option("-n", "--name", type=str, required=True)
@click.option("-a", "--amount", type=int, required=True)
@click.option("-d", "--desc", type=str)
@click.option("-c", "--category", type=int)
@click.option("-t", "--time", type=str, default=TIME)
@click.pass_context
def new(ctx, name: str, amount: int, desc: str, category: str, time: str):
    ctx.obj.create_purchase(name, amount, desc, category, time)


@purchase.command
@click.option("--id", type=int, required=True)
@click.pass_context
def rm(ctx, id: int):
    ctx.obj.delete_purchase(id)


@purchase.command
@click.option("--id", type=int, required=True)
@click.option("-n", "--name", type=str)
@click.option("-a", "--amount", type=int)
@click.option("-d", "--description", type=str)
@click.option("-c", "--category", type=str)
@click.option("-t", "--time", type=str)
@click.pass_context
def edit(ctx, id: int, name: str, amount: int, desc: str, categories: str, time: str):
    ctx.obj.edit_purchase(id, name, amount, desc, categories, time)


@purchase.command
@click.option("-n", "--name", type=str)
@click.option("-from", "--from_date", type=str, default=FROM_DATE)
@click.option("-to", "to_date", type=str, default=TO_DATE)
@click.option("-c", "--category", type=str)
@click.option("-s", "--sort", type=click.Choice(["time", "amount", "alphabet"]))
@click.option("-m", "--max", type=int)
@click.pass_context
def ls(ctx, name: str, from_date: str, to_date: str, category: str, sort: str, max: int):
    ctx.obj.list_purchases(name, from_date, to_date, category, sort, max)
