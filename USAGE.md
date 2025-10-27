# Usage Guide

This file provides instructions and examples for using the `sharesansar-api` library.

---

## 1. Installation

First, install the package using pip:

```bash
pip install sharesansar-api
```

---

## 2. 🚀 Quick Start

Here are the most common commands to get you started immediately.

```python
import sharesansar as ss

# Single stock (yfinance style)
nabil = ss.Ticker("NABIL")
info = nabil.info()
history = nabil.history(period="1w")

# Multiple stocks
data = ss.download(["NABIL", "SCB", "NICA"], period="1m")

# Market data for specific date
market_data = ss.get_market_data("2024-12-20")
```

---

## 3. 📚 Usage Examples

Detailed examples for specific use cases.

### Get Stock Information

```python
import sharesansar as ss

ticker = ss.Ticker("NABIL")
info = ticker.info()

print(f"LTP: {info['ltp']}")
print(f"Change: {info['change']} ({info['change_percent']}%)")
```

### Historical Data

```python
import sharesansar as ss

# Various period formats
data_1w = ss.Ticker("SCB").history(period="1w")
data_1m = ss.Ticker("NICA").history(period="1m")
data_custom = ss.Ticker("KBL").history(start="2024-01-01", end="2024-12-31")
```

### Multiple Stocks

```python
import sharesansar as ss

# Download multiple stocks
symbols = ["NABIL", "SCB", "NICA", "NMB", "KBL"]
data = ss.download(symbols, period="1w")
```

### Market Overview

```python
import sharesansar as ss

# Get all available symbols
symbols = ss.get_available_symbols()
print(f"Total stocks: {len(symbols)}")

# Get complete market data for the latest day
market_data = ss.get_market_data()
```

---

## 4. 🛠️ API Reference

A quick reference for available classes and functions.

### `Ticker` Class

-   **`Ticker(symbol)`**: Create a stock ticker object.
-   **`ticker.info()`**: Get current stock information.
-   **`ticker.history(period, start, end)`**: Get historical data.

### Module Functions

-   **`download(symbols, period)`**: Download multiple stocks.
-   **`history(symbol, start, end)`**: Get historical data for a single stock.
-   **`get_stock_info(symbol)`**: Get detailed stock info.
-   **`get_market_data(date)`**: Get market-wide data (latest if `date` is omitted).
-   **`get_available_symbols()`**: List all stock symbols.

### Period Options

Valid strings for the `period` parameter:

-   `"1d"` - One day
-   `"1w"` - One week
-   `"1m"` - One month
-   `"3m"` - Three months
-   `"6m"` - Six months
-   `"1y"` - One year
-   `"ytd"` - Year to date

---

## 5. 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

## 6. 📄 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

---

## 7. 🙏 Acknowledgments

-   ShareSansar.com for providing the data.