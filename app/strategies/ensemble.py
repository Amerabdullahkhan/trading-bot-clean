from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.strategies.indicators import market_features


@dataclass
class StrategyDecision:
    symbol: str
    side: str
    confidence: float
    reasons: list[str] = field(default_factory=list)
    strategy_scores: dict[str, float] = field(default_factory=dict)


class StrategyEnsemble:
    def __init__(self, min_confidence: float = 0.55):
        self.min_confidence = min_confidence

    def analyze(self, symbol: str, candles: list[Any]) -> StrategyDecision:
        features = market_features(candles)
        close = features["close"]
        ema_fast = features["ema_fast"]
        ema_slow = features["ema_slow"]
        sma_20 = features["sma_20"]
        rsi = features["rsi"]
        macd_hist = features["macd_hist"]
        bb_mid = features["bb_mid"]
        bb_upper = features["bb_upper"]
        bb_lower = features["bb_lower"]
        atr = features["atr"]

        trend_signal = 0.0
        reasons: list[str] = []

        if ema_fast > ema_slow and close > sma_20:
            trend_signal += 0.45
            reasons.append("trend_up")
        elif ema_fast < ema_slow and close < sma_20:
            trend_signal -= 0.45
            reasons.append("trend_down")
        else:
            reasons.append("range_market")

        momentum_signal = 0.0
        if rsi > 55:
            momentum_signal += 0.25
            reasons.append("momentum_bullish")
        elif rsi < 45:
            momentum_signal -= 0.25
            reasons.append("momentum_bearish")
        else:
            reasons.append("momentum_neutral")

        mean_reversion_signal = 0.0
        if close < bb_lower:
            mean_reversion_signal += 0.15
            reasons.append("oversold")
        elif close > bb_upper:
            mean_reversion_signal -= 0.15
            reasons.append("overbought")

        volatility_signal = 0.0
        if atr > 0 and (close - bb_mid) / max(atr, 1e-9) > 1.0:
            volatility_signal += 0.10
            reasons.append("volatility_healthy")
        elif atr > 0 and abs((close - bb_mid) / max(atr, 1e-9)) < 0.5:
            volatility_signal -= 0.10
            reasons.append("volatility_low")

        macd_signal = 0.0
        if macd_hist > 0:
            macd_signal += 0.15
        elif macd_hist < 0:
            macd_signal -= 0.15

        score = trend_signal + momentum_signal + mean_reversion_signal + volatility_signal + macd_signal

        if score > 0.4:
            side = "BUY"
            confidence = min(0.95, max(0.5, abs(score) / 1.5))
        elif score < -0.4:
            side = "SELL"
            confidence = min(0.95, max(0.5, abs(score) / 1.5))
        else:
            side = "HOLD"
            confidence = 0.1

        if side != "HOLD" and confidence < self.min_confidence:
            side = "HOLD"
            confidence = 0.1

        return StrategyDecision(
            symbol=symbol,
            side=side,
            confidence=float(confidence),
            reasons=reasons,
            strategy_scores={
                "trend": float(trend_signal),
                "momentum": float(momentum_signal),
                "mean_reversion": float(mean_reversion_signal),
                "volatility": float(volatility_signal),
                "macd": float(macd_signal),
            },
        )
