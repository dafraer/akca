import calendar as _calendar
from dataclasses import dataclass
from datetime import date

_MONTH_ABBR = {i: _calendar.month_abbr[i] for i in range(1, 13)}


@dataclass
class Purchase:
    name: str
    amount: float

@dataclass
class Stats:
    total: float
    purchase_quantity: int
    avg_daily_spending: float
    avg_monthly_spending: float
    largest_purchase: Purchase
    smallest_purchase: Purchase
    max_day: list[str, float]
    min_day: list[str, float]
    max_month: list[str, float]
    min_month: list[str, float]
    categories: list[dict]
    top_merchant: tuple[str, float] | None
    currency: str


def _date_to_int(d: date) -> int:
    return d.year * 10000 + d.month * 100 + d.day


def _int_to_date_str(n: int) -> str:
    return f"{n // 10000:04d}-{(n % 10000) // 100:02d}-{n % 100:02d}"


def _int_to_month_str(n: int) -> str:
    return f"{n // 100:04d}-{n % 100:02d}"


def trends(self, from_date: date, to_date: date, account: str, group_by: str, category: str | None, merchant: str | None):
    raw = self.store.trends_stats(_date_to_int(from_date), _date_to_int(to_date), account, group_by, category, merchant)
    currency = raw["currency"]

    result = []
    for period_key, amount_cents in raw["rows"]:
        amount = round(amount_cents / 100, 2)
        if group_by == "month":
            label = f"{_MONTH_ABBR[period_key % 100]} {period_key // 100}"
        elif group_by == "year":
            label = str(period_key)
        else:
            label = _int_to_date_str(period_key)
        result.append((label, amount))

    return result, currency


def _build_category_tree(rows, currency: str) -> list[dict]:
    # rows: (id, parent_id, name, direct_cents)
    nodes = {row[0]: {"id": row[0], "parent_id": row[1], "name": row[2], "total": row[3]} for row in rows}

    children: dict = {}
    for nid, node in nodes.items():
        children.setdefault(node["parent_id"], []).append(nid)

    def accumulate(nid):
        for child_id in children.get(nid, []):
            accumulate(child_id)
            nodes[nid]["total"] += nodes[child_id]["total"]

    for nid, node in nodes.items():
        if node["parent_id"] is None or node["parent_id"] not in nodes:
            accumulate(nid)

    return [
        {
            "id": n["id"],
            "parent_id": n["parent_id"] if n["parent_id"] in nodes else None,
            "name": f"{n['name']}  {round(n['total'] / 100, 2)} {currency}",
        }
        for n in nodes.values()
    ]


def general(self, from_date: date, to_date: date, account: str) -> Stats:
    raw = self.store.general_stats(_date_to_int(from_date), _date_to_int(to_date), account)

    total = raw["total_cents"] / 100
    count = raw["count"]
    currency = raw["currency"]

    days = max((to_date - from_date).days + 1, 1)
    months = max(days / 30, 1)

    avg_daily = round(total / days, 2)
    avg_monthly = round(total / months, 2)

    def to_purchase(row):
        if row is None:
            return Purchase("N/A", 0.0)
        return Purchase(row[0], round(row[1] / 100, 2))

    def to_day_tuple(row):
        if row is None:
            return ["N/A", 0.0]
        return [_int_to_date_str(row[0]), round(row[1] / 100, 2)]

    def to_month_tuple(row):
        if row is None:
            return ["N/A", 0.0]
        return [_int_to_month_str(row[0]), round(row[1] / 100, 2)]

    categories = _build_category_tree(raw["categories"], currency)

    tm = raw["top_merchant"]
    top_merchant = (tm[0], round(tm[1] / 100, 2)) if tm else None

    return Stats(
        total=round(total, 2),
        purchase_quantity=count,
        avg_daily_spending=avg_daily,
        avg_monthly_spending=avg_monthly,
        largest_purchase=to_purchase(raw["largest"]),
        smallest_purchase=to_purchase(raw["smallest"]),
        max_day=to_day_tuple(raw["max_day"]),
        min_day=to_day_tuple(raw["min_day"]),
        max_month=to_month_tuple(raw["max_month"]),
        min_month=to_month_tuple(raw["min_month"]),
        categories=categories,
        top_merchant=top_merchant,
        currency=currency,
    )
