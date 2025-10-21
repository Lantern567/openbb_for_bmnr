"""
Configuration file for BMNR Stock Analysis
"""
from datetime import datetime, timedelta
import os

# Stock Symbol
DEFAULT_SYMBOL = "BMNR"

# Date Range Settings
DEFAULT_START_DATE = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
DEFAULT_END_DATE = datetime.now().strftime("%Y-%m-%d")

# Data Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

# Technical Indicators Parameters
MA_PERIODS = [5, 10, 20, 50, 100, 200]
EMA_PERIODS = [12, 26]
RSI_PERIOD = 14
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9
BOLLINGER_PERIOD = 20
BOLLINGER_STD = 2
ATR_PERIOD = 14

# mNAV Parameters
DEFAULT_DEFERRED_TAX_RATE = 0.0
MNAV_DECIMAL_PLACES = 2

# Visualization Settings
CHART_HEIGHT = 800
CHART_WIDTH = 1200
CHART_THEME = "plotly_white"

# Color Scheme
COLOR_BULLISH = "green"
COLOR_BEARISH = "red"
COLOR_NEUTRAL = "blue"
COLOR_MA = ["orange", "purple", "brown", "pink", "cyan", "magenta"]

# Streamlit Settings
PAGE_TITLE = "BMNR Stock Analysis Dashboard"
PAGE_ICON = "📊"
LAYOUT = "wide"

# Data Caching
CACHE_EXPIRY_HOURS = 24

# OpenBB Settings
# Add your OpenBB API keys here if needed
OPENBB_PAT = os.getenv("OPENBB_PAT", None)  # Personal Access Token
