from __future__ import annotations

import pandas as pd


def to_dataframe(candles):
    data = pd.DataFrame(
        [
            {
                "timestamp": c.timestamp,
                "open": c.open,
                "high": c.high,
                "low": c.low,
                "close": c.close,
                "volume": c.volume,
            }
            for c in candles
        ]
    )
    if data.empty:
        return data
    data = data.sort_values("timestamp").reset_index(drop=True)
    return data


def ema(series: pd.Series, period: int) -> float:
    if series.empty:
        return 0.0
    return float(series.ewm(span=period, adjust=False).mean().iloc[-1])


def sma(series: pd.Series, period: int) -> float:
    if series.empty:
        return 0.0
    return float(series.tail(period).mean())


def rsi(series: pd.Series, period: int = 14) -> float:
    if series.empty:
        return 50.0
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    avg_gain = up.ewm(com=period - 1, adjust=False).mean()
    avg_loss = down.ewm(com=period - 1, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, pd.NA)
    val = 100 - (100 / (1 + rs))
    return float(val.iloc[-1])


def macd_histogram(series: pd.Series) -> float:
    if series.empty:
        return 0.0
    fast = series.ewm(span=12, adjust=False).mean()
    slow = series.ewm(span=26, adjust=False).mean()
    macd = fast - slow
    signal = macd.ewm(span=9, adjust=False).mean()
    return float((macd - signal).iloc[-1])


def bollinger_bands(series: pd.Series, period: int = 20, std_dev: int = 2):
    if series.empty:
        return (0.0, 0.0, 0.0)
    rolling = series.rolling(window=period)
    mid = rolling.mean().iloc[-1]
    std = rolling.std().iloc[-1]
    upper = mid + std_dev * std
    lower = mid - std_dev * std
    return float(mid), float(upper), float(lower)


def atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> float:
    if high.empty:
        return 0.0
    df = pd.DataFrame({"high": high, "low": low, "close": close})
    hl = df["high"] - df["low"]
    hc = (df["high"] - df["close"].shift(1)).abs()
    lc = (df["low"] - df["close"].shift(1)).abs()
    true_range = pd.concat([hl, hc, lc], axis=1).max(axis=1)
    return float(true_range.rolling(window=period).mean().iloc[-1])


def market_features(candles):
    df = to_dataframe(candles)
    if df.empty:
        return {
            "close": 0.0,
            "ema_fast": 0.0,
            "ema_slow": 0.0,
            "sma_20": 0.0,
            "rsi": 50.0,
            "macd_hist": 0.0,
            "bb_mid": 0.0,
            "bb_upper": 0.0,
            "bb_lower": 0.0,
            "atr": 0.0,
        }

    close = df["close"]
    return {
        "close": float(close.iloc[-1]),
        "ema_fast": ema(close, 12),
        "ema_slow": ema(close, 26),
        "sma_20": sma(close, 20),
        "rsi": rsi(close, 14),
        "macd_hist": macd_histogram(close),
        "bb_mid": bollinger_bands(close)[0],
        "bb_upper": bollinger_bands(close)[1],
        "bb_lower": bollinger_bands(close)[2],
        "atr": atr(df["high"], df["low"], df["close"], 14),
    }
