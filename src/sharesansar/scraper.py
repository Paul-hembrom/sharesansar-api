import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import io
from typing import Optional, Dict, Any, List
import time
import re


class ShareSansarScraper:
    """Core scraper for ShareSansar data."""

    def __init__(self):
        self.session = requests.Session()
        self._setup_session()
        self._token = None
        self._token_timestamp = None

    def _setup_session(self):
        """Setup session with headers."""
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.sharesansar.com/',
        })

    def _get_csrf_token(self, force_refresh: bool = False) -> str:
        """Get CSRF token with caching."""
        if (self._token and not force_refresh and
                self._token_timestamp and
                (datetime.now() - self._token_timestamp).seconds < 300):  # 5 min cache
            return self._token

        main_url = 'https://www.sharesansar.com/today-share-price'
        try:
            response = self.session.get(main_url, timeout=30)

            if response.status_code != 200:
                raise Exception(f"Error fetching main page: {response.status_code}")

            soup = BeautifulSoup(response.text, 'html.parser')

            # Try to find the _token in various ways
            token = None
            token_input = soup.find('input', {'name': '_token'})
            if token_input:
                token = token_input.get('value')

            if not token:
                meta_token = soup.find('meta', {'name': 'csrf-token'})
                if meta_token:
                    token = meta_token.get('content')

            if not token:
                # Try to extract from script tags
                script_tags = soup.find_all('script')
                for script in script_tags:
                    if script.string:
                        token_match = re.search(r'_token\s*:\s*["\']([^"\']+)["\']', script.string)
                        if token_match:
                            token = token_match.group(1)
                            break

            if not token:
                raise Exception("CSRF token not found")

            self._token = token
            self._token_timestamp = datetime.now()
            return token

        except requests.RequestException as e:
            raise Exception(f"Network error while fetching token: {e}")

    def get_today_data(self, date: Optional[str] = None) -> pd.DataFrame:
        """
        Get stock data for a specific date.

        Args:
            date: Date in YYYY-MM-DD format. If None, uses yesterday.

        Returns:
            pandas.DataFrame: Stock data for the specified date
        """
        if date is None:
            date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')

        # Validate date format
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")

        token = self._get_csrf_token()

        ajax_url = 'https://www.sharesansar.com/ajaxtodayshareprice'
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://www.sharesansar.com',
            'Referer': 'https://www.sharesansar.com/today-share-price',
            'X-Requested-With': 'XMLHttpRequest',
        }

        data = {
            '_token': token,
            'sector': 'all_sec',
            'date': date
        }

        try:
            response = self.session.post(ajax_url, headers=headers, data=data, timeout=30)

            if response.status_code != 200:
                raise Exception(f"Error in AJAX request: {response.status_code} - {response.text}")

            # Parse the response
            return self._parse_response(response.text, date)

        except requests.RequestException as e:
            raise Exception(f"Network error while fetching data: {e}")

    def _parse_response(self, html_content: str, date: str) -> pd.DataFrame:
        """Parse HTML response into DataFrame."""
        try:
            tables = pd.read_html(io.StringIO(html_content))
            if not tables:
                raise Exception("No tables found in response")

            df = tables[0]

            if df.empty:
                raise Exception(f"No data available for {date}")

            # Check for "No Record Found"
            if len(df) > 0 and ('No Record Found' in str(df.iloc[0, 0]) or 'No data available' in str(df.iloc[0, 0])):
                raise Exception(f"No trading data available for {date}")

            # Clean and process the data
            df = self._clean_dataframe(df)
            df['Date'] = date

            return df

        except Exception as e:
            raise Exception(f"Error parsing table: {e}")

    def get_historical_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Get historical data for a specific symbol.

        Args:
            symbol: Stock symbol
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format

        Returns:
            pandas.DataFrame: Historical data for the symbol
        """
        # Validate dates
        try:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d')

            if start_dt > end_dt:
                raise ValueError("Start date cannot be after end date")

            if start_dt > datetime.now():
                raise ValueError("Start date cannot be in the future")

        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")

        all_data = []
        current_date = start_dt

        while current_date <= end_dt:
            try:
                date_str = current_date.strftime('%Y-%m-%d')
                daily_data = self.get_today_data(date_str)

                if symbol in daily_data['Symbol'].values:
                    symbol_data = daily_data[daily_data['Symbol'] == symbol].copy()
                    all_data.append(symbol_data)

                current_date += timedelta(days=1)
                time.sleep(0.2)  # Be nice to the server

            except Exception as e:
                # Skip dates with no data
                print(f"No data for {current_date.strftime('%Y-%m-%d')}: {e}")
                current_date += timedelta(days=1)
                continue

        if all_data:
            result_df = pd.concat(all_data, ignore_index=True)
            result_df = result_df.sort_values('Date').reset_index(drop=True)
            return result_df
        else:
            return pd.DataFrame()

    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and process the dataframe."""
        # Clean column names
        df.columns = [col.strip() for col in df.columns]

        # Standardize column names
        column_mapping = {
            'S.No': 'SNo',
            'S.No.': 'SNo',
            'Conf.': 'Confidence',
            'Prev. Close': 'PrevClose',
            'Trans.': 'Transactions',
            'Diff %': 'ChangePercent',
            'Range %': 'RangePercent',
            '120 Days': 'Days120',
            '180 Days': 'Days180',
            '52 Weeks High': 'Weeks52High',
            '52 Weeks Low': 'Weeks52Low',
        }

        df = df.rename(columns=column_mapping)

        # Convert numeric columns
        numeric_columns = ['Open', 'High', 'Low', 'Close', 'LTP', 'Volume', 'Turnover',
                           'Confidence', 'VWAP', 'ChangePercent', 'RangePercent', 'Diff', 'Range',
                           'Days120', 'Days180', 'Weeks52High', 'Weeks52Low', 'PrevClose', 'Transactions']

        for col in df.columns:
            if any(num_key in col for num_key in numeric_columns):
                # Clean the data
                df[col] = (df[col].astype(str)
                           .str.replace(',', '')
                           .str.replace('%', '')
                           .replace('', '0')
                           .replace('-', '0')
                           .replace('NaN', '0')
                           .replace('nan', '0'))

                # Convert to numeric, coercing errors to NaN
                df[col] = pd.to_numeric(df[col], errors='coerce')

        return df

    def get_available_symbols(self, date: Optional[str] = None) -> List[str]:
        """Get list of available symbols for a date."""
        try:
            df = self.get_today_data(date)
            return df['Symbol'].tolist() if not df.empty else []
        except Exception:
            return []