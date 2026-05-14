def create(self, name: str) -> int:
    cur = self.conn.cursor()
    cur.execute("insert into merchants (name) values (?);", (name,))
    self.conn.commit()

    id_ = cur.lastrowid

    self.logger.info(f"Merchant created: {id_=}, {name=}")

    return id_


def list_(self, limit: int, order_by: str) -> list[tuple]:
    cur = self.conn.cursor()
    res = cur.execute(f"select id, name from merchants order by {order_by} limit ?;", (limit,))
    rows = res.fetchall()

    self.logger.info(f"Merchants retrieved successfully: {rows}")

    return rows
