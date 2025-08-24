# Version: 0.3
# Last Modified: 2025-08-24
# Changes: Fixed navigation overlay issue - sidebar now properly resizes content instead of overlaying
"""
Main Dash app entry point for VADS Call Center Dashboard
Premium Edition with pixel-perfect 1920x1080 layout
"""
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State

# Import sidebar and page layouts
from components.sidebar import get_sidebar
from pages.executive_dashboard import executive_dashboard_layout
from pages.operational_dashboard import operational_dashboard_layout

# Initialize app with premium theme
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/custom.css'],
    meta_tags=[
        {"name": "viewport", "content": "width=1920, initial-scale=0.5, user-scalable=yes"}
    ]
)
app.title = "VADS Call Center - Premium Dashboard"

# Main app layout - Force full viewport usage
app.layout = html.Div([
    dcc.Store(id='current-page', data='executive'),
    html.Div(
        id="main-header",
        className="header-fixed",
        children=[
            html.Div([
                html.Button(
                    "☰",  # Just the hamburger icon without text
                    id="main-header-toggle",
                    className="burger-menu",
                    style={
                        "background": "red", 
                        "color": "white", 
                        "padding": "5px 10px", 
                        "border": "none", 
                        "cursor": "pointer",
                        "fontSize": "14px"
                    }
                ),
                html.Span(id="header-page-title", className="header-page-title", style={"color": "#fff", "fontWeight": "600", "fontSize": "0.95rem", "marginLeft": "12px"}),
                html.Span(id="live-monitoring-label", children="LIVE MONITORING", style={
                    "fontSize": "0.7rem",
                    "fontWeight": "600",
                    "color": "var(--accent-green)",
                    "margin": "0 auto",
                    "opacity": 0.85,
                    "animation": "blink 2s infinite",
                    "display": "none",
                    "position": "absolute",
                    "left": "50%",
                    "transform": "translateX(-50%)"
                }),
                html.Span("VADS Call Center", className="header-title", style={"marginLeft": "auto", "color": "#fff", "fontWeight": "600", "fontSize": "1.1rem"})
            ], style={"display": "flex", "alignItems": "center", "height": "100%", "width": "100%", "padding": "0 24px", "position": "relative"})
        ]
    ),
    get_sidebar(hidden=True),
    html.Div(
        id='page-content', 
        children=executive_dashboard_layout,  # Default to executive dashboard
        className='main-content-wrapper'
        # No inline styles - let callback control positioning
    )
], style={
    "width": "100vw", 
    "height": "100vh",
    "margin": "0", 
    "padding": "0",
    "overflow": "hidden"
})

# Callback to update header page title
@app.callback(
    [Output('header-page-title', 'children'), Output('live-monitoring-label', 'style')],
    [Input('current-page', 'data')]
)
def update_header_page_title(current_page):
    if current_page == 'executive':
        return 'Executive Dashboard', {"display": "none"}
    elif current_page == 'operational':
        return 'Operational Dashboard', {
            "fontSize": "0.7rem",
            "fontWeight": "600",
            "color": "var(--accent-green)",
            "margin": "0 auto",
            "opacity": 0.85,
            "animation": "blink 2s infinite",
            "display": "inline",
            "position": "absolute",
            "left": "50%",
            "transform": "translateX(-50%)"
        }
    else:
        return '', {"display": "none"}

# Callback to toggle sidebar - FINAL VERSION
@app.callback(
    [Output('sidebar', 'style'), Output('page-content', 'style')],
    [Input('main-header-toggle', 'n_clicks')],
    prevent_initial_call=False
)
def toggle_sidebar(n_clicks):
    SIDEBAR_WIDTH = 220  # px, match current sidebar width
    
    # Sidebar toggle logic: None/even = hidden, odd = visible
    
    # Create base styles
    base_sidebar_style = {
        'width': f'{SIDEBAR_WIDTH}px',
        'height': 'calc(100vh - 35px)',  # Start below header (35px)
        'position': 'fixed',
        'top': '35px',  # Position below header
        'zIndex': 1001,
        'overflow': 'hidden',
        'background': '#181A22',
        'borderRight': '1px solid #23263A',
        'boxShadow': '0 2px 16px rgba(0,0,0,0.08)',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'stretch',
        'transition': 'left 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
    }
    
    base_content_style = {
        'position': 'fixed',
        'top': '35px',
        'height': 'calc(100vh - 35px)',  # Full height minus header
        'transition': 'left 0.3s cubic-bezier(0.4, 0, 0.2, 1), width 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        'boxSizing': 'border-box',
        'zIndex': 1,
        'overflow': 'auto',
        'display': 'block'
    }
    
    if n_clicks is None or n_clicks % 2 == 0:
        # Sidebar hidden, content full width
        s_style = base_sidebar_style.copy()
        s_style['left'] = f'-{SIDEBAR_WIDTH}px'
        s_style['display'] = 'none'  # Force hide when not visible
        
        c_style = base_content_style.copy()
        c_style['left'] = '0'
        c_style['width'] = '100vw'
        return s_style, c_style
    else:
        # Sidebar visible, content resized to available width
        s_style = base_sidebar_style.copy()
        s_style['left'] = '0'
        s_style['display'] = 'flex'  # Show when visible
        
        c_style = base_content_style.copy()
        c_style['left'] = f'{SIDEBAR_WIDTH}px'
        c_style['width'] = f'calc(100vw - {SIDEBAR_WIDTH}px)'
        
        return s_style, c_style

# Callback for navigation between pages
@app.callback(
    [Output('page-content', 'children'), Output('current-page', 'data')],
    [Input('nav-exec', 'n_clicks'), Input('nav-ops', 'n_clicks')],
    [State('current-page', 'data')]
)
def navigate_pages(exec_clicks, ops_clicks, current_page):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return executive_dashboard_layout, 'executive'
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'nav-exec':
        return executive_dashboard_layout, 'executive'
    elif button_id == 'nav-ops':
        return operational_dashboard_layout, 'operational'
    
    return executive_dashboard_layout, 'executive'

# Callback to update active navigation state
@app.callback(
    [Output('nav-exec', 'active'), Output('nav-ops', 'active')],
    [Input('current-page', 'data')]
)
def update_nav_active(current_page):
    if current_page == 'executive':
        return True, False
    elif current_page == 'operational':
        return False, True
    return True, False

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8050)
