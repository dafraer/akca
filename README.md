<br />
<div align="center">

<h3 align="center">akca</h3>

  <p align="center">
    Akca (pronounced akcha) is a very simple terminal expense tracker. Log purchases, organize them into nested categories, and get spending stats and trends — all from the command line.
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#features">Features</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



## About The Project

Akca is a CLI tool for tracking personal expenses. It stores everything in a local SQLite database, supports arbitrarily nested spending categories, and lets you analyze your spending over any date range through general stats and bar-chart trends — with no accounts, subscriptions, or internet connection required.



## Getting Started

### Prerequisites

- Python 3.11 or newer
- pip

### Installation

Install directly from GitHub (no cloning required):

```sh
pip install git+https://github.com/dafraer/akca.git
```

That's it. The `akca` command is now available in your terminal.

> Install inside a virtual environment if you want to  keep your system Python clean:
> ```sh
> python -m venv .venv
> source .venv/bin/activate
> pip install git+https://github.com/dafraer/akca.git
> ```

Akca stores its database at `~/.local/share/akca/akca.db` and creates it automatically on first run.



## Features

- 🏦 **Multiple accounts** — track different budgets (personal, business, etc.) each with their own currency
- 🗂 **Nested categories** — organize spending into a tree of categories and subcategories of any depth
- 🏪 **Merchant tracking** — manage merchants as a first-class list and tag every purchase with one, so spelling stays consistent and filtering is exact
- 🧾 **Purchase log** — add, edit, delete, and list purchases with filtering by name, category, merchant, and date range
- 📊 **General stats** — total spend, purchase count, averages, largest/smallest purchase, most/least expensive day and month, top merchant, and spending breakdown as a category tree that rolls up subcategory totals
- 📈 **Trends** — bar-chart view of spending grouped by day, month, or year, filterable by category and merchant



## Usage

### Accounts

```sh
akca account new --name "personal" --currency "USD"
akca account ls
```

### Categories

```sh
# Root category
akca category new -n "food"

# Subcategory
akca category new -n "groceries" -p "food"
akca category new -n "restaurants" -p "food"
akca category new -n "fast-food" -p "restaurants"

# View the full tree
akca category tree
```

### Merchants

Merchants are managed as their own list and must be created before they can be attached to a purchase. This prevents typo duplicates (`Aldi` vs `aldi` vs `Aldii`) and makes filtering exact.

```sh
akca merchant new --name "Aldi"
akca merchant new --name "Whole Foods"

# List merchants (sorted by id or name)
akca merchant ls
akca merchant ls --order_by name

# Remove a merchant (only if no purchases still reference it)
akca merchant rm --name "Aldi"
```

### Purchases

Every purchase requires an account, a category, and a merchant — all referenced by name.

```sh
# Add a purchase (date defaults to today)
akca purchase new -n "Weekly shop" -a 54.30 -c "groceries" -acc "personal" -m "Aldi"

# Add with an explicit date
akca purchase new -n "Uber" -a 12.50 -c "rideshare" -acc "personal" -m "Uber" -d 2026-05-01

# List recent purchases
akca purchase ls

# Filter by category, merchant, and date range; sort by amount
akca purchase ls -c "food" -m "Aldi" -from 2026-01-01 -to 2026-05-13 -s amount -l 20

# Edit a purchase (add or change merchant)
akca purchase edit --id 42 -a 60.00 -m "Whole Foods"

# Delete a purchase
akca purchase rm --id 42
```

### Stats

```sh
# General stats for this month
akca stats general -acc "personal" -p month

# General stats for this year
akca stats general -acc "personal" -p year

# General stats for a custom date range
akca stats general -acc "personal" -from 2025-01-01 -to 2025-12-31
```

Example output:
```
+------------------------------------------------------+
| Stats for personal account                           |
+------------------------------------------------------+
| Total spent this month: 1034.29 USD                  |
|                                                      |
| Number of purchases: 58                              |
|                                                      |
| Average daily spending: 86.19 USD                    |
|                                                      |
| Average monthly spending: 1034.29 USD                |
|                                                      |
| Largest purchase: Weekly shop 139.25 USD             |
|                                                      |
| Smallest purchase: Espresso 2.65 USD                 |
|                                                      |
| Most expensive day: 2026-05-07, spent: 211.53 USD    |
|                                                      |
| Cheapest day: 2026-05-06, spent: 4.25 USD            |
|                                                      |
| Top merchant: Aldi 350.00 USD                        |
|                                                      |
+------------------------------------------------------+
Spending by category:
.
├── food  352.92 USD
│   ├── groceries  259.01 USD
│   └── restaurants  80.58 USD
│       ├── fast-food  6.37 USD
│       └── fine-dining  74.21 USD
└── transport  131.64 USD
    └── rideshare  131.64 USD
```

### Trends

```sh
# Monthly spending bar chart (all time)
akca stats trends -acc "personal" -gb month

# Daily chart for a specific month
akca stats trends -acc "personal" -gb day -from 2026-04-01 -to 2026-04-30

# Monthly chart filtered to a category (includes all subcategories)
akca stats trends -acc "personal" -gb month -c "food"

# Monthly chart filtered to a specific merchant
akca stats trends -acc "personal" -gb month -m "Aldi"

# Combine category and merchant filters
akca stats trends -acc "personal" -gb month -c "groceries" -m "Aldi"
```

Example output:
```
Jan 2026  █████████████████████████████  4809.34 USD
Feb 2026  ████████████████████████████   4630.72 USD
Mar 2026  ██████████████████████         3630.13 USD
Apr 2026  █████████████████████████████  4751.15 USD
May 2026  ██████                         1034.29 USD
```



## Contact

Kamil Nuriev — [Telegram](https://t.me/dafraer) — kdnuriev@gmail.com
