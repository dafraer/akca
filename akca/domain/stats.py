import click

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
    max_day: tuple[date, float] 
    min_day: tuple[date, float] 
    max_month: tuple[str, float] 
    min_month: tuple[str, float] 
    categories: list[str, float]
    currency: str

def stats(self, from_date: datetime, to_date: datetime, account: str) -> Stats:
   return Stats() 
