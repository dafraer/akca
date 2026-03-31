import logging

import click 

from akca.app.account import account
from akca.app.category import category 
from akca.app.purchase import purchase 
from akca.app.backup import backup
from akca.app.stats import stats
from akca.store import Store
from akca.domain import Service


@click.group
@click.pass_context
@click.option("-v","--verbose", is_flag=True)
def cli(ctx, verbose):
    #disable logging if verbose flag is not set
    if not verbose:
        logging.getLogger().setLevel(logging.CRITICAL + 1)
    
    logging.basicConfig(
            level=logging.DEBUG,
            format="%(name)s - |%(levelname)s| - %(message)s" 
        )
    logger = logging.getLogger(__name__)
    store = Store(logger)
    ctx.obj = Service(store, logger)


cli.add_command(account)
cli.add_command(category)
cli.add_command(purchase)
cli.add_command(backup)
cli.add_command(stats)