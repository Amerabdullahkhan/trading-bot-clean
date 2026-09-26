from __future__ import annotations

from app.broker.paper_broker import PaperBroker
from app.config import get_settings
from app.data.provider import SyntheticMarketDataProvider
from app.engine.signal_engine import SignalEngine
from app.risk.risk_manager import RiskManager
from app.trade_summary import print_trade_summary
from app.trade_metrics import print_trade_metrics

class ConsoleDashboard:
    def __init__(self, symbols: list[str]):
        settings = get_settings()
        self.symbols = symbols
        self.provider = SyntheticMarketDataProvider()
        self.broker = PaperBroker(account_balance=settings.account_balance)
        self.risk_manager = RiskManager(
            account_balance=settings.account_balance,
            max_daily_loss=settings.max_daily_loss,
            max_risk_per_trade=settings.max_risk_per_trade,
        )
        self.engine = SignalEngine(
            provider=self.provider,
            risk_manager=self.risk_manager,
            broker=self.broker,
        )

    def render(self) -> None:
        ideas = self.engine.scan(self.symbols)

        print("\nTrading dashboard")
        print("=" * 120)
        print(f"{'Symbol':<12} {'Side':<6} {'Confidence':<12} {'Action':<8} {'Risk':<18} {'Reasons':<60}")
        print("-" * 120)

        for idea in ideas:
            reasons = ", ".join(idea.strategy.reasons)
            print(
                f"{idea.symbol:<12} {idea.strategy.side:<6} {idea.strategy.confidence:<12.2f} "
                f"{idea.action:<8} {str(idea.risk['risk_per_trade']):<18} {reasons:<60}"
            )

        for idea in ideas:
            if idea.action == "EXECUTE":
                print(self.engine.execute_from_idea(idea))

        print_trade_summary()
        print_trade_metrics()

if __name__ == "__main__":
    settings = get_settings()
    dashboard = ConsoleDashboard(settings.default_symbols)
    dashboard.render()