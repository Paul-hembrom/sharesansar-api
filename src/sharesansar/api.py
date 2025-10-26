import pandas as pd
from typing import Optional, Dict, List, Union
import datetime
from .scraper import ShareSansarScraper
from .models import StockInfo, MarketSummary


class Ticker:
    """Main Ticker class similar to yfinance for individual stocks."""

    def __init__(self, symbol: str):
        self.symbol = symbol.upper()
        self.scraper = ShareSansarScraper()
        self._info = None
        self._history = None

    def info(self) -> Dict[str, any]:
        """Get current stock information."""
        if self._info is None:
            self._info = self._fetch_info()
        return self._info

    def history(self, period: str = "1d", start: str = None, end: str = None) -> pd.DataFrame:
        """Get historical data for the stock."""
        return self._fetch_history(period, start, end)

    def _fetch_info(self) -> Dict[str, any]:
        """Fetch current stock information."""
        try:
            # Get today's data and filter for this symbol
            df = self.scraper.get_today_data()
            symbol_data = df[df['Symbol'] == self.symbol]

            if symbol_data.empty:
                return {}

            row = symbol_data.iloc[0]
            return {
                'symbol': self.symbol,
                'company': '',  # You might need to map symbols to company names
                'ltp': row.get('LTP', 0),
                'change': row.get('Diff', 0),
                'change_percent': row.get('Diff %', 0),
                'open': row.get('Open', 0),
                'high': row.get('High', 0),
                'low': row.get('Low', 0),
                'volume': row.get('Volume', 0),
                'previous_close': row.get('Prev. Close', 0),
                'vwap': row.get('VWAP', 0),
                'turnover': row.get('Turnover', 0)
            }
        except Exception as e:
            print(f"Error fetching info for {self.symbol}: {e}")
            return {}

    def _fetch_history(self, period: str = "1d", start: str = None, end: str = None) -> pd.DataFrame:
        """Fetch historical data."""
        # Handle period parameter
        if period != "1d" and start is None:
            # Convert period to date range
            end_date = datetime.datetime.now()
            if period == "1w":
                start_date = end_date - datetime.timedelta(weeks=1)
            elif period == "1m":
                start_date = end_date - datetime.timedelta(days=30)
            elif period == "3m":
                start_date = end_date - datetime.timedelta(days=90)
            elif period == "6m":
                start_date = end_date - datetime.timedelta(days=180)
            elif period == "1y":
                start_date = end_date - datetime.timedelta(days=365)
            else:
                start_date = end_date - datetime.timedelta(days=1)

            start = start_date.strftime('%Y-%m-%d')
            end = end_date.strftime('%Y-%m-%d')

        elif start is None:
            # Default to yesterday
            yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            start = yesterday
            end = yesterday

        return self.scraper.get_historical_data(self.symbol, start, end)


def download(
        symbols: Union[str, List[str]],
        start: str = None,
        end: str = None,
        period: str = "1d"
) -> pd.DataFrame:
    """Download stock data for multiple symbols."""

    if isinstance(symbols, str):
        symbols = [symbols]

    all_data = []
    scraper = ShareSansarScraper()

    for symbol in symbols:
        try:
            ticker = Ticker(symbol)
            data = ticker.history(period=period, start=start, end=end)
            if not data.empty:
                all_data.append(data)
        except Exception as e:
            print(f"Error downloading data for {symbol}: {e}")

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()


def history(
        symbol: str,
        start: str = None,
        end: str = None,
        period: str = "1d"
) -> pd.DataFrame:
    """Get historical data for a single symbol."""
    ticker = Ticker(symbol)
    return ticker.history(period=period, start=start, end=end)


def get_stock_info(symbol: str) -> Optional[StockInfo]:
    """Get detailed information for a specific stock."""
    ticker = Ticker(symbol)
    info = ticker.info()

    if info:
        return StockInfo(
            symbol=symbol,
            company=info.get('company', ''),
            ltp=info.get('ltp', 0),
            change=info.get('change', 0),
            change_percent=info.get('change_percent', 0),
            open=info.get('open', 0),
            high=info.get('high', 0),
            low=info.get('low', 0),
            volume=info.get('volume', 0),
            previous_close=info.get('previous_close', 0)
        )
    return None


def get_market_data(date: str = None) -> pd.DataFrame:
    """Get complete market data for a specific date."""
    scraper = ShareSansarScraper()
    return scraper.get_today_data(date)


def get_available_symbols(date: str = None) -> List[str]:
    """Get list of available stock symbols."""
    scraper = ShareSansarScraper()
    return scraper.get_available_symbols(date)