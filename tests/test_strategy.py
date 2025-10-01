import unittest
import pandas as pd
from src.strategy import MovingAverageCrossoverStrategy

class TestMovingAverageCrossoverStrategy(unittest.TestCase):

    def setUp(self):
        # Dados de teste fictícios
        self.data = pd.DataFrame({
            'Close': [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
        }, index=pd.to_datetime(pd.date_range(start='2023-01-01', periods=50)))
        self.strategy = MovingAverageCrossoverStrategy(short_window=5, long_window=10)

    def test_generate_signals_columns(self):
        signals = self.strategy.generate_signals(self.data)
        self.assertIn('short_mavg', signals.columns)
        self.assertIn('long_mavg', signals.columns)
        self.assertIn('action', signals.columns)

    def test_generate_signals_length(self):
        signals = self.strategy.generate_signals(self.data)
        self.assertEqual(len(signals), len(self.data))

    def test_generate_signals_no_nan_in_action(self):
        signals = self.strategy.generate_signals(self.data)
        self.assertFalse(signals['action'].isnull().any())

    def test_generate_signals_logic(self):
        # Testar um cenário específico de cruzamento
        # short_mavg cruza acima de long_mavg -> Buy
        # short_mavg cruza abaixo de long_mavg -> Sell

        # Criar dados onde um cruzamento de compra e venda ocorra
        test_data = pd.DataFrame({
            'Close': [
                10, 10, 10, 10, 10, # 5 dias para short_mavg = 10
                11, 12, 13, 14, 15, # short_mavg começa a subir
                16, 17, 18, 19, 20, # short_mavg continua subindo
                19, 18, 17, 16, 15, # short_mavg começa a cair
                14, 13, 12, 11, 10  # short_mavg continua caindo
            ]
        }, index=pd.to_datetime(pd.date_range(start='2023-01-01', periods=25)))

        strategy = MovingAverageCrossoverStrategy(short_window=3, long_window=5)
        signals = strategy.generate_signals(test_data)

        # Esperar um sinal de compra quando short_mavg cruza acima de long_mavg
        # E um sinal de venda quando short_mavg cruza abaixo de long_mavg

        # Exemplo de verificação manual para um ponto específico
        # No nosso test_data, o cruzamento de compra deve ocorrer por volta do dia 7-9
        # E o cruzamento de venda por volta do dia 17-19

        # Encontrar o primeiro 'Buy' e 'Sell' após as janelas
        buy_signals = signals[signals['action'] == 'Buy']
        sell_signals = signals[signals['action'] == 'Sell']

        self.assertTrue(len(buy_signals) > 0, "Deveria haver pelo menos um sinal de compra")
        self.assertTrue(len(sell_signals) > 0, "Deveria haver pelo menos um sinal de venda")

        # Verificar se o primeiro sinal de compra ocorre após o período inicial de cálculo das MAs
        self.assertTrue(buy_signals.index[0] > test_data.index[strategy.long_window - 1])

        # Verificar se o primeiro sinal de venda ocorre após o primeiro sinal de compra
        self.assertTrue(sell_signals.index[0] > buy_signals.index[0])

if __name__ == '__main__':
    unittest.main()

