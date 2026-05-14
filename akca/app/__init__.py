import logging

import click 

from akca.app.account import account
from akca.app.category import category
from akca.app.merchant import merchant
from akca.app.purchase import purchase
from akca.app.backup import backup
from akca.app.stats import stats
from akca.store import Store
from akca.domain import Service


MAX_LIMIT = 100

@click.group
@click.pass_context
@click.option("-v","--verbose", is_flag=True)
def cli(ctx, verbose):
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(name)s - |%(levelname)s| - %(filename)s:%(lineno)d - %(message)s"
    )
    logger = logging.getLogger(__name__)

    #disable all logging except for errors if verbose flag is not set
    if not verbose:
        logger.setLevel(logging.ERROR)

    try:
        store = Store(logger)
        ctx.obj = Service(store, logger)
    except Exception as e:
        logger.error(f"Error creating store: {e}")
        raise SystemExit(1)

cli.add_command(account)
cli.add_command(category)
cli.add_command(merchant)
cli.add_command(purchase)
cli.add_command(backup)
cli.add_command(stats)