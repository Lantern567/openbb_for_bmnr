"""
mNAV (Modified Net Asset Value) Calculator Module
Calculates mNAV for REITs and asset-heavy companies
"""
import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple
from datetime import datetime


class mNAVCalculator:
    """
    Modified Net Asset Value (mNAV) Calculator

    mNAV is commonly used for valuing:
    - Real Estate Investment Trusts (REITs)
    - Asset management companies
    - Companies with significant tangible assets

    Formula:
    mNAV = (Fair Value of Assets - Liabilities - Minority Interest) / Shares Outstanding
    """

    def __init__(self, balance_sheet: pd.DataFrame, shares_outstanding: float):
        """
        Initialize mNAV Calculator

        Parameters:
        -----------
        balance_sheet : pd.DataFrame
            Balance sheet data from financial statements
        shares_outstanding : float
            Number of shares outstanding
        """
        if balance_sheet.empty:
            raise ValueError("Balance sheet cannot be empty")

        if shares_outstanding <= 0:
            raise ValueError("Shares outstanding must be positive")

        self.balance_sheet = balance_sheet
        self.shares_outstanding = shares_outstanding

        # Store latest balance sheet
        self.latest_bs = self._get_latest_balance_sheet()

    def _get_latest_balance_sheet(self) -> pd.Series:
        """Get the most recent balance sheet period"""
        if isinstance(self.balance_sheet, pd.DataFrame):
            return self.balance_sheet.iloc[0]
        else:
            return self.balance_sheet

    def _get_value_safe(self, key: str, default: float = 0.0) -> float:
        """
        Safely get value from balance sheet with multiple key attempts
        """
        # Common variations of balance sheet keys
        key_variations = [
            key,
            key.lower(),
            key.upper(),
            key.replace('_', ''),
            key.replace('_', ' ').title(),
        ]

        for k in key_variations:
            if k in self.latest_bs.index:
                value = self.latest_bs[k]
                return float(value) if pd.notna(value) else default

        return default

    def calculate_basic_nav(self) -> Dict:
        """
        Calculate basic Net Asset Value (NAV)
        Uses book values from balance sheet

        Returns:
        --------
        Dict
            Dictionary containing:
            - nav: Total net asset value
            - nav_per_share: NAV per share
            - total_assets: Total assets
            - total_liabilities: Total liabilities
            - book_value_equity: Book value of equity
        """
        # Get values from balance sheet
        total_assets = self._get_value_safe('total_assets')
        total_liabilities = self._get_value_safe('total_liabilities')

        # Alternative keys for equity
        equity = (
            self._get_value_safe('total_equity') or
            self._get_value_safe('shareholders_equity') or
            self._get_value_safe('stockholders_equity') or
            (total_assets - total_liabilities)
        )

        # Calculate NAV
        nav = total_assets - total_liabilities
        nav_per_share = nav / self.shares_outstanding

        return {
            'nav': nav,
            'nav_per_share': nav_per_share,
            'total_assets': total_assets,
            'total_liabilities': total_liabilities,
            'book_value_equity': equity,
            'shares_outstanding': self.shares_outstanding,
            'calculation_type': 'Basic NAV (Book Value)'
        }

    def calculate_mnav_with_fair_value(
        self,
        property_fair_value: Optional[float] = None,
        property_book_value: Optional[float] = None,
        deferred_tax_rate: float = 0.0,
        minority_interest: Optional[float] = None
    ) -> Dict:
        """
        Calculate Modified NAV with fair value adjustments

        Parameters:
        -----------
        property_fair_value : float, optional
            Fair/market value of investment properties
        property_book_value : float, optional
            Book value of investment properties
        deferred_tax_rate : float
            Tax rate for deferred tax adjustment (default: 0.0)
        minority_interest : float, optional
            Minority/non-controlling interest to deduct

        Returns:
        --------
        Dict
            Dictionary containing detailed mNAV calculation
        """
        # Get base values
        total_assets = self._get_value_safe('total_assets')
        total_liabilities = self._get_value_safe('total_liabilities')

        # Minority interest
        if minority_interest is None:
            minority_interest = self._get_value_safe('minority_interest', 0.0)

        # Calculate revaluation gain if fair value provided
        if property_fair_value and property_book_value:
            revaluation_gain = property_fair_value - property_book_value
            adjusted_assets = total_assets + revaluation_gain
        else:
            revaluation_gain = 0
            adjusted_assets = total_assets

        # Calculate deferred tax on revaluation
        deferred_tax_adjustment = revaluation_gain * deferred_tax_rate

        # Modified NAV calculation
        mnav = (
            adjusted_assets
            - total_liabilities
            - minority_interest
            - deferred_tax_adjustment
        )

        # mNAV per share
        mnav_per_share = mnav / self.shares_outstanding

        return {
            'mnav': mnav,
            'mnav_per_share': mnav_per_share,
            'adjusted_assets': adjusted_assets,
            'total_assets': total_assets,
            'total_liabilities': total_liabilities,
            'minority_interest': minority_interest,
            'property_fair_value': property_fair_value or property_book_value or 0,
            'property_book_value': property_book_value or 0,
            'revaluation_gain': revaluation_gain,
            'deferred_tax_rate': deferred_tax_rate,
            'deferred_tax_adjustment': deferred_tax_adjustment,
            'shares_outstanding': self.shares_outstanding,
            'calculation_type': 'Modified NAV (Fair Value Adjusted)'
        }

    def calculate_premium_discount(
        self,
        current_price: float,
        mnav_per_share: float
    ) -> Dict:
        """
        Calculate premium/discount to mNAV

        Parameters:
        -----------
        current_price : float
            Current market price of the stock
        mnav_per_share : float
            mNAV per share

        Returns:
        --------
        Dict
            Premium/discount analysis
        """
        if mnav_per_share <= 0:
            raise ValueError("mNAV per share must be positive")

        # P/mNAV ratio
        p_mnav_ratio = current_price / mnav_per_share

        # Premium/discount percentage
        premium_discount_pct = ((current_price - mnav_per_share) / mnav_per_share) * 100

        # Premium/discount amount
        premium_discount_amount = current_price - mnav_per_share

        # Interpretation
        if premium_discount_pct > 5:
            interpretation = "Trading at Premium"
            status = "overvalued"
        elif premium_discount_pct < -5:
            interpretation = "Trading at Discount"
            status = "undervalued"
        else:
            interpretation = "Trading near Fair Value"
            status = "fairly_valued"

        return {
            'current_price': current_price,
            'mnav_per_share': mnav_per_share,
            'p_mnav_ratio': p_mnav_ratio,
            'premium_discount_pct': premium_discount_pct,
            'premium_discount_amount': premium_discount_amount,
            'interpretation': interpretation,
            'status': status
        }

    def calculate_historical_mnav(
        self,
        historical_prices: pd.DataFrame,
        mnav_per_share: float,
        price_column: str = 'close'
    ) -> pd.DataFrame:
        """
        Calculate historical P/mNAV ratios

        Parameters:
        -----------
        historical_prices : pd.DataFrame
            Historical price data
        mnav_per_share : float
            mNAV per share (constant value)
        price_column : str
            Column name for price (default: 'close')

        Returns:
        --------
        pd.DataFrame
            Original data with added mNAV columns
        """
        df = historical_prices.copy()

        # Add mNAV columns
        df['mnav_per_share'] = mnav_per_share
        df['p_mnav_ratio'] = df[price_column] / mnav_per_share
        df['premium_discount_pct'] = ((df[price_column] - mnav_per_share) / mnav_per_share) * 100
        df['premium_discount_amount'] = df[price_column] - mnav_per_share

        # Status
        df['valuation_status'] = df['premium_discount_pct'].apply(
            lambda x: 'premium' if x > 5 else ('discount' if x < -5 else 'fair')
        )

        return df

    def get_mnav_summary(self, mnav_data: Dict, premium_data: Dict) -> str:
        """
        Generate a text summary of mNAV analysis

        Parameters:
        -----------
        mnav_data : Dict
            Output from calculate_mnav_with_fair_value or calculate_basic_nav
        premium_data : Dict
            Output from calculate_premium_discount

        Returns:
        --------
        str
            Formatted summary text
        """
        summary = f"""
{'='*70}
                        mNAV ANALYSIS SUMMARY
{'='*70}

VALUATION METRICS:
------------------
mNAV per Share:          ${mnav_data['mnav_per_share']:,.2f}
Current Market Price:    ${premium_data['current_price']:,.2f}
P/mNAV Ratio:            {premium_data['p_mnav_ratio']:.2f}x
Premium/Discount:        {premium_data['premium_discount_pct']:+.2f}%
Status:                  {premium_data['interpretation']}

BALANCE SHEET COMPONENTS:
------------------------
Total Assets:            ${mnav_data.get('adjusted_assets', mnav_data.get('total_assets')):,.0f}
Total Liabilities:       ${mnav_data['total_liabilities']:,.0f}
Minority Interest:       ${mnav_data.get('minority_interest', 0):,.0f}
Net Asset Value:         ${mnav_data['mnav']:,.0f}

"""
        if mnav_data.get('revaluation_gain', 0) != 0:
            summary += f"""
FAIR VALUE ADJUSTMENTS:
-----------------------
Property Fair Value:     ${mnav_data['property_fair_value']:,.0f}
Property Book Value:     ${mnav_data['property_book_value']:,.0f}
Revaluation Gain:        ${mnav_data['revaluation_gain']:,.0f}
Deferred Tax ({mnav_data['deferred_tax_rate']*100:.1f}%):      ${mnav_data['deferred_tax_adjustment']:,.0f}

"""
        summary += f"""
SHARE INFORMATION:
-----------------
Shares Outstanding:      {mnav_data['shares_outstanding']:,.0f}
Total Market Cap:        ${premium_data['current_price'] * mnav_data['shares_outstanding']:,.0f}
Total mNAV:              ${mnav_data['mnav']:,.0f}

{'='*70}
"""
        return summary

    def compare_multiple_valuations(
        self,
        current_price: float,
        scenarios: Dict[str, float]
    ) -> pd.DataFrame:
        """
        Compare multiple mNAV scenarios

        Parameters:
        -----------
        current_price : float
            Current stock price
        scenarios : Dict[str, float]
            Dictionary of scenario names and mNAV values
            Example: {'Conservative': 50.0, 'Base': 55.0, 'Optimistic': 60.0}

        Returns:
        --------
        pd.DataFrame
            Comparison table
        """
        results = []

        for scenario_name, mnav_value in scenarios.items():
            prem_disc = self.calculate_premium_discount(current_price, mnav_value)

            results.append({
                'Scenario': scenario_name,
                'mNAV per Share': mnav_value,
                'Current Price': current_price,
                'P/mNAV Ratio': prem_disc['p_mnav_ratio'],
                'Premium/Discount %': prem_disc['premium_discount_pct'],
                'Status': prem_disc['status']
            })

        return pd.DataFrame(results)


if __name__ == "__main__":
    """
    Test the mNAV calculator
    """
    print("\n" + "="*70)
    print("Testing mNAV Calculator")
    print("="*70 + "\n")

    # Sample balance sheet data
    sample_bs = pd.DataFrame({
        'total_assets': [1000000000],
        'total_liabilities': [600000000],
        'minority_interest': [50000000],
    })

    shares_outstanding = 10000000  # 10 million shares

    # Initialize calculator
    calc = mNAVCalculator(sample_bs, shares_outstanding)

    # Test basic NAV
    print("1. Basic NAV Calculation:")
    print("-" * 70)
    basic_nav = calc.calculate_basic_nav()
    for key, value in basic_nav.items():
        print(f"{key}: {value}")

    # Test mNAV with fair value
    print("\n2. mNAV with Fair Value Adjustment:")
    print("-" * 70)
    mnav_data = calc.calculate_mnav_with_fair_value(
        property_fair_value=500000000,  # $500M fair value
        property_book_value=400000000,  # $400M book value
        deferred_tax_rate=0.10
    )
    for key, value in mnav_data.items():
        print(f"{key}: {value}")

    # Test premium/discount
    print("\n3. Premium/Discount Analysis:")
    print("-" * 70)
    current_price = 38.50
    premium_data = calc.calculate_premium_discount(
        current_price, mnav_data['mnav_per_share']
    )
    for key, value in premium_data.items():
        print(f"{key}: {value}")

    # Print summary
    print(calc.get_mnav_summary(mnav_data, premium_data))

    # Test scenario comparison
    print("\n4. Scenario Comparison:")
    print("-" * 70)
    scenarios = {
        'Conservative': 30.0,
        'Base Case': 35.0,
        'Optimistic': 40.0
    }
    comparison = calc.compare_multiple_valuations(current_price, scenarios)
    print(comparison.to_string(index=False))
