# BMNR Stock Analysis Dashboard

A comprehensive stock analysis tool featuring technical analysis and Modified Net Asset Value (mNAV) calculations for BMNR stock.

## Features

### Technical Analysis
- **Price Charts**: Interactive candlestick charts with volume
- **Trend Indicators**: Moving Averages (MA 5, 10, 20, 50, 100, 200), EMA, MACD
- **Momentum Indicators**: RSI, Stochastic Oscillator
- **Volatility Indicators**: Bollinger Bands, ATR
- **Volume Indicators**: OBV, VWAP

### mNAV Analysis
- **Modified Net Asset Value Calculation**: Industry-standard valuation for REITs and asset-heavy companies
- **P/mNAV Ratio Analysis**: Track premium/discount to net asset value
- **Fair Value Adjustments**: Support for property revaluation
- **Historical Trends**: Visualize P/mNAV ratio over time
- **Scenario Comparison**: Compare multiple valuation scenarios

### Interactive Dashboard
- Real-time data fetching via OpenBB Platform
- Customizable parameters and date ranges
- Interactive Plotly visualizations
- Data export functionality

## Project Structure

```
openbb_for_finance/
├── data/
│   ├── raw/                 # Raw data cache
│   └── processed/           # Processed data
├── src/
│   ├── config.py           # Configuration settings
│   ├── data_fetcher.py     # Data acquisition module
│   ├── mnav_calculator.py  # mNAV calculation engine
│   ├── indicators.py       # Technical & fundamental indicators
│   └── visualizer.py       # Plotting and visualization
├── notebooks/              # Jupyter notebooks for exploration
├── output/                 # Exported charts and reports
├── app.py                  # Streamlit web application
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Installation

### Prerequisites
- Python 3.9 - 3.12
- pip package manager

### Step 1: Clone or Download
```bash
cd openbb_for_finance
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Install OpenBB (if not already installed)
```bash
pip install openbb
```

## Usage

### Option 1: Streamlit Dashboard (Recommended)

Run the interactive web dashboard:

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

**Dashboard Features:**
- Adjust date ranges
- Enable/disable mNAV analysis
- Configure fair value adjustments
- View technical indicators
- Export data to CSV

### Option 2: Python Scripts

#### Test Data Fetcher
```bash
cd src
python data_fetcher.py
```

#### Test mNAV Calculator
```bash
cd src
python mnav_calculator.py
```

#### Test Technical Indicators
```bash
cd src
python indicators.py
```

### Option 3: Jupyter Notebooks

```bash
jupyter notebook
```

Navigate to the `notebooks/` folder and create your own analysis.

## mNAV Calculation

### What is mNAV?

Modified Net Asset Value (mNAV) is a valuation method commonly used for:
- Real Estate Investment Trusts (REITs)
- Asset management companies
- Companies with significant tangible assets

### Formula

```
mNAV = (Fair Value of Assets - Liabilities - Minority Interest) / Shares Outstanding
```

### How to Use mNAV Analysis

1. **Enable mNAV** in the sidebar
2. **Enter Shares Outstanding**: Total number of shares
3. **Optional - Fair Value Adjustment**:
   - Property Fair Value: Market/appraisal value
   - Property Book Value: Balance sheet value
   - Deferred Tax Rate: Tax on revaluation gains

4. **Interpret Results**:
   - **P/mNAV > 1.0**: Trading at premium (potentially overvalued)
   - **P/mNAV < 1.0**: Trading at discount (potentially undervalued)
   - **P/mNAV ≈ 1.0**: Trading near fair value

## Configuration

### Customizing Settings

Edit `src/config.py` to customize:

```python
# Stock Symbol
DEFAULT_SYMBOL = "BMNR"

# Technical Indicator Parameters
MA_PERIODS = [5, 10, 20, 50, 100, 200]
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26

# Chart Settings
CHART_HEIGHT = 800
CHART_THEME = "plotly_white"
```

### OpenBB Configuration

If you have an OpenBB Personal Access Token (PAT):

```bash
# Windows
set OPENBB_PAT=your_token_here

# Mac/Linux
export OPENBB_PAT=your_token_here
```

Or add it to `src/config.py`:
```python
OPENBB_PAT = "your_token_here"
```

## Example Workflows

### Workflow 1: Quick Technical Analysis

```python
from src.data_fetcher import StockDataFetcher
from src.indicators import TechnicalIndicators
from src.visualizer import StockVisualizer

# Fetch data
fetcher = StockDataFetcher("BMNR")
data = fetcher.get_historical_data("2024-01-01", "2024-12-31")

# Calculate indicators
tech = TechnicalIndicators(data)
df = tech.calculate_all_indicators()

# Visualize
viz = StockVisualizer("BMNR")
fig = viz.plot_technical_indicators(df)
fig.show()
```

### Workflow 2: mNAV Analysis

```python
from src.data_fetcher import StockDataFetcher
from src.mnav_calculator import mNAVCalculator

# Fetch fundamental data
fetcher = StockDataFetcher("BMNR")
fundamental = fetcher.get_all_fundamental_data()

# Calculate mNAV
calc = mNAVCalculator(
    balance_sheet=fundamental['balance_sheet'],
    shares_outstanding=10000000
)

mnav_data = calc.calculate_mnav_with_fair_value(
    property_fair_value=500000000,
    property_book_value=400000000,
    deferred_tax_rate=0.10
)

print(f"mNAV per Share: ${mnav_data['mnav_per_share']:.2f}")
```

## Data Sources

- **Price Data**: OpenBB Platform (Yahoo Finance provider)
- **Fundamental Data**: OpenBB Platform
- **Technical Indicators**: TA-Lib library

## Troubleshooting

### Issue: "No data found for BMNR"

**Solutions:**
1. Verify BMNR is the correct ticker symbol
2. Check internet connection
3. Try different date ranges
4. Verify OpenBB is properly installed

### Issue: "Error fetching fundamental data"

**Solutions:**
1. Some stocks may have limited fundamental data
2. Try using `provider="fmp"` or other OpenBB providers
3. Check if the stock is publicly traded

### Issue: "Module not found"

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

## Performance Tips

1. **Data Caching**: Historical data is cached for 1 hour in Streamlit
2. **Date Range**: Use shorter date ranges for faster loading
3. **Indicators**: Deselect unused indicators to improve performance

## Advanced Usage

### Custom Indicators

Add your own indicators in `src/indicators.py`:

```python
def calculate_custom_indicator(self) -> pd.DataFrame:
    df = self.df.copy()
    # Your calculation here
    df['custom_indicator'] = ...
    return df
```

### Custom Visualizations

Add charts in `src/visualizer.py`:

```python
def plot_custom_chart(self, df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    # Your visualization here
    return fig
```

## Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add more technical indicators
- [ ] Support for multiple stocks comparison
- [ ] Add alerts and notifications
- [ ] Portfolio tracking
- [ ] Backtesting functionality

## Dependencies

Main dependencies:
- `openbb>=4.0.0` - Financial data platform
- `pandas>=2.0.0` - Data manipulation
- `plotly>=5.14.0` - Interactive charts
- `streamlit>=1.28.0` - Web dashboard
- `ta>=0.11.0` - Technical analysis
- `numpy>=1.24.0` - Numerical computing

See `requirements.txt` for complete list.

## License

This project is open source and available for educational and personal use.

## Disclaimer

⚠️ **IMPORTANT**: This tool is for educational and informational purposes only.

- NOT financial advice
- Past performance does not guarantee future results
- Always do your own research
- Consult with a qualified financial advisor before making investment decisions
- The developers are not responsible for any financial losses

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review OpenBB documentation: https://docs.openbb.co
3. Check Streamlit documentation: https://docs.streamlit.io

## Version History

### v1.0.0 (Current)
- Initial release
- Technical analysis with 15+ indicators
- mNAV calculation with fair value adjustments
- Interactive Streamlit dashboard
- Data export functionality

## Acknowledgments

- **OpenBB Platform**: Financial data infrastructure
- **Plotly**: Interactive visualization library
- **Streamlit**: Web application framework
- **TA-Lib**: Technical analysis indicators

---

**Built with** ❤️ **for BMNR stock analysis**

Last Updated: 2025
