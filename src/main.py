import pandas as pd
from .strategy import MovingAverageCrossoverStrategy

def fetch_historical_data(symbol='AAPL', start_date='2023-01-01', end_date='2023-12-31'):
    """Simula a busca de dados históricos de um ativo."""
    # Em um cenário real, aqui seria feita uma chamada a uma API de dados financeiros.
    # Para este exemplo, vamos gerar dados fictícios.
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    data = pd.DataFrame({
        'Open': 100 + (0.5 * (dates.dayofyear % 100)) + (5 * (dates.month % 3)),
        'High': 105 + (0.5 * (dates.dayofyear % 100)) + (5 * (dates.month % 3)),
        'Low': 95 + (0.5 * (dates.dayofyear % 100)) + (5 * (dates.month % 3)),
        'Close': 100 + (0.5 * (dates.dayofyear % 100)) + (5 * (dates.month % 3)),
        'Volume': 100000 + (1000 * (dates.dayofyear % 50))
    }, index=dates)
    data['Close'] = data['Close'] + (data.index.dayofyear % 7 - 3) * 0.5 # Adiciona alguma variação
    return data

def run_trading_algorithm():
    """Executa o algoritmo de trading automatizado."""
    print("Iniciando o algoritmo de trading...")
    data = fetch_historical_data()

    strategy = MovingAverageCrossoverStrategy(short_window=20, long_window=50)
    signals = strategy.generate_signals(data)

    print("Sinais de trading gerados:")
    print(signals.tail())

    # Aqui você integraria a lógica de execução de ordens com uma corretora real.
    # Por exemplo: execute_order(signal.index, signal.action)

    print("Algoritmo de trading concluído.")

if __name__ == "__main__":
    run_trading_algorithm()

