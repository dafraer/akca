import click

def create(self, name: str, parent: str):
    cur = self.conn.cursor()
    parent_id = None
    if parent:
        cur.execute("select id from categories where name = ?", (parent,))
        row = cur.fetchone()
        if row is None:
            raise ValueError(f"Parent category '{parent}' not found")
        parent_id = row[0]

    cur.execute("insert into categories (name, parent_id) values (?, ?)", (name, parent_id))
    self.conn.commit()

    id_ = cur.lastrowid

    self.logger.info(f"Category created: {id_=}, {name=}, {parent=}")

    return id_

def edit(self, id_: int, name: str, parent: str):
    cur = self.conn.cursor()

    updates = []
    values = []

    if name is not None:
        updates.append("name = ?")
        values.append(name)

    if parent is not None:
        cur.execute("select id from categories where name = ?", (parent,))
        row = cur.fetchone()
        if row is None:
            raise ValueError(f"Parent category '{parent}' not found")
        parent_id = row[0]
        self.check_category_cycle(id_, parent_id)
        updates.append("parent_id = ?")
        values.append(parent_id)

    if not updates:
        return

    values.append(id_)
    cur.execute(f"update categories set {', '.join(updates)} where id = ?;", values)
    if cur.rowcount == 0:
        raise ValueError(f"Category with id {id_} not found")
    self.conn.commit()


def delete(self, name: str):
    cur = self.conn.cursor()
    cur.execute("delete from categories where name = ?;", (name,))
    if cur.rowcount == 0:
        raise ValueError(f"Category named {name} not found")
    self.conn.commit()

def tree(self) -> list[dict]:
    cur = self.conn.cursor()
    cur.execute("select id, name, parent_id from categories")
    return [dict(row) for row in cur.fetchall()]


def list_(self, limit: int, order_by: str) -> list[tuple]:
    cur = self.conn.cursor()
    res = cur.execute(f"select id, name, parent_id from categories order by {order_by} limit ?;", (limit,))
    rows = res.fetchall()

    self.logger.info(f"Accounts retrieved successfully: {rows}")

    return rows

def check_cycle(self, id_: int, parent_id: int):
    """Checks that adding a node doesn't create a cycle"""
    cur = self.conn.cursor()
    current = parent_id
    visited = set()
    while current is not None:
        if current == id_:
            raise ValueError(f"Setting parent id to {parent_id} creates a cycle")
        if current in visited:
            raise ValueError(f"Cycle detected in existing category tree at id {current}")
        visited.add(current)
        cur.execute("select parent_id from categories where id = ?", (current,))
        row = cur.fetchone()
        if row is None:
            raise ValueError(f"Parent category {current} not found")
        current = row[0]