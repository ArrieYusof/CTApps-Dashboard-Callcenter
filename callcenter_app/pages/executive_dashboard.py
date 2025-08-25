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
        # Format text as millions since data is in thousands (1000 = $1.0M)
        text = [f"${v/1000:.1f}M" for v in chart_data]
        return create_line_chart(months[:len(chart_data)], chart_data, config, text)
    if kpi_title == "Cash Flow":
        quarters = ['Q1', 'Q2', 'Q3', 'Q4']
        # Use the provided chart_data, but take only the first 4 values for quarterly display
        values = [v * 1000 for v in chart_data[:4]]  # Convert from thousands to actual values
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
                html.Button("AI Analysis", className="ai-analysis-btn", id={"type": "ai-analysis-btn", "index": card_id})
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
    ], className="kpi-card")

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

def create_sparkline_chart(title, data, current_value, trend_direction, color):
    """Create a compact sparkline chart for leading indicators."""
    fig = go.Figure()
    
    # Convert hex color to rgba with transparency
    if color.startswith('#'):
        # Convert hex to rgba
        r, g, b = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        fill_color = f'rgba({r}, {g}, {b}, 0.2)'
    else:
        fill_color = 'rgba(0, 212, 255, 0.2)'  # Default fallback
    
    # Add sparkline
    fig.add_trace(go.Scatter(
        x=list(range(len(data))),
        y=data,
        mode='lines',
        line=dict(color=color, width=2),
        fill='tonexty',
        fillcolor=fill_color,
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Configure layout for compact sparkline
    fig.update_layout(
        height=60,
        margin=dict(t=1, b=1, l=1, r=1),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False, showgrid=False),
        yaxis=dict(visible=False, showgrid=False),
        showlegend=False
    )
    
    return fig

def create_sparkline_bar_chart(title, data, current_value, trend_direction, color):
    """Create a compact bar chart for call volume data."""
    fig = go.Figure()
    
    # Convert hex color to rgba with transparency
    if color.startswith('#'):
        r, g, b = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        fill_color = f'rgba({r}, {g}, {b}, 0.3)'
    else:
        fill_color = 'rgba(255, 184, 0, 0.3)'  # Default fallback
    
    # Add bar chart
    fig.add_trace(go.Bar(
        x=['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],  # Last 5 days
        y=data,
        marker_color=color,
        marker_line_color=color,
        marker_line_width=1,
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Configure layout for compact bar chart
    fig.update_layout(
        height=60,
        margin=dict(t=1, b=15, l=1, r=1),  # More bottom margin for day labels
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            visible=True, 
            showgrid=False, 
            showticklabels=True,
            tickfont=dict(size=8, color='white'),
            tickangle=0
        ),
        yaxis=dict(visible=False, showgrid=False),
        showlegend=False
    )
    
    return fig

def create_sparkline_gauge_chart(title, value, max_value, trend_direction, color):
    """Create a compact gauge chart for executive performance indicators."""
    fig = go.Figure()
    
    # Determine gauge color based on value
    if value >= 85:
        gauge_color = "#00FF88"  # Green - Excellent
        bar_color = "#00FF88"
    elif value >= 70:
        gauge_color = "#FFB800"  # Yellow - Good
        bar_color = "#FFB800"
    else:
        gauge_color = "#FF6B6B"  # Red - Needs Attention
        bar_color = "#FF6B6B"
    
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "", 'font': {'size': 10, 'color': 'white'}},
        number={'font': {'size': 14, 'color': gauge_color}},  # Reduced number font size
        gauge={
            'axis': {
                'range': [None, max_value],
                'tickwidth': 1,
                'tickcolor': "white",
                'tickfont': {'size': 7, 'color': 'white'}  # Smaller tick font
            },
            'bar': {'color': bar_color, 'thickness': 0.25},  # Thinner bar
            'bgcolor': "rgba(255,255,255,0.1)",
            'borderwidth': 1,
            'bordercolor': "rgba(255,255,255,0.3)",
            'steps': [
                {'range': [0, 70], 'color': 'rgba(255, 107, 107, 0.3)'},  # Red zone
                {'range': [70, 85], 'color': 'rgba(255, 184, 0, 0.3)'},   # Yellow zone
                {'range': [85, max_value], 'color': 'rgba(0, 255, 136, 0.3)'}  # Green zone
            ],
            'threshold': {
                'line': {'color': "white", 'width': 1},  # Thinner threshold line
                'thickness': 0.6,  # Smaller threshold indicator
                'value': 85  # Excellence threshold
            }
        }
    ))
    
    fig.update_layout(
        height=45,  # Reduced from 50 to 45px
        margin=dict(t=5, b=2, l=5, r=5),  # Added 5px top padding for labels
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "white", 'size': 8}  # Smaller font size
    )
    
    return fig

def create_sparkline_panel():
    """Create leading indicators sparkline panel."""
    # Sample data for leading indicators
    sparkline_data = {
        "performance_index": {
            "title": "Performance Index",
            "data": [87],  # Single value for gauge
            "current": "87/100",
            "trend": "up",
            "color": "#00FF88",
            "chart_type": "gauge",  # Special flag for gauge chart
            "max_value": 100
        },
        "employee_satisfaction": {
            "title": "Customer Satisfaction",
            "data": [7.8, 7.9, 7.7, 8.1, 8.3, 8.2, 8.4, 8.6, 8.5, 8.7, 8.8, 8.9],
            "current": "8.9/10",
            "trend": "up",
            "color": "#00D4FF"
        },
        "call_volume": {
            "title": "Call Volume (5 Days)",
            "data": [2840, 3120, 2950, 3280, 3450],  # Last 5 days call counts
            "current": "3,450",
            "trend": "up",
            "color": "#FFB800",
            "chart_type": "bar"  # Special flag for bar chart
        },
        "compliance_score": {
            "title": "Compliance Score",
            "data": [94, 95, 93, 96, 97, 95, 98, 96, 97, 98, 99, 98],
            "current": "98%",
            "trend": "stable",
            "color": "#A78BFA"
        }
    }
    
    sparkline_cards = []
    for key, metric in sparkline_data.items():
        trend_icon = "↗" if metric["trend"] == "up" else "→" if metric["trend"] == "stable" else "↘"
        trend_color = "#00FF88" if metric["trend"] == "up" else "#FFB800" if metric["trend"] == "stable" else "#FF6B6B"
        
        card = html.Div([
            html.Div([
                html.Div([
                    html.H4(metric["title"], style={
                        "fontSize": "0.7rem", 
                        "margin": "0", 
                        "color": "#ffffff", 
                        "fontWeight": "500",
                        "lineHeight": "1",
                        "flex": "1"
                    }),
                    html.Div([
                        html.Span(metric["current"], style={
                            "fontSize": "0.85rem", 
                            "fontWeight": "bold", 
                            "color": metric["color"],
                            "marginRight": "4px"
                        }),
                        html.Span(trend_icon, style={
                            "fontSize": "0.8rem", 
                            "color": trend_color
                        })
                    ], style={"display": "flex", "alignItems": "center"})
                ], style={
                    "display": "flex", 
                    "alignItems": "center", 
                    "justifyContent": "space-between",
                    "marginBottom": "4px"
                }),
                dcc.Graph(
                    figure=create_sparkline_bar_chart(
                        metric["title"], 
                        metric["data"], 
                        metric["current"], 
                        metric["trend"], 
                        metric["color"]
                    ) if metric.get("chart_type") == "bar" else create_sparkline_gauge_chart(
                        metric["title"],
                        metric["data"][0],  # First value for gauge
                        metric.get("max_value", 100),
                        metric["trend"],
                        metric["color"]
                    ) if metric.get("chart_type") == "gauge" else create_sparkline_chart(
                        metric["title"], 
                        metric["data"], 
                        metric["current"], 
                        metric["trend"], 
                        metric["color"]
                    ),
                    config={'displayModeBar': False},
                    style={"height": "45px", "flex": "1"}  # Reduced height for gauge
                )
            ], style={"height": "100%", "display": "flex", "flexDirection": "column"})
        ], style={
            "background": "rgba(255,255,255,0.08)",
            "borderRadius": "8px",
            "padding": "4px",
            "border": f"1px solid {metric['color']}33",
            "height": "100%",
            "display": "flex",
            "flexDirection": "column",
            "minHeight": "0"
        })
        sparkline_cards.append(card)
    
    return html.Div([
        html.H3("Leading Indicators", style={
            "fontSize": "0.9rem", 
            "margin": "0 0 8px 0", 
            "color": "#ffffff",
            "fontWeight": "600",
            "lineHeight": "1"
        }),
        html.Div(sparkline_cards, style={
            "display": "grid",
            "gridTemplateColumns": "1fr 1fr 1fr 1fr",  # 4 columns in one row
            "gridTemplateRows": "1fr",  # Single row
            "gap": "6px",
            "height": "calc(100% - 24px)"
        })
    ], style={
        "height": "100%",
        "padding": "8px",
        "overflow": "hidden",
        "boxSizing": "border-box"
    })

# Get dummy data after all functions are defined
data = get_executive_data()

executive_dashboard_layout = html.Div([
    # Dashboard Grid using CSS Grid
    html.Div([
        # First row: 3 KPI
        create_kpi_card("Revenue Growth", f"${data['revenue_growth'][-1]/1000:.1f}M", "+12%", "positive", data["revenue_growth"], "revenue-chart"),
        create_kpi_card("Cost per Call", "$2.45", "-12%", "positive", data["cost_per_call"], "cost-chart"),
        create_kpi_card("Cash Flow", f"${data['cash_flow'][3]}K", "+2.3%", "positive", data["cash_flow"], "cash-chart"),
        # Second row: 3 KPI
        create_kpi_card("Efficiency Rate", "94.2%", "+3.1%", "positive", data["efficiency"], "efficiency-chart"),
        create_kpi_card("Customer Retention", "96.8%", "+2.4%", "positive", [96.8], "retention-chart"),
        create_kpi_card("Performance Index", "8.7/10", "+0.5", "positive", [8.5, 8.8, 9.2, 8.4, 8.9], "summary-chart"),
        # Third row: 1/3 alert card, 2/3 leading indicators sparklines
        html.Div(create_alert_card(), className="alert-card"),
        html.Div(create_sparkline_panel(), className="wide-card orange-border"),
    ], className="dashboard-grid"),
], style={
    "height": "calc(100vh - 35px)",  # Match exact header height from app.py
    "display": "flex",
    "flexDirection": "column",
    "overflow": "hidden",
    "padding": "0",  # No padding to use full space
    "boxSizing": "border-box"
})
