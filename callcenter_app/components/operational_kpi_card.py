# Version: 0.1
# Last Modified: 2025-08-22
# Changes: Operational KPI card wireframe (dummy data)
"""
Operational KPI card components for VADS Call Center Dashboard
All dummy data below must be replaced with live DB data in production.
"""
from dash import html

operational_kpi_cards = [
    html.Div([
        html.Div([
            html.H4("Queue Status", className="text-white"),
            html.P("Waiting: 12 | Avg Wait: 2m | Longest: 8m (dummy)", className="text-warning"),
        ], className="card-body"),
    ], className="card bg-dark m-2 col"),
    html.Div([
        html.Div([
            html.H4("Agent Performance", className="text-white"),
            html.P("Handled: 120 | Avg Time: 4m | FCR: 85% (dummy)", className="text-success"),
        ], className="card-body"),
    ], className="card bg-dark m-2 col"),
    html.Div([
        html.Div([
            html.H4("SLA Monitoring", className="text-white"),
            html.P("SLA: 97% | Breaches: 3 (dummy)", className="text-info"),
        ], className="card-body"),
    ], className="card bg-dark m-2 col"),
    html.Div([
        html.Div([
            html.H4("Customer Satisfaction", className="text-white"),
            html.P("CSAT: 4.6 | Complaints: 2 | NPS: 72 (dummy)", className="text-primary"),
        ], className="card-body"),
    ], className="card bg-dark m-2 col"),
    html.Div([
        html.Div([
            html.H4("Call Outcomes & Quality", className="text-white"),
            html.P("Resolved: 110 | Escalated: 8 | Error: 2 (dummy)", className="text-danger"),
        ], className="card-body"),
    ], className="card bg-dark m-2 col"),
    html.Div([
        html.Div([
            html.H4("Resource Utilization", className="text-white"),
            html.P("Staffing: 95% | Overtime: 2h (dummy)", className="text-secondary"),
        ], className="card-body"),
    ], className="card bg-dark m-2 col"),
]
