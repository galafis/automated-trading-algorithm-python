"""
Unit tests for automated-trading-algorithm-python
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.strategy import MovingAverageCrossoverStrategy
from src.main import fetch_historical_data


@pytest.fixture
def sample_data():
    """Generate sample OHLCV data."""
    dates = pd.date_range('2023-01-01', periods=100, freq='D')
    np.random.seed(42)
    prices = 100 + np.cumsum(np.random.randn(100) * 0.5)
    return pd.DataFrame({
        'Open': prices + np.random.uniform(-0.5, 0.5, 100),
        'High': prices + np.abs(np.random.uniform(0, 1, 100)),
        'Low': prices - np.abs(np.random.uniform(0, 1, 100)),
        'Close': prices,
        'Volume': np.random.uniform(1e5, 5e5, 100),
    }, index=dates)


@pytest.fixture
def strategy():
    return MovingAverageCrossoverStrategy(short_window=5, long_window=10)


class TestFetchHistoricalData:
    def test_returns_dataframe(self):
        df = fetch_historical_data()
        assert isinstance(df, pd.DataFrame)

    def test_has_ohlcv_columns(self):
        df = fetch_historical_data()
        for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
            assert col in df.columns

    def test_custom_date_range(self):
        df = fetch_historical_data(start_date='2023-06-01', end_date='2023-06-30')
        assert len(df) == 30


class TestMovingAverageCrossoverStrategy:
    def test_generate_signals_columns(self, strategy, sample_data):
        signals = strategy.generate_signals(sample_data)
        assert 'short_mavg' in signals.columns
        assert 'long_mavg' in signals.columns
        assert 'action' in signals.columns

    def test_signals_same_length_as_data(self, strategy, sample_data):
        signals = strategy.generate_signals(sample_data)
        assert len(signals) == len(sample_data)

    def test_no_nan_in_action(self, strategy, sample_data):
        signals = strategy.generate_signals(sample_data)
        assert not signals['action'].isnull().any()

    def test_actions_are_valid(self, strategy, sample_data):
        signals = strategy.generate_signals(sample_data)
        valid_actions = {'Buy', 'Sell', 'Hold'}
        assert set(signals['action'].unique()).issubset(valid_actions)

    def test_crossover_generates_buy_and_sell(self):
        """Price that rises then falls should produce both Buy and Sell signals."""
        prices = list(range(10, 35)) + list(range(35, 10, -1))
        data = pd.DataFrame({
            'Close': prices,
        }, index=pd.date_range('2023-01-01', periods=len(prices)))

        strategy = MovingAverageCrossoverStrategy(short_window=3, long_window=5)
        signals = strategy.generate_signals(data)

        assert 'Buy' in signals['action'].values
        assert 'Sell' in signals['action'].values

    def test_flat_prices_no_trades(self):
        """Constant price should produce no Buy/Sell signals."""
        data = pd.DataFrame({
            'Close': [100.0] * 50,
        }, index=pd.date_range('2023-01-01', periods=50))

        strategy = MovingAverageCrossoverStrategy(short_window=5, long_window=10)
        signals = strategy.generate_signals(data)

        trades = signals[signals['action'].isin(['Buy', 'Sell'])]
        assert len(trades) == 0

    def test_short_window_smaller_than_long(self, strategy):
        assert strategy.short_window < strategy.long_window

    def test_different_window_sizes(self, sample_data):
        s1 = MovingAverageCrossoverStrategy(short_window=5, long_window=20)
        s2 = MovingAverageCrossoverStrategy(short_window=10, long_window=30)
        sig1 = s1.generate_signals(sample_data)
        sig2 = s2.generate_signals(sample_data)
        # Different window sizes should produce different moving averages
        assert not sig1['short_mavg'].equals(sig2['short_mavg'])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
