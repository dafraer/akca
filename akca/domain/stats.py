from dataclasses import dataclass
from datetime import datetime, date


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
    max_day: list[date, float]
    min_day: list[date, float]
    max_month: list[str, float]
    min_month: list[str, float]
    categories: list[str, float]
    currency: str


def stats(self, from_date, to_date, account: str) -> Stats:
    raw = self.store.stats(int(from_date.timestamp()), int(to_date.timestamp()), account)

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
                                                
    categories = [[row[0], round(row[1] / 100, 2)] for row in raw["categories"]]

    return Stats(
        total=round(total, 2),
        purchase_quantity=count,
        avg_daily_spending=avg_daily,
        avg_monthly_spending=avg_monthly,
        largest_purchase=to_purchase(raw["largest"]),
        smallest_purchase=to_purchase(raw["smallest"]),
        max_day=(raw["max_day"] or ["N/A", 0.0]),
        min_day=(raw["min_day"] or ["N/A", 0.0]),
        max_month=(raw["max_month"] or ["N/A", 0.0]),
        min_month=(raw["min_month"] or ["N/A", 0.0]),
        categories=categories,
        currency=currency,
    )
