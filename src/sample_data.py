"""
Sample Data Generator
Generates realistic sample stock data for testing and demo purposes
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_sample_stock_data(
    symbol: str,
    start_date: str,
    end_date: str,
    initial_price: float = 100.0,
    volatility: float = 0.02
) -> pd.DataFrame:
    """
    Generate realistic sample stock price data

    Parameters:
    -----------
    symbol : str
        Stock symbol
    start_date : str
        Start date in 'YYYY-MM-DD' format
    end_date : str
        End date in 'YYYY-MM-DD' format
    initial_price : float
        Starting price (default: 100.0)
    volatility : float
        Daily volatility (default: 0.02 = 2%)

    Returns:
    --------
    pd.DataFrame
        DataFrame with OHLCV data
    """
    # Parse dates
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    # Generate date range (business days only)
    dates = pd.bdate_range(start=start, end=end)
    n_days = len(dates)

    # Generate random returns
    np.random.seed(hash(symbol) % (2**32))  # Consistent data for same symbol
    returns = np.random.normal(0.001, volatility, n_days)  # Slight upward drift

    # Calculate close prices
    close_prices = initial_price * np.cumprod(1 + returns)

    # Generate OHLC data
    data = []
    for i, date in enumerate(dates):
        close = close_prices[i]

        # Generate realistic intraday ranges
        daily_range = close * np.random.uniform(0.005, 0.03)  # 0.5% to 3% range

        high = close + np.random.uniform(0, daily_range * 0.7)
        low = close - np.random.uniform(0, daily_range * 0.7)
        open_price = np.random.uniform(low, high)

        # Ensure OHLC relationships are maintained
        high = max(high, close, open_price)
        low = min(low, close, open_price)

        # Generate volume (realistic range)
        base_volume = 1000000
        volume = int(base_volume * np.random.uniform(0.5, 2.0))

        data.append({
            'open': round(open_price, 2),
            'high': round(high, 2),
            'low': round(low, 2),
            'close': round(close, 2),
            'volume': volume
        })

    # Create DataFrame
    df = pd.DataFrame(data, index=dates)
    df.index.name = 'date'

    return df


def generate_sample_balance_sheet(symbol: str) -> pd.DataFrame:
    """
    Generate sample balance sheet data

    Parameters:
    -----------
    symbol : str
        Stock symbol

    Returns:
    --------
    pd.DataFrame
        Balance sheet data
    """
    np.random.seed(hash(symbol) % (2**32))

    # Generate realistic balance sheet values (in millions)
    total_assets = np.random.uniform(500, 2000)
    total_liabilities = total_assets * np.random.uniform(0.4, 0.7)
    equity = total_assets - total_liabilities

    data = {
        'total_assets': [total_assets * 1e6],
        'total_liabilities': [total_liabilities * 1e6],
        'total_equity': [equity * 1e6],
        'cash_and_cash_equivalents': [total_assets * 0.1 * 1e6],
        'property_plant_equipment': [total_assets * 0.3 * 1e6]
    }

    df = pd.DataFrame(data)
    df.index = [datetime.now().strftime('%Y-%m-%d')]

    return df


def get_sample_data_for_symbol(symbol: str, days: int = 365) -> dict:
    """
    Get complete sample dataset for a symbol

    Parameters:
    -----------
    symbol : str
        Stock symbol
    days : int
        Number of days of historical data

    Returns:
    --------
    dict
        Dictionary containing historical prices and fundamental data
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Determine initial price based on symbol
    price_map = {
        'BMNR': 15.50,
        'AAPL': 175.00,
        'TSLA': 250.00,
        'MSFT': 380.00,
        'GOOGL': 140.00
    }

    initial_price = price_map.get(symbol.upper(), 100.0)

    return {
        'historical_prices': generate_sample_stock_data(
            symbol,
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d'),
            initial_price=initial_price
        ),
        'balance_sheet': generate_sample_balance_sheet(symbol)
    }


if __name__ == "__main__":
    # Test the sample data generator
    print("Generating sample data for BMNR...")
    data = get_sample_data_for_symbol('BMNR', days=30)

    print("\nHistorical Prices (last 5 days):")
    print(data['historical_prices'].tail())

    print("\nBalance Sheet:")
    print(data['balance_sheet'])

    print("\n[OK] Sample data generated successfully!")
