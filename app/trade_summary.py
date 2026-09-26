from __future__ import annotations

import csv
from pathlib import Path

FILE_PATH = Path(__file__).resolve().parent.parent / "trades.csv"

def get_trade_summary(csv_path: str | Path = FILE_PATH) -> dict:
    csv_path = Path(csv_path)

    summary = {
        "total_trades": 0,
        "buy_trades": 0,
        "sell_trades": 0,
        "hold_trades": 0,
        "total_quantity": 0.0,
        "executed_trades": 0,
    }

    if not csv_path.exists():
        return summary

    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row or not row.get("symbol"):
                continue

            summary["total_trades"] += 1
            side = (row.get("side") or "").upper()

            if side == "BUY":
                summary["buy_trades"] += 1
            elif side == "SELL":
                summary["sell_trades"] += 1
            elif side == "HOLD":
                summary["hold_trades"] += 1

            quantity = float(row.get("quantity") or 0)
            summary["total_quantity"] += quantity

            status = (row.get("status") or "").lower()
            if status == "executed":
                summary["executed_trades"] += 1

    return summary

def print_trade_summary(csv_path: str | Path = FILE_PATH) -> None:
    summary = get_trade_summary(csv_path)

    print("\nTrade Summary")
    print("=" * 120)
    print(f"Total trades: {summary['total_trades']}")
    print(f"Buy trades: {summary['buy_trades']}")
    print(f"Sell trades: {summary['sell_trades']}")
    print(f"Hold trades: {summary['hold_trades']}")
    print(f"Executed trades: {summary['executed_trades']}")
    print(f"Total quantity: {summary['total_quantity']:.2f}")
    print("=" * 120)