# Version: 0.1
# Last Modified: 2025-08-22
# Changes: Executive chart wireframe (dummy data)
"""
Executive chart components for VADS Call Center Dashboard
All dummy data below must be replaced with live DB data in production.
"""
from dash import dcc, html
import plotly.graph_objs as go

executive_charts = [
    dcc.Graph(
        id='revenue-growth-chart',
        figure=go.Figure({
            'data': [go.Bar(x=['Q1', 'Q2', 'Q3', 'Q4'], y=[300, 400, 250, 250], name='Revenue')],
            'layout': go.Layout(
                title={'text': 'Revenue Growth', 'font': {'size': 10}}, 
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': 'white', 'size': 8},
                margin={'l': 20, 'r': 20, 't': 25, 'b': 20},
                height=None,
                xaxis={'tickfont': {'size': 8}},
                yaxis={'tickfont': {'size': 8}}
            )
        }),
        config={'displayModeBar': False}
    ),
    dcc.Graph(
        id='cost-per-call-chart',
        figure=go.Figure({
            'data': [go.Bar(x=['Jan', 'Feb', 'Mar'], y=[2.5, 2.7, 2.4], name='Cost/Call')],
            'layout': go.Layout(
                title={'text': 'Cost per Call', 'font': {'size': 10}}, 
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': 'white', 'size': 8},
                margin={'l': 20, 'r': 20, 't': 25, 'b': 20},
                height=None,
                xaxis={'tickfont': {'size': 8}},
                yaxis={'tickfont': {'size': 8}}
            )
        }),
        config={'displayModeBar': False}
    ),
    dcc.Graph(
        id='cash-flow-impact-chart',
        figure=go.Figure({
            'data': [go.Surface(z=[[100, 120, 80], [90, 110, 70], [80, 100, 60]])],
            'layout': go.Layout(
                title={'text': 'Cash Flow Impact', 'font': {'size': 10}}, 
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': 'white', 'size': 8},
                margin={'l': 10, 'r': 10, 't': 25, 'b': 10},
                height=None
            )
        }),
        config={'displayModeBar': False}
    ),
    dcc.Graph(
        id='operational-efficiency-chart',
        figure=go.Figure({
            'data': [go.Indicator(mode="gauge+number", value=92, title={"text": "Efficiency"})],
            'layout': go.Layout(
                title={'text': 'Operational Efficiency', 'font': {'size': 10}}, 
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': 'white', 'size': 8},
                margin={'l': 10, 'r': 10, 't': 25, 'b': 10},
                height=None
            )
        }),
        config={'displayModeBar': False}
    ),
    dcc.Graph(
        id='customer-retention-chart',
        figure=go.Figure({
            'data': [go.Scatter3d(x=[2023, 2024, 2025], y=[0, 0, 0], z=[85, 87, 88], mode='lines+markers', name='Retention')],
            'layout': go.Layout(
                title={'text': 'Customer Retention', 'font': {'size': 10}}, 
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': 'white', 'size': 8},
                margin={'l': 10, 'r': 10, 't': 25, 'b': 10},
                height=None
            )
        }),
        config={'displayModeBar': False}
    ),
    dcc.Graph(
        id='summary-quick-links-chart',
        figure=go.Figure({
            'data': [go.Pie(labels=['A', 'B', 'C'], values=[30, 50, 20], hole=0.3)],
            'layout': go.Layout(
                title={'text': 'Summary/Quick Links', 'font': {'size': 10}}, 
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': 'white', 'size': 8},
                margin={'l': 10, 'r': 10, 't': 25, 'b': 10},
                height=None
            )
        }),
        config={'displayModeBar': False}
    ),
]
