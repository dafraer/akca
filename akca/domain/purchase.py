from datetime import datetime, timezone

from dataclasses import dataclass


@dataclass
class CreatePurchaseParams:
    name: str
    amount: float | int
    desc: str
    category: str
    time: datetime 
    account: str


def create(self, params: CreatePurchaseParams) -> int:
    #convert amount to cents
    params.amount = int(params.amount*100)
    return self.store.create_purchase(params)


@dataclass
class EditPurchaseParams:
    id: int
    name: str
    amount: float | int
    description: str
    category: str
    time: datetime 
    account: str


def edit(self, params: EditPurchaseParams):
    if params.amount is not None:
        params.amount = int(params.amount * 100)
    self.store.edit_purchase(params)


def delete(self, id_: int):
    self.store.delete_purchase(id_)


@dataclass
class ListPurchasesParams:
    name: str 
    from_date: datetime 
    to_date: datetime 
    category: str 
    sort: str 
    limit: int


def list_(self, params: ListPurchasesParams) -> list:
    purchases = self.store.list_purchases(params)
    for purchase in purchases:
        amount_ind = 1
        purchased_at_id=4
        purchase[amount_ind] = round(purchase[amount_ind]/100, 2)
        purchase[purchased_at_id] = datetime.fromtimestamp(purchase[purchased_at_id]).strftime("%Y-%m-%d %H:%M")
    return purchases