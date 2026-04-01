
def create(self, name: str, currency: str) -> int:
    cur = self.conn.cursor()
    cur.execute("insert into accounts (name, currency) values (?, ?);", (name, currency))
    self.conn.commit()

    id_ = cur.lastrowid

    self.logger.info(f"Account created: {id_=}, {name=}, {currency=}")

    return id_

def edit(self, id_: int, name: str, currency: str):
    cur = self.conn.cursor()
    cur.execute("""update accounts 
                set name = coalesce(?, name), 
                currency = coalesce(?, currency) 
                where id=?
                returning id, name, currency
                ;""", (name, currency, id_))

    row = cur.fetchone()
    id_, name, currency = row

    self.logger.info(f"Account updated: {id_=}, {name=}, {currency=}")

    self.conn.commit()

def delete(self, id_: int):
    cur = self.conn.cursor()
    cur.execute("delete from accounts where id=?;", id_)
    self.conn.commit()

    self.logger.info(f"Account deleted: {id_}")


def list_(self, limit: int, order_by: str) -> list[tuple]:
    cur = self.conn.cursor()
    res = cur.execute("select id, name, currency from accounts order by ? limit ?;", (order_by, limit))
    rows = res.fetchall()

    self.logger.info(f"Accounts retrieved successfully: {rows}")

    return rows

