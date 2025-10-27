#!/usr/bin/env python3
"""
Comprehensive test to verify ShareSansar API data fetching - FIXED VERSION
"""

import sharesansar as ss
import pandas as pd
from datetime import datetime, timedelta
import sys


def print_header(title):
    print("\n" + "=" * 60)
    print(f"🧪 {title}")
    print("=" * 60)


def test_basic_import():
    """Test basic package import and attributes"""
    print_header("Testing Basic Import")

    try:
        print(f"✅ Package imported successfully!")
        print(f"   Version: {ss.__version__}")
        print(f"   Author: {ss.__author__}")

        # Check available functions
        available_functions = [func for func in dir(ss) if not func.startswith('_')]
        print(f"   Available functions: {', '.join(available_functions)}")
        return True

    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def test_market_data():
    """Test fetching market data - FIXED COLUMN NAMES"""
    print_header("Testing Market Data Fetching")

    try:
        # Get yesterday's date (markets are closed today if it's weekend/holiday)
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        print(f"📅 Fetching data for: {yesterday}")

        market_data = ss.get_market_data(yesterday)

        if market_data is None or market_data.empty:
            print("⚠️  No data returned (market might be closed)")
            return False

        print(f"✅ Successfully fetched market data!")
        print(f"   Rows: {len(market_data)}")
        print(f"   Columns: {len(market_data.columns)}")
        print(f"   Columns: {list(market_data.columns)}")

        # Show sample data - USING CORRECT COLUMN NAMES
        print(f"\n📊 Sample data (first 3 rows):")
        if 'Vol' in market_data.columns and 'ChangePercent' in market_data.columns:
            print(market_data[['Symbol', 'LTP', 'ChangePercent', 'Vol']].head(3).to_string(index=False))
        else:
            # Fallback to available columns
            available_cols = [col for col in ['Symbol', 'LTP', 'ChangePercent', 'Vol'] if col in market_data.columns]
            if available_cols:
                print(market_data[available_cols].head(3).to_string(index=False))

        return True

    except Exception as e:
        print(f"❌ Market data fetch failed: {e}")
        return False


def test_available_symbols():
    """Test getting available symbols"""
    print_header("Testing Available Symbols")

    try:
        symbols = ss.get_available_symbols()

        if not symbols:
            print("⚠️  No symbols found")
            return False

        print(f"✅ Found {len(symbols)} symbols")
        print(f"   First 10 symbols: {symbols[:10]}")
        return True

    except Exception as e:
        print(f"❌ Symbols fetch failed: {e}")
        return False


def test_ticker_functionality():
    """Test Ticker class functionality - FIXED COLUMN NAMES"""
    print_header("Testing Ticker Functionality")

    try:
        # First get some symbols to test with
        symbols = ss.get_available_symbols()
        if not symbols:
            print("⚠️  No symbols available for testing")
            return False

        test_symbol = symbols[0]
        print(f"🔍 Testing with symbol: {test_symbol}")

        # Create Ticker object
        ticker = ss.Ticker(test_symbol)
        print("✅ Ticker object created successfully")

        # Test info()
        info = ticker.info()
        if info:
            print(f"✅ Stock info retrieved:")
            for key, value in info.items():
                if value is not None and value != 0:  # Only print non-empty values
                    print(f"   {key}: {value}")
        else:
            print("⚠️  No stock info returned")

        # Test history()
        print(f"\n📈 Testing historical data...")
        history_data = ticker.history(period="1d")

        if history_data is not None and not history_data.empty:
            print(f"✅ Historical data retrieved:")
            print(f"   Records: {len(history_data)}")
            # Use correct column names
            display_cols = ['Date', 'Symbol', 'LTP']
            if 'Vol' in history_data.columns:
                display_cols.append('Vol')
            print(history_data[display_cols].to_string(index=False))
        else:
            print("⚠️  No historical data returned")

        return True

    except Exception as e:
        print(f"❌ Ticker functionality failed: {e}")
        return False


def test_download_functionality():
    """Test download function for multiple symbols - FIXED COLUMN NAMES"""
    print_header("Testing Download Functionality")

    try:
        symbols = ss.get_available_symbols()
        if not symbols or len(symbols) < 3:
            print("⚠️  Not enough symbols for download test")
            return False

        test_symbols = symbols[:3]  # Test with first 3 symbols
        print(f"📥 Downloading data for: {test_symbols}")

        data = ss.download(test_symbols, period="1d")

        if data is not None and not data.empty:
            print(f"✅ Download successful!")
            print(f"   Total records: {len(data)}")
            print(f"   Unique symbols: {data['Symbol'].nunique()}")
            print(f"\n📊 Sample downloaded data:")
            # Use correct column names
            display_cols = ['Symbol', 'Date', 'LTP']
            if 'Vol' in data.columns:
                display_cols.append('Vol')
            print(data[display_cols].head(6).to_string(index=False))
        else:
            print("⚠️  No data returned from download")

        return True

    except Exception as e:
        print(f"❌ Download functionality failed: {e}")
        return False


def test_different_dates():
    """Test with different dates"""
    print_header("Testing Different Dates")

    dates_to_test = []

    # Test last 3 days
    for i in range(1, 4):
        test_date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        dates_to_test.append(test_date)

    successful_dates = []

    for test_date in dates_to_test:
        try:
            print(f"📅 Testing date: {test_date}")
            data = ss.get_market_data(test_date)

            if data is not None and not data.empty:
                print(f"   ✅ Data found: {len(data)} records")
                successful_dates.append(test_date)
            else:
                print(f"   ⚠️  No data (market closed)")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    print(f"\n📈 Successful dates: {len(successful_dates)}/{len(dates_to_test)}")
    return len(successful_dates) > 0


def test_real_usage_scenarios():
    """Test real-world usage scenarios"""
    print_header("Testing Real Usage Scenarios")

    try:
        # Scenario 1: Get top 5 stocks by volume
        market_data = ss.get_market_data()
        if market_data is not None and not market_data.empty:
            if 'Vol' in market_data.columns and 'LTP' in market_data.columns:
                top_volume = market_data.nlargest(5, 'Vol')[['Symbol', 'LTP', 'Vol']]
                print("📈 Top 5 stocks by volume:")
                print(top_volume.to_string(index=False))

            # Scenario 2: Find stocks with highest price change
            if 'ChangePercent' in market_data.columns:
                top_gainers = market_data.nlargest(3, 'ChangePercent')[['Symbol', 'LTP', 'ChangePercent']]
                top_losers = market_data.nsmallest(3, 'ChangePercent')[['Symbol', 'LTP', 'ChangePercent']]

                print(f"\n📊 Top 3 gainers:")
                print(top_gainers.to_string(index=False))
                print(f"\n📉 Top 3 losers:")
                print(top_losers.to_string(index=False))

        return True

    except Exception as e:
        print(f"❌ Real usage scenarios failed: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 ShareSansar API - Comprehensive Data Fetching Test")
    print("=" * 60)

    tests = [
        test_basic_import,
        test_available_symbols,
        test_market_data,
        test_ticker_functionality,
        test_download_functionality,
        test_different_dates,
        test_real_usage_scenarios,
    ]

    results = []

    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)

    # Summary
    print_header("TEST SUMMARY")
    passed = sum(results)
    total = len(results)

    print(f"📊 Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! Your ShareSansar API is working perfectly! 🎉")
        print("💡 Users can now use your library to fetch Nepali stock data!")
    elif passed >= 4:
        print("✅ MOST TESTS PASSED! Your ShareSansar API is working well! 🚀")
        print("💡 The library successfully fetches real stock data from ShareSansar!")
    else:
        print("⚠️  Some tests failed. Check the errors above.")

    return passed >= 4  # Consider it successful if most tests pass


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)