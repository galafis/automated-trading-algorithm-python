import pandas as pd
import matplotlib.pyplot as plt
from src.main import fetch_historical_data
from src.strategy import MovingAverageCrossoverStrategy

def plot_signals(data, signals):
    plt.figure(figsize=(12, 8))
    plt.plot(data["Close"], label="Preço de Fechamento")
    plt.plot(signals["short_mavg"], label="Média Móvel Curta")
    plt.plot(signals["long_mavg"], label="Média Móvel Longa")

    # Plotar sinais de compra
    plt.plot(signals.loc[signals["action"] == "Buy"].index,
             data["Close"][signals["action"] == "Buy"],
             "^", markersize=10, color="g", lw=0, label="Sinal de Compra")

    # Plotar sinais de venda
    plt.plot(signals.loc[signals["action"] == "Sell"].index,
             data["Close"][signals["action"] == "Sell"],
             "v", markersize=10, color="r", lw=0, label="Sinal de Venda")

    plt.title("Estratégia de Cruzamento de Médias Móveis")
    plt.xlabel("Data")
    plt.ylabel("Preço")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # 1. Obter dados históricos
    historical_data = fetch_historical_data(symbol="TEST", start_date="2023-01-01", end_date="2023-12-31")
    print("Dados históricos obtidos:")
    print(historical_data.head())

    # 2. Inicializar e gerar sinais da estratégia
    strategy = MovingAverageCrossoverStrategy(short_window=20, long_window=50)
    trading_signals = strategy.generate_signals(historical_data)
    print("Sinais de trading gerados:")
    print(trading_signals.tail())

    # 3. Visualizar os sinais
    plot_signals(historical_data, trading_signals)

    print("Exemplo de uso concluído.")

