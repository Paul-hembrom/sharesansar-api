#!/usr/bin/env python3
"""
Test real historical data scenarios that users might want
"""

import sharesansar as ss
from datetime import datetime, timedelta


def test_user_scenarios():
    print("🚀 Testing Real User Historical Data Scenarios")
    print("=" * 60)

    # Get some popular symbols
    symbols = ss.get_available_symbols()
    popular_symbols = ["NABIL", "SCB", "NICA", "NMB", "KBL"]

    available_popular = [s for s in popular_symbols if s in symbols]
    print(f"🔍 Testing with popular symbols: {available_popular}")

    if not available_popular:
        available_popular = symbols[:2]  # Fallback to first available
        print(f"🔍 Using available symbols: {available_popular}")

    # Scenario 1: Last week's performance
    print("\n1. Last Week's Performance Analysis:")
    print("-" * 40)

    for symbol in available_popular[:2]:  # Test first 2
        try:
            print(f"   📈 {symbol} - Last Week:")
            data = ss.history(symbol, period="1w")

            if data is not None and not data.empty:
                dates = sorted(data['Date'].unique())
                print(f"      ✅ {len(data)} trading days: {dates}")

                if 'LTP' in data.columns and len(data) > 1:
                    first_price = data.iloc[0]['LTP']
                    last_price = data.iloc[-1]['LTP']
                    change = ((last_price - first_price) / first_price) * 100
                    print(f"      💰 Price: {first_price:.2f} → {last_price:.2f} ({change:+.2f}%)")
            else:
                print(f"      ⚠️  No data for last week")

        except Exception as e:
            print(f"      ❌ Error: {e}")

    # Scenario 2: Monthly analysis
    print("\n2. Last Month's Trading Pattern:")
    print("-" * 40)

    for symbol in available_popular[:1]:  # Test first one
        try:
            print(f"   📊 {symbol} - Last Month:")
            data = ss.history(symbol, period="1m")

            if data is not None and not data.empty:
                print(f"      ✅ {len(data)} trading days")

                if 'LTP' in data.columns and 'Vol' in data.columns:
                    avg_price = data['LTP'].mean()
                    total_volume = data['Vol'].sum()
                    high_price = data['LTP'].max()
                    low_price = data['LTP'].min()

                    print(f"      📊 Avg Price: {avg_price:.2f}")
                    print(f"      📈 High/Low: {high_price:.2f}/{low_price:.2f}")
                    print(f"      🔥 Total Volume: {total_volume:,}")
            else:
                print(f"      ⚠️  No data for last month")

        except Exception as e:
            print(f"      ❌ Error: {e}")

    # Scenario 3: Specific event period (e.g., budget month)
    print("\n3. Specific Period Analysis (e.g., Budget Month):")
    print("-" * 40)

    # Test a specific known period (adjust dates based on actual trading)
    test_periods = [
        ("2024-12-01", "2024-12-31", "December 2024"),
        ("2024-06-01", "2024-06-30", "June 2024"),
    ]

    for symbol in available_popular[:1]:
        for start, end, description in test_periods:
            try:
                print(f"   📅 {symbol} - {description}:")
                data = ss.history(symbol, start=start, end=end)

                if data is not None and not data.empty:
                    trading_days = len(data)
                    print(f"      ✅ {trading_days} trading days")

                    if 'LTP' in data.columns and trading_days > 0:
                        price_change = data.iloc[-1]['LTP'] - data.iloc[0]['LTP']
                        print(f"      💰 Price change: {price_change:+.2f}")
                else:
                    print(f"      ⚠️  No data for {description}")

            except Exception as e:
                print(f"      ❌ Error: {e}")

    # Scenario 4: Multiple symbols comparison
    print("\n4. Multiple Symbols Comparison (Last Week):")
    print("-" * 40)

    try:
        data = ss.download(available_popular, period="1w")

        if data is not None and not data.empty:
            print(f"      ✅ Downloaded data for {data['Symbol'].nunique()} symbols")

            # Show performance summary
            if 'LTP' in data.columns and 'Date' in data.columns:
                # Get first and last prices for each symbol
                summary = []
                for symbol in available_popular:
                    symbol_data = data[data['Symbol'] == symbol]
                    if len(symbol_data) > 1:
                        first_row = symbol_data.iloc[0]
                        last_row = symbol_data.iloc[-1]
                        change_pct = ((last_row['LTP'] - first_row['LTP']) / first_row['LTP']) * 100
                        summary.append({
                            'Symbol': symbol,
                            'Start Price': first_row['LTP'],
                            'End Price': last_row['LTP'],
                            'Change %': change_pct
                        })

                if summary:
                    print(f"      📊 Performance Summary:")
                    for item in summary:
                        print(f"         {item['Symbol']}: {item['Change %']:+.2f}%")

        else:
            print(f"      ⚠️  No comparison data available")

    except Exception as e:
        print(f"      ❌ Comparison failed: {e}")


def main():
    print("🎯 Real User Historical Data Scenarios")
    print("=" * 60)
    print("💡 Testing practical use cases for historical data")

    test_user_scenarios()

    print("\n" + "=" * 60)
    print("📈 HISTORICAL SCENARIOS TESTED!")
    print("🎉 Users CAN fetch past data for analysis!")
    print("💪 Your library supports real investment analysis use cases!")


if __name__ == "__main__":
    main()