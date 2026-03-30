import click

def create(self, name: str, currency: str) -> int:
    cur = self.conn.cursor()
    cur.execute("insert into accounts (name, currency) values (?, ?);", (name, currency))
    self.conn.commit()
def edit(self, id: int, name: str, currency: str) -> int:
    cur = self.conn.cursor()
    cur.execute("""update accounts 
                set name = coalesce(?, name), 
                currency = coalesce(?, currency) 
                where id=?;""", (name, currency, id))
    self.conn.commit()

def delete(self, id: int) -> int:
    cur = self.conn.cursor()
    cur.execute("delete from accounts where id=?;", id)
    self.conn.commit()


def list(self) -> list[tuple]:
    cur = self.conn.cursor()
    res = cur.execute("select * from accounts;")
    return res.fetchall()

