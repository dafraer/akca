def create(self, name: str) -> int:
    return self.store.create_merchant(name)


def list_(self, limit: int, order_by: str) -> list[tuple]:
    return self.store.list_merchants(limit, order_by)
