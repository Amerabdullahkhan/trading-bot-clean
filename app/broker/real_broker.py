from __future__ import annotations

import os

from app.broker.base import BrokerAdapter, Order

class PocketBrokerAdapter(BrokerAdapter):
    def __init__(self, endpoint: str | None = None, api_key: str | None = None, secret: str | None = None, account_id: str | None = None):
        self.endpoint = endpoint or os.getenv("POCKET_BROKER_ENDPOINT")
        self.api_key = api_key or os.getenv("POCKET_BROKER_API_KEY")
        self.secret = secret or os.getenv("POCKET_BROKER_SECRET")
        self.account_id = account_id or os.getenv("POCKET_BROKER_ACCOUNT_ID")

    def get_account_summary(self) -> dict[str, str]:
        if not self.endpoint or not self.api_key:
            raise RuntimeError("Pocket Broker is not configured. Add env vars before enabling live mode.")
        return {"endpoint": self.endpoint, "account_id": self.account_id or "unknown", "status": "configured"}

    def place_order(self, symbol: str, side: str, quantity: float, reason: str, price: float | None = None) -> Order:
        if not self.endpoint or not self.api_key:
            raise RuntimeError("Live mode is disabled until broker credentials are configured.")
        return Order(symbol=symbol, side=side, quantity=quantity, reason=reason, price=price)
