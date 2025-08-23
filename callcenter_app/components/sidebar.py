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
        # Accent bar
        html.Div([], className="sidebar-accent-bar"),
        # Profile section
        html.Div([
            html.Img(src="/assets/avatar.png", className="sidebar-avatar"),
            html.Div([
                html.H4("Obie", className="sidebar-username"),
                html.P("Supervisor", className="sidebar-role")
            ], style={"marginLeft": "12px"})
        ], className="sidebar-profile"),
        # Navigation
        html.Div([
            dbc.Nav([
                dbc.NavLink([
                    html.Div([
                        html.Span("📊", className="sidebar-icon"),
                        html.Span("Executive Dashboard", className="sidebar-label")
                    ], className="sidebar-nav-item")
                ], href="#", id="nav-exec", active=True, className="nav-link"),
                dbc.NavLink([
                    html.Div([
                        html.Span("⚡", className="sidebar-icon"),
                        html.Span("Operational Dashboard", className="sidebar-label")
                    ], className="sidebar-nav-item")
                ], href="#", id="nav-ops", className="nav-link"),
                dbc.NavLink([
                    html.Div([
                        html.Span("🔧", className="sidebar-icon"),
                        html.Span("Settings", className="sidebar-label")
                    ], className="sidebar-nav-item")
                ], href="#", id="nav-settings", className="nav-link"),
                dbc.NavLink([
                    html.Div([
                        html.Span("❓", className="sidebar-icon"),
                        html.Span("Help & Support", className="sidebar-label")
                    ], className="sidebar-nav-item")
                ], href="#", id="nav-help", className="nav-link"),
            ], vertical=True, pills=False)
        ], className="sidebar-nav-wrapper"),
        # Version info at bottom
        html.Div([
            html.P("Version 0.2", className="sidebar-version"),
            html.P("Premium Edition", className="sidebar-premium")
        ], className="sidebar-version-wrapper", style={"bottom": "64px"})
    ], id="sidebar", className="sidebar", style={
        "width": "280px",
        "height": "100vh",
        "position": "fixed",
        "top": "0",
        "left": "0",
        "transition": "transform 0.4s cubic-bezier(0.4, 0, 0.2, 1), opacity 0.4s",
        "transform": "translateX(-280px)" if hidden else "translateX(0)",
        "opacity": "0.7" if hidden else "1",
        "zIndex": 1000,
        "padding": "0",
        "background": "var(--card-bg)",
        "backdropFilter": "blur(24px)",
        "borderRight": "2px solid var(--accent-blue)",
        "boxShadow": "0 0 32px 0 rgba(0,212,255,0.12)",
        "overflow": "hidden"
    })
