from __future__ import annotations

import csv
from pathlib import Path

FILE_PATH = Path(__file__).resolve().parent.parent / "trades.csv"

def get_trade_metrics(csv_path: str | Path = FILE_PATH) -> dict:
    csv_path = Path(csv_path)

    metrics = {
        "total_trades": 0,
        "winning_trades": 0,
        "losing_trades": 0,
        "total_pnl": 0.0,
        "average_win": 0.0,
        "average_loss": 0.0,
        "best_trade": 0.0,
        "worst_trade": 0.0,
        "win_rate": 0.0,
        "profit_factor": 0.0,
    }

    if not csv_path.exists():
        return metrics

    trades = []
    with open(csv_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row or not row.get("symbol"):
                continue
            trades.append(row)

    if not trades:
        return metrics

    metrics["total_trades"] = len(trades)

    wins = []
    losses = []
    total_pnl = 0.0

    for trade in trades:
        try:
            quantity = float(trade.get("quantity") or 0)
            price = trade.get("price") or ""

            if price and price.strip():
                price_float = float(price)
                pnl = quantity * price_float
            else:
                pnl = quantity * 0.02

            total_pnl += pnl

            if pnl > 0:
                wins.append(pnl)
                metrics["winning_trades"] += 1
            elif pnl < 0:
                losses.append(pnl)
                metrics["losing_trades"] += 1

        except (ValueError, TypeError):
            pass

    metrics["total_pnl"] = total_pnl

    if wins:
        metrics["average_win"] = sum(wins) / len(wins)
        metrics["best_trade"] = max(wins)
    else:
        metrics["average_win"] = 0.0
        metrics["best_trade"] = 0.0

    if losses:
        metrics["average_loss"] = sum(losses) / len(losses)
        metrics["worst_trade"] = min(losses)
    else:
        metrics["average_loss"] = 0.0
        metrics["worst_trade"] = 0.0

    if metrics["total_trades"] > 0:
        metrics["win_rate"] = (metrics["winning_trades"] / metrics["total_trades"]) * 100
    else:
        metrics["win_rate"] = 0.0

    total_wins = sum(wins) if wins else 0.0
    total_losses = abs(sum(losses)) if losses else 0.0

    if total_losses > 0:
        metrics["profit_factor"] = total_wins / total_losses
    else:
        metrics["profit_factor"] = 0.0 if total_wins == 0 else float("inf")

    return metrics

def print_trade_metrics(csv_path: str | Path = FILE_PATH) -> None:
    metrics = get_trade_metrics(csv_path)

    print("\nPerformance Metrics")
    print("=" * 120)
    print(f"Total trades: {metrics['total_trades']}")
    print(f"Winning trades: {metrics['winning_trades']}")
    print(f"Losing trades: {metrics['losing_trades']}")
    print(f"Win rate: {metrics['win_rate']:.2f}%")
    print(f"Total P&L: ${metrics['total_pnl']:.2f}")
    print(f"Average win: ${metrics['average_win']:.2f}")
    print(f"Average loss: ${metrics['average_loss']:.2f}")
    print(f"Best trade: ${metrics['best_trade']:.2f}")
    print(f"Worst trade: ${metrics['worst_trade']:.2f}")
    print(f"Profit factor: {metrics['profit_factor']:.2f}")
    print("=" * 120)