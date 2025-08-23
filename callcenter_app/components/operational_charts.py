# Version: 0.1
# Last Modified: 2025-08-22
# Changes: Operational chart wireframe (dummy data)
"""
Operational chart components for VADS Call Center Dashboard
All dummy data below must be replaced with live DB data in production.
"""
from dash import dcc, html
import plotly.graph_objs as go

operational_charts = [
    dcc.Graph(
        id='queue-status-chart',
        figure=go.Figure({
            'data': [go.Bar(x=['Queue 1', 'Queue 2', 'Queue 3'], y=[12, 8, 5], name='Waiting')],
            'layout': go.Layout(
                title={'text': 'Queue Status', 'font': {'size': 10}}, 
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
        id='agent-performance-chart',
        figure=go.Figure({
            'data': [go.Bar(x=['Agent A', 'Agent B', 'Agent C'], y=[40, 35, 45], name='Handled')],
            'layout': go.Layout(
                title={'text': 'Agent Performance', 'font': {'size': 10}}, 
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
        id='sla-monitoring-chart',
        figure=go.Figure({
            'data': [go.Scatter3d(x=[1, 2, 3], y=[0, 0, 0], z=[98, 97, 96], mode='lines+markers', name='SLA')],
            'layout': go.Layout(
                title={'text': 'SLA Monitoring', 'font': {'size': 10}}, 
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
        id='customer-satisfaction-chart',
        figure=go.Figure({
            'data': [go.Bar(x=['CSAT', 'Complaints', 'NPS'], y=[4.6, 2, 72], name='Satisfaction')],
            'layout': go.Layout(
                title={'text': 'Customer Satisfaction', 'font': {'size': 10}}, 
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
        id='call-outcomes-quality-chart',
        figure=go.Figure({
            'data': [go.Pie(labels=['Resolved', 'Escalated', 'Error'], values=[110, 8, 2], hole=0.3)],
            'layout': go.Layout(
                title={'text': 'Call Outcomes & Quality', 'font': {'size': 10}}, 
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
        id='resource-utilization-chart',
        figure=go.Figure({
            'data': [go.Bar(x=['Staffing', 'Overtime'], y=[95, 2], name='Utilization')],
            'layout': go.Layout(
                title={'text': 'Resource Utilization', 'font': {'size': 10}}, 
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
]
