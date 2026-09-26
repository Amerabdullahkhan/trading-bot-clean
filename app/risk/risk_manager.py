from __future__ import annotations

from dataclasses import dataclass

@dataclass
class RiskAssessment:
    allowed: bool
    reason: str
    position_size: float
    risk_per_trade: float
    confidence_adjusted: float

class RiskManager:
    def __init__(self, account_balance: float, max_daily_loss: float, max_risk_per_trade: float):
        self.account_balance = account_balance
        self.max_daily_loss = max_daily_loss
        self.max_risk_per_trade = max_risk_per_trade

    def evaluate(self, decision, daily_loss_so_far: float = 0.0, recent_drawdown: float = 0.0) -> RiskAssessment:
        if decision.side == "HOLD":
            return RiskAssessment(False, "hold_signal", 0.0, 0.0, decision.confidence)

        if daily_loss_so_far >= self.max_daily_loss:
            return RiskAssessment(False, "daily_loss_limit_reached", 0.0, 0.0, decision.confidence)

        if recent_drawdown > 0.18:
            return RiskAssessment(False, "drawdown_limit_reached", 0.0, 0.0, decision.confidence)

        max_loss_cap = self.account_balance * self.max_risk_per_trade
        position_size = min(max_loss_cap, self.account_balance * 0.02)
        risk_per_trade = position_size / max(self.account_balance, 1.0)

        if risk_per_trade > self.max_risk_per_trade:
            position_size = self.account_balance * self.max_risk_per_trade
            risk_per_trade = self.max_risk_per_trade

        confidence_adjusted = decision.confidence
        if decision.confidence < 0.6:
            confidence_adjusted = decision.confidence * 0.8

        return RiskAssessment(
            allowed=True,
            reason="risk_ok",
            position_size=float(position_size),
            risk_per_trade=float(risk_per_trade),
            confidence_adjusted=float(confidence_adjusted),
        )
