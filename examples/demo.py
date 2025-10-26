#!/usr/bin/env python3
"""
Demo script showing how to use ShareSansar API
"""

import sharesansar as ss


def main():
    print("ShareSansar API Demo")
    print("=" * 50)

    # Get available symbols
    print("1. Getting available symbols...")
    symbols = ss.get_available_symbols()
    print(f"   Found {len(symbols)} symbols")
    if symbols:
        print(f"   First 5 symbols: {symbols[:5]}")

    # Get single stock info
    if symbols:
        symbol = symbols[0]
        print(f"\n2. Getting info for {symbol}...")
        ticker = ss.Ticker(symbol)
        info = ticker.info()
        print(f"   LTP: {info.get('ltp')}")
        print(f"   Change: {info.get('change')} ({info.get('change_percent')}%)")

    # Get historical data
    print(f"\n3. Getting historical data for {symbol}...")
    history_data = ticker.history(period="1w")
    if not history_data.empty:
        print(f"   Retrieved {len(history_data)} records")
        print(history_data[['Date', 'Symbol', 'LTP', 'Volume']].head())

    # Download multiple stocks
    print("\n4. Downloading multiple stocks...")
    if len(symbols) >= 3:
        multiple_data = ss.download(symbols[:3], period="1d")
        print(f"   Downloaded data for {multiple_data['Symbol'].nunique()} symbols")
        print(f"   Total records: {len(multiple_data)}")

    # Get market data
    print("\n5. Getting market data...")
    market_data = ss.get_market_data()
    if not market_data.empty:
        print(f"   Market data shape: {market_data.shape}")
        print(f"   Columns: {market_data.columns.tolist()}")


if __name__ == "__main__":
    main()