"""
OpenBB Workspace Backend for BMNR Stock Analysis
FastAPI application providing custom widgets for OpenBB Workspace
"""
import json
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import plotly.graph_objects as go

# Add parent directory to path to import src modules
sys.path.insert(0, str(Path(__file__).parent.parent))

# Configure API keys BEFORE importing OpenBB modules
from openbb import obb

# Set API credentials
API_KEYS = {
    'fmp_api_key': 'aMygwSPUSv1KUf1OxlVPvk12JrJnIGpi',
    'polygon_api_key': 'hzQYA0NSR15nlAT3Bym3nFCsTuF05inq',
}

# Configure environment variables
for key, value in API_KEYS.items():
    env_key = f'OPENBB_{key.upper()}'
    os.environ[env_key] = value

# Set credentials directly
try:
    obb.user.credentials.fmp_api_key = API_KEYS['fmp_api_key']
    obb.user.credentials.polygon_api_key = API_KEYS['polygon_api_key']
    print("[OK] API keys configured successfully")
except Exception as e:
    print(f"[WARNING] Could not set API keys directly: {e}")
    print("         Using environment variables instead")

from src.data_fetcher import StockDataFetcher
from src.indicators import TechnicalIndicators, FundamentalIndicators
from src.visualizer import StockVisualizer
from src.mnav_calculator import mNAVCalculator
from backend.plotly_theme import get_theme

# Initialize FastAPI app
app = FastAPI(
    title="BMNR Stock Analysis Backend",
    description="Custom backend for BMNR stock analysis in OpenBB Workspace",
    version="1.0.0"
)

# CORS configuration - Allow OpenBB Workspace to access this backend
origins = [
    "https://pro.openbb.co",      # OpenBB Workspace production
    "https://excel.openbb.co",    # OpenBB Excel
    "http://localhost:1420",      # OpenBB Desktop app
    "http://localhost:3000",      # Development
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
DEFAULT_SYMBOL = "BMNR"
DEFAULT_DAYS = 365


@app.get("/")
def read_root():
    """Root endpoint - API information"""
    return {
        "name": "BMNR Stock Analysis Backend",
        "version": "1.0.0",
        "description": "Custom backend for OpenBB Workspace",
        "endpoints": {
            "widgets": "/widgets.json",
            "apps": "/apps.json",
            "technical_chart": "/bmnr/technical_chart",
            "mnav_chart": "/bmnr/mnav_chart",
            "price_table": "/bmnr/price_table",
            "metrics": "/bmnr/metrics"
        }
    }


@app.get("/widgets.json")
def get_widgets():
    """Widgets configuration file for OpenBB Workspace"""
    widgets_path = Path(__file__).parent / "widgets.json"
    return JSONResponse(
        content=json.load(widgets_path.open())
    )


@app.get("/apps.json")
def get_apps():
    """Apps configuration file for OpenBB Workspace"""
    apps_path = Path(__file__).parent / "apps.json"
    return JSONResponse(
        content=json.load(apps_path.open())
    )


@app.get("/bmnr/technical_chart")
def get_technical_chart(
    symbol: str = Query(DEFAULT_SYMBOL, description="Stock ticker symbol"),
    days: int = Query(DEFAULT_DAYS, description="Number of days of historical data"),
    theme: str = Query("dark", description="Chart theme (dark or light)"),
    raw: bool = Query(False, description="Return raw data for AI analysis")
):
    """
    Get technical analysis chart with candlesticks and indicators

    Returns Plotly chart as JSON for OpenBB Workspace rendering
    """
    try:
        # Calculate date range
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        # Fetch data
        fetcher = StockDataFetcher(symbol)
        hist_data = fetcher.get_historical_data(start_date, end_date)

        # Calculate indicators
        tech_ind = TechnicalIndicators(hist_data)
        df_with_indicators = tech_ind.calculate_all_indicators()

        # Return raw data if requested (for AI analysis)
        if raw:
            return df_with_indicators.tail(100).to_dict(orient="records")

        # Create visualizer
        viz = StockVisualizer(symbol)

        # Get theme
        plot_theme = get_theme(theme)

        # Create figure with candlesticks and indicators
        fig = go.Figure()

        # Candlestick
        fig.add_trace(go.Candlestick(
            x=df_with_indicators.index,
            open=df_with_indicators['open'],
            high=df_with_indicators['high'],
            low=df_with_indicators['low'],
            close=df_with_indicators['close'],
            name='Price'
        ))

        # Add Moving Averages
        for ma in ['MA_20', 'MA_50']:
            if ma in df_with_indicators.columns:
                fig.add_trace(go.Scatter(
                    x=df_with_indicators.index,
                    y=df_with_indicators[ma],
                    name=ma,
                    line=dict(width=2)
                ))

        # Apply theme and layout
        fig.update_layout(
            template=plot_theme,
            title=f"{symbol} - Technical Analysis",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            height=600,
            hovermode='x unified'
        )

        # Return Plotly JSON
        return json.loads(fig.to_json())

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )


@app.get("/bmnr/mnav_chart")
def get_mnav_chart(
    symbol: str = Query(DEFAULT_SYMBOL, description="Stock ticker symbol"),
    days: int = Query(DEFAULT_DAYS, description="Number of days of historical data"),
    shares_outstanding: float = Query(10000000, description="Shares outstanding"),
    property_fair_value: Optional[float] = Query(None, description="Property fair value"),
    property_book_value: Optional[float] = Query(None, description="Property book value"),
    deferred_tax_rate: float = Query(0.0, description="Deferred tax rate"),
    theme: str = Query("dark", description="Chart theme"),
    raw: bool = Query(False, description="Return raw data for AI analysis")
):
    """
    Get mNAV analysis chart showing P/mNAV ratio and premium/discount
    """
    try:
        # Calculate date range
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        # Fetch data
        fetcher = StockDataFetcher(symbol)
        hist_data = fetcher.get_historical_data(start_date, end_date)
        fundamental_data = fetcher.get_all_fundamental_data()

        # Calculate mNAV
        fund_ind = FundamentalIndicators(fundamental_data, hist_data)
        fund_ind.setup_mnav_calculator(shares_outstanding)

        current_price = hist_data['close'].iloc[-1]

        mnav_analysis = fund_ind.get_mnav_analysis(
            current_price=current_price,
            property_fair_value=property_fair_value,
            property_book_value=property_book_value,
            deferred_tax_rate=deferred_tax_rate
        )

        mnav_data = mnav_analysis['mnav_data']
        historical_mnav = mnav_analysis['historical_mnav']

        # Return raw data if requested
        if raw:
            return {
                "mnav_per_share": mnav_data['mnav_per_share'],
                "current_price": float(current_price),
                "p_mnav_ratio": mnav_analysis['premium_data']['p_mnav_ratio'],
                "premium_discount_pct": mnav_analysis['premium_data']['premium_discount_pct'],
                "historical_data": historical_mnav.tail(100).to_dict(orient="records")
            }

        # Create chart
        plot_theme = get_theme(theme)

        fig = go.Figure()

        # Stock price
        fig.add_trace(go.Scatter(
            x=historical_mnav.index,
            y=historical_mnav['close'],
            name='Stock Price',
            line=dict(color='#00ACFF', width=2)
        ))

        # mNAV line
        fig.add_trace(go.Scatter(
            x=historical_mnav.index,
            y=[mnav_data['mnav_per_share']] * len(historical_mnav),
            name=f"mNAV (${mnav_data['mnav_per_share']:.2f})",
            line=dict(color='#e4003a', width=2, dash='dash')
        ))

        # Apply theme
        fig.update_layout(
            template=plot_theme,
            title=f"{symbol} - mNAV Analysis",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            height=500,
            hovermode='x unified'
        )

        return json.loads(fig.to_json())

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )


@app.get("/bmnr/price_table")
def get_price_table(
    symbol: str = Query(DEFAULT_SYMBOL, description="Stock ticker symbol"),
    days: int = Query(90, description="Number of days"),
):
    """
    Get historical price data as table
    """
    try:
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        fetcher = StockDataFetcher(symbol)
        hist_data = fetcher.get_historical_data(start_date, end_date)

        # Format for table
        table_data = hist_data[['open', 'high', 'low', 'close', 'volume']].copy()
        table_data.index.name = 'date'
        table_data.reset_index(inplace=True)
        table_data['date'] = table_data['date'].astype(str)

        # Round numerical values
        for col in ['open', 'high', 'low', 'close']:
            table_data[col] = table_data[col].round(2)

        return table_data.to_dict(orient="records")

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )


@app.get("/bmnr/metrics")
def get_metrics(
    symbol: str = Query(DEFAULT_SYMBOL, description="Stock ticker symbol"),
    shares_outstanding: float = Query(10000000, description="Shares outstanding"),
):
    """
    Get key metrics for BMNR stock
    """
    try:
        # Fetch recent data
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

        fetcher = StockDataFetcher(symbol)
        hist_data = fetcher.get_historical_data(start_date, end_date)

        # Calculate current metrics
        current_price = float(hist_data['close'].iloc[-1])
        prev_price = float(hist_data['close'].iloc[-2])
        price_change = current_price - prev_price
        price_change_pct = (price_change / prev_price) * 100

        # Calculate RSI if we have enough data
        tech_ind = TechnicalIndicators(hist_data)
        df_with_ind = tech_ind.calculate_rsi()
        rsi = float(df_with_ind['RSI'].iloc[-1]) if 'RSI' in df_with_ind.columns else None

        # Try to get mNAV
        try:
            fundamental_data = fetcher.get_all_fundamental_data()
            fund_ind = FundamentalIndicators(fundamental_data, hist_data)
            fund_ind.setup_mnav_calculator(shares_outstanding)

            mnav_analysis = fund_ind.get_mnav_analysis(current_price=current_price)
            mnav_per_share = mnav_analysis['mnav_data']['mnav_per_share']
            p_mnav_ratio = mnav_analysis['premium_data']['p_mnav_ratio']
            premium_discount = mnav_analysis['premium_data']['premium_discount_pct']
        except:
            mnav_per_share = None
            p_mnav_ratio = None
            premium_discount = None

        return {
            "symbol": symbol,
            "current_price": round(current_price, 2),
            "price_change": round(price_change, 2),
            "price_change_pct": round(price_change_pct, 2),
            "rsi": round(rsi, 2) if rsi else None,
            "mnav_per_share": round(mnav_per_share, 2) if mnav_per_share else None,
            "p_mnav_ratio": round(p_mnav_ratio, 2) if p_mnav_ratio else None,
            "premium_discount_pct": round(premium_discount, 2) if premium_discount else None,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )


@app.get("/bmnr/scenario_analysis")
def get_scenario_analysis(
    symbol: str = Query(DEFAULT_SYMBOL, description="Stock ticker symbol"),
    shares_outstanding: float = Query(10000000, description="Shares outstanding"),
    conservative_mnav: Optional[float] = Query(None, description="Conservative mNAV estimate"),
    base_mnav: Optional[float] = Query(None, description="Base case mNAV"),
    optimistic_mnav: Optional[float] = Query(None, description="Optimistic mNAV estimate"),
    theme: str = Query("dark", description="Chart theme")
):
    """
    Get mNAV scenario comparison chart
    """
    try:
        # Fetch current price
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

        fetcher = StockDataFetcher(symbol)
        hist_data = fetcher.get_historical_data(start_date, end_date)
        current_price = float(hist_data['close'].iloc[-1])

        # Calculate base mNAV if not provided
        if base_mnav is None:
            fundamental_data = fetcher.get_all_fundamental_data()
            fund_ind = FundamentalIndicators(fundamental_data, hist_data)
            fund_ind.setup_mnav_calculator(shares_outstanding)
            mnav_analysis = fund_ind.get_mnav_analysis(current_price=current_price)
            base_mnav = mnav_analysis['mnav_data']['mnav_per_share']

        # Set defaults for conservative and optimistic
        if conservative_mnav is None:
            conservative_mnav = base_mnav * 0.9
        if optimistic_mnav is None:
            optimistic_mnav = base_mnav * 1.1

        # Create scenario data
        scenarios = {
            'Conservative': conservative_mnav,
            'Base Case': base_mnav,
            'Optimistic': optimistic_mnav
        }

        plot_theme = get_theme(theme)

        # Create bar chart
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=list(scenarios.keys()),
            y=list(scenarios.values()),
            name='mNAV per Share',
            marker_color='#00ACFF',
            text=[f"${v:.2f}" for v in scenarios.values()],
            textposition='auto'
        ))

        # Add current price line
        fig.add_hline(
            y=current_price,
            line_dash="dash",
            line_color="#e4003a",
            annotation_text=f"Current Price: ${current_price:.2f}"
        )

        fig.update_layout(
            template=plot_theme,
            title=f"{symbol} - mNAV Scenario Analysis",
            xaxis_title="Scenario",
            yaxis_title="Price per Share ($)",
            height=400
        )

        return json.loads(fig.to_json())

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
