from .cli import cli
from .db import store
from .domain import service

new_store = store.Store()

new_service = service.Service(new_store)

new_cli = cli.App(new_service)
new_cli.run()