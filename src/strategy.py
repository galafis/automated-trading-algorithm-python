import pandas as pd
import numpy as np

class MovingAverageCrossoverStrategy:
    """Estratégia de trading baseada no cruzamento de médias móveis."""

    def __init__(self, short_window, long_window):
        self.short_window = short_window
        self.long_window = long_window

    def generate_signals(self, data):
        """Gera sinais de compra/venda com base na estratégia de cruzamento de médias móveis.

        Args:
            data (pd.DataFrame): DataFrame com os dados históricos do ativo, incluindo a coluna 'Close'.

        Returns:
            pd.DataFrame: DataFrame com os sinais de trading ('Buy', 'Sell', 'Hold').
        """
        signals = pd.DataFrame(index=data.index)
        signals['signal'] = 0.0

        # Calcular médias móveis
        signals['short_mavg'] = data['Close'].rolling(window=self.short_window, min_periods=1, center=False).mean()
        signals['long_mavg'] = data['Close'].rolling(window=self.long_window, min_periods=1, center=False).mean()

        # Gerar sinais de compra (1.0) quando a média móvel curta cruza acima da longa
        signals.loc[signals.index[self.short_window:], 'signal'] = np.where(signals['short_mavg'][self.short_window:] > signals['long_mavg'][self.short_window:], 1.0, 0.0)


        # Gerar sinais de trading (compra/venda)
        signals['positions'] = signals['signal'].diff()

        # Mapear posições para 'Buy', 'Sell', 'Hold'
        signals['action'] = 'Hold'
        signals.loc[signals['positions'] == 1.0, 'action'] = 'Buy'
        signals.loc[signals['positions'] == -1.0, 'action'] = 'Sell'

        return signals[['short_mavg', 'long_mavg', 'action']]

