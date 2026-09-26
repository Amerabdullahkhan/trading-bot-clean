from __future__ import annotations

import math
import random
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

@dataclass
class Candle:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0

class MarketDataProvider:
    def get_history(self, symbol: str, periods: int = 200) -> List[Candle]:
        raise NotImplementedError

class SyntheticMarketDataProvider(MarketDataProvider):
    def __init__(self, base_prices: dict[str, float] | None = None):
        self.base_prices = base_prices or {
            "EUR/USD": 1.085,
            "GBP/USD": 1.265,
            "XAU/USD": 2045.0,
            "USD/JPY": 152.2,
            "BTC/USD": 62000.0,
        }

    def get_history(self, symbol: str, periods: int = 200) -> List[Candle]:
        base = self.base_prices.get(symbol, 100.0)
        candles: List[Candle] = []
        now = datetime.utcnow().replace(minute=0, second=0, microsecond=0)

        for i in range(periods):
            drift = (i / periods) * 0.08
            phase = math.sin(i * 0.35)
            open_price = base * (1 + drift + phase * 0.01 + random.uniform(-0.003, 0.003))
            close_price = open_price * (1 + random.uniform(-0.006, 0.006))
            high = max(open_price, close_price) * (1 + random.uniform(0.001, 0.008))
            low = min(open_price, close_price) * (1 - random.uniform(0.001, 0.008))
            candles.append(
                Candle(
                    timestamp=now - timedelta(hours=periods - i),
                    open=float(open_price),
                    high=float(high),
                    low=float(low),
                    close=float(close_price),
                    volume=float(abs(math.sin(i * 0.7)) * 1000 + random.uniform(100, 700)),
                )
            )
        return candles
