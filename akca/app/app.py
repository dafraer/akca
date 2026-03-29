import click 

from akca.app.account import account
from akca.app.category import category 
from akca.app.purchase import purchase 
from akca.app.backup import backup
from akca.app.stats import stats


@click.group
@click.pass_context
def cli(ctx):
    from akca.db.store import Store
    from akca.domain.service import Service
    store = Store()
    ctx.obj = Service(store)


cli.add_command(account)
cli.add_command(category)
cli.add_command(purchase)
cli.add_command(backup)
cli.add_command(stats)