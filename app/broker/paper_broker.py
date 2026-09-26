from __future__ import annotations

from dataclasses import dataclass, field

from app.broker.base import BrokerAdapter, Order

@dataclass
class PaperBroker(BrokerAdapter):
    account_balance: float = 10000.0
    trades: list[Order] = field(default_factory=list)

    def get_account_summary(self) -> dict[str, float | list[Order]]:
        return {"balance": self.account_balance, "trades": self.trades}

    def place_order(self, symbol: str, side: str, quantity: float, reason: str, price: float | None = None) -> Order:
        order = Order(symbol=symbol, side=side, quantity=quantity, reason=reason, price=price)
        self.trades.append(order)
        return order
