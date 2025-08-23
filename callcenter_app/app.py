# Version: 0.2
# Last Modified: 2025-08-23
# Changes: Premium app structure with enhanced navigation and 1920x1080 support
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
                    id="main-header-toggle",
                    className="burger-menu",
                    children=[
                        html.Span(className="burger-line"),
                        html.Span(className="burger-line"),
                        html.Span(className="burger-line")
                    ]
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
        className='main-content-wrapper',
        style={
            "height": "calc(100vh - 35px - 5px)",
            "overflow": "hidden",
            "boxSizing": "border-box",
            "position": "fixed",
            "top": "35px",
            # Remove left and width here; callback will set them
        }
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

# Callback to toggle sidebar
@app.callback(
    [Output('sidebar', 'style'), Output('page-content', 'style')],
    [Input('main-header-toggle', 'n_clicks')],
    [State('sidebar', 'style'), State('page-content', 'style')]
)
def toggle_sidebar(n_clicks, sidebar_style, content_style):
    SIDEBAR_WIDTH = 220  # px, match current sidebar width
    if n_clicks is None or n_clicks % 2 == 0:
        # Sidebar hidden, content full width
        s_style = sidebar_style.copy() if sidebar_style else {}
        s_style['transform'] = f'translateX(-{SIDEBAR_WIDTH}px)'
        s_style['zIndex'] = 1001
        s_style['width'] = f'{SIDEBAR_WIDTH}px'
        s_style['position'] = 'fixed'
        s_style['left'] = '0'
        s_style['top'] = '0'
        s_style['height'] = '100vh'
        s_style['overflow'] = 'hidden'

        c_style = content_style.copy() if content_style else {}
        c_style['left'] = '0'
        c_style['width'] = '100vw'
        c_style['position'] = 'fixed'
        c_style['top'] = '35px'
        c_style['height'] = 'calc(100vh - 35px - 5px)'
        c_style['transition'] = 'left 0.3s, width 0.3s'
        c_style['boxSizing'] = 'border-box'
        c_style['zIndex'] = 1
        c_style['display'] = 'block'
        return s_style, c_style
    else:
        # Sidebar visible, content resized to available width
        s_style = sidebar_style.copy() if sidebar_style else {}
        s_style['transform'] = 'translateX(0)'
        s_style['zIndex'] = 1001
        s_style['width'] = f'{SIDEBAR_WIDTH}px'
        s_style['position'] = 'fixed'
        s_style['left'] = '0'
        s_style['top'] = '0'
        s_style['height'] = '100vh'
        s_style['overflow'] = 'hidden'
        s_style['display'] = 'block'

        c_style = content_style.copy() if content_style else {}
        c_style['left'] = f'{SIDEBAR_WIDTH}px'
        c_style['width'] = f'calc(100vw - {SIDEBAR_WIDTH}px)'
        c_style['position'] = 'fixed'
        c_style['top'] = '35px'
        c_style['height'] = 'calc(100vh - 35px - 5px)'
        c_style['transition'] = 'left 0.3s, width 0.3s'
        c_style['boxSizing'] = 'border-box'
        c_style['zIndex'] = 1
        c_style['display'] = 'block'
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
