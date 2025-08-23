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
    get_sidebar(hidden=True),
    html.Div(
        id='page-content', 
        children=executive_dashboard_layout,  # Default to executive dashboard
        className='main-content-wrapper',
        style={
            "height": "100vh",
            "width": "100vw",
            "overflow": "hidden",
            "boxSizing": "border-box",
            "position": "fixed",
            "top": "0",
            "left": "0"
        }
    )
], style={
    "width": "100vw", 
    "height": "100vh",
    "margin": "0", 
    "padding": "0",
    "overflow": "hidden"
})

# Callback to toggle sidebar
@app.callback(
    [Output('sidebar', 'style'), Output('page-content', 'style')],
    [Input('sidebar-toggle', 'n_clicks')],
    [State('sidebar', 'style'), State('page-content', 'style')]
)
def toggle_sidebar(n_clicks, sidebar_style, content_style):
    if n_clicks is None or n_clicks % 2 == 0:
        # Sidebar hidden, content full width
        s_style = sidebar_style.copy() if sidebar_style else {}
        s_style['transform'] = 'translateX(-280px)'
        s_style['zIndex'] = 1000
        
        c_style = content_style.copy() if content_style else {}
        c_style['marginLeft'] = '0px'
        c_style['width'] = '100vw'
        c_style['transition'] = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
        c_style['boxSizing'] = 'border-box'
        
        return s_style, c_style
    else:
        # Sidebar visible, content shifted right
        s_style = sidebar_style.copy() if sidebar_style else {}
        s_style['transform'] = 'translateX(0)'
        s_style['zIndex'] = 1000
        
        c_style = content_style.copy() if content_style else {}
        c_style['marginLeft'] = '280px'
        c_style['width'] = 'calc(100vw - 280px)'
        c_style['transition'] = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
        c_style['boxSizing'] = 'border-box'
        
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
