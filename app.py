"""
Streamlit Application for BMNR Stock Analysis
Interactive dashboard with technical and mNAV analysis
"""
import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime, timedelta

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.data_fetcher import StockDataFetcher
from src.indicators import TechnicalIndicators, FundamentalIndicators
from src.visualizer import StockVisualizer
from src.mnav_calculator import mNAVCalculator
from src.config import (
    DEFAULT_SYMBOL, DEFAULT_START_DATE, DEFAULT_END_DATE,
    PAGE_TITLE, PAGE_ICON, LAYOUT
)

# Page configuration
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=LAYOUT,
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-text {
        color: #28a745;
        font-weight: bold;
    }
    .danger-text {
        color: #dc3545;
        font-weight: bold;
    }
    .warning-text {
        color: #ffc107;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


# Cache data fetching
@st.cache_data(ttl=3600)
def fetch_historical_data(symbol, start_date, end_date):
    """Fetch and cache historical data"""
    fetcher = StockDataFetcher(symbol)
    return fetcher.get_historical_data(start_date, end_date)


@st.cache_data(ttl=3600)
def fetch_fundamental_data(symbol):
    """Fetch and cache fundamental data"""
    fetcher = StockDataFetcher(symbol)
    return fetcher.get_all_fundamental_data()


@st.cache_data(ttl=3600)
def calculate_indicators(hist_data):
    """Calculate and cache technical indicators"""
    tech_ind = TechnicalIndicators(hist_data)
    return tech_ind.calculate_all_indicators()


# Main application
def main():
    """Main application logic"""

    # Header
    st.markdown(f'<div class="main-header">{PAGE_ICON} BMNR Stock Analysis Dashboard</div>',
                unsafe_allow_html=True)

    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Settings")

        # Stock symbol
        symbol = st.text_input("Stock Symbol", value=DEFAULT_SYMBOL).upper()

        # Date range
        st.subheader("📅 Date Range")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                value=datetime.strptime(DEFAULT_START_DATE, "%Y-%m-%d").date()
            )
        with col2:
            end_date = st.date_input(
                "End Date",
                value=datetime.strptime(DEFAULT_END_DATE, "%Y-%m-%d").date()
            )

        st.markdown("---")

        # mNAV Parameters
        st.subheader("💰 mNAV Parameters")

        enable_mnav = st.checkbox("Enable mNAV Analysis", value=True)

        if enable_mnav:
            use_fair_value = st.checkbox("Use Fair Value Adjustment", value=False)

            if use_fair_value:
                st.info("💡 Enter property valuation data")

                property_fair_value = st.number_input(
                    "Property Fair Value ($)",
                    min_value=0.0,
                    value=0.0,
                    step=1000000.0,
                    format="%.0f",
                    help="Market value of investment properties"
                )

                property_book_value = st.number_input(
                    "Property Book Value ($)",
                    min_value=0.0,
                    value=0.0,
                    step=1000000.0,
                    format="%.0f",
                    help="Book value from balance sheet"
                )

                deferred_tax_rate = st.slider(
                    "Deferred Tax Rate (%)",
                    min_value=0.0,
                    max_value=30.0,
                    value=0.0,
                    step=1.0,
                    help="Tax rate for property revaluation"
                ) / 100
            else:
                property_fair_value = None
                property_book_value = None
                deferred_tax_rate = 0.0

            shares_outstanding = st.number_input(
                "Shares Outstanding",
                min_value=1.0,
                value=10000000.0,
                step=100000.0,
                format="%.0f",
                help="Total number of shares outstanding"
            )

        st.markdown("---")

        # Refresh button
        if st.button("🔄 Refresh Data", type="primary"):
            st.cache_data.clear()
            st.rerun()

    # Main content area
    try:
        with st.spinner("📊 Fetching data..."):
            # Fetch data
            hist_data = fetch_historical_data(
                symbol,
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )

            if hist_data.empty:
                st.error(f"❌ No data found for {symbol}")
                return

        # Calculate indicators
        with st.spinner("🔢 Calculating indicators..."):
            df_with_indicators = calculate_indicators(hist_data)

        # Create visualizer
        viz = StockVisualizer(symbol)

        # Get current price
        current_price = hist_data['close'].iloc[-1]
        prev_price = hist_data['close'].iloc[-2]
        price_change = current_price - prev_price
        price_change_pct = (price_change / prev_price) * 100

        # Display key metrics
        st.markdown("### 📊 Key Metrics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Current Price",
                f"${current_price:.2f}",
                f"{price_change:+.2f} ({price_change_pct:+.2f}%)"
            )

        with col2:
            st.metric(
                "Volume",
                f"{hist_data['volume'].iloc[-1]:,.0f}"
            )

        with col3:
            if 'RSI' in df_with_indicators.columns:
                rsi_value = df_with_indicators['RSI'].iloc[-1]
                st.metric("RSI", f"{rsi_value:.2f}")

        with col4:
            high_52w = hist_data['high'].tail(252).max()
            low_52w = hist_data['low'].tail(252).min()
            st.metric(
                "52W Range",
                f"${low_52w:.2f} - ${high_52w:.2f}"
            )

        # Tabs for different analyses
        tab1, tab2, tab3, tab4 = st.tabs([
            "📈 Technical Analysis",
            "💰 mNAV Analysis",
            "📋 Data Tables",
            "ℹ️ About"
        ])

        # Tab 1: Technical Analysis
        with tab1:
            st.markdown("### Technical Analysis")

            # Chart selection
            chart_type = st.selectbox(
                "Select Chart Type",
                ["Candlestick with Volume", "Technical Indicators", "All Indicators"]
            )

            if chart_type == "Candlestick with Volume":
                fig = viz.plot_candlestick_with_volume(df_with_indicators)
                st.plotly_chart(fig, use_container_width=True)

            elif chart_type == "Technical Indicators":
                indicators_to_show = st.multiselect(
                    "Select Indicators",
                    ['MA_20', 'MA_50', 'RSI', 'MACD', 'BB_upper', 'BB_lower'],
                    default=['MA_20', 'MA_50', 'RSI', 'MACD']
                )
                fig = viz.plot_technical_indicators(df_with_indicators, indicators_to_show)
                st.plotly_chart(fig, use_container_width=True)

            else:  # All Indicators
                fig = viz.plot_technical_indicators(
                    df_with_indicators,
                    ['MA_20', 'MA_50', 'RSI', 'MACD']
                )
                st.plotly_chart(fig, use_container_width=True)

            # Latest indicator values
            st.markdown("### 📊 Latest Indicator Values")
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown("**Moving Averages**")
                for ma in ['MA_5', 'MA_10', 'MA_20', 'MA_50']:
                    if ma in df_with_indicators.columns:
                        value = df_with_indicators[ma].iloc[-1]
                        st.text(f"{ma}: ${value:.2f}")

            with col2:
                st.markdown("**Momentum Indicators**")
                if 'RSI' in df_with_indicators.columns:
                    rsi = df_with_indicators['RSI'].iloc[-1]
                    rsi_status = "Overbought" if rsi > 70 else ("Oversold" if rsi < 30 else "Neutral")
                    st.text(f"RSI: {rsi:.2f} ({rsi_status})")

                if 'Stoch_K' in df_with_indicators.columns:
                    stoch = df_with_indicators['Stoch_K'].iloc[-1]
                    st.text(f"Stochastic: {stoch:.2f}")

            with col3:
                st.markdown("**Volatility Indicators**")
                if 'ATR' in df_with_indicators.columns:
                    atr = df_with_indicators['ATR'].iloc[-1]
                    st.text(f"ATR: ${atr:.2f}")

                if 'BB_width' in df_with_indicators.columns:
                    bb_width = df_with_indicators['BB_width'].iloc[-1]
                    st.text(f"BB Width: {bb_width:.4f}")

        # Tab 2: mNAV Analysis
        with tab2:
            st.markdown("### 💰 Modified Net Asset Value (mNAV) Analysis")

            if not enable_mnav:
                st.info("ℹ️ Enable mNAV Analysis in the sidebar to view this section")
            else:
                try:
                    with st.spinner("Calculating mNAV..."):
                        # Fetch fundamental data
                        fundamental_data = fetch_fundamental_data(symbol)

                        # Initialize fundamental indicators
                        fund_ind = FundamentalIndicators(fundamental_data, hist_data)
                        fund_ind.setup_mnav_calculator(shares_outstanding)

                        # Get mNAV analysis
                        mnav_analysis = fund_ind.get_mnav_analysis(
                            current_price=current_price,
                            property_fair_value=property_fair_value if use_fair_value else None,
                            property_book_value=property_book_value if use_fair_value else None,
                            deferred_tax_rate=deferred_tax_rate if use_fair_value else 0.0
                        )

                    # Display mNAV summary
                    mnav_data = mnav_analysis['mnav_data']
                    premium_data = mnav_analysis['premium_data']

                    # Key metrics
                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric(
                            "mNAV per Share",
                            f"${mnav_data['mnav_per_share']:.2f}"
                        )

                    with col2:
                        st.metric(
                            "P/mNAV Ratio",
                            f"{premium_data['p_mnav_ratio']:.2f}x"
                        )

                    with col3:
                        prem_disc = premium_data['premium_discount_pct']
                        st.metric(
                            "Premium/Discount",
                            f"{prem_disc:+.2f}%"
                        )

                    with col4:
                        status = premium_data['interpretation']
                        if "Premium" in status:
                            st.markdown(f'<p class="danger-text">Status: {status}</p>',
                                        unsafe_allow_html=True)
                        elif "Discount" in status:
                            st.markdown(f'<p class="success-text">Status: {status}</p>',
                                        unsafe_allow_html=True)
                        else:
                            st.markdown(f'<p class="warning-text">Status: {status}</p>',
                                        unsafe_allow_html=True)

                    # mNAV chart
                    st.markdown("### 📊 mNAV Visualization")
                    mnav_fig = viz.plot_mnav_analysis(
                        hist_data,
                        mnav_data['mnav_per_share'],
                        current_price
                    )
                    st.plotly_chart(mnav_fig, use_container_width=True)

                    # Detailed breakdown
                    st.markdown("### 📋 mNAV Breakdown")
                    with st.expander("View Detailed Calculation"):
                        st.text(mnav_analysis['summary'])

                    # Scenario analysis
                    st.markdown("### 🎯 Scenario Analysis")
                    col1, col2 = st.columns(2)

                    with col1:
                        conservative_mnav = st.number_input(
                            "Conservative mNAV",
                            value=mnav_data['mnav_per_share'] * 0.9,
                            step=1.0
                        )

                    with col2:
                        optimistic_mnav = st.number_input(
                            "Optimistic mNAV",
                            value=mnav_data['mnav_per_share'] * 1.1,
                            step=1.0
                        )

                    scenarios = {
                        'Conservative': conservative_mnav,
                        'Base Case': mnav_data['mnav_per_share'],
                        'Optimistic': optimistic_mnav
                    }

                    scenario_comparison = fund_ind.mnav_calculator.compare_multiple_valuations(
                        current_price,
                        scenarios
                    )

                    st.dataframe(scenario_comparison, use_container_width=True)

                except Exception as e:
                    st.error(f"❌ Error calculating mNAV: {str(e)}")
                    st.info("💡 Try adjusting parameters or check if fundamental data is available for this stock")

        # Tab 3: Data Tables
        with tab3:
            st.markdown("### 📋 Historical Data")

            # Data selection
            data_view = st.radio(
                "Select Data View",
                ["Price Data", "Technical Indicators", "Full Dataset"],
                horizontal=True
            )

            if data_view == "Price Data":
                display_df = hist_data[['open', 'high', 'low', 'close', 'volume']].tail(100)
            elif data_view == "Technical Indicators":
                ind_cols = [col for col in df_with_indicators.columns
                            if col not in ['open', 'high', 'low', 'close', 'volume']]
                display_df = df_with_indicators[ind_cols].tail(100)
            else:
                display_df = df_with_indicators.tail(100)

            st.dataframe(display_df, use_container_width=True)

            # Download data
            csv = df_with_indicators.to_csv()
            st.download_button(
                label="📥 Download Full Dataset (CSV)",
                data=csv,
                file_name=f"{symbol}_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

        # Tab 4: About
        with tab4:
            st.markdown("### ℹ️ About This Dashboard")

            st.markdown("""
            #### 📊 BMNR Stock Analysis Dashboard

            This interactive dashboard provides comprehensive analysis of BMNR stock including:

            **Technical Analysis:**
            - Candlestick charts with volume
            - Moving Averages (MA 5, 10, 20, 50, 100, 200)
            - Momentum indicators (RSI, Stochastic)
            - Trend indicators (MACD)
            - Volatility indicators (Bollinger Bands, ATR)
            - Volume indicators (OBV, VWAP)

            **mNAV Analysis:**
            - Modified Net Asset Value calculation
            - P/mNAV ratio analysis
            - Premium/Discount to mNAV
            - Historical mNAV trends
            - Scenario comparisons

            **Features:**
            - Real-time data from OpenBB Platform
            - Interactive charts powered by Plotly
            - Customizable parameters
            - Data export functionality

            ---

            **Data Sources:**
            - Price Data: OpenBB Platform (Yahoo Finance)
            - Technical Indicators: TA Library
            - Fundamental Data: OpenBB Platform

            **Version:** 1.0.0

            **Created for:** BMNR Stock Analysis
            """)

    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
        st.info("💡 Please check your internet connection and try refreshing the page")


if __name__ == "__main__":
    main()
