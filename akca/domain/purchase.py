from dataclasses import dataclass
import click

@dataclass
class CreatePurchaseParams:
    name: str 
    amount: int 
    desc: str 
    category: int 
    time: str


def create(self, params: CreatePurchaseParams):
    click.echo(f"""new purchase created: 
               {params.name=}, 
               {params.amount=}, 
               {params.desc=}, 
               {params.category=}, 
               {params.time=}
            """)


@dataclass
class EditPurchaseParams:
    id: int
    name: str
    amount: int 
    description: str
    category: str
    time: str


def edit(self, params: EditPurchaseParams):
    click.echo(f"""purchase edited: 
               {params.id=}, 
               {params.name=}, 
               {params.amount=}, 
               {params.description=}, 
               {params.category=}, 
               {params.time=}
            """)


def delete(self, id: int):
    click.echo(f"purchase deleted: {id=}")


@dataclass
class ListPurchasesParams:
    name: str 
    from_date: str 
    to_date: str 
    category: str 
    sort: str 
    limit: int


def list(self, params: ListPurchasesParams):
    click.echo(f"purchases listed: {params.name=}, {params.from_date=}, {params.to_date=}, {params.category=}, {params.sort=}, {params.limit=}")
