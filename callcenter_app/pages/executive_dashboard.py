# Version: 0.2
# Last Modified: 2025-08-23
# Changes: Premium pixel-perfect 1920x1080 layout with glass-morphism design
"""
Executive Dashboard layout for VADS Call Center
Fixed 1920x1080 resolution with premium visual design
"""
from dash import html, dcc
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
from data.executive_dummy_data import get_executive_data

# Centralized chart configuration for maintainability
CHART_CONFIG = {
    "revenue_growth": {
        "height": 260,
        "margin": dict(t=10, b=20, l=70, r=30),  # Increased right margin for label
        "x_range": [-0.25, 6.5],  # Expanded x-axis range for more space
        "text_position": "bottom center",
        "text_font_size": 11,
        "color": "#00D4FF",
        "y_title": "Revenue ($)",
        "axis_font_size": 11
    },
    "cash_flow": {
        "height": 140,
        "margin": dict(t=10, b=10, l=10, r=10),
        "x_range": [None, None],  # Not used for bar chart
        "bar_color": "#FFB800",
        "text_font_size": 11,  # Reduced font size
        "y_title": "Cash Flow ($)",
        "axis_font_size": 11   # Reduced font size
    },
    "cost_per_call": {
        "height": 180,
        "margin": dict(t=10, b=10, l=10, r=10),
        "bar_colors": ['#00D4FF', '#FFFF00', '#FFB800', '#FF6B6B', '#A78BFA'],
        "y_title": "Cost ($)",
        "text_font_size": 11,  # Reduced font size
        "axis_font_size": 11   # Reduced font size
    },
    "performance_index": {
        "height": 180,
        "margin": dict(l=20, r=20, t=20, b=20),
        "bar_colors": ['#00FF88', '#00D4FF', '#FFB800', '#A78BFA', '#FF6B9D'],
        "y_title": "Performance Breakdown",
        "text_font_size": 11,  # Reduced font size
        "axis_font_size": 11   # Reduced font size
    },
    "efficiency_rate": {
        "value": 94.2,
        "reference": 91,
        "bar_color": "#00D4FF",
        "number_color": "#00D4FF",
        "threshold": 95,
        "steps": [
            {"range": [0, 60], "color": "rgba(255, 51, 102, 0.4)"},
            {"range": [60, 85], "color": "rgba(255, 184, 0, 0.4)"},
            {"range": [85, 100], "color": "rgba(0, 255, 136, 0.4)"}
        ],
        "text_font_size": 11,  # Reduced font size
        "axis_font_size": 11   # Reduced font size
    },
    "customer_retention": {
        "value": 96.8,
        "reference": 94.4,
        "bar_color": "#00FF88",
        "number_color": "#00FF88",
        "threshold": 98,
        "steps": [
            {"range": [0, 85], "color": "rgba(255, 51, 102, 0.4)"},
            {"range": [85, 95], "color": "rgba(255, 184, 0, 0.4)"},
            {"range": [95, 100], "color": "rgba(0, 255, 136, 0.4)"}
        ],
        "text_font_size": 11,  # Reduced font size
        "axis_font_size": 11   # Reduced font size
    }
}

def create_line_chart(x, y, config, text=None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        fill='tozeroy',
        mode='lines+markers+text',
        line=dict(color=config["color"], width=3),
        marker=dict(size=12, color=config["color"]),
        text=text,
        textposition=config["text_position"],
        textfont=dict(color="white", size=config["text_font_size"]),
        hoverinfo="x+y",
        showlegend=False
    ))
    fig.update_layout(
        height=config["height"],
        margin=config["margin"],
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            visible=True,
            color="#666",
            tickmode='array',
            tickvals=x,
            ticktext=x,
            range=config["x_range"],
            constrain='domain',
            automargin=False
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            visible=True,
            color="#666",
            gridcolor="rgba(0,0,0,0)",
            title=config["y_title"],
            tickfont=dict(color="#fff"),
            range=[0, max(y)*1.15],
            constrain='domain',
            automargin=False
        ),
        font=dict(color="#fff"),
    )
    return fig

def create_bar_chart(x, y, config, text=None):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x,
        y=y,
        text=text,
        textposition='outside',
        marker=dict(color=config["bar_color"]),
        textfont=dict(size=config["text_font_size"], color='white', family='Arial')
    ))
    fig.update_layout(
        height=config["height"],
        margin=config["margin"],
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            visible=True,
            color='#666',
            tickmode='array',
            tickvals=x,
            ticktext=x,
            constrain='domain',
            automargin=True
        ),
        yaxis=dict(
            showgrid=True,
            zeroline=False,
            visible=True,
            color='#666',
            gridcolor='rgba(128,128,128,0.3)',
            title=config["y_title"],
            tickfont=dict(color="#fff"),
            range=[min(y)*0.85, max(y)*1.15],
            constrain='domain',
            automargin=True
        ),
        font=dict(color="#fff"),
    )
    return fig

def create_horizontal_bar_chart(categories, values, config, text=None):
    fig = go.Figure()
    for cat, val, color in zip(categories, values, config["bar_colors"]):
        # Set hover text color: black for yellow, white otherwise
        hover_font_color = 'black' if color.lower() in ['#ffff00', 'yellow', 'rgb(255,255,0)'] else 'white'
        fig.add_trace(go.Bar(
            y=[cat],
            x=[val],
            orientation='h',
            marker=dict(color=color, line=dict(color='rgba(255,255,255,0.3)', width=1)),
            text=[f"${val:,.2f}" if config["y_title"] == "Cost ($)" else f'{val}'],
            textposition='outside',
            textfont=dict(color='white', size=13, family='Arial Black'),
            showlegend=False,
            name=cat,
            hovertemplate=f"<b>{cat}</b><br>Cost: ${val:,.2f}<extra></extra>",
            hoverlabel=dict(bgcolor=color, font=dict(color=hover_font_color))
        ))
    fig.update_layout(
        height=config["height"],
        margin=config["margin"],
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            visible=True,
            color='#666',
            title=config["y_title"],
            range=[0, max(values)*1.25],
            constrain='domain',
            automargin=True
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            visible=True,
            color='#666',
            tickfont=dict(color='#fff'),
            categoryorder='array',
            categoryarray=categories[::-1]
        ),
        font=dict(color='#fff'),
    )
    return fig

def create_gauge_chart(title, config):
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=config["value"],
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 13, 'color': '#A0AEC0'}},
        delta={'reference': config["reference"], 'increasing': {'color': "#00FF88"}, 'font': {'size': 12}},
        number={'font': {'size': 16, 'color': config["number_color"]}},  # Reduced font size
        gauge={
            'axis': {'range': [None, 100], 'tickcolor': '#A0AEC0', 'tickwidth': 2},
            'bar': {'color': config["bar_color"], 'thickness': 0.8},
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 3,
            'bordercolor': "rgba(255,255,255,0.3)",
            'steps': config["steps"],
            'threshold': {
                'line': {'color': "white", 'width': 6},
                'thickness': 0.8,
                'value': config["threshold"]
            }
        }
    ))
    fig.update_layout(
        title="",
        font={'color': "#A0AEC0"},
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def create_chart_for_kpi(kpi_title, chart_data, trend_type):
    if kpi_title == "Revenue Growth":
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
        config = CHART_CONFIG["revenue_growth"]
        text = [f"${v:,.0f}" for v in chart_data]
        return create_line_chart(months[:len(chart_data)], chart_data, config, text)
    if kpi_title == "Cash Flow":
        quarters = ['Q1', 'Q2', 'Q3', 'Q4']
        values = [350000, 420000, 390000, 480000]
        config = CHART_CONFIG["cash_flow"]
        text = [f'${v//1000}K' for v in values]
        return create_bar_chart(quarters, values, config, text)
    if kpi_title == "Cost per Call":
        categories = ['Labor', 'Tech', 'Training', 'Overhead', 'Other']
        costs = [1.20, 0.45, 0.25, 0.35, 0.20]
        config = CHART_CONFIG["cost_per_call"]
        return create_horizontal_bar_chart(categories, costs, config)
    if kpi_title == "Performance Index":
        categories = ['Quality', 'Speed', 'Satisfaction', 'Efficiency', 'Cost Control']
        values = [8.5, 8.8, 9.2, 8.4, 8.9]
        config = CHART_CONFIG["performance_index"]
        return create_horizontal_bar_chart(categories, values, config)
    if kpi_title == "Efficiency Rate":
        config = CHART_CONFIG["efficiency_rate"]
        return create_gauge_chart("Efficiency Rate", config)
    if kpi_title == "Customer Retention":
        config = CHART_CONFIG["customer_retention"]
        return create_gauge_chart("Customer Retention", config)
def create_kpi_card(title, value, trend, trend_type, chart_data, card_id):
    """Create a premium KPI card with integrated chart"""
    # Create appropriate chart based on KPI type
    fig = create_chart_for_kpi(title, chart_data, trend_type)
    trend_class = f"trend-{trend_type}"
    trend_icon = "↗" if trend_type == 'positive' else "↘" if trend_type == 'negative' else "→"
    return html.Div([
        html.Div([
            # Compact header section - all text elements at top
            html.Div([
                html.Div([
                    html.P(title, className="kpi-title"),
                    html.H2(value, className="kpi-metric"),
                ], style={"flex": "1"}),
                html.Button("More Details", className="more-details-btn", id=f"btn-{card_id}")
            ], style={"display": "flex", "justifyContent": "space-between", "alignItems": "flex-start", "marginBottom": "1px"}),
            # Trend indicator
            html.Div([
                html.Span(trend_icon, style={"fontSize": "0.6rem", "marginRight": "3px"}),
                html.Span(trend)
            ], className=f"kpi-trend {trend_class}", style={"marginBottom": "2px"}),
            # Chart section - takes all remaining space
            html.Div([
                dcc.Graph(
                    figure=fig,
                    config={
                        'displayModeBar': False,
                        'displaylogo': False,
                        'responsive': True
                    },
                    style={"height": "100%", "width": "100%", "display": "block"}
                )
            ], className="chart-container", style={"position": "relative", "overflow": "hidden", "height": "100%"})
        ], className="kpi-card-content")
    ], className="premium-card grid-item")

def create_alert_card():
    """Create a styled alert card for dashboard grid with smaller font size."""
    alerts = [
        {"severity": "critical", "message": "Queue 3 SLA breach: 15min avg wait time"},
        {"severity": "warning", "message": "Agent utilization at 95% - consider overflow"},
        {"severity": "info", "message": "System maintenance scheduled 2AM-4AM tonight"}
    ]
    return html.Div([
        html.H3("Alerts", className="alert-title", style={"fontSize": "1.1rem", "marginBottom": "12px"}),
        html.Ul([
            html.Li([
                html.Span("⚠️", style={"marginRight": "8px", "fontSize": "0.9rem"}),
                html.Span(alert["message"], className=f"alert-{alert['severity']}", style={"fontSize": "0.85rem"})
            ], style={"marginBottom": "6px"}) for alert in alerts
        ], className="alert-list", style={"paddingLeft": "0", "listStyle": "none"})
    ], className="alert-card", style={
        "background": "rgba(255,255,255,0.08)",
        "borderRadius": "18px",
        "padding": "16px",
        "boxShadow": "0 2px 16px rgba(0,0,0,0.08)",
        "height": "100%"
    })

# Get dummy data after all functions are defined
data = get_executive_data()

executive_dashboard_layout = html.Div([
    # Dashboard Grid using CSS Grid
    html.Div([
        # First row: 3 KPI
        html.Div(create_kpi_card("Revenue Growth", "$1.2M", "+8.5%", "positive", data["revenue_growth"], "revenue-chart"), className="kpi-card"),
        html.Div(create_kpi_card("Cost per Call", "$2.45", "-12%", "positive", data["cost_per_call"], "cost-chart"), className="kpi-card"),
        html.Div(create_kpi_card("Cash Flow", "$890K", "+15.2%", "positive", [350000, 420000, 390000, 480000], "kpi-card cash-chart"), className="kpi-card"),
        # Second row: 3 KPI
        html.Div(create_kpi_card("Efficiency Rate", "94.2%", "+3.1%", "positive", data["efficiency"], "efficiency-chart"), className="kpi-card"),
        html.Div(create_kpi_card("Customer Retention", "96.8%", "+2.4%", "positive", [96.8], "retention-chart"), className="kpi-card"),
        html.Div(create_kpi_card("Performance Index", "8.7/10", "+0.5", "positive", [8.5, 8.8, 9.2, 8.4, 8.9], "summary-chart"), className="kpi-card"),
        # Third row: 1/3 alert card, 2/3 wide orange border card
        html.Div(create_alert_card(), className="alert-card"),
        html.Div([], className="wide-card orange-border"),
    ], className="dashboard-grid"),
], style={
    "height": "100%",  # Use full content area height
    "display": "flex",
    "flexDirection": "column",
    "overflow": "hidden",
    "padding": "5px 10px 0 10px",  # 5px top padding, 10px left/right, 0 bottom
    "boxSizing": "border-box"
})
