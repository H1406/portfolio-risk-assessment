import numpy as np
import pandas as pd
from typing import Dict, Tuple


def calculate_sma(prices: np.ndarray, period: int) -> np.ndarray:
    """Calculate Simple Moving Average"""
    return pd.Series(prices).rolling(window=period).mean().values


def calculate_rsi(prices: np.ndarray, period: int = 14) -> float:
    """Calculate Relative Strength Index"""
    if len(prices) < period + 1:
        return 50.0  # Neutral if not enough data

    deltas = np.diff(prices[-period - 1 :])
    seed = deltas[:period].mean()
    up = deltas[-period:].copy()
    down = -deltas[-period:].copy()
    up[up < 0] = 0
    down[down < 0] = 0

    rs = np.zeros_like(up)
    rs[:] = up

    for i in range(1, len(rs)):
        rs[i] = (rs[i - 1] * (period - 1) + up[i]) / period

    down_ema = np.zeros_like(down)
    down_ema[:] = down

    for i in range(1, len(down_ema)):
        down_ema[i] = (down_ema[i - 1] * (period - 1) + down[i]) / period

    rs = rs / (down_ema + 1e-10)
    rsi = 100.0 - (100.0 / (1.0 + rs[-1]))

    return rsi


def detect_dca_signal(prices_df: pd.DataFrame, asset_name: str) -> Dict:
    """
    Detect DCA (Dollar-Cost Averaging) timing signal based on technical indicators

    Args:
        prices_df: DataFrame with 'date' and 'close' columns
        asset_name: Name of the asset being analyzed

    Returns:
        Dictionary with signal, confidence, and reasoning
    """

    if len(prices_df) < 50:
        return {
            "signal": "HOLD",
            "confidence": 0.3,
            "reasoning": "Not enough historical data for reliable analysis",
            "current_price": float(prices_df["close"].iloc[-1]),
            "sma_20": float(prices_df["close"].iloc[-1]),
            "sma_50": float(prices_df["close"].iloc[-1]),
            "rsi": 50.0,
        }

    prices = prices_df["close"].values
    current_price = prices[-1]

    # Calculate technical indicators
    sma_20 = calculate_sma(prices, 20)[-1]
    sma_50 = calculate_sma(prices, 50)[-1]
    rsi = calculate_rsi(prices, 14)

    # Validate calculations
    if np.isnan(sma_20) or np.isnan(sma_50) or np.isnan(rsi):
        return {
            "signal": "HOLD",
            "confidence": 0.3,
            "reasoning": "Unable to calculate technical indicators",
            "current_price": float(current_price),
            "sma_20": float(sma_20) if not np.isnan(sma_20) else float(current_price),
            "sma_50": float(sma_50) if not np.isnan(sma_50) else float(current_price),
            "rsi": float(rsi) if not np.isnan(rsi) else 50.0,
        }

    # Initialize signal and confidence
    signal = "HOLD"
    confidence = 0.5
    reasoning_parts = []

    # Analysis logic
    price_to_sma20 = (current_price - sma_20) / sma_20 if sma_20 > 0 else 0
    price_to_sma50 = (current_price - sma_50) / sma_50 if sma_50 > 0 else 0

    # RSI Analysis (Oversold/Overbought)
    if rsi < 30:
        signal = "BUY"
        confidence += 0.25
        reasoning_parts.append(f"RSI is {rsi:.1f} (oversold)")
    elif rsi > 70:
        signal = "SELL"
        confidence = max(0.3, confidence - 0.15)
        reasoning_parts.append(f"RSI is {rsi:.1f} (overbought)")
    else:
        reasoning_parts.append(f"RSI is {rsi:.1f} (neutral)")

    # Price vs SMA Analysis
    if current_price < sma_20 and current_price < sma_50:
        if signal != "SELL":
            signal = "BUY"
        confidence += 0.2
        reasoning_parts.append(
            "Price is below both 20-day and 50-day SMAs (potential buying opportunity)"
        )
    elif current_price > sma_20 and current_price > sma_50:
        signal = "HOLD"
        if rsi > 60:
            confidence = min(0.9, confidence + 0.15)
        reasoning_parts.append("Price is above both moving averages (strong uptrend)")
    else:
        if price_to_sma20 < -0.05:  # More than 5% below
            if signal != "SELL":
                signal = "BUY"
            confidence += 0.15
            reasoning_parts.append("Price is significantly below 20-day SMA")
        elif price_to_sma20 > 0.05:  # More than 5% above
            if signal != "BUY":
                signal = "HOLD"
            reasoning_parts.append("Price is significantly above 20-day SMA")

    # Trend analysis using SMA crossing
    if sma_20 > sma_50:
        if signal != "SELL":
            confidence += 0.1
        reasoning_parts.append("20-day SMA above 50-day SMA (bullish trend)")
    else:
        if signal != "BUY":
            confidence = max(0.2, confidence - 0.1)
        reasoning_parts.append("20-day SMA below 50-day SMA (bearish trend)")

    # Volatility consideration
    recent_prices = prices[-20:]
    volatility = np.std(recent_prices) / np.mean(recent_prices)

    if volatility > 0.05:  # High volatility
        confidence = max(0.3, confidence - 0.1)
        reasoning_parts.append(
            f"High volatility detected ({volatility:.2%}) - be cautious"
        )

    # Normalize confidence to 0-1 range
    confidence = max(0.2, min(0.95, confidence))

    reasoning = ". ".join(reasoning_parts)

    return {
        "signal": signal,
        "confidence": float(confidence),
        "reasoning": reasoning,
        "current_price": float(current_price),
        "sma_20": float(sma_20),
        "sma_50": float(sma_50),
        "rsi": float(rsi),
    }


def get_asset_prices(asset_id: str, data_dict: Dict) -> pd.DataFrame:
    """Extract price data for a specific asset"""

    if asset_id == "btcusd":
        data = data_dict.get("btcusd_data")
        if data is not None:
            df = data.copy()
            df["close"] = pd.to_numeric(df["close"], errors="coerce")
            return df.dropna()
    elif asset_id == "xautusd":
        data = data_dict.get("xautusd_data")
        if data is not None:
            df = data.copy()
            df["close"] = pd.to_numeric(df["close"], errors="coerce")
            return df.dropna()
    elif asset_id == "vn30":
        data = data_dict.get("vn30_data")
        if data is not None:
            df = data.copy()
            df["close"] = pd.to_numeric(df["close"], errors="coerce")
            return df.dropna()

    return pd.DataFrame()
