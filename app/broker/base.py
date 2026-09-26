from __future__ import annotations

from dataclasses import dataclass, field

@dataclass
class Order:
    symbol: str
    side: str
    quantity: float
    reason: str
    price: float | None = None

class BrokerAdapter:
    def get_account_summary(self):
        raise NotImplementedError

    def place_order(self, symbol: str, side: str, quantity: float, reason: str, price: float | None = None) -> Order:
        raise NotImplementedError
