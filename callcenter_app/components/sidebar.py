# Version: 0.2
# Last Modified: 2025-08-23
# Changes: Premium sidebar with glass-morphism design
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
                dbc.NavLink("Settings", href="#", id="nav-settings", className="nav-link sidebar-nav-item"),
                dbc.NavLink("Help & Support", href="#", id="nav-help", className="nav-link sidebar-nav-item"),
            ], vertical=True, pills=False)
        ], className="sidebar-nav-wrapper"),
        html.Div([
            html.P("Version 0.2", className="sidebar-version"),
            html.P("Premium Edition", className="sidebar-premium")
        ], className="sidebar-version-wrapper", style={"bottom": "64px"})
    ], id="sidebar", className="sidebar minimalist-sidebar", style={
        "width": "220px",
        "height": "100vh",
        "position": "fixed",
        "top": "0",
        "left": "0",
        "transition": "transform 0.3s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.3s",
        "transform": "translateX(-220px)" if hidden else "translateX(0)",
        "opacity": "0.7" if hidden else "1",
        "zIndex": 1000,
        "padding": "0",
        "background": "#181A22",
        "borderRight": "1px solid #23263A",
        "boxShadow": "0 2px 16px rgba(0,0,0,0.08)",
        "overflow": "hidden"
    })
