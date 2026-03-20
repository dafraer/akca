import click 
from akca.app import commands

@click.group
@click.pass_context
def cli(ctx):
    from akca.db.store import Store
    from akca.domain.service import Service
    store = Store()
    ctx.obj = Service(store)

cli.add_command(commands.account)
cli.add_command(commands.category)
cli.add_command(commands.purchase)