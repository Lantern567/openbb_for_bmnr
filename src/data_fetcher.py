"""
Data Fetcher Module
Fetches stock data using OpenBB Platform
"""
from openbb import obb
import pandas as pd
from datetime import datetime
from typing import Dict, Optional, Tuple
import os
import json
import time
from .sample_data import generate_sample_stock_data, generate_sample_balance_sheet


class StockDataFetcher:
    """
    Fetches financial data for stock analysis
    """

    def __init__(self, symbol: str, use_sample_data: bool = False):
        """
        Initialize the data fetcher

        Parameters:
        -----------
        symbol : str
            Stock ticker symbol (e.g., 'BMNR')
        use_sample_data : bool
            If True, use sample data instead of fetching from APIs (for testing)
        """
        self.symbol = symbol.upper()
        self.use_sample_data = use_sample_data

    def get_historical_data(
        self,
        start_date: str,
        end_date: str,
        provider: Optional[str] = None,
        max_retries: int = 2,
        retry_delay: int = 3,
        fallback_to_sample: bool = True
    ) -> pd.DataFrame:
        """
        Get historical price data with automatic fallback to multiple providers

        Parameters:
        -----------
        start_date : str
            Start date in format 'YYYY-MM-DD'
        end_date : str
            End date in format 'YYYY-MM-DD'
        provider : Optional[str]
            Specific data provider to use. If None, will try multiple providers in order
        max_retries : int
            Maximum number of retry attempts per provider (default: 2)
        retry_delay : int
            Delay in seconds between retries (default: 3)
        fallback_to_sample : bool
            If True, use sample data when all providers fail (default: True)

        Returns:
        --------
        pd.DataFrame
            Historical price data with columns: date, open, high, low, close, volume
        """
        # If use_sample_data flag is set, return sample data immediately
        if self.use_sample_data:
            print(f"[DEMO MODE] Using sample data for {self.symbol}")
            from datetime import datetime as dt
            days = (dt.strptime(end_date, '%Y-%m-%d') - dt.strptime(start_date, '%Y-%m-%d')).days
            return generate_sample_stock_data(self.symbol, start_date, end_date)

        # List of providers to try (in order of preference)
        # Polygon is first because it supports BMNR and has good free tier
        providers_to_try = [
            "polygon",     # Polygon.io - Works with BMNR! (free tier: 5 calls/min)
            "fmp",         # Financial Modeling Prep (free tier: 250 calls/day)
            "yfinance",    # Yahoo Finance (free but has rate limits)
        ]

        # If specific provider requested, only try that one
        if provider:
            providers_to_try = [provider]

        last_error = None

        for provider_name in providers_to_try:
            print(f"Trying provider: {provider_name}")

            for attempt in range(max_retries):
                try:
                    if attempt > 0:
                        print(f"  Retry attempt {attempt + 1}/{max_retries} after {retry_delay}s delay...")
                        time.sleep(retry_delay)

                    print(f"  Fetching {self.symbol} data from {start_date} to {end_date}...")

                    output = obb.equity.price.historical(
                        symbol=self.symbol,
                        start_date=start_date,
                        end_date=end_date,
                        provider=provider_name
                    )

                    df = output.to_dataframe()

                    if df.empty:
                        raise ValueError(f"No data found for {self.symbol}")

                    print(f"  SUCCESS: Fetched {len(df)} records from {provider_name}")
                    return df

                except Exception as e:
                    error_msg = str(e)
                    last_error = e

                    # Check if it's a rate limit error
                    if "rate limit" in error_msg.lower() or "too many requests" in error_msg.lower():
                        print(f"  Rate limit hit on {provider_name}")
                        if attempt < max_retries - 1:
                            continue  # Retry same provider
                        else:
                            print(f"  Max retries for {provider_name}, trying next provider...")
                            break  # Try next provider
                    elif "api key" in error_msg.lower() or "credentials" in error_msg.lower():
                        print(f"  {provider_name} requires API key, trying next provider...")
                        break  # Try next provider
                    else:
                        # Other error
                        print(f"  Error with {provider_name}: {error_msg}")
                        if attempt < max_retries - 1:
                            continue  # Retry
                        else:
                            break  # Try next provider

        # If we get here, all providers failed
        print(f"\nFailed to fetch data from all providers: {providers_to_try}")

        if fallback_to_sample:
            print("\n" + "="*60)
            print("[DEMO MODE] Falling back to sample data for demonstration")
            print("="*60)
            print("Note: This is generated sample data, not real market data.")
            print("Solutions to get real data:")
            print("1. Wait 5-10 minutes for rate limit to reset")
            print("2. Set up a free API key (FMP: https://financialmodelingprep.com)")
            print("3. Use the system with sample data for now")
            print("="*60 + "\n")

            return generate_sample_stock_data(self.symbol, start_date, end_date)
        else:
            print("Possible solutions:")
            print("1. Wait a few minutes and try again (rate limiting)")
            print("2. Set up API keys for providers like FMP or Polygon")
            print("3. Use a different stock symbol")
            raise last_error

    def get_company_profile(self, provider: str = "yfinance") -> Dict:
        """
        Get company profile information

        Returns:
        --------
        Dict
            Company information
        """
        try:
            print(f"Fetching company profile for {self.symbol}...")

            output = obb.equity.profile(
                symbol=self.symbol,
                provider=provider
            )

            # Convert to dict
            if hasattr(output, 'to_dict'):
                profile = output.to_dict()
            else:
                profile = output.model_dump()

            print("Company profile fetched successfully")
            return profile

        except Exception as e:
            print(f"Error fetching company profile: {str(e)}")
            return {}

    def get_balance_sheet(
        self,
        period: str = "annual",
        limit: int = 4,
        provider: str = "yfinance"
    ) -> pd.DataFrame:
        """
        Get balance sheet data

        Parameters:
        -----------
        period : str
            'annual' or 'quarter'
        limit : int
            Number of periods to fetch
        provider : str
            Data provider

        Returns:
        --------
        pd.DataFrame
            Balance sheet data
        """
        try:
            print(f"Fetching balance sheet for {self.symbol}...")

            output = obb.equity.fundamental.balance(
                symbol=self.symbol,
                period=period,
                limit=limit,
                provider=provider
            )

            df = output.to_dataframe()
            print(f"Balance sheet fetched: {len(df)} periods")
            return df

        except Exception as e:
            print(f"Error fetching balance sheet: {str(e)}")
            return pd.DataFrame()

    def get_income_statement(
        self,
        period: str = "annual",
        limit: int = 4,
        provider: str = "yfinance"
    ) -> pd.DataFrame:
        """
        Get income statement data

        Parameters:
        -----------
        period : str
            'annual' or 'quarter'
        limit : int
            Number of periods to fetch
        provider : str
            Data provider

        Returns:
        --------
        pd.DataFrame
            Income statement data
        """
        try:
            print(f"Fetching income statement for {self.symbol}...")

            output = obb.equity.fundamental.income(
                symbol=self.symbol,
                period=period,
                limit=limit,
                provider=provider
            )

            df = output.to_dataframe()
            print(f"Income statement fetched: {len(df)} periods")
            return df

        except Exception as e:
            print(f"Error fetching income statement: {str(e)}")
            return pd.DataFrame()

    def get_cash_flow(
        self,
        period: str = "annual",
        limit: int = 4,
        provider: str = "yfinance"
    ) -> pd.DataFrame:
        """
        Get cash flow statement data

        Parameters:
        -----------
        period : str
            'annual' or 'quarter'
        limit : int
            Number of periods to fetch
        provider : str
            Data provider

        Returns:
        --------
        pd.DataFrame
            Cash flow data
        """
        try:
            print(f"Fetching cash flow for {self.symbol}...")

            output = obb.equity.fundamental.cash(
                symbol=self.symbol,
                period=period,
                limit=limit,
                provider=provider
            )

            df = output.to_dataframe()
            print(f"Cash flow fetched: {len(df)} periods")
            return df

        except Exception as e:
            print(f"Error fetching cash flow: {str(e)}")
            return pd.DataFrame()

    def get_key_metrics(self, provider: str = "yfinance") -> Dict:
        """
        Get key financial metrics

        Returns:
        --------
        Dict
            Key metrics including P/E, P/B, market cap, etc.
        """
        try:
            print(f"Fetching key metrics for {self.symbol}...")

            output = obb.equity.fundamental.metrics(
                symbol=self.symbol,
                provider=provider
            )

            if hasattr(output, 'to_dict'):
                metrics = output.to_dict()
            else:
                metrics = output.model_dump()

            print("Key metrics fetched successfully")
            return metrics

        except Exception as e:
            print(f"Error fetching key metrics: {str(e)}")
            return {}

    def get_all_fundamental_data(
        self,
        period: str = "annual",
        provider: str = "yfinance"
    ) -> Dict[str, pd.DataFrame]:
        """
        Get all fundamental data at once

        Returns:
        --------
        Dict
            Dictionary containing all fundamental data
        """
        print(f"\n{'='*60}")
        print(f"Fetching all fundamental data for {self.symbol}")
        print(f"{'='*60}\n")

        data = {
            'profile': self.get_company_profile(provider=provider),
            'balance_sheet': self.get_balance_sheet(period=period, provider=provider),
            'income_statement': self.get_income_statement(period=period, provider=provider),
            'cash_flow': self.get_cash_flow(period=period, provider=provider),
            'metrics': self.get_key_metrics(provider=provider)
        }

        print(f"\n{'='*60}")
        print("All fundamental data fetched successfully")
        print(f"{'='*60}\n")

        return data

    def save_data(self, data: pd.DataFrame, filename: str, data_type: str = "raw") -> str:
        """
        Save data to CSV file

        Parameters:
        -----------
        data : pd.DataFrame
            Data to save
        filename : str
            Filename (without extension)
        data_type : str
            'raw' or 'processed'

        Returns:
        --------
        str
            Full path to saved file
        """
        from config import RAW_DATA_DIR, PROCESSED_DATA_DIR

        # Choose directory
        if data_type == "raw":
            directory = RAW_DATA_DIR
        else:
            directory = PROCESSED_DATA_DIR

        # Create directory if not exists
        os.makedirs(directory, exist_ok=True)

        # Full path
        filepath = os.path.join(directory, f"{filename}.csv")

        # Save
        data.to_csv(filepath)
        print(f"Data saved to: {filepath}")

        return filepath

    def load_cached_data(self, filename: str, data_type: str = "raw") -> Optional[pd.DataFrame]:
        """
        Load cached data from CSV file

        Parameters:
        -----------
        filename : str
            Filename (without extension)
        data_type : str
            'raw' or 'processed'

        Returns:
        --------
        pd.DataFrame or None
            Loaded data or None if file doesn't exist
        """
        from config import RAW_DATA_DIR, PROCESSED_DATA_DIR

        # Choose directory
        if data_type == "raw":
            directory = RAW_DATA_DIR
        else:
            directory = PROCESSED_DATA_DIR

        # Full path
        filepath = os.path.join(directory, f"{filename}.csv")

        # Load if exists
        if os.path.exists(filepath):
            print(f"Loading cached data from: {filepath}")
            return pd.read_csv(filepath, index_col=0, parse_dates=True)
        else:
            print(f"No cached data found at: {filepath}")
            return None


if __name__ == "__main__":
    """
    Test the data fetcher
    """
    from config import DEFAULT_SYMBOL, DEFAULT_START_DATE, DEFAULT_END_DATE

    # Initialize fetcher
    fetcher = StockDataFetcher(DEFAULT_SYMBOL)

    # Test historical data
    print("\n" + "="*60)
    print("Testing Historical Data Fetch")
    print("="*60)

    try:
        hist_data = fetcher.get_historical_data(
            start_date=DEFAULT_START_DATE,
            end_date=DEFAULT_END_DATE
        )
        print(f"\nHistorical Data Shape: {hist_data.shape}")
        print(f"\nFirst 5 rows:")
        print(hist_data.head())

        # Save data
        fetcher.save_data(hist_data, f"{DEFAULT_SYMBOL}_historical")

    except Exception as e:
        print(f"Error: {e}")

    # Test fundamental data
    print("\n" + "="*60)
    print("Testing Fundamental Data Fetch")
    print("="*60)

    try:
        fundamental_data = fetcher.get_all_fundamental_data()

        print("\nBalance Sheet columns:")
        if not fundamental_data['balance_sheet'].empty:
            print(fundamental_data['balance_sheet'].columns.tolist())

        print("\nCompany Profile keys:")
        print(list(fundamental_data['profile'].keys())[:10])

    except Exception as e:
        print(f"Error: {e}")
