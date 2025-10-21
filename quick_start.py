"""
Quick Start Example - BMNR Stock Analysis
Run this script to test the basic functionality
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.data_fetcher import StockDataFetcher
from src.indicators import TechnicalIndicators, FundamentalIndicators
from src.mnav_calculator import mNAVCalculator
from src.visualizer import StockVisualizer
from datetime import datetime, timedelta


def quick_start_demo():
    """
    Quick demonstration of the BMNR analysis tools
    """
    print("="*70)
    print("BMNR STOCK ANALYSIS - QUICK START DEMO")
    print("="*70)
    print()

    # Configuration
    SYMBOL = "BMNR"
    END_DATE = datetime.now().strftime("%Y-%m-%d")
    START_DATE = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

    print(f"📊 Analyzing {SYMBOL} from {START_DATE} to {END_DATE}")
    print()

    # Step 1: Fetch Historical Data
    print("Step 1: Fetching historical price data...")
    print("-" * 70)
    try:
        fetcher = StockDataFetcher(SYMBOL)
        hist_data = fetcher.get_historical_data(START_DATE, END_DATE)

        print(f"✓ Successfully fetched {len(hist_data)} days of data")
        print(f"  Latest price: ${hist_data['close'].iloc[-1]:.2f}")
        print(f"  Price range: ${hist_data['low'].min():.2f} - ${hist_data['high'].max():.2f}")
        print()

    except Exception as e:
        print(f"✗ Error fetching data: {e}")
        print("  Try checking if BMNR is the correct symbol or your internet connection")
        return

    # Step 2: Calculate Technical Indicators
    print("Step 2: Calculating technical indicators...")
    print("-" * 70)
    try:
        tech_ind = TechnicalIndicators(hist_data)
        df_with_indicators = tech_ind.calculate_all_indicators()

        print(f"✓ Calculated {len(df_with_indicators.columns)} indicators")
        print(f"  Available indicators:")
        indicator_cols = [col for col in df_with_indicators.columns
                          if col not in ['open', 'high', 'low', 'close', 'volume']]
        for ind in indicator_cols[:10]:  # Show first 10
            print(f"    - {ind}")
        if len(indicator_cols) > 10:
            print(f"    ... and {len(indicator_cols) - 10} more")
        print()

    except Exception as e:
        print(f"✗ Error calculating indicators: {e}")
        return

    # Step 3: Latest Technical Values
    print("Step 3: Latest technical indicator values...")
    print("-" * 70)
    latest = df_with_indicators.iloc[-1]

    print(f"  MA(20):  ${latest.get('MA_20', 0):.2f}")
    print(f"  MA(50):  ${latest.get('MA_50', 0):.2f}")
    print(f"  RSI:     {latest.get('RSI', 0):.2f}")
    rsi_status = "Overbought" if latest.get('RSI', 50) > 70 else ("Oversold" if latest.get('RSI', 50) < 30 else "Neutral")
    print(f"           ({rsi_status})")
    print(f"  MACD:    {latest.get('MACD', 0):.4f}")
    print()

    # Step 4: Fetch Fundamental Data (for mNAV)
    print("Step 4: Fetching fundamental data for mNAV...")
    print("-" * 70)
    try:
        fundamental_data = fetcher.get_all_fundamental_data()

        if not fundamental_data['balance_sheet'].empty:
            print("✓ Successfully fetched fundamental data")
            print(f"  Balance sheet periods: {len(fundamental_data['balance_sheet'])}")
            print()

            # Step 5: Calculate mNAV
            print("Step 5: Calculating mNAV (Basic)...")
            print("-" * 70)

            # Use a default shares outstanding (adjust as needed)
            SHARES_OUTSTANDING = 10_000_000  # 10 million shares (example)

            calc = mNAVCalculator(
                fundamental_data['balance_sheet'],
                SHARES_OUTSTANDING
            )

            # Basic NAV
            nav_data = calc.calculate_basic_nav()
            current_price = hist_data['close'].iloc[-1]

            print(f"  NAV per Share:    ${nav_data['nav_per_share']:.2f}")
            print(f"  Current Price:    ${current_price:.2f}")

            # Premium/Discount
            premium_data = calc.calculate_premium_discount(
                current_price,
                nav_data['nav_per_share']
            )

            print(f"  P/NAV Ratio:      {premium_data['p_mnav_ratio']:.2f}x")
            print(f"  Premium/Discount: {premium_data['premium_discount_pct']:+.2f}%")
            print(f"  Status:           {premium_data['interpretation']}")
            print()

        else:
            print("✗ Fundamental data not available")
            print("  mNAV calculation skipped")
            print()

    except Exception as e:
        print(f"✗ Error with fundamental data: {e}")
        print("  This is normal if fundamental data is not available for this stock")
        print()

    # Step 6: Summary
    print("="*70)
    print("DEMO COMPLETED!")
    print("="*70)
    print()
    print("Next Steps:")
    print("1. Run the Streamlit dashboard: streamlit run app.py")
    print("2. Customize parameters in src/config.py")
    print("3. Explore individual modules in src/")
    print()
    print("For mNAV analysis:")
    print("- Adjust SHARES_OUTSTANDING in this script")
    print("- Add property fair value adjustments")
    print("- Use the Streamlit dashboard for interactive analysis")
    print()


if __name__ == "__main__":
    try:
        quick_start_demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        print("Please check the README.md for troubleshooting")
