from __future__ import annotations

import csv
from pathlib import Path

FILE_PATH = Path(__file__).resolve().parent.parent / "trades.csv"

def ensure_header():
    if not FILE_PATH.exists():
        with open(FILE_PATH, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "symbol",
                "side",
                "quantity",
                "reason",
                "price",
                "status"
            ])

def log_trade(
    symbol: str,
    side: str,
    quantity: float,
    reason: str,
    price: float | None = None,
    status: str = "executed",
):
    ensure_header()
    with open(FILE_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            symbol,
            side,
            quantity,
            reason,
            price if price is not None else "",
            status
        ])