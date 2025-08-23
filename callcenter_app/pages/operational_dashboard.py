# Version: 0.2
# Last Modified: 2025-08-23
# Changes: Premium pixel-perfect operational dashboard with glass-morphism design
"""
Operational Dashboard layout for VADS Cal    ], style={
        "padding": "20px",
        "width": "100%",
        "minHeight": "1080px",
        "background": "var(--primary-bg)",
        "margin": "0 auto",
        "boxSizing": "border-box"
    })ixed 1920x1080 resolution with premium visual design for real-time operations
"""
from dash import html, dcc
import plotly.graph_objs as go
from data.operational_dummy_data import get_operational_data
from data.operational_dummy_data import get_agent_availability

def create_operational_kpi_card(title, value, status, chart_data, card_id):
    """Create a premium operational KPI card with status indicator"""
    
    # Select chart type for wow factor and clarity
    if card_id == "queue":
        # Visually striking 2D Bar Chart for queue status
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=["Queue 1", "Queue 2", "Queue 3"],
            y=chart_data,
            marker=dict(
                color=['#00D4FF', '#FFB800', '#FF3366'],
                line=dict(color='#23263A', width=4),
                opacity=0.95
            ),
            text=chart_data,
            textposition="outside"
        ))
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title=None, showgrid=False, showticklabels=True, zeroline=False, color="#fff"),
            yaxis=dict(title="Calls", showgrid=False, showticklabels=True, zeroline=False, color="#fff"),
            showlegend=False,
            bargap=0.35,
            bargroupgap=0.15,
            font=dict(size=14, color="#fff")
        )
    elif card_id == "agents":
        # Animated Line Chart for agent performance, x-axis shows agent names
        x_vals = [f"Agent {i+1}" for i in range(len(chart_data))]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=chart_data,
            mode='lines+markers',
            line=dict(color='#00FF88', width=4, dash='solid'),
            marker=dict(size=12, color='#00FF88', symbol='circle-open-dot'),
            hoverinfo="x+y"
        ))
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, showticklabels=True, zeroline=False, color="#fff", tickmode='array', tickvals=list(range(len(x_vals))), ticktext=x_vals),
            yaxis=dict(showgrid=False, showticklabels=True, zeroline=False, color="#fff"),
            showlegend=False
        )
    elif card_id == "csat":
        # Donut Chart for Customer Satisfaction
        fig = go.Figure(go.Pie(
            labels=["Excellent", "Good", "Average", "Poor"],
            values=chart_data,
            hole=0.55,
            marker=dict(colors=["#00FF88", "#00D4FF", "#FFB800", "#FF3366"]),
            textinfo="label+percent",
            textfont=dict(color="#fff", size=12),
            hoverinfo="label+percent+value"
        ))
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
    elif card_id == "sla":
        # Radial Gauge for SLA Monitoring, no axis labels
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=chart_data[0],
            delta={"reference": 90, "increasing": {"color": "#FF3366"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#fff", "showticklabels": False},
                "bar": {"color": "#FFB800"},
                "steps": [
                    {"range": [0, 80], "color": "rgba(255,51,102,0.3)"},
                    {"range": [80, 90], "color": "rgba(255,184,0,0.3)"},
                    {"range": [90, 100], "color": "rgba(0,255,136,0.3)"}
                ],
                "threshold": {"line": {"color": "#FF3366", "width": 4}, "thickness": 0.75, "value": 90}
            },
            number={"suffix": "%"},
            domain={"x": [0, 1], "y": [0, 1]}
        ))
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
    elif card_id == "resources":
        # Gradient Horizontal Bar for Resource Utilization
        fig = go.Figure(go.Bar(
            x=[chart_data[0]],
            y=["Active"],
            orientation="h",
            marker=dict(
                color="rgba(0,212,255,0.8)",
                line=dict(color="#FFB800", width=3)
            ),
            text=[f"{chart_data[0]}%"],
            textposition="auto"
        ))
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(range=[0, 100], showgrid=False, showticklabels=True, zeroline=False, color="#fff"),
            yaxis=dict(showgrid=False, showticklabels=True, zeroline=False, color="#fff"),
            showlegend=False
        )
    elif card_id == "outcomes":
        # Stacked Bar for Call Outcomes
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=["Resolved", "Unresolved"],
            y=chart_data,
            marker_color=["#00FF88", "#FF3366"],
            text=chart_data,
            textposition="auto",
            textfont=dict(color=["#fff", "#fff"])
        ))
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(title="Outcome", showgrid=False, showticklabels=True, zeroline=False, color="#fff"),
            yaxis=dict(title="Count", showgrid=False, showticklabels=True, zeroline=False, color="#fff"),
            showlegend=False
        )
    elif card_id == "agents_wide":
        # Vertical Bar Chart for Agent Performance, sorted by handle time
        agent_names = [f"Agent {i+1}" for i in range(len(chart_data))]
        sorted_agents = sorted(zip(agent_names, chart_data), key=lambda x: x[1])
        sorted_names = [a[0] for a in sorted_agents]
        sorted_times = [a[1] for a in sorted_agents]
        # Color bands: green for <=3.8, amber for <=4.2, red for >4.2
        bar_colors = ["#00FF88" if t <= 3.8 else "#FFB800" if t <= 4.2 else "#FF3366" for t in sorted_times]
        # Show only every 3rd agent label on x-axis
        x_tickvals = [sorted_names[i] for i in range(len(sorted_names)) if i % 3 == 0]
        fig = go.Figure(go.Bar(
            x=sorted_names,
            y=sorted_times,
            marker=dict(color=bar_colors, line=dict(color="#23263A", width=2)),
            text=[f"{t:.2f} min" for t in sorted_times],
            textposition="auto",
            textfont=dict(color="#fff"),
            hovertemplate="<b>%{x}</b><br>Handle Time: %{y:.2f} min<extra></extra>"
        ))
        fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, showticklabels=True, zeroline=False, color="#fff", tickvals=x_tickvals, ticktext=x_tickvals),
            yaxis=dict(title="Avg Handle Time (min)", showgrid=False, showticklabels=True, zeroline=False, color="#fff"),
            showlegend=False
        )
    else:
        # Default sparkline
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(len(chart_data))),
            y=chart_data,
            mode='lines+markers',
            line=dict(color='#00D4FF', width=3),
            marker=dict(size=6)
        ))
        fig.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            showlegend=False
        )
    
    status_class = f"trend-{status}"
    status_icon = "🟢" if status == 'positive' else "🔴" if status == 'negative' else "🟡"
    
    return html.Div([
        html.Div([
            # Compact header section - all text elements at top
            html.Div([
                html.Div([
                    html.P(title, className="kpi-title"),
                    html.H2(value, className="kpi-metric"),
                ], style={"flex": "1"}),
                html.Button("View Details", className="more-details-btn", id=f"btn-{card_id}")
            ], style={"display": "flex", "justifyContent": "space-between", "alignItems": "flex-start", "marginBottom": "1px"}),
            
            # Trend indicator
            html.Div([
                html.Span(status_icon, style={"fontSize": "0.6rem", "marginRight": "3px"}),
                html.Span("LIVE" if status == 'positive' else "ALERT" if status == 'negative' else "WATCH")
            ], className=f"kpi-trend {status_class}", style={"marginBottom": "2px"}),
            
            # Chart section - takes all remaining space
            html.Div([
                dcc.Graph(
                    figure=fig,
                    config={'displayModeBar': False, 'staticPlot': False},
                    style={"height": "100%", "width": "100%"}
                )
            ], className="chart-container")
            
        ], className="kpi-card-content")
    ], className="premium-card grid-item")

def create_agent_availability_card():
    availability = get_agent_availability()
    labels = list(availability.keys())
    values = list(availability.values())
    colors = ["#00FF88", "#FFB800", "#3388FF"]
    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=colors, line=dict(color="#23263A", width=2)),
        textinfo="label+percent",
        textfont=dict(color="#fff", size=16),
        hoverinfo="label+value",
        showlegend=False
    ))
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return html.Div([
        html.P("Agent Availability", className="kpi-title"),
        dcc.Graph(figure=fig, config={"displayModeBar": False}, className="kpi-chart"),
    ], className="kpi-card")

# Get operational dummy data
data = get_operational_data()

operational_dashboard_layout = html.Div([
    html.Div([
        # Header
        html.Div([
            html.Div([
                html.Button([
                    html.Div(className="hamburger-line"),
                    html.Div(className="hamburger-line"),
                    html.Div(className="hamburger-line"),
                ], id="sidebar-toggle", className="hamburger-btn"),
                html.H1("Operational Dashboard", className="header-title"),
            ], style={"display": "flex", "alignItems": "center", "gap": "24px"}),
            html.Div([
                html.Span("LIVE MONITORING", style={
                    "fontSize": "0.9rem", 
                    "color": "var(--accent-green)",
                    "fontWeight": "600",
                    "animation": "blink 2s infinite"
                })
            ])
        ], className="dashboard-header"),
        
        # Operational KPI Grid
        html.Div([
            # First row: 3 KPI
            create_operational_kpi_card(
                "Real-Time Queue Status", 
                "47 calls", 
                "negative",  # High queue = negative
                data["queue_status"],
                "queue"
            ),
            create_agent_availability_card(),
            create_operational_kpi_card(
                "SLA Monitoring", 
                "78.5%", 
                "negative",  # Below target = negative
                data["sla_monitoring"],
                "sla"
            ),
            # Second row: 2 KPI (remove Agent Performance from here)
            create_operational_kpi_card(
                "Customer Satisfaction", 
                "4.1/5.0", 
                "positive",
                data["customer_satisfaction"],
                "csat"
            ),
            create_operational_kpi_card(
                "Call Outcomes", 
                f"{data['call_outcomes'][-1]}% resolved", 
                "positive",
                [data['call_outcomes'][-1], 100 - data['call_outcomes'][-1]],
                "outcomes"
            ),
            create_operational_kpi_card(
                "Resource Utilization", 
                f"{data['resource_utilization'][-1]}% active", 
                "neutral",  # High but manageable
                [data['resource_utilization'][-1]],
                "resources"
            ),
            # Third row: 1/3 alert card, 2/3 wide orange border card
            html.Div([
                html.H3("Operational Alerts", className="alert-title", style={"fontSize": "1.1rem", "marginBottom": "12px"}),
                html.Ul([
                    html.Li([
                        html.Span("🚨", style={"marginRight": "8px", "fontSize": "0.9rem"}),
                        html.Span("Queue 2 SLA BREACH: 18min wait time", className="alert-critical", style={"fontSize": "0.85rem"})
                    ], style={"marginBottom": "6px"}),
                    html.Li([
                        html.Span("⚠️", style={"marginRight": "8px", "fontSize": "0.9rem"}),
                        html.Span("3 agents offline - backup needed", className="alert-warning", style={"fontSize": "0.85rem"})
                    ], style={"marginBottom": "6px"}),
                    html.Li([
                        html.Span("ℹ️", style={"marginRight": "8px", "fontSize": "0.9rem"}),
                        html.Span("System response time degraded to 2.3s", className="alert-info", style={"fontSize": "0.85rem"})
                    ], style={"marginBottom": "6px"})
                ], className="alert-list", style={"paddingLeft": "0", "listStyle": "none"})
            ], className="alert-card"),
            html.Div([
                create_operational_kpi_card(
                    "Agent Performance", 
                    f"avg {sum(data['agent_performance'])/len(data['agent_performance']):.1f}min", 
                    "positive",
                    data["agent_performance"],
                    "agents_wide"
                )
            ], className="wide-card orange-border"),
        ], className="dashboard-grid"),
    ], style={
        "height": "100vh",
        "display": "flex",
        "flexDirection": "column",
        "overflow": "hidden"
    })
], className="dashboard-container")
