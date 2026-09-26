from __future__ import annotations

from app.broker.paper_broker import PaperBroker
from app.data.provider import SyntheticMarketDataProvider
from app.engine.signal_engine import SignalEngine
from app.risk.risk_manager import RiskManager


def test_signal_engine_generates_actions():
    provider = SyntheticMarketDataProvider()
    broker = PaperBroker(account_balance=10000)
    risk_manager = RiskManager(account_balance=10000, max_daily_loss=200, max_risk_per_trade=0.02)
    engine = SignalEngine(provider=provider, risk_manager=risk_manager, broker=broker)

    ideas = engine.scan(["EUR/USD", "XAU/USD", "BTC/USD"])
    assert isinstance(ideas, list)
    assert len(ideas) == 3
    for idea in ideas:
        assert idea.strategy.side in {"BUY", "SELL", "HOLD"}
        assert idea.action in {"EXECUTE", "SKIP"}
