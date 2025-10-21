"""
OpenBB Workspace Plotly Themes
Dark and Light themes matching OpenBB Workspace styling
"""

# OpenBB Dark Theme
openbb_dark_template = {
    "data": {
        "candlestick": [
            {
                "decreasing": {
                    "fillcolor": "#e4003a",
                    "line": {"color": "#e4003a"}
                },
                "increasing": {
                    "fillcolor": "#00ACFF",
                    "line": {"color": "#00ACFF"}
                },
                "type": "candlestick"
            }
        ],
        "bar": [
            {
                "error_x": {"color": "#f2f5fa"},
                "error_y": {"color": "#f2f5fa"},
                "marker": {
                    "line": {"color": "rgb(17,17,17)", "width": 0.5},
                    "pattern": {"fillmode": "overlay", "size": 10, "solidity": 0.2}
                },
                "type": "bar"
            }
        ],
        "scatter": [
            {
                "marker": {"line": {"color": "#283442"}},
                "type": "scatter"
            }
        ]
    },
    "layout": {
        "font": {
            "color": "#f2f5fa",
            "family": "Inter",
            "size": 14
        },
        "colorway": [
            "#005CA9", "#4ADE80", "#16A34A", "#33BBFF",
            "#F5B166", "#EF7D00", "#991B1B", "#FACCD8",
            "#E93361", "#CCBE00"
        ],
        "paper_bgcolor": "#151518",
        "plot_bgcolor": "#151518",
        "xaxis": {
            "automargin": False,
            "gridcolor": "#283442",
            "linecolor": "#F5EFF3",
            "ticks": "outside",
            "title": {"standoff": 20},
            "zerolinecolor": "#283442",
            "zerolinewidth": 2,
            "autorange": True,
            "mirror": True,
            "rangeslider": {"visible": False},
            "showgrid": True,
            "showline": True,
            "tickfont": {"size": 12},
            "zeroline": False
        },
        "yaxis": {
            "automargin": False,
            "gridcolor": "#283442",
            "linecolor": "#F5EFF3",
            "ticks": "outside",
            "title": {"standoff": 20, "font": {"size": 12}},
            "tickfont": {"size": 12},
            "zerolinecolor": "#283442",
            "zerolinewidth": 2,
            "anchor": "x",
            "fixedrange": False,
            "mirror": True,
            "showgrid": True,
            "showline": True,
            "side": "right",
            "tick0": 0.5,
            "zeroline": False
        },
        "dragmode": "pan",
        "legend": {
            "bgcolor": "rgba(0, 0, 0, 0)",
            "font": {"size": 12},
            "x": 0.01,
            "xanchor": "left",
            "y": 0.99,
            "yanchor": "top"
        },
        "hovermode": "x unified",
        "title": {"x": 0.05}
    }
}

# OpenBB Light Theme
openbb_light_template = {
    "data": {
        "candlestick": [
            {
                "decreasing": {
                    "fillcolor": "#e4003a",
                    "line": {"color": "#e4003a"}
                },
                "increasing": {
                    "fillcolor": "#00ACFF",
                    "line": {"color": "#00ACFF"}
                },
                "type": "candlestick"
            }
        ],
        "bar": [
            {
                "error_x": {"color": "#2d3748"},
                "error_y": {"color": "#2d3748"},
                "marker": {
                    "line": {"color": "#ffffff", "width": 0.5},
                    "pattern": {"fillmode": "overlay", "size": 10, "solidity": 0.2}
                },
                "type": "bar"
            }
        ],
        "scatter": [
            {
                "marker": {"line": {"color": "#e2e8f0"}},
                "type": "scatter"
            }
        ]
    },
    "layout": {
        "font": {
            "color": "#2d3748",
            "family": "Inter",
            "size": 14
        },
        "colorway": [
            "#005CA9", "#16A34A", "#0891B2", "#7C3AED",
            "#DC2626", "#EA580C", "#CA8A04", "#DB2777",
            "#4F46E5", "#059669"
        ],
        "paper_bgcolor": "#ffffff",
        "plot_bgcolor": "#ffffff",
        "xaxis": {
            "automargin": False,
            "gridcolor": "#e2e8f0",
            "linecolor": "#cbd5e0",
            "ticks": "outside",
            "title": {"standoff": 20},
            "zerolinecolor": "#e2e8f0",
            "zerolinewidth": 2,
            "autorange": True,
            "mirror": True,
            "rangeslider": {"visible": False},
            "showgrid": True,
            "showline": True,
            "tickfont": {"size": 12},
            "zeroline": False
        },
        "yaxis": {
            "automargin": False,
            "gridcolor": "#e2e8f0",
            "linecolor": "#cbd5e0",
            "ticks": "outside",
            "title": {"standoff": 20, "font": {"size": 12}},
            "tickfont": {"size": 12},
            "zerolinecolor": "#e2e8f0",
            "zerolinewidth": 2,
            "anchor": "x",
            "fixedrange": False,
            "mirror": True,
            "showgrid": True,
            "showline": True,
            "side": "right",
            "tick0": 0.5,
            "zeroline": False
        },
        "dragmode": "pan",
        "legend": {
            "bgcolor": "rgba(255, 255, 255, 0.9)",
            "font": {"size": 12},
            "x": 0.01,
            "xanchor": "left",
            "y": 0.99,
            "yanchor": "top"
        },
        "hovermode": "x unified",
        "title": {"x": 0.05}
    }
}


def get_theme(theme: str = "dark"):
    """
    Get Plotly theme based on theme name

    Parameters:
    -----------
    theme : str
        Theme name ('dark' or 'light')

    Returns:
    --------
    dict
        Plotly theme template
    """
    if theme.lower() == "light":
        return openbb_light_template
    return openbb_dark_template
