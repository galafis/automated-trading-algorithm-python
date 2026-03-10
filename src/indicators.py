"""
Technical Indicators Module

SMA, EMA, RSI, MACD, Bollinger Bands, and portfolio risk metrics.

Author: Gabriel Demetrios Lafis
"""

import math
from typing import Dict, List, Tuple


def sma(prices: List[float], window: int) -> List[float]:
    """Simple Moving Average."""
    result = [None] * (window - 1)
    for i in range(window - 1, len(prices)):
        result.append(sum(prices[i - window + 1: i + 1]) / window)
    return result


def ema(prices: List[float], window: int) -> List[float]:
    """Exponential Moving Average."""
    if not prices:
        return []
    multiplier = 2 / (window + 1)
    result = [None] * (window - 1)
    first_sma = sum(prices[:window]) / window
    result.append(first_sma)
    for i in range(window, len(prices)):
        val = (prices[i] - result[-1]) * multiplier + result[-1]
        result.append(val)
    return result


def rsi(prices: List[float], window: int = 14) -> List[float]:
    """Relative Strength Index."""
    if len(prices) < window + 1:
        return [None] * len(prices)
    deltas = [prices[i] - prices[i - 1] for i in range(1, len(prices))]
    gains = [max(0, d) for d in deltas]
    losses = [max(0, -d) for d in deltas]

    avg_gain = sum(gains[:window]) / window
    avg_loss = sum(losses[:window]) / window

    result = [None] * window
    if avg_loss == 0:
        result.append(100.0)
    else:
        rs = avg_gain / avg_loss
        result.append(100 - 100 / (1 + rs))

    for i in range(window, len(deltas)):
        avg_gain = (avg_gain * (window - 1) + gains[i]) / window
        avg_loss = (avg_loss * (window - 1) + losses[i]) / window
        if avg_loss == 0:
            result.append(100.0)
        else:
            rs = avg_gain / avg_loss
            result.append(100 - 100 / (1 + rs))

    return result


def macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, List[float]]:
    """MACD indicator with signal line and histogram."""
    ema_fast = ema(prices, fast)
    ema_slow = ema(prices, slow)
    macd_line = []
    for f, s in zip(ema_fast, ema_slow):
        if f is None or s is None:
            macd_line.append(None)
        else:
            macd_line.append(f - s)
    valid_macd = [v for v in macd_line if v is not None]
    signal_line_vals = ema(valid_macd, signal) if valid_macd else []
    # Pad signal line
    pad = len(macd_line) - len(valid_macd)
    signal_padded = [None] * (pad + signal - 1) + signal_line_vals[signal - 1:] if signal_line_vals else [None] * len(macd_line)
    # Extend if needed
    while len(signal_padded) < len(macd_line):
        signal_padded.append(None)
    histogram = []
    for m, s in zip(macd_line, signal_padded):
        if m is not None and s is not None:
            histogram.append(m - s)
        else:
            histogram.append(None)
    return {"macd": macd_line, "signal": signal_padded, "histogram": histogram}


def bollinger_bands(prices: List[float], window: int = 20, num_std: float = 2.0) -> Dict[str, List[float]]:
    """Bollinger Bands."""
    middle = sma(prices, window)
    upper = []
    lower = []
    for i in range(len(prices)):
        if middle[i] is None:
            upper.append(None)
            lower.append(None)
        else:
            subset = prices[i - window + 1: i + 1]
            mean = sum(subset) / len(subset)
            variance = sum((x - mean) ** 2 for x in subset) / len(subset)
            std = math.sqrt(variance)
            upper.append(middle[i] + num_std * std)
            lower.append(middle[i] - num_std * std)
    return {"upper": upper, "middle": middle, "lower": lower}


# ── Risk Metrics ──────────────────────────────────────────────────────

def calculate_returns(prices: List[float]) -> List[float]:
    """Calculate simple returns from a price series."""
    return [(prices[i] / prices[i - 1]) - 1 for i in range(1, len(prices))]


def sharpe_ratio(returns: List[float], risk_free_rate: float = 0.0, periods: int = 252) -> float:
    """Annualized Sharpe Ratio."""
    if not returns:
        return 0.0
    mean_ret = sum(returns) / len(returns)
    excess = mean_ret - risk_free_rate / periods
    variance = sum((r - mean_ret) ** 2 for r in returns) / len(returns)
    std = math.sqrt(variance)
    if std == 0:
        return 0.0
    return (excess / std) * math.sqrt(periods)


def sortino_ratio(returns: List[float], risk_free_rate: float = 0.0, periods: int = 252) -> float:
    """Annualized Sortino Ratio."""
    if not returns:
        return 0.0
    mean_ret = sum(returns) / len(returns)
    excess = mean_ret - risk_free_rate / periods
    downside = [min(0, r - risk_free_rate / periods) ** 2 for r in returns]
    downside_dev = math.sqrt(sum(downside) / len(downside))
    if downside_dev == 0:
        return 0.0
    return (excess / downside_dev) * math.sqrt(periods)


def max_drawdown(prices: List[float]) -> Dict[str, float]:
    """Calculate maximum drawdown and its duration."""
    if len(prices) < 2:
        return {"max_drawdown": 0.0, "peak_idx": 0, "trough_idx": 0}
    peak = prices[0]
    max_dd = 0
    peak_idx = 0
    trough_idx = 0
    current_peak_idx = 0
    for i, price in enumerate(prices):
        if price > peak:
            peak = price
            current_peak_idx = i
        dd = (peak - price) / peak
        if dd > max_dd:
            max_dd = dd
            peak_idx = current_peak_idx
            trough_idx = i
    return {"max_drawdown": round(max_dd, 6), "peak_idx": peak_idx, "trough_idx": trough_idx}
