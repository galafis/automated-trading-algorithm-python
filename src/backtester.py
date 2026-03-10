"""
Strategy Backtesting Engine and Portfolio Management.

Author: Gabriel Demetrios Lafis
"""

from typing import Dict, List, Optional
from .indicators import calculate_returns, sharpe_ratio, sortino_ratio, max_drawdown


class BacktestEngine:
    """Backtests a trading strategy against historical price data."""

    def __init__(self, initial_capital: float = 100_000.0, commission: float = 0.001):
        self.initial_capital = initial_capital
        self.commission = commission

    def run(self, prices: List[float], signals: List[str]) -> Dict:
        """Run backtest.

        Args:
            prices: List of closing prices.
            signals: List of 'Buy', 'Sell', 'Hold' per bar.

        Returns:
            Dict with equity curve, trade log and performance metrics.
        """
        if len(prices) != len(signals):
            raise ValueError("prices and signals must have the same length")

        capital = self.initial_capital
        position = 0
        equity_curve = []
        trades: List[Dict] = []
        entry_price = 0.0

        for i, (price, signal) in enumerate(zip(prices, signals)):
            if signal == "Buy" and position == 0:
                shares = int(capital / (price * (1 + self.commission)))
                if shares > 0:
                    cost = shares * price * (1 + self.commission)
                    capital -= cost
                    position = shares
                    entry_price = price
                    trades.append({"type": "BUY", "price": price, "shares": shares, "bar": i})

            elif signal == "Sell" and position > 0:
                revenue = position * price * (1 - self.commission)
                capital += revenue
                pnl = (price - entry_price) * position
                trades.append({"type": "SELL", "price": price, "shares": position, "bar": i, "pnl": round(pnl, 2)})
                position = 0

            portfolio_value = capital + position * price
            equity_curve.append(round(portfolio_value, 2))

        final_value = equity_curve[-1] if equity_curve else self.initial_capital
        total_return = (final_value - self.initial_capital) / self.initial_capital
        returns = calculate_returns(equity_curve) if len(equity_curve) > 1 else []
        dd = max_drawdown(equity_curve) if equity_curve else {"max_drawdown": 0}

        winning_trades = [t for t in trades if t.get("pnl", 0) > 0]
        losing_trades = [t for t in trades if t.get("pnl", 0) < 0]

        return {
            "equity_curve": equity_curve,
            "final_value": round(final_value, 2),
            "total_return": round(total_return, 4),
            "total_trades": len([t for t in trades if t["type"] == "SELL"]),
            "winning_trades": len(winning_trades),
            "losing_trades": len(losing_trades),
            "sharpe_ratio": round(sharpe_ratio(returns), 4) if returns else 0,
            "sortino_ratio": round(sortino_ratio(returns), 4) if returns else 0,
            "max_drawdown": dd["max_drawdown"],
            "trades": trades,
        }


class PortfolioManager:
    """Track and manage a multi-asset portfolio."""

    def __init__(self, initial_capital: float = 100_000.0):
        self.cash = initial_capital
        self.positions: Dict[str, Dict] = {}
        self.history: List[Dict] = []

    def buy(self, symbol: str, price: float, quantity: int) -> bool:
        cost = price * quantity
        if cost > self.cash:
            return False
        self.cash -= cost
        if symbol in self.positions:
            pos = self.positions[symbol]
            total_qty = pos["quantity"] + quantity
            pos["avg_price"] = (pos["avg_price"] * pos["quantity"] + price * quantity) / total_qty
            pos["quantity"] = total_qty
        else:
            self.positions[symbol] = {"quantity": quantity, "avg_price": price}
        self.history.append({"action": "BUY", "symbol": symbol, "price": price, "quantity": quantity})
        return True

    def sell(self, symbol: str, price: float, quantity: int) -> bool:
        if symbol not in self.positions or self.positions[symbol]["quantity"] < quantity:
            return False
        revenue = price * quantity
        self.cash += revenue
        self.positions[symbol]["quantity"] -= quantity
        if self.positions[symbol]["quantity"] == 0:
            del self.positions[symbol]
        self.history.append({"action": "SELL", "symbol": symbol, "price": price, "quantity": quantity})
        return True

    def portfolio_value(self, current_prices: Dict[str, float]) -> float:
        value = self.cash
        for symbol, pos in self.positions.items():
            value += pos["quantity"] * current_prices.get(symbol, pos["avg_price"])
        return round(value, 2)

    def get_allocation(self, current_prices: Dict[str, float]) -> Dict[str, float]:
        total = self.portfolio_value(current_prices)
        alloc = {"cash": round(self.cash / total * 100, 2)}
        for symbol, pos in self.positions.items():
            val = pos["quantity"] * current_prices.get(symbol, pos["avg_price"])
            alloc[symbol] = round(val / total * 100, 2)
        return alloc
