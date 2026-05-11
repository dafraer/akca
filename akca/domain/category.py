def create(self, name: str, parent: str):
    return self.store.create_category(name, parent)


def edit(self, id_: int, name: str, parent: str):
    self.store.edit_category(id_, name, parent)

def delete(self, name: str):
    self.store.delete_category(name)


def tree(self) -> list[dict]:
    return self.store.category_tree()

def list_(self, limit: int, order_by: str) -> list[tuple]:
    return self.store.list_categories(limit, order_by)
