"""
Tests for Automated Trading Algorithm.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.strategy import MovingAverageCrossoverStrategy
from src.main import fetch_historical_data
from src.indicators import sma, ema, rsi, macd, bollinger_bands, calculate_returns, sharpe_ratio, sortino_ratio, max_drawdown
from src.backtester import BacktestEngine, PortfolioManager


# ── Indicator Tests ───────────────────────────────────────────────────

class TestSMA:
    def test_basic(self):
        result = sma([1, 2, 3, 4, 5], 3)
        assert result[2] == 2.0
        assert result[4] == 4.0

    def test_none_padding(self):
        result = sma([1, 2, 3], 2)
        assert result[0] is None
        assert result[1] == 1.5


class TestEMA:
    def test_basic(self):
        result = ema([1, 2, 3, 4, 5], 3)
        assert result[2] is not None
        assert len(result) == 5

    def test_empty(self):
        assert ema([], 3) == []


class TestRSI:
    def test_length(self):
        prices = list(range(1, 30))
        result = rsi(prices, 14)
        assert len(result) == len(prices)

    def test_padded_with_none(self):
        result = rsi(list(range(1, 20)), 14)
        assert result[0] is None


class TestMACD:
    def test_returns_dict(self):
        prices = [float(x) for x in range(1, 50)]
        result = macd(prices)
        assert "macd" in result
        assert "signal" in result
        assert "histogram" in result

    def test_length_match(self):
        prices = [float(x) for x in range(1, 50)]
        result = macd(prices)
        assert len(result["macd"]) == len(prices)


class TestBollingerBands:
    def test_returns_bands(self):
        prices = [float(x) for x in range(1, 30)]
        result = bollinger_bands(prices, 10)
        assert "upper" in result
        assert "middle" in result
        assert "lower" in result

    def test_upper_above_lower(self):
        prices = [100 + x * 0.5 for x in range(30)]
        result = bollinger_bands(prices, 10)
        for u, l in zip(result["upper"], result["lower"]):
            if u is not None and l is not None:
                assert u >= l


class TestRiskMetrics:
    def test_calculate_returns(self):
        returns = calculate_returns([100, 110, 105])
        assert len(returns) == 2
        assert abs(returns[0] - 0.1) < 1e-6

    def test_sharpe_ratio(self):
        returns = [0.01] * 252
        sr = sharpe_ratio(returns)
        assert sr > 0

    def test_sortino_ratio(self):
        returns = [0.01, -0.005, 0.02, -0.001, 0.015]
        result = sortino_ratio(returns)
        assert isinstance(result, float)

    def test_max_drawdown(self):
        prices = [100, 110, 90, 95, 80, 120]
        dd = max_drawdown(prices)
        expected = (110 - 80) / 110
        assert abs(dd["max_drawdown"] - round(expected, 6)) < 1e-5


# ── Strategy Tests ────────────────────────────────────────────────────

class TestMovingAverageCrossover:
    def test_signals_columns(self):
        import pandas as pd
        data = fetch_historical_data()
        strategy = MovingAverageCrossoverStrategy(20, 50)
        signals = strategy.generate_signals(data)
        assert "short_mavg" in signals.columns
        assert "long_mavg" in signals.columns
        assert "action" in signals.columns

    def test_valid_actions(self):
        data = fetch_historical_data()
        strategy = MovingAverageCrossoverStrategy(5, 10)
        signals = strategy.generate_signals(data)
        assert set(signals["action"].unique()).issubset({"Buy", "Sell", "Hold"})


# ── Backtest Tests ────────────────────────────────────────────────────

class TestBacktestEngine:
    def test_buy_and_hold(self):
        engine = BacktestEngine(initial_capital=10000, commission=0)
        prices = [100, 105, 110, 115, 120]
        signals = ["Buy", "Hold", "Hold", "Hold", "Sell"]
        result = engine.run(prices, signals)
        assert result["total_trades"] == 1
        assert result["final_value"] > 10000

    def test_no_trades(self):
        engine = BacktestEngine()
        prices = [100, 101, 102]
        signals = ["Hold", "Hold", "Hold"]
        result = engine.run(prices, signals)
        assert result["total_trades"] == 0
        assert result["final_value"] == 100000

    def test_length_mismatch(self):
        engine = BacktestEngine()
        with pytest.raises(ValueError):
            engine.run([100, 200], ["Buy"])


# ── Portfolio Tests ───────────────────────────────────────────────────

class TestPortfolioManager:
    def test_buy(self):
        pm = PortfolioManager(10000)
        assert pm.buy("AAPL", 150, 10)
        assert pm.cash == 10000 - 1500

    def test_sell(self):
        pm = PortfolioManager(10000)
        pm.buy("AAPL", 100, 10)
        assert pm.sell("AAPL", 110, 10)
        assert pm.cash == 10000 - 1000 + 1100

    def test_insufficient_funds(self):
        pm = PortfolioManager(100)
        assert not pm.buy("AAPL", 150, 10)

    def test_insufficient_position(self):
        pm = PortfolioManager(10000)
        assert not pm.sell("AAPL", 100, 5)

    def test_portfolio_value(self):
        pm = PortfolioManager(10000)
        pm.buy("AAPL", 100, 10)
        value = pm.portfolio_value({"AAPL": 120})
        assert value == 10000 - 1000 + 1200

    def test_allocation(self):
        pm = PortfolioManager(10000)
        pm.buy("AAPL", 100, 50)
        alloc = pm.get_allocation({"AAPL": 100})
        assert "cash" in alloc
        assert "AAPL" in alloc
        assert abs(alloc["cash"] + alloc["AAPL"] - 100) < 0.1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
