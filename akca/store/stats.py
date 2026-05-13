
def general(self, from_date: int, to_date: int, account: str) -> dict:
    cur = self.conn.cursor()

    cur.execute("select id, currency from accounts where name = ?", (account,))
    row = cur.fetchone()
    if row is None:
        raise ValueError(f"Account '{account}' not found")
    account_id = row[0]
    currency = row[1]

    row = cur.execute(
        "select coalesce(sum(amount), 0), count(*) from purchases where account_id = ? and date >= ? and date <= ?",
        (account_id, from_date, to_date),
    ).fetchone()
    total_cents = row[0]
    count = row[1]

    largest = cur.execute(
        "select item_name, amount from purchases where account_id = ? and date >= ? and date <= ? order by amount desc limit 1",
        (account_id, from_date, to_date),
    ).fetchone()

    smallest = cur.execute(
        "select item_name, amount from purchases where account_id = ? and date >= ? and date <= ? order by amount asc limit 1",
        (account_id, from_date, to_date),
    ).fetchone()

    max_day = cur.execute(
        """select date, sum(amount)
           from purchases
           where account_id = ? and date >= ? and date <= ?
           group by date 
           order by sum(amount) desc limit 1""",
        (account_id, from_date, to_date),
    ).fetchone()

    min_day = cur.execute(
        """select date, sum(amount)
           from purchases
           where account_id = ? and date >= ? and date <= ?
           group by date 
           order by sum(amount) asc limit 1""",
        (account_id, from_date, to_date),
    ).fetchone()

    max_month = cur.execute(
        """select date / 100, sum(amount)
           from purchases
           where account_id = ? and date >= ? and date <= ?
           group by date / 100
           order by sum(amount) desc limit 1""",
        (account_id, from_date, to_date),
    ).fetchone()

    min_month = cur.execute(
        """select date / 100, sum(amount)
           from purchases
           where account_id = ? and date >= ? and date <= ?
           group by date / 100
           order by sum(amount) asc limit 1""",
        (account_id, from_date, to_date),
    ).fetchone()

    categories = cur.execute(
        """with recursive
               relevant(id) as (
                   select distinct category_id
                   from purchases
                   where account_id = ? and date >= ? and date <= ?
               ),
               ancestors(id) as (
                   select id from relevant
                   union
                   select c.parent_id
                   from categories c join ancestors a on c.id = a.id
                   where c.parent_id is not null
               )
           select c.id, c.parent_id, c.name, coalesce(sum(p.amount), 0)
           from categories c
           join ancestors anc on c.id = anc.id
           left join purchases p on p.category_id = c.id
               and p.account_id = ? and p.date >= ? and p.date <= ?
           group by c.id, c.parent_id, c.name""",
        (account_id, from_date, to_date, account_id, from_date, to_date),
    ).fetchall()

    self.logger.info(f"Stats retrieved for account {account!r}")

    return {
        "total_cents": total_cents,
        "count": count,
        "currency": currency,
        "largest": largest,
        "smallest": smallest,
        "max_day": max_day,
        "min_day": min_day,
        "max_month": max_month,
        "min_month": min_month,
        "categories": categories,
    }
