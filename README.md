# Automated Trading Algorithm (Python)

Algoritmo de trading automatizado baseado em cruzamento de medias moveis (Moving Average Crossover).

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB.svg)](https://www.python.org/)
[![pandas](https://img.shields.io/badge/pandas-2.0+-150458.svg)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Portugues](#portugues) | [English](#english)

---

## Portugues

### Sobre

Implementacao de uma estrategia de cruzamento de medias moveis (Moving Average Crossover) em Python. O projeto contem:

- **Classe `MovingAverageCrossoverStrategy`** (`src/strategy.py`): calcula medias moveis curta e longa sobre precos de fechamento e gera sinais de Buy, Sell ou Hold com base no cruzamento
- **Gerador de dados sinteticos** (`src/main.py`): funcao `fetch_historical_data()` que cria dados OHLCV ficticios para testes (nao se conecta a APIs reais)
- **Exemplo com visualizacao** (`notebooks/example_usage.py`): script que gera sinais e plota o grafico com matplotlib

### Como Usar

```bash
# Clonar o repositorio
git clone https://github.com/galafis/automated-trading-algorithm-python.git
cd automated-trading-algorithm-python

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Executar algoritmo com dados sinteticos
python src/main.py

# Executar exemplo com grafico
python notebooks/example_usage.py

# Executar testes
pytest tests/ -v
```

### Uso Programatico

```python
from src.strategy import MovingAverageCrossoverStrategy
from src.main import fetch_historical_data

# Obter dados (sinteticos ou seus proprios dados com coluna 'Close')
data = fetch_historical_data(symbol='AAPL', start_date='2023-01-01', end_date='2023-12-31')

# Criar estrategia e gerar sinais
strategy = MovingAverageCrossoverStrategy(short_window=20, long_window=50)
signals = strategy.generate_signals(data)

# Ver sinais
print(signals[signals['action'] != 'Hold'])
```

### Estrutura do Projeto

```
automated-trading-algorithm-python/
├── src/
│   ├── __init__.py
│   ├── main.py              # Gerador de dados e ponto de entrada
│   └── strategy.py          # MovingAverageCrossoverStrategy
├── notebooks/
│   └── example_usage.py     # Exemplo com visualizacao matplotlib
├── tests/
│   ├── __init__.py
│   └── test_strategy.py     # 11 testes funcionais
├── requirements.txt
├── LICENSE
└── README.md
```

### Tecnologias

- **Python 3.9+** — linguagem principal
- **pandas 2.0+** — manipulacao de dados e series temporais
- **NumPy 1.23+** — computacao numerica
- **matplotlib 3.7+** — visualizacao de graficos (no exemplo)

### Limitacoes

- Implementa apenas uma estrategia (cruzamento de medias moveis)
- Nao inclui backtesting, calculo de metricas de performance (Sharpe, drawdown), ou execucao real de ordens
- Dados sao sinteticos — nao se conecta a corretoras ou APIs de mercado
- Nao inclui Docker ou CI/CD

---

## English

### About

Implementation of a Moving Average Crossover strategy in Python. The project contains:

- **`MovingAverageCrossoverStrategy` class** (`src/strategy.py`): computes short and long moving averages on close prices and generates Buy, Sell, or Hold signals based on crossover
- **Synthetic data generator** (`src/main.py`): `fetch_historical_data()` function that creates mock OHLCV data for testing (does not connect to real APIs)
- **Visualization example** (`notebooks/example_usage.py`): script that generates signals and plots the chart with matplotlib

### Usage

```bash
# Clone the repository
git clone https://github.com/galafis/automated-trading-algorithm-python.git
cd automated-trading-algorithm-python

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run algorithm with synthetic data
python src/main.py

# Run visualization example
python notebooks/example_usage.py

# Run tests
pytest tests/ -v
```

### Programmatic Usage

```python
from src.strategy import MovingAverageCrossoverStrategy
from src.main import fetch_historical_data

# Get data (synthetic or your own data with a 'Close' column)
data = fetch_historical_data(symbol='AAPL', start_date='2023-01-01', end_date='2023-12-31')

# Create strategy and generate signals
strategy = MovingAverageCrossoverStrategy(short_window=20, long_window=50)
signals = strategy.generate_signals(data)

# View signals
print(signals[signals['action'] != 'Hold'])
```

### Project Structure

```
automated-trading-algorithm-python/
├── src/
│   ├── __init__.py
│   ├── main.py              # Data generator and entry point
│   └── strategy.py          # MovingAverageCrossoverStrategy
├── notebooks/
│   └── example_usage.py     # Visualization example with matplotlib
├── tests/
│   ├── __init__.py
│   └── test_strategy.py     # 11 functional tests
├── requirements.txt
├── LICENSE
└── README.md
```

### Technologies

- **Python 3.9+** — core language
- **pandas 2.0+** — data manipulation and time series
- **NumPy 1.23+** — numerical computing
- **matplotlib 3.7+** — chart visualization (in example)

### Limitations

- Implements only one strategy (moving average crossover)
- Does not include backtesting, performance metrics (Sharpe, drawdown), or real order execution
- Data is synthetic — does not connect to brokers or market APIs
- Does not include Docker or CI/CD

---

## Autor / Author

**Gabriel Demetrios Lafis**
- GitHub: [@galafis](https://github.com/galafis)
- LinkedIn: [Gabriel Demetrios Lafis](https://linkedin.com/in/gabriel-demetrios-lafis)

## Licenca / License

MIT License - veja [LICENSE](LICENSE) para detalhes / see [LICENSE](LICENSE) for details.
