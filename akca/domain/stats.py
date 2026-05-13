from dataclasses import dataclass
from datetime import date


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
    categories: list[str, float]
    currency: str


def _date_to_int(d: date) -> int:
    return d.year * 10000 + d.month * 100 + d.day


def _int_to_date_str(n: int) -> str:
    return f"{n // 10000:04d}-{(n % 10000) // 100:02d}-{n % 100:02d}"


def _int_to_month_str(n: int) -> str:
    return f"{n // 100:04d}-{n % 100:02d}"


def stats(self, from_date: date, to_date: date, account: str) -> Stats:
    raw = self.store.stats(_date_to_int(from_date), _date_to_int(to_date), account)

    total = raw["total_cents"] / 100
    count = raw["count"]
    currency = raw["currency"]

    days = max((to_date - from_date).days, 1)
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

    categories = [[row[0], round(row[1] / 100, 2)] for row in raw["categories"]]

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
        currency=currency,
    )
