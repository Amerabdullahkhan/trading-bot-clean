from __future__ import annotations

from app.backtest import BacktestEngine, print_backtest_results
from app.config import get_settings


def main() -> None:
    settings = get_settings()
    engine = BacktestEngine(initial_balance=settings.account_balance)
    results = engine.backtest_portfolio(settings.default_symbols, periods=200)
    print_backtest_results(results)


if __name__ == "__main__":
    main()