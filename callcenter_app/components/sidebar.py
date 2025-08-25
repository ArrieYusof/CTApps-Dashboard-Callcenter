# Version: 0.6
# Last Modified: 2025-08-25  
# Changes: Added AI Assistant navigation link
"""
Sidebar navigation component with burger menu for VADS Call Center Dashboard
"""
import dash_bootstrap_components as dbc
from dash import html

def get_sidebar(hidden=True):
    return html.Div([
        html.Div([
            dbc.Nav([
                dbc.NavLink("Executive Dashboard", href="#", id="nav-exec", active=True, className="nav-link sidebar-nav-item"),
                dbc.NavLink("Operational Dashboard", href="#", id="nav-ops", className="nav-link sidebar-nav-item"),
                dbc.NavLink("AI Assistant", href="#", id="nav-assistant", className="nav-link sidebar-nav-item"),
                dbc.NavLink("Settings", href="#", id="nav-settings", className="nav-link sidebar-nav-item"),
                dbc.NavLink("Help & Support", href="#", id="nav-help", className="nav-link sidebar-nav-item"),
            ], vertical=True, pills=False)
        ], className="sidebar-nav-wrapper"),
        html.Div([
            html.P("Version 0.2", className="sidebar-version"),
            html.P("Premium Edition", className="sidebar-premium")
        ], className="sidebar-version-wrapper", style={"bottom": "64px"})
    ], id="sidebar", className="sidebar minimalist-sidebar", style={
        # Let callback control all styles - no initial interference
    })
