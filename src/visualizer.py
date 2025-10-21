"""
Visualization Module
Creates interactive charts for stock analysis
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from config import (
    CHART_HEIGHT, CHART_WIDTH, CHART_THEME,
    COLOR_BULLISH, COLOR_BEARISH, COLOR_NEUTRAL, COLOR_MA
)


class StockVisualizer:
    """
    Stock Data Visualizer
    Creates interactive Plotly charts for technical and fundamental analysis
    """

    def __init__(self, symbol: str):
        """
        Initialize visualizer

        Parameters:
        -----------
        symbol : str
            Stock ticker symbol
        """
        self.symbol = symbol

    def plot_candlestick_with_volume(
        self,
        df: pd.DataFrame,
        title: Optional[str] = None
    ) -> go.Figure:
        """
        Create candlestick chart with volume

        Parameters:
        -----------
        df : pd.DataFrame
            Price data
        title : str, optional
            Chart title

        Returns:
        --------
        go.Figure
            Plotly figure
        """
        if title is None:
            title = f"{self.symbol} - Price and Volume"

        # Create subplots
        fig = make_subplots(
            rows=2, cols=1,
            row_heights=[0.7, 0.3],
            subplot_titles=(title, 'Volume'),
            vertical_spacing=0.05,
            shared_xaxes=True
        )

        # Candlestick chart
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name='Price',
                increasing_line_color=COLOR_BULLISH,
                decreasing_line_color=COLOR_BEARISH
            ),
            row=1, col=1
        )

        # Volume bars
        colors = [COLOR_BULLISH if df['close'].iloc[i] >= df['open'].iloc[i]
                  else COLOR_BEARISH for i in range(len(df))]

        fig.add_trace(
            go.Bar(
                x=df.index,
                y=df['volume'],
                name='Volume',
                marker_color=colors,
                showlegend=False
            ),
            row=2, col=1
        )

        # Update layout
        fig.update_layout(
            height=CHART_HEIGHT,
            xaxis_rangeslider_visible=False,
            template=CHART_THEME,
            hovermode='x unified'
        )

        return fig

    def plot_technical_indicators(
        self,
        df: pd.DataFrame,
        indicators: List[str] = ['MA_20', 'MA_50', 'RSI', 'MACD']
    ) -> go.Figure:
        """
        Create comprehensive technical analysis chart

        Parameters:
        -----------
        df : pd.DataFrame
            Data with indicators
        indicators : List[str]
            List of indicators to plot

        Returns:
        --------
        go.Figure
            Plotly figure
        """
        # Determine number of subplots
        has_rsi = 'RSI' in indicators
        has_macd = 'MACD' in indicators
        ma_indicators = [ind for ind in indicators if 'MA' in ind or 'EMA' in ind]

        rows = 1 + int(has_rsi) + int(has_macd)
        row_heights = [0.5] + [0.25] * (rows - 1)

        subplot_titles = [f"{self.symbol} - Price & Moving Averages"]
        if has_rsi:
            subplot_titles.append('RSI')
        if has_macd:
            subplot_titles.append('MACD')

        # Create subplots
        fig = make_subplots(
            rows=rows, cols=1,
            row_heights=row_heights,
            subplot_titles=subplot_titles,
            vertical_spacing=0.05,
            shared_xaxes=True
        )

        # Price and MA
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name='Price',
                increasing_line_color=COLOR_BULLISH,
                decreasing_line_color=COLOR_BEARISH
            ),
            row=1, col=1
        )

        # Add moving averages
        for i, ma in enumerate(ma_indicators):
            if ma in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df.index,
                        y=df[ma],
                        name=ma,
                        line=dict(width=2, color=COLOR_MA[i % len(COLOR_MA)])
                    ),
                    row=1, col=1
                )

        # Add Bollinger Bands if available
        if 'BB_upper' in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['BB_upper'],
                    name='BB Upper',
                    line=dict(width=1, dash='dash', color='gray'),
                    showlegend=False
                ),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['BB_lower'],
                    name='BB Lower',
                    line=dict(width=1, dash='dash', color='gray'),
                    fill='tonexty',
                    fillcolor='rgba(128,128,128,0.2)',
                    showlegend=False
                ),
                row=1, col=1
            )

        current_row = 2

        # RSI
        if has_rsi and 'RSI' in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['RSI'],
                    name='RSI',
                    line=dict(color='purple', width=2)
                ),
                row=current_row, col=1
            )

            # Add RSI levels
            fig.add_hline(y=70, line_dash="dash", line_color="red",
                          row=current_row, col=1, annotation_text="Overbought")
            fig.add_hline(y=30, line_dash="dash", line_color="green",
                          row=current_row, col=1, annotation_text="Oversold")

            current_row += 1

        # MACD
        if has_macd and 'MACD' in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['MACD'],
                    name='MACD',
                    line=dict(color='blue', width=2)
                ),
                row=current_row, col=1
            )
            fig.add_trace(
                go.Scatter(
                    x=df.index,
                    y=df['MACD_signal'],
                    name='Signal',
                    line=dict(color='orange', width=2)
                ),
                row=current_row, col=1
            )
            if 'MACD_diff' in df.columns:
                colors = [COLOR_BULLISH if x > 0 else COLOR_BEARISH for x in df['MACD_diff']]
                fig.add_trace(
                    go.Bar(
                        x=df.index,
                        y=df['MACD_diff'],
                        name='Histogram',
                        marker_color=colors
                    ),
                    row=current_row, col=1
                )

        # Update layout
        fig.update_layout(
            height=CHART_HEIGHT,
            xaxis_rangeslider_visible=False,
            template=CHART_THEME,
            hovermode='x unified',
            showlegend=True
        )

        return fig

    def plot_mnav_analysis(
        self,
        price_data: pd.DataFrame,
        mnav_per_share: float,
        current_price: float,
        price_column: str = 'close'
    ) -> go.Figure:
        """
        Create mNAV analysis visualization

        Parameters:
        -----------
        price_data : pd.DataFrame
            Historical price data
        mnav_per_share : float
            Calculated mNAV per share
        current_price : float
            Current stock price
        price_column : str
            Column name for price

        Returns:
        --------
        go.Figure
            Plotly figure with mNAV analysis
        """
        # Create subplots
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=(
                f'{self.symbol} - Stock Price vs mNAV',
                'P/mNAV Ratio Over Time',
                'Premium/Discount %'
            ),
            row_heights=[0.4, 0.3, 0.3],
            vertical_spacing=0.08,
            shared_xaxes=True
        )

        # Subplot 1: Price vs mNAV
        fig.add_trace(
            go.Scatter(
                x=price_data.index,
                y=price_data[price_column],
                name='Stock Price',
                line=dict(color=COLOR_NEUTRAL, width=2),
                fill='tonexty'
            ),
            row=1, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=price_data.index,
                y=[mnav_per_share] * len(price_data),
                name=f'mNAV (${mnav_per_share:.2f})',
                line=dict(color=COLOR_BEARISH, width=2, dash='dash')
            ),
            row=1, col=1
        )

        # Subplot 2: P/mNAV Ratio
        p_mnav = price_data[price_column] / mnav_per_share

        fig.add_trace(
            go.Scatter(
                x=price_data.index,
                y=p_mnav,
                name='P/mNAV Ratio',
                fill='tozeroy',
                line=dict(color='purple', width=2)
            ),
            row=2, col=1
        )

        # Add reference line at 1.0
        fig.add_hline(
            y=1.0,
            line_dash="dash",
            line_color="gray",
            row=2, col=1,
            annotation_text="Fair Value (1.0x)"
        )

        # Subplot 3: Premium/Discount %
        premium_pct = (price_data[price_column] - mnav_per_share) / mnav_per_share * 100
        colors = [COLOR_BEARISH if x > 0 else COLOR_BULLISH for x in premium_pct]

        fig.add_trace(
            go.Bar(
                x=price_data.index,
                y=premium_pct,
                name='Premium/Discount %',
                marker_color=colors
            ),
            row=3, col=1
        )

        # Add zero line
        fig.add_hline(
            y=0,
            line_dash="solid",
            line_color="black",
            line_width=1,
            row=3, col=1
        )

        # Update layout
        fig.update_layout(
            height=CHART_HEIGHT + 100,
            title_text=f"mNAV Analysis - {self.symbol} (Current: ${current_price:.2f})",
            template=CHART_THEME,
            showlegend=True,
            hovermode='x unified'
        )

        # Update y-axis labels
        fig.update_yaxes(title_text="Price ($)", row=1, col=1)
        fig.update_yaxes(title_text="Ratio", row=2, col=1)
        fig.update_yaxes(title_text="Percentage (%)", row=3, col=1)

        return fig

    def plot_mnav_scenarios(
        self,
        current_price: float,
        scenarios_df: pd.DataFrame
    ) -> go.Figure:
        """
        Plot multiple mNAV scenarios comparison

        Parameters:
        -----------
        current_price : float
            Current stock price
        scenarios_df : pd.DataFrame
            DataFrame with scenario comparisons

        Returns:
        --------
        go.Figure
            Plotly figure
        """
        fig = go.Figure()

        # Bar chart for mNAV values
        fig.add_trace(
            go.Bar(
                x=scenarios_df['Scenario'],
                y=scenarios_df['mNAV per Share'],
                name='mNAV per Share',
                marker_color='lightblue',
                text=scenarios_df['mNAV per Share'].apply(lambda x: f'${x:.2f}'),
                textposition='auto'
            )
        )

        # Add current price line
        fig.add_hline(
            y=current_price,
            line_dash="dash",
            line_color=COLOR_BEARISH,
            annotation_text=f"Current Price: ${current_price:.2f}"
        )

        # Update layout
        fig.update_layout(
            title=f"{self.symbol} - mNAV Scenario Analysis",
            xaxis_title="Scenario",
            yaxis_title="Price per Share ($)",
            height=500,
            template=CHART_THEME,
            showlegend=True
        )

        return fig

    def create_dashboard(
        self,
        df_with_indicators: pd.DataFrame,
        mnav_analysis: Optional[Dict] = None
    ) -> go.Figure:
        """
        Create comprehensive dashboard with all charts

        Parameters:
        -----------
        df_with_indicators : pd.DataFrame
            Data with all technical indicators
        mnav_analysis : Dict, optional
            mNAV analysis results

        Returns:
        --------
        go.Figure
            Comprehensive dashboard
        """
        # Determine number of subplots
        rows = 4 if mnav_analysis else 3

        fig = make_subplots(
            rows=rows, cols=1,
            row_heights=[0.3, 0.2, 0.2, 0.3] if mnav_analysis else [0.4, 0.3, 0.3],
            subplot_titles=(
                f'{self.symbol} - Price & Volume',
                'RSI',
                'MACD',
                'mNAV Analysis' if mnav_analysis else None
            ),
            vertical_spacing=0.05,
            shared_xaxes=True
        )

        df = df_with_indicators

        # Row 1: Candlestick
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                name='Price'
            ),
            row=1, col=1
        )

        # Row 2: RSI
        if 'RSI' in df.columns:
            fig.add_trace(
                go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color='purple')),
                row=2, col=1
            )
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

        # Row 3: MACD
        if 'MACD' in df.columns:
            fig.add_trace(
                go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color='blue')),
                row=3, col=1
            )
            fig.add_trace(
                go.Scatter(x=df.index, y=df['MACD_signal'], name='Signal', line=dict(color='orange')),
                row=3, col=1
            )

        # Row 4: mNAV (if available)
        if mnav_analysis and rows == 4:
            historical_mnav = mnav_analysis.get('historical_mnav')
            if historical_mnav is not None and 'premium_discount_pct' in historical_mnav.columns:
                fig.add_trace(
                    go.Scatter(
                        x=historical_mnav.index,
                        y=historical_mnav['premium_discount_pct'],
                        name='Premium/Discount %',
                        fill='tozeroy'
                    ),
                    row=4, col=1
                )

        fig.update_layout(
            height=1200,
            template=CHART_THEME,
            xaxis_rangeslider_visible=False,
            hovermode='x unified'
        )

        return fig


if __name__ == "__main__":
    """
    Test visualizer
    """
    from data_fetcher import StockDataFetcher
    from indicators import TechnicalIndicators
    from config import DEFAULT_SYMBOL, DEFAULT_START_DATE, DEFAULT_END_DATE

    print("\n" + "="*70)
    print("Testing Visualizer")
    print("="*70 + "\n")

    # Fetch data
    fetcher = StockDataFetcher(DEFAULT_SYMBOL)

    try:
        hist_data = fetcher.get_historical_data(
            start_date=DEFAULT_START_DATE,
            end_date=DEFAULT_END_DATE
        )

        # Calculate indicators
        tech_ind = TechnicalIndicators(hist_data)
        df_with_ind = tech_ind.calculate_all_indicators()

        # Create visualizer
        viz = StockVisualizer(DEFAULT_SYMBOL)

        # Test candlestick chart
        print("Creating candlestick chart...")
        fig1 = viz.plot_candlestick_with_volume(df_with_ind)
        print("✓ Candlestick chart created")

        # Test technical indicators chart
        print("Creating technical indicators chart...")
        fig2 = viz.plot_technical_indicators(df_with_ind)
        print("✓ Technical indicators chart created")

        print("\nVisualization tests completed successfully!")
        print("Note: Charts are created but not displayed in console.")
        print("Use in Streamlit or Jupyter to view charts.")

    except Exception as e:
        print(f"Error: {e}")
