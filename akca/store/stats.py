from datetime import datetime


def stats(self, f_ts: int, t_ts: int, account: str) -> dict:
    cur = self.conn.cursor()

    cur.execute("select id, currency from accounts where name = ?", (account,))
    row = cur.fetchone()
    if row is None:
        raise ValueError(f"Account '{account}' not found")
    account_id = row[0]
    currency = row[1]

    row = cur.execute(
        "select coalesce(sum(amount), 0), count(*) from purchases where account_id = ? and purchased_at >= ? and purchased_at <= ?",
        (account_id, f_ts, t_ts),
    ).fetchone()
    total_cents = row[0]
    count = row[1]

    largest = cur.execute(
        "select item_name, amount from purchases where account_id = ? and purchased_at >= ? and purchased_at <= ? order by amount desc limit 1",
        (account_id, f_ts, t_ts),
    ).fetchone()

    smallest = cur.execute(
        "select item_name, amount from purchases where account_id = ? and purchased_at >= ? and purchased_at <= ? order by amount asc limit 1",
        (account_id, f_ts, t_ts),
    ).fetchone()

    max_day = cur.execute(
        """select date(purchased_at, 'unixepoch', 'localtime'), sum(amount)
           from purchases
           where account_id = ? and purchased_at >= ? and purchased_at <= ?
           group by date(purchased_at, 'unixepoch', 'localtime')
           order by sum(amount) desc limit 1""",
        (account_id, f_ts, t_ts),
    ).fetchone()

    min_day = cur.execute(
        """select date(purchased_at, 'unixepoch', 'localtime'), sum(amount)
           from purchases
           where account_id = ? and purchased_at >= ? and purchased_at <= ?
           group by date(purchased_at, 'unixepoch', 'localtime')
           order by sum(amount) asc limit 1""",
        (account_id, f_ts, t_ts),
    ).fetchone()

    max_month = cur.execute(
        """select strftime('%Y-%m', purchased_at, 'unixepoch', 'localtime'), sum(amount)
           from purchases
           where account_id = ? and purchased_at >= ? and purchased_at <= ?
           group by strftime('%Y-%m', purchased_at, 'unixepoch', 'localtime')
           order by sum(amount) desc limit 1""",
        (account_id, f_ts, t_ts),
    ).fetchone()

    min_month = cur.execute(
        """select strftime('%Y-%m', purchased_at, 'unixepoch', 'localtime'), sum(amount)
           from purchases
           where account_id = ? and purchased_at >= ? and purchased_at <= ?
           group by strftime('%Y-%m', purchased_at, 'unixepoch', 'localtime')
           order by sum(amount) asc limit 1""",
        (account_id, f_ts, t_ts),
    ).fetchone()

    categories = cur.execute(
        """select c.name, sum(p.amount)
           from purchases p
           join categories c on p.category_id = c.id
           where p.account_id = ? and p.purchased_at >= ? and p.purchased_at <= ?
           group by c.id, c.name
           order by sum(p.amount) desc""",
        (account_id, f_ts, t_ts),
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
