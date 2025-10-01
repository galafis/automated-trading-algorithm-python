import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Gerar dados fictícios para um gráfico de linha de tempo de preços
dates = pd.date_range(start='2023-01-01', periods=100)
prices = 100 + np.cumsum(np.random.randn(100) * 2)

plt.figure(figsize=(12, 6))
plt.plot(dates, prices, color='skyblue', linewidth=2)
plt.title('Automated Trading Algorithm - Price Trend', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Price', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.fill_between(dates, prices, 100, color='skyblue', alpha=0.3)
plt.tight_layout()
plt.savefig('automated-trading-algorithm-python/docs/hero_image.png')
plt.close()

