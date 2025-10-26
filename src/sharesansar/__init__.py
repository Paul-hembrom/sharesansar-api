"""ShareSansar API - A yfinance-like API for Nepali stock data."""

__version__ = "0.1.0"
__author__ = "Your Name"

from .api import (
    Ticker,
    download,
    history,
    get_stock_info,
    get_market_data,
    get_available_symbols
)

__all__ = [
    "Ticker",
    "download",
    "history",
    "get_stock_info",
    "get_market_data",
    "get_available_symbols"
]