from __future__ import annotations

from dataclasses import dataclass

from app.broker.paper_broker import PaperBroker
from app.risk.risk_manager import RiskManager
from app.strategies.ensemble import StrategyDecision, StrategyEnsemble

@dataclass
class TradeIdea:
    symbol: str
    strategy: StrategyDecision
    risk: dict
    action: str

class SignalEngine:
    def __init__(self, provider, risk_manager: RiskManager, broker: PaperBroker, min_confidence: float = 0.55):
        self.provider = provider
        self.risk_manager = risk_manager
        self.broker = broker
        self.ensemble = StrategyEnsemble(min_confidence=min_confidence)

    def scan(self, symbols: list[str], daily_loss_so_far: float = 0.0, recent_drawdown: float = 0.0) -> list[TradeIdea]:
        ideas: list[TradeIdea] = []
        for symbol in symbols:
            candles = self.provider.get_history(symbol, periods=200)
            decision = self.ensemble.analyze(symbol, candles)
            assessment = self.risk_manager.evaluate(decision, daily_loss_so_far, recent_drawdown)
            action = "EXECUTE" if assessment.allowed else "SKIP"
            ideas.append(
                TradeIdea(
                    symbol=symbol,
                    strategy=decision,
                    risk={
                        "allowed": assessment.allowed,
                        "reason": assessment.reason,
                        "position_size": assessment.position_size,
                        "risk_per_trade": assessment.risk_per_trade,
                        "confidence_adjusted": assessment.confidence_adjusted,
                    },
                    action=action,
                )
            )
        return ideas

    def execute_from_idea(self, idea: TradeIdea) -> str:
        if idea.action != "EXECUTE":
            return f"Signal for {idea.symbol} skipped: {idea.risk['reason']}"
        order = self.broker.place_order(
            symbol=idea.symbol,
            side=idea.strategy.side,
            quantity=idea.risk["position_size"],
            reason=",".join(idea.strategy.reasons),
            price=None,
        )
        return f"Order placed: {order.side} {order.symbol} qty={order.quantity}"
