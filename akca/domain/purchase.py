from datetime import date, datetime

from dataclasses import dataclass


@dataclass
class CreatePurchaseParams:
    name: str
    amount: float | int
    desc: str
    category: str
    date: date
    account: str
    merchant: str | None


def create(self, params: CreatePurchaseParams) -> int:
    params.amount = int(params.amount * 100)
    return self.store.create_purchase(params)


@dataclass
class EditPurchaseParams:
    id: int
    name: str
    amount: float | int
    description: str
    category: str
    date: date
    account: str
    merchant: str | None


def edit(self, params: EditPurchaseParams):
    if params.amount is not None:
        params.amount = int(params.amount * 100)
    self.store.edit_purchase(params)


def delete(self, id_: int):
    self.store.delete_purchase(id_)


@dataclass
class ListPurchasesParams:
    name: str
    from_date: date
    to_date: date
    category: str
    sort: str
    limit: int
    merchant: str | None


def _int_to_date(n: int) -> str:
    return f"{n // 10000:04d}-{(n % 10000) // 100:02d}-{n % 100:02d}"


def list_(self, params: ListPurchasesParams) -> list:
    purchases = self.store.list_purchases(params)
    for purchase in purchases:
        purchase[1] = round(purchase[1] / 100, 2)
        purchase[5] = _int_to_date(purchase[5])
    return purchases
