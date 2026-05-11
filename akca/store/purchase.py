from datetime import datetime


from akca.domain.purchase import CreatePurchaseParams, EditPurchaseParams, ListPurchasesParams


def create(self, params: CreatePurchaseParams) -> int:
    cur = self.conn.cursor()

    cur.execute("select id from categories where name = ?", (params.category,))
    row = cur.fetchone()
    if row is None:
        raise ValueError(f"Category '{params.category}' not found")
    category_id = row[0]

    cur.execute("select id from accounts where name = ?", (params.account,))
    row = cur.fetchone()
    if row is None:
        raise ValueError(f"Account '{params.account}' not found")
    account_id = row[0]

    purchased_at = int(datetime.strptime(params.time, "%d/%m/%Y %H:%M:%S").timestamp())

    cur.execute(
        "insert into purchases (amount, item_name, description, purchased_at, category_id, account_id) values (?, ?, ?, ?, ?, ?)",
        (params.amount, params.name, params.desc, purchased_at, category_id, account_id),
    )
    self.conn.commit()

    id_ = cur.lastrowid

    self.logger.info(f"Purchase created: {id_=}, name={params.name!r}, amount={params.amount}, account={params.account!r}, category={params.category!r}")

    return id_

def edit(self, params: EditPurchaseParams):
    cur = self.conn.cursor()

    updates = []
    values = []

    if params.name is not None:
        updates.append("item_name = ?")
        values.append(params.name)

    if params.amount is not None:
        updates.append("amount = ?")
        values.append(params.amount)

    if params.description is not None:
        updates.append("description = ?")
        values.append(params.description)

    if params.time is not None:
        updates.append("purchased_at = ?")
        values.append(int(datetime.strptime(params.time, "%d/%m/%Y %H:%M:%S").timestamp()))


    if params.category is not None:
        cur.execute("select id from categories where name = ?", (params.category,))
        row = cur.fetchone()
        if row is None:
            raise ValueError(f"Category '{params.category}' not found")
        updates.append("category_id = ?")
        values.append(row[0])

    if params.account is not None:
        cur.execute("select id from accounts where name = ?", (params.account,))
        row = cur.fetchone()
        if row is None:
            raise ValueError(f"Account '{params.account}' not found")
        updates.append("account_id = ?")
        values.append(row[0])

    if not updates:
        return

    values.append(params.id)
    cur.execute(f"update purchases set {', '.join(updates)} where id = ?", values)
    if cur.rowcount == 0:
        raise ValueError(f"Purchase with id {params.id} not found")
    self.conn.commit()

    self.logger.info(f"Purchase updated: {params.id=}")

def delete(self, id_: int):
    cur = self.conn.cursor()
    cur.execute("delete from purchases where id = ?", (id_,))
    if cur.rowcount == 0:
        raise ValueError(f"Purchase with id {id_} not found")
    self.conn.commit()


def list_(self, params: ListPurchasesParams) -> list:
    cur = self.conn.cursor()

    conditions = []
    values = []

    if params.name is not None:
        conditions.append("item_name like ?")
        values.append(f"%{params.name}%")

    if params.from_date is not None:
        from_ts = int(datetime.strptime(params.from_date, "%d/%m/%Y").timestamp())
        conditions.append("purchased_at >= ?")
        values.append(from_ts)

    if params.to_date is not None:
        to_dt = datetime.strptime(params.to_date, "%d/%m/%Y").replace(hour=23, minute=59, second=59)
        conditions.append("purchased_at <= ?")
        values.append(int(to_dt.timestamp()))

    if params.category is not None:
        cur.execute("select id from categories where name = ?", (params.category,))
        row = cur.fetchone()
        if row is None:
            raise ValueError(f"Category '{params.category}' not found")
        conditions.append("category_id = ?")
        values.append(row[0])

    sort_map = {
        "time": "purchased_at desc",
        "amount": "amount desc",
        "alphabet": "item_name asc",
    }
    order_by = sort_map.get(params.sort, "purchased_at desc")

    where = f"where {' and '.join(conditions)}" if conditions else ""

    values.append(params.limit)
    rows = cur.execute(
        f"select id, amount, item_name, description, purchased_at, category_id, account_id from purchases {where} order by {order_by} limit ?",
        values,
    ).fetchall()

    self.logger.info(f"Purchases retrieved: {len(rows)} rows")

    return [list(row) for row in rows]
