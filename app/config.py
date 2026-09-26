from __future__ import annotations

import os
from dataclasses import dataclass, field

@dataclass
class Settings:
    broker_mode: str = "paper"
    account_balance: float = 10000.0
    max_daily_loss: float = 200.0
    max_risk_per_trade: float = 0.02
    default_symbols: list[str] = field(
        default_factory=lambda: ["EUR/USD", "GBP/USD", "XAU/USD", "USD/JPY", "BTC/USD"]
    )
    timeframe: str = "1h"

    @classmethod
    def from_env(cls) -> "Settings":
        symbols_raw = os.getenv("DEFAULT_SYMBOLS", "EUR/USD,GBP/USD,XAU/USD,USD/JPY,BTC/USD")
        return cls(
            broker_mode=os.getenv("BROKER_MODE", "paper"),
            account_balance=float(os.getenv("ACCOUNT_BALANCE", "10000")),
            max_daily_loss=float(os.getenv("MAX_DAILY_LOSS", "200")),
            max_risk_per_trade=float(os.getenv("MAX_RISK_PER_TRADE", "0.02")),
            default_symbols=[s.strip() for s in symbols_raw.split(",") if s.strip()],
            timeframe=os.getenv("TIMEFRAME", "1h"),
        )

def get_settings() -> Settings:
    return Settings.from_env()
