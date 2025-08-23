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
            html.H4("VADS", style={
                "color": "var(--accent-blue)",
                "fontWeight": "700",
                "marginBottom": "8px",
                "fontSize": "1.5rem"
            }),
            html.P("Call Center", style={
                "color": "var(--text-secondary)",
                "margin": "0 0 32px 0",
                "fontSize": "0.9rem"
            })
        ], style={"textAlign": "center", "padding": "24px 0"}),
        
        html.Hr(style={"border": "1px solid var(--border-subtle)", "margin": "0 0 24px 0"}),
        
        dbc.Nav([
            dbc.NavLink([
                html.Div([
                    html.Span("📊", style={"marginRight": "12px", "fontSize": "1.2rem"}),
                    "Executive Dashboard"
                ])
            ], href="#", id="nav-exec", active=True, className="nav-link"),
            
            dbc.NavLink([
                html.Div([
                    html.Span("⚡", style={"marginRight": "12px", "fontSize": "1.2rem"}),
                    "Operational Dashboard"
                ])
            ], href="#", id="nav-ops", className="nav-link"),
            
            html.Hr(style={"border": "1px solid var(--border-subtle)", "margin": "24px 0"}),
            
            dbc.NavLink([
                html.Div([
                    html.Span("🔧", style={"marginRight": "12px", "fontSize": "1.2rem"}),
                    "Settings"
                ])
            ], href="#", id="nav-settings", className="nav-link"),
            
            dbc.NavLink([
                html.Div([
                    html.Span("❓", style={"marginRight": "12px", "fontSize": "1.2rem"}),
                    "Help & Support"
                ])
            ], href="#", id="nav-help", className="nav-link"),
            
        ], vertical=True, pills=False),
        
        # Version info at bottom
        html.Div([
            html.P("Version 0.2", style={
                "color": "var(--text-secondary)",
                "fontSize": "0.8rem",
                "margin": "0",
                "textAlign": "center"
            }),
            html.P("Premium Edition", style={
                "color": "var(--accent-blue)",
                "fontSize": "0.7rem",
                "margin": "4px 0 0 0",
                "textAlign": "center",
                "fontWeight": "500"
            })
        ], style={
            "position": "absolute",
            "bottom": "24px",
            "left": "0",
            "right": "0",
            "padding": "0 24px"
        })
        
    ], id="sidebar", className="sidebar", style={
        "width": "280px",
        "height": "100vh",
        "position": "fixed",
        "top": "0",
        "left": "0",
        "transition": "transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        "transform": "translateX(-280px)" if hidden else "translateX(0)",
        "zIndex": 1000,
        "padding": "0",
        "background": "var(--card-bg)",
        "backdropFilter": "blur(20px)",
        "borderRight": "1px solid var(--border-subtle)"
    })
