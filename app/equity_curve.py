from __future__ import annotations

import csv
from pathlib import Path

FILE_PATH = Path(__file__).resolve().parent.parent / "trades.csv"

def get_equity_curve(csv_path: str | Path = FILE_PATH) -> list[dict]:
    csv_path = Path(csv_path)

    equity_curve: list[dict] = []
    balance = 10000.0

    if not csv_path.exists():
        return equity_curve

    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for index, row in enumerate(reader, start=1):
            if not row or not row.get("symbol"):
                continue

            side = (row.get("side") or "").upper()
            quantity = float(row.get("quantity") or 0.0)

            if side == "BUY":
                pnl = quantity * 0.02
            elif side == "SELL":
                pnl = quantity * -0.02
            else:
                pnl = 0.0

            balance += pnl

            equity_curve.append(
                {
                    "trade_index": index,
                    "balance": round(balance, 2),
                    "pnl": round(pnl, 2),
                }
            )

    return equity_curve

def print_equity_curve(csv_path: str | Path = FILE_PATH) -> None:
    curve = get_equity_curve(csv_path)

    print("\nEquity Curve")
    print("=" * 120)

    if not curve:
        print("No trade data available. Run the dashboard first.")
        print("=" * 120)
        return

    for point in curve:
        print(
            f"Trade #{point['trade_index']}: "
            f"balance=${point['balance']:.2f}, "
            f"pnl=${point['pnl']:.2f}"
        )

    print("=" * 120)