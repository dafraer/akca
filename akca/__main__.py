from .cli import cli
from .db import store
from .domain import service


def main():
    new_store = store.Store()
    new_service = service.Service(new_store)
    new_cli = cli.App(new_service)
    new_cli.run()

if __name__=="__main__":
    main()