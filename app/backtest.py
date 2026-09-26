from __future__ import annotations

from dataclasses import dataclass

from app.data.provider import SyntheticMarketDataProvider
from app.strategies.ensemble import StrategyEnsemble


@dataclass
class BacktestResult:
    symbol: str
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    total_pnl: float
    average_win: float
    average_loss: float
    best_trade: float
    worst_trade: float
    profit_factor: float
    max_drawdown: float
    total_return_pct: float


class BacktestEngine:
    def __init__(self, initial_balance: float = 10000.0):
        self.initial_balance = initial_balance
        self.provider = SyntheticMarketDataProvider()
        self.ensemble = StrategyEnsemble(min_confidence=0.55)

    def backtest_symbol(self, symbol: str, periods: int = 200) -> BacktestResult:
        candles = self.provider.get_history(symbol, periods=periods)

        balance = self.initial_balance
        peak_balance = self.initial_balance
        max_drawdown = 0.0

        trades = []
        wins = []
        losses = []

        for i, candle in enumerate(candles):
            if i < 20:
                continue

            historical_candles = candles[:i+1]
            decision = self.ensemble.analyze(symbol, historical_candles)

            if decision.side in ("BUY", "SELL"):
                quantity = 200.0
                pnl = quantity * 0.02 if decision.side == "BUY" else quantity * -0.02

                balance += pnl
                trades.append(pnl)

                if pnl > 0:
                    wins.append(pnl)
                elif pnl < 0:
                    losses.append(pnl)

            if balance > peak_balance:
                peak_balance = balance
            else:
                drawdown = (peak_balance - balance) / peak_balance * 100
                if drawdown > max_drawdown:
                    max_drawdown = drawdown

        total_pnl = sum(trades) if trades else 0.0
        total_return_pct = (balance - self.initial_balance) / self.initial_balance * 100

        winning_trades = len(wins)
        losing_trades = len(losses)
        total_trades = len(trades)

        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0.0
        average_win = sum(wins) / len(wins) if wins else 0.0
        average_loss = sum(losses) / len(losses) if losses else 0.0
        best_trade = max(wins) if wins else 0.0
        worst_trade = min(losses) if losses else 0.0

        total_wins = sum(wins) if wins else 0.0
        total_losses = abs(sum(losses)) if losses else 0.0
        profit_factor = total_wins / total_losses if total_losses > 0 else (0.0 if total_wins == 0 else float("inf"))

        return BacktestResult(
            symbol=symbol,
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate=win_rate,
            total_pnl=total_pnl,
            average_win=average_win,
            average_loss=average_loss,
            best_trade=best_trade,
            worst_trade=worst_trade,
            profit_factor=profit_factor,
            max_drawdown=max_drawdown,
            total_return_pct=total_return_pct,
        )

    def backtest_portfolio(self, symbols: list[str], periods: int = 200) -> list[BacktestResult]:
        results = []
        for symbol in symbols:
            result = self.backtest_symbol(symbol, periods=periods)
            results.append(result)
        return results


def print_backtest_results(results: list[BacktestResult]) -> None:
    print("\nBacktest Results")
    print("=" * 120)
    print(
        f"{'Symbol':<12} {'Trades':<8} {'Win%':<8} {'P&L':<12} "
        f"{'Avg Win':<12} {'Avg Loss':<12} {'Max DD%':<10} {'Return%':<10}"
    )
    print("-" * 120)

    for result in results:
        print(
            f"{result.symbol:<12} {result.total_trades:<8} {result.win_rate:<8.2f} "
            f"${result.total_pnl:<11.2f} ${result.average_win:<11.2f} "
            f"${result.average_loss:<11.2f} {result.max_drawdown:<9.2f}% {result.total_return_pct:<9.2f}%"
        )

    print("=" * 120)