import pytest
import pandas as pd
from sharesansar import Ticker, download, get_available_symbols

def test_ticker_initialization():
    """Test Ticker class initialization."""
    ticker = Ticker("NABIL")
    assert ticker.symbol == "NABIL"

def test_ticker_info():
    """Test getting stock info."""
    ticker = Ticker("NABIL")
    info = ticker.info()
    assert isinstance(info, dict)

def test_download():
    """Test download function."""
    # This will actually make network requests
    # Might want to mock this in real tests
    pass

def test_get_available_symbols():
    """Test getting available symbols."""
    symbols = get_available_symbols()
    assert isinstance(symbols, list)

if __name__ == "__main__":
    pytest.main([__file__])