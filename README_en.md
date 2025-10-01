# automated-trading-algorithm-python

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-lightgrey?style=flat-square&logo=pandas)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat-square&logo=numpy)
![Matplotlib](https://img.shields.io/badge/Matplotlib-darkgreen?style=flat-square&logo=matplotlib)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-orange?style=flat-square&logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)


This repository contains an automated trading algorithm developed in Python.

![Hero Image](docs/hero_image.png)

## Project Structure

![Architecture Diagram](docs/architecture.png)


- `src/`: Main source code of the algorithm.
- `tests/`: Unit tests for the code.
- `docs/`: Project documentation.
- `data/`: Example or historical data.
- `notebooks/`: Jupyter notebooks for analysis and experimentation.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/GabrielDemetriosLafis/automated-trading-algorithm-python.git
   cd automated-trading-algorithm-python
   ```
2. Create and activate a virtual environment (optional, but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   .\venv\Scripts\activate   # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the algorithm and visualize trading signals, you can use the example script:

```bash
python notebooks/example_usage.py
```

This script will fetch simulated historical data, apply the moving average crossover strategy, and plot the results.


## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

**Author:** Gabriel Demetrios Lafis
