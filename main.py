from __future__ import annotations

from app.broker.paper_broker import PaperBroker
from app.config import get_settings
from app.data.provider import SyntheticMarketDataProvider
from app.engine.signal_engine import SignalEngine
from app.risk.risk_manager import RiskManager

def main() -> None:
    settings = get_settings()
    provider = SyntheticMarketDataProvider()
    broker = PaperBroker(account_balance=settings.account_balance)
    risk_manager = RiskManager(
        account_balance=settings.account_balance,
        max_daily_loss=settings.max_daily_loss,
        max_risk_per_trade=settings.max_risk_per_trade,
    )
    engine = SignalEngine(
        provider=provider,
        risk_manager=risk_manager,
        broker=broker,
    )

    ideas = engine.scan(settings.default_symbols)
    print("Market scan results")
    print("=" * 120)
    for idea in ideas:
        print(
            f"{idea.symbol:<12} {idea.strategy.side:<6} "
            f"confidence={idea.strategy.confidence:.2f} | "
            f"reasons={idea.strategy.reasons} | action={idea.action} | "
            f"risk={idea.risk}"
        )

    for idea in ideas:
        if idea.action == "EXECUTE":
            print(engine.execute_from_idea(idea))

if __name__ == "__main__":
    main()
