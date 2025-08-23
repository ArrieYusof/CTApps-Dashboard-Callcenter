# Version: 0.1
# Last Modified: 2025-08-22
# Changes: Executive KPI card wireframe (dummy data)
"""
Executive KPI card components for VADS Call Center Dashboard
All dummy data below must be replaced with live DB data in production.
"""
from dash import html

executive_kpi_cards = [
    html.Div([
        html.Div([
            html.H4("Revenue Growth", className="text-white"),
            html.P("$1.2M (dummy)", className="text-success"),
        ], className="card-body"),
    ], className="card bg-dark m-2 col"),
    html.Div([
        html.Div([
            html.H4("Cost per Call", className="text-white"),
            html.P("$2.50 (dummy)", className="text-warning"),
        ], className="card-body"),
    ], className="card bg-dark m-2 col"),
    html.Div([
        html.Div([
            html.H4("Cash Flow Impact", className="text-white"),
            html.P("+$300K (dummy)", className="text-info"),
        ], className="card-body"),
    ], className="card bg-dark m-2 col"),
    html.Div([
        html.Div([
            html.H4("Operational Efficiency", className="text-white"),
            html.P("92% (dummy)", className="text-primary"),
        ], className="card-body"),
    ], className="card bg-dark m-2 col"),
    html.Div([
        html.Div([
            html.H4("Customer Retention & Churn", className="text-white"),
            html.P("Retention: 88% | Churn: 12% (dummy)", className="text-danger"),
        ], className="card-body"),
    ], className="card bg-dark m-2 col"),
    html.Div([
        html.Div([
            html.H4("Summary/Quick Links", className="text-white"),
            html.P("See more details (dummy)", className="text-secondary"),
        ], className="card-body"),
    ], className="card bg-dark m-2 col"),
]
