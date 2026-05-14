def create(self, name: str) -> int:
    return self.store.create_merchant(name)


def delete(self, id_: int):
    self.store.delete_merchant(id_)


def list_(self, limit: int, order_by: str) -> list[tuple]:
    return self.store.list_merchants(limit, order_by)
