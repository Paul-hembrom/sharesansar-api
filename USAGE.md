# Usage Guide

## Basic Usage

```python
import sharesansar as ss

# Single stock
ticker = ss.Ticker("NABIL")
info = ticker.info()
history = ticker.history("1m")

# Multiple stocks
data = ss.download(["NABIL", "SCB", "NICA"], period="1w")

# Market data
market_data = ss.get_market_data("2024-12-01")

# Specific date range
data = ss.history("NMB", start="2024-01-01", end="2024-12-31")

# All available symbols
symbols = ss.get_available_symbols()

# Get stock info object
stock_info = ss.get_stock_info("KBL")

# Simple installation
pip install sharesansar-api

# From GitHub
pip install git+https://github.com/yourusername/sharesansar-api.git