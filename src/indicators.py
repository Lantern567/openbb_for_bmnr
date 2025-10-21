"""
Indicators Module
Calculates technical and fundamental indicators
"""
import pandas as pd
import numpy as np
import ta
from typing import Dict, List, Optional
from .mnav_calculator import mNAVCalculator


class TechnicalIndicators:
    """
    Technical Analysis Indicators Calculator
    """

    def __init__(self, df: pd.DataFrame):
        """
        Initialize with price data

        Parameters:
        -----------
        df : pd.DataFrame
            Price data with columns: open, high, low, close, volume
        """
        if df.empty:
            raise ValueError("DataFrame cannot be empty")

        required_cols = ['open', 'high', 'low', 'close', 'volume']
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            print(f"Warning: Missing columns {missing_cols}. Some indicators may not work.")

        self.df = df.copy()

    def calculate_ma(self, periods: List[int] = [5, 10, 20, 50, 100, 200]) -> pd.DataFrame:
        """
        Calculate Simple Moving Averages

        Parameters:
        -----------
        periods : List[int]
            List of MA periods

        Returns:
        --------
        pd.DataFrame
            Original data with MA columns added
        """
        df = self.df.copy()

        for period in periods:
            df[f'MA_{period}'] = df['close'].rolling(window=period).mean()

        return df

    def calculate_ema(self, periods: List[int] = [12, 26]) -> pd.DataFrame:
        """
        Calculate Exponential Moving Averages

        Parameters:
        -----------
        periods : List[int]
            List of EMA periods

        Returns:
        --------
        pd.DataFrame
            Original data with EMA columns added
        """
        df = self.df.copy()

        for period in periods:
            df[f'EMA_{period}'] = df['close'].ewm(span=period, adjust=False).mean()

        return df

    def calculate_macd(
        self,
        fast: int = 12,
        slow: int = 26,
        signal: int = 9
    ) -> pd.DataFrame:
        """
        Calculate MACD (Moving Average Convergence Divergence)

        Parameters:
        -----------
        fast : int
            Fast EMA period
        slow : int
            Slow EMA period
        signal : int
            Signal line period

        Returns:
        --------
        pd.DataFrame
            Original data with MACD columns
        """
        df = self.df.copy()

        # Calculate MACD using ta library
        macd = ta.trend.MACD(
            close=df['close'],
            window_fast=fast,
            window_slow=slow,
            window_sign=signal
        )

        df['MACD'] = macd.macd()
        df['MACD_signal'] = macd.macd_signal()
        df['MACD_diff'] = macd.macd_diff()

        return df

    def calculate_rsi(self, period: int = 14) -> pd.DataFrame:
        """
        Calculate RSI (Relative Strength Index)

        Parameters:
        -----------
        period : int
            RSI period

        Returns:
        --------
        pd.DataFrame
            Original data with RSI column
        """
        df = self.df.copy()

        # Calculate RSI using ta library
        df['RSI'] = ta.momentum.RSIIndicator(
            close=df['close'],
            window=period
        ).rsi()

        return df

    def calculate_bollinger_bands(
        self,
        period: int = 20,
        std_dev: int = 2
    ) -> pd.DataFrame:
        """
        Calculate Bollinger Bands

        Parameters:
        -----------
        period : int
            Moving average period
        std_dev : int
            Number of standard deviations

        Returns:
        --------
        pd.DataFrame
            Original data with Bollinger Band columns
        """
        df = self.df.copy()

        # Calculate Bollinger Bands using ta library
        bollinger = ta.volatility.BollingerBands(
            close=df['close'],
            window=period,
            window_dev=std_dev
        )

        df['BB_upper'] = bollinger.bollinger_hband()
        df['BB_middle'] = bollinger.bollinger_mavg()
        df['BB_lower'] = bollinger.bollinger_lband()
        df['BB_width'] = bollinger.bollinger_wband()
        df['BB_pct'] = bollinger.bollinger_pband()

        return df

    def calculate_atr(self, period: int = 14) -> pd.DataFrame:
        """
        Calculate ATR (Average True Range)

        Parameters:
        -----------
        period : int
            ATR period

        Returns:
        --------
        pd.DataFrame
            Original data with ATR column
        """
        df = self.df.copy()

        # Calculate ATR using ta library
        df['ATR'] = ta.volatility.AverageTrueRange(
            high=df['high'],
            low=df['low'],
            close=df['close'],
            window=period
        ).average_true_range()

        return df

    def calculate_stochastic(
        self,
        k_period: int = 14,
        d_period: int = 3
    ) -> pd.DataFrame:
        """
        Calculate Stochastic Oscillator

        Parameters:
        -----------
        k_period : int
            %K period
        d_period : int
            %D period

        Returns:
        --------
        pd.DataFrame
            Original data with Stochastic columns
        """
        df = self.df.copy()

        # Calculate Stochastic using ta library
        stoch = ta.momentum.StochasticOscillator(
            high=df['high'],
            low=df['low'],
            close=df['close'],
            window=k_period,
            smooth_window=d_period
        )

        df['Stoch_K'] = stoch.stoch()
        df['Stoch_D'] = stoch.stoch_signal()

        return df

    def calculate_obv(self) -> pd.DataFrame:
        """
        Calculate OBV (On-Balance Volume)

        Returns:
        --------
        pd.DataFrame
            Original data with OBV column
        """
        df = self.df.copy()

        # Calculate OBV using ta library
        df['OBV'] = ta.volume.OnBalanceVolumeIndicator(
            close=df['close'],
            volume=df['volume']
        ).on_balance_volume()

        return df

    def calculate_vwap(self) -> pd.DataFrame:
        """
        Calculate VWAP (Volume Weighted Average Price)
        Note: Daily VWAP calculation

        Returns:
        --------
        pd.DataFrame
            Original data with VWAP column
        """
        df = self.df.copy()

        # Calculate typical price
        df['typical_price'] = (df['high'] + df['low'] + df['close']) / 3

        # Calculate VWAP
        df['VWAP'] = (df['typical_price'] * df['volume']).cumsum() / df['volume'].cumsum()

        df.drop('typical_price', axis=1, inplace=True)

        return df

    def calculate_all_indicators(self) -> pd.DataFrame:
        """
        Calculate all technical indicators at once

        Returns:
        --------
        pd.DataFrame
            Data with all indicators
        """
        df = self.df.copy()

        print("Calculating all technical indicators...")

        # Trend indicators
        df = TechnicalIndicators(df).calculate_ma()
        df = TechnicalIndicators(df).calculate_ema()
        df = TechnicalIndicators(df).calculate_macd()

        # Momentum indicators
        df = TechnicalIndicators(df).calculate_rsi()
        df = TechnicalIndicators(df).calculate_stochastic()

        # Volatility indicators
        df = TechnicalIndicators(df).calculate_bollinger_bands()
        df = TechnicalIndicators(df).calculate_atr()

        # Volume indicators
        df = TechnicalIndicators(df).calculate_obv()
        df = TechnicalIndicators(df).calculate_vwap()

        print("All technical indicators calculated successfully!")

        return df


class FundamentalIndicators:
    """
    Fundamental Analysis Indicators
    Including mNAV calculations
    """

    def __init__(
        self,
        fundamental_data: Dict[str, pd.DataFrame],
        price_data: pd.DataFrame
    ):
        """
        Initialize with fundamental and price data

        Parameters:
        -----------
        fundamental_data : Dict
            Dictionary with keys: 'balance_sheet', 'income_statement', etc.
        price_data : pd.DataFrame
            Historical price data
        """
        self.fundamental_data = fundamental_data
        self.price_data = price_data
        self.mnav_calculator = None

    def setup_mnav_calculator(self, shares_outstanding: float):
        """
        Setup mNAV calculator

        Parameters:
        -----------
        shares_outstanding : float
            Number of shares outstanding
        """
        balance_sheet = self.fundamental_data.get('balance_sheet')

        if balance_sheet is None or balance_sheet.empty:
            raise ValueError("Balance sheet data is required for mNAV calculation")

        self.mnav_calculator = mNAVCalculator(balance_sheet, shares_outstanding)
        print(f"mNAV Calculator initialized with {shares_outstanding:,.0f} shares outstanding")

    def get_basic_metrics(self) -> Dict:
        """
        Get basic fundamental metrics

        Returns:
        --------
        Dict
            Basic metrics from financial data
        """
        metrics = self.fundamental_data.get('metrics', {})

        if isinstance(metrics, dict):
            return metrics
        elif isinstance(metrics, pd.DataFrame):
            return metrics.to_dict('records')[0] if not metrics.empty else {}
        else:
            return {}

    def get_mnav_analysis(
        self,
        current_price: float,
        property_fair_value: Optional[float] = None,
        property_book_value: Optional[float] = None,
        deferred_tax_rate: float = 0.0
    ) -> Dict:
        """
        Get complete mNAV analysis

        Parameters:
        -----------
        current_price : float
            Current stock price
        property_fair_value : float, optional
            Fair value of properties
        property_book_value : float, optional
            Book value of properties
        deferred_tax_rate : float
            Tax rate for deferred tax

        Returns:
        --------
        Dict
            Complete mNAV analysis
        """
        if self.mnav_calculator is None:
            raise ValueError("Please call setup_mnav_calculator() first")

        # Calculate mNAV
        if property_fair_value and property_book_value:
            mnav_data = self.mnav_calculator.calculate_mnav_with_fair_value(
                property_fair_value=property_fair_value,
                property_book_value=property_book_value,
                deferred_tax_rate=deferred_tax_rate
            )
        else:
            mnav_data = self.mnav_calculator.calculate_basic_nav()

        # Calculate premium/discount
        premium_data = self.mnav_calculator.calculate_premium_discount(
            current_price,
            mnav_data['mnav_per_share']
        )

        # Historical P/mNAV
        historical_mnav = self.mnav_calculator.calculate_historical_mnav(
            self.price_data,
            mnav_data['mnav_per_share']
        )

        # Summary
        summary = self.mnav_calculator.get_mnav_summary(mnav_data, premium_data)

        return {
            'mnav_data': mnav_data,
            'premium_data': premium_data,
            'historical_mnav': historical_mnav,
            'summary': summary
        }

    def calculate_financial_ratios(self) -> Dict:
        """
        Calculate key financial ratios

        Returns:
        --------
        Dict
            Financial ratios
        """
        bs = self.fundamental_data.get('balance_sheet')
        inc = self.fundamental_data.get('income_statement')

        if bs is None or inc is None or bs.empty or inc.empty:
            return {}

        latest_bs = bs.iloc[0]
        latest_inc = inc.iloc[0]

        ratios = {}

        # Helper function to safely get values
        def get_val(df, key, default=0):
            if key in df.index:
                val = df[key]
                return float(val) if pd.notna(val) else default
            return default

        # Liquidity ratios
        current_assets = get_val(latest_bs, 'current_assets')
        current_liabilities = get_val(latest_bs, 'current_liabilities')

        if current_liabilities > 0:
            ratios['current_ratio'] = current_assets / current_liabilities

        # Leverage ratios
        total_debt = get_val(latest_bs, 'total_debt')
        total_equity = get_val(latest_bs, 'total_equity')

        if total_equity > 0:
            ratios['debt_to_equity'] = total_debt / total_equity

        # Profitability ratios
        net_income = get_val(latest_inc, 'net_income')
        revenue = get_val(latest_inc, 'revenue')

        if revenue > 0:
            ratios['net_margin'] = (net_income / revenue) * 100

        if total_equity > 0:
            ratios['roe'] = (net_income / total_equity) * 100

        return ratios


if __name__ == "__main__":
    """
    Test the indicators module
    """
    from data_fetcher import StockDataFetcher
    from config import DEFAULT_SYMBOL, DEFAULT_START_DATE, DEFAULT_END_DATE

    print("\n" + "="*70)
    print("Testing Technical Indicators")
    print("="*70 + "\n")

    # Fetch data
    fetcher = StockDataFetcher(DEFAULT_SYMBOL)

    try:
        # Get historical data
        hist_data = fetcher.get_historical_data(
            start_date=DEFAULT_START_DATE,
            end_date=DEFAULT_END_DATE
        )

        print(f"Historical data shape: {hist_data.shape}\n")

        # Calculate indicators
        tech_ind = TechnicalIndicators(hist_data)
        df_with_indicators = tech_ind.calculate_all_indicators()

        print("Available indicators:")
        print(df_with_indicators.columns.tolist())

        print("\nLatest values:")
        print(df_with_indicators[['close', 'MA_20', 'RSI', 'MACD']].tail())

    except Exception as e:
        print(f"Error in technical indicators test: {e}")
