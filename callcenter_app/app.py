# Version: 0.1
# Last Modified: 2025-08-25
# Changes: Added AI Assistant navigation and chat functionality
"""
Main Dash app entry point for VADS Call Center Dashboard
Premium Edition with pixel-perfect 1920x1080 layout
"""
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback_context, no_update
from dash.exceptions import PreventUpdate
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import threading
import time
import uuid
import os
import json
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, ALL, callback_context
from datetime import datetime

# Import sidebar and page layouts
from components.sidebar import get_sidebar
from components.ai_modal import create_ai_insights_modal, format_insights_for_display
from ai.insights_manager import AIInsightsManager
from pages.executive_dashboard import executive_dashboard_layout
from pages.operational_dashboard import operational_dashboard_layout
from pages.ai_assistant import ai_assistant_layout

# Initialize app with premium theme
app = dash.Dash(
    __name__, 
    external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/custom.css'],
    meta_tags=[
        {"name": "viewport", "content": "width=1920, initial-scale=0.5, user-scalable=yes"}
    ],
    suppress_callback_exceptions=True  # Allow callbacks to dynamically generated components
)

# Global state for AI processing
ai_processing_state = {}
ai_processing_initiated = False
app.title = "VADS Call Center - Premium Dashboard"

# Initialize AI insights manager
ai_manager = AIInsightsManager()

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
                    className="burger-menu"
                    # All styling handled by CSS class
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
    ),
    
    # AI Insights Modal
    create_ai_insights_modal()
    
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
            "display": "inline",
            "position": "absolute",
            "left": "50%",
            "transform": "translateX(-50%)"
        }
    elif current_page == 'assistant':
        return 'AI Assistant', {
            "fontSize": "0.7rem",
            "fontWeight": "600",
            "color": "var(--accent-blue)",
            "margin": "0 auto",
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

# Clientside callback to refresh charts when sidebar toggles
app.clientside_callback(
    """
    function(n_clicks) {
        // Force a refresh of all Plotly charts after sidebar animation completes
        setTimeout(function() {
            var charts = document.querySelectorAll('.js-plotly-plot');
            charts.forEach(function(chart) {
                if (window.Plotly && chart._fullLayout) {
                    window.Plotly.Plots.resize(chart);
                    // Force a redraw to ensure colors are correct
                    window.Plotly.redraw(chart);
                }
            });
        }, 350); // Wait for transition to complete (300ms + buffer)
        
        return window.dash_clientside.no_update;
    }
    """,
    Output('main-header-toggle', 'style'),  # Dummy output
    Input('main-header-toggle', 'n_clicks')
)

# Callback for navigation between pages  
@app.callback(
    [Output('page-content', 'children'), Output('current-page', 'data')],
    [Input('nav-exec', 'n_clicks'), Input('nav-ops', 'n_clicks'), Input('nav-assistant', 'n_clicks')],
    [State('current-page', 'data')]
)
def navigate_pages(exec_clicks, ops_clicks, assistant_clicks, current_page):
    ctx = dash.callback_context
    
    if not ctx.triggered:
        return executive_dashboard_layout, 'executive'
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'nav-exec':
        return executive_dashboard_layout, 'executive'
    elif button_id == 'nav-ops':
        return operational_dashboard_layout, 'operational'
    elif button_id == 'nav-assistant':
        return ai_assistant_layout(), 'assistant'
    
    return executive_dashboard_layout, 'executive'

# Callback to update active navigation state
@app.callback(
    [Output('nav-exec', 'active'), Output('nav-ops', 'active'), Output('nav-assistant', 'active')],
    [Input('current-page', 'data')]
)
def update_nav_active(current_page):
    if current_page == 'executive':
        return True, False, False
    elif current_page == 'operational':
        return False, True, False
    elif current_page == 'assistant':
        return False, False, True
    return True, False, False

# AI Insights Modal Callbacks - Updated for async loading with animated indicator
@app.callback(
    [Output('modal-kpi-insights', 'is_open'),
     Output('modal-kpi-title', 'children'),
     Output('modal-markdown-content', 'children'),
     Output('ai-status-indicator', 'children'),
     Output('ai-processing-store', 'data'),
     Output('ai-processing-interval', 'disabled'),
     Output('ai-processing-interval', 'n_intervals')],  # Add n_intervals output to reset counter
    [Input({'type': 'more-details-btn', 'index': ALL}, 'n_clicks'),
     Input('btn-close-modal', 'n_clicks'),
     Input('btn-refresh-insights', 'n_clicks'),
     Input('ai-processing-interval', 'n_intervals')],
    [State('modal-kpi-insights', 'is_open'),
     State('modal-kpi-title', 'children'),
     State('ai-processing-store', 'data')],
    prevent_initial_call=True
)
def handle_ai_insights_modal(more_details_clicks, close_click, refresh_click, interval_n, is_open, current_title, processing_data):
    """Handle modal opening/closing and populate with AI insights - Updated for async loading"""
    import dash
    from dash.exceptions import PreventUpdate
    import threading
    import time
    
    global ai_processing_initiated
    
    # Clear stale processing states on startup
    current_time = time.time()
    stale_ids = [pid for pid, pdata in ai_processing_state.items() 
                 if current_time - pdata.get('start_time', 0) > 300]  # 5 minutes
    for pid in stale_ids:
        print(f"🤖 AI INFO: Cleaning up stale processing state: {pid}")
        del ai_processing_state[pid]
    
    ctx = callback_context
    if not ctx.triggered:
        print("🤖 AI INFO: No trigger detected, returning no_update")
        raise PreventUpdate
    
    trigger = ctx.triggered[0]
    prop_id = trigger['prop_id']
    
    print(f"🤖 AI INFO: Callback triggered - prop_id: {prop_id}")
    print(f"🤖 AI INFO: Trigger details: {trigger}")
    
    # Close modal
    if prop_id == 'btn-close-modal.n_clicks' and close_click:
        print("🤖 AI INFO: Closing modal - cleaning up all processing state and disabling interval permanently")
        # Clean up any remaining processing state
        ai_processing_initiated = False
        # Clear all processing states
        ai_processing_state.clear()
        return False, dash.no_update, dash.no_update, dash.no_update, None, True, dash.no_update
    
    # Check if AI processing is complete (interval callback)
    if prop_id == 'ai-processing-interval.n_intervals':
        
        # If AI processing was never initiated, disable the interval immediately
        if not ai_processing_initiated:
            print(f"🤖 AI INFO: Interval running but AI processing never initiated - disabling interval")
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, None, True, dash.no_update  # Disable interval
        
        # If no processing data, disable the interval to stop it immediately
        if not processing_data:
            print(f"🤖 AI INFO: Interval triggered but no processing data - disabling interval and resetting flag")
            ai_processing_initiated = False  # Reset flag
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, None, True, dash.no_update  # Disable interval
            
        print(f"🤖 AI INFO: Checking AI processing status...")
        
        # Get processing ID from store data
        processing_id = processing_data if isinstance(processing_data, str) else processing_data.get('id')
        if not processing_id:
            print(f"🤖 AI INFO: No processing ID found - disabling interval and resetting flag")
            ai_processing_initiated = False  # Reset flag
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, None, True, dash.no_update  # Disable interval
            
        if processing_id not in ai_processing_state:
            print(f"🤖 AI INFO: Processing ID {processing_id} not found in global state - likely completed and cleaned up")
            ai_processing_initiated = False  # Reset flag since processing is done
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, None, True, dash.no_update  # Disable interval
            
        # Get current processing state from global store
        current_state = ai_processing_state[processing_id]
        
        # Check if processing is complete
        if current_state.get('status') == 'complete':
            print(f"🤖 AI INFO: AI processing complete, displaying results and permanently disabling interval")
            
            insights_data = current_state.get('result', {})
            formatted_data = format_insights_for_display(insights_data)
            
            # Clean up global state and reset processing flag permanently
            del ai_processing_state[processing_id]
            ai_processing_initiated = False  # Reset flag to prevent any future intervals
            
            return (
                dash.no_update,  # Don't change modal state (keep it open)
                formatted_data['title'], 
                formatted_data['markdown_content'],
                formatted_data['ai_status'],
                None,  # Clear processing data to prevent further callbacks
                True,  # Disable interval permanently
                0      # Reset n_intervals to 0 for next use
            )
        
        # Processing still ongoing - only update if there's a meaningful change
        elif current_state.get('status') == 'processing':
            elapsed_time = int(time.time() - current_state.get('start_time', 0))
            
            # Only update if elapsed time changed significantly (to reduce updates)
            last_update_time = current_state.get('last_update_time', -1)
            if elapsed_time <= last_update_time:
                # No significant change, prevent ALL updates to stop flickering
                print(f"🤖 AI INFO: No time change ({elapsed_time}s), preventing update")
                raise PreventUpdate
            
            # Update the last update time to current elapsed time
            current_state['last_update_time'] = elapsed_time
            
            # Timeout check - disable if processing takes too long (30+ seconds)
            if elapsed_time > 30:
                print(f"🤖 AI INFO: Processing timeout after {elapsed_time}s - cleaning up and disabling interval")
                if processing_id in ai_processing_state:
                    del ai_processing_state[processing_id]
                ai_processing_initiated = False  # Reset flag
                return (
                    dash.no_update,
                    dash.no_update,
                    "# ⚠️ Processing Timeout\n\nAI processing took longer than expected. Please try again.",
                    "⚠️ Timeout",
                    None,  # Clear processing data
                    True,  # Disable interval
                    0      # Reset n_intervals to 0
                )
            
            print(f"🤖 AI INFO: Updating loading content for {elapsed_time}s elapsed")
            
            # Create animated loading content (only if elapsed time is new)
            loading_content = f"""
# 🤖 Analyzing Your Data...

## Please wait while our AI processes your KPI information

⏱️ **Processing for {elapsed_time} seconds...**

🔍 **Current Steps:**
- Gathering contextual data from RAG engine
- Analyzing patterns and trends  
- Generating actionable insights
- Formatting comprehensive report

*This typically takes 5-15 seconds depending on data complexity.*

---
*Powered by Advanced AI with Enhanced Context Analysis*
            """.strip()
            
            return (
                dash.no_update,  # Don't change modal state (keep it open)
                dash.no_update,  # Don't change title
                loading_content, # Only update content
                "🤖 Processing...",
                processing_id,  # Keep processing ID
                False,  # Keep interval active but reduce updates
                dash.no_update  # Don't reset n_intervals while processing
            )
        
        # If we get here, something went wrong - disable interval
        print(f"🤖 AI INFO: Unexpected processing state, disabling interval")
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, None, True, dash.no_update
    
    # Open modal when any "More Details" button is clicked or refresh
    if 'more-details-btn' in prop_id or prop_id == 'btn-refresh-insights.n_clicks':
        
        # Validate that the button was actually clicked (not just initialized)
        if 'more-details-btn' in prop_id:
            # Check the actual trigger value - it should not be None for a real click
            trigger_value = trigger['value']
            if trigger_value is None:
                print(f"🤖 AI INFO: Button initialized with trigger value={trigger_value}, ignoring")
                raise PreventUpdate
                
            print(f"🤖 AI INFO: More Details button clicked - parsing prop_id: {prop_id}")
            
            # Extract card ID from button ID
            try:
                button_data = json.loads(prop_id.split('.')[0])
                card_id = button_data['index']
                print(f"🤖 AI INFO: Extracted card ID: {card_id}")
            except Exception as e:
                print(f"🤖 AI INFO: ❌ Error parsing button data: {e}")
                raise PreventUpdate
        elif prop_id == 'btn-refresh-insights.n_clicks':
            # Check if refresh button click is valid
            trigger_value = trigger['value']
            if trigger_value is None:
                print(f"🤖 AI INFO: Refresh button initialized with trigger value={trigger_value}, ignoring")
                raise PreventUpdate
        else:
            # Refresh case - extract from current title
            print(f"🤖 AI INFO: Refresh button clicked, current_title: {current_title}")
            card_id = 'refresh'  # Will be mapped below
        
        # Determine KPI type and display info from the above logic
        # (This comment replaces the original position of "Determine KPI type and display info")
        
        # Map card ID to KPI type and display name
        card_to_kpi_mapping = {
            # Operational Dashboard Cards
            'queue': {'kpi': 'call_volume', 'display': 'Real-Time Queue Status', 'value': 1248},
            'agent-availability': {'kpi': 'agent_availability', 'display': 'Agent Availability', 'value': 89.2},
            'sla': {'kpi': 'service_level', 'display': 'SLA Monitoring', 'value': 87.4},
            'csat': {'kpi': 'satisfaction_score', 'display': 'Customer Satisfaction', 'value': 4.2}, 
            'outcomes': {'kpi': 'first_call_resolution', 'display': 'Call Outcomes', 'value': 76.8},
            'resources': {'kpi': 'resource_utilization', 'display': 'Resource Utilization', 'value': 82.5},
            'agents_wide': {'kpi': 'avg_response_time', 'display': 'Agent Performance', 'value': 32},
            
            # Executive Dashboard Cards
            'revenue-chart': {'kpi': 'revenue_growth', 'display': 'Revenue Growth', 'value': 1400000},  # Convert to actual currency (1.4M)
            'cost-chart': {'kpi': 'cost_per_call', 'display': 'Cost per Call', 'value': 2.45},
            'cash-flow': {'kpi': 'cash_flow', 'display': 'Cash Flow', 'value': 870000},
            'cash-chart': {'kpi': 'cash_flow', 'display': 'Cash Flow', 'value': 870000},
            'kpi-card cash-chart': {'kpi': 'cash_flow', 'display': 'Cash Flow', 'value': 870000},
            'margin-chart': {'kpi': 'profit_margin', 'display': 'Profit Margin', 'value': 18.3},
            'performance': {'kpi': 'kpi_performance', 'display': 'Performance Index', 'value': 85.3},
            'retention-chart': {'kpi': 'customer_retention', 'display': 'Customer Retention', 'value': 94.7},
            'efficiency-chart': {'kpi': 'operational_efficiency', 'display': 'Efficiency Rate', 'value': 91.2},
            'summary-chart': {'kpi': 'overall_performance', 'display': 'Performance Summary', 'value': 88.7},
            
            # Refresh case - extract from title
            'refresh': {'kpi': 'call_volume', 'display': 'Refreshed Analysis', 'value': 100}
        }
        
        # Handle refresh case by extracting KPI from current title
        if card_id == 'refresh' and current_title:
            title_lower = str(current_title).lower()
            if 'response time' in title_lower or 'agent performance' in title_lower:
                card_to_kpi_mapping['refresh'] = {'kpi': 'avg_response_time', 'display': 'Agent Performance', 'value': 32}
            elif 'agent availability' in title_lower:
                card_to_kpi_mapping['refresh'] = {'kpi': 'agent_availability', 'display': 'Agent Availability', 'value': 89.2}
            elif 'satisfaction' in title_lower:
                card_to_kpi_mapping['refresh'] = {'kpi': 'satisfaction_score', 'display': 'Customer Satisfaction', 'value': 4.2}
            # Add more mappings as needed
        
        mapping = card_to_kpi_mapping.get(card_id)
        if not mapping:
            print(f"🤖 AI INFO: ⚠️ No mapping found for card ID: {card_id}")
            kpi_type = 'general_kpi'
            display_name = f"Unknown KPI ({card_id})"
            current_value = 100
        else:
            kpi_type = mapping['kpi']
            display_name = mapping['display']
            current_value = mapping['value']
        
        print(f"🤖 AI INFO: Mapped to KPI: {kpi_type}, Display: {display_name}, Value: {current_value}")
        
        # Mark that AI processing has been initiated
        ai_processing_initiated = True
        
        # Start AI processing in background thread
        processing_id = f"{kpi_type}_{int(time.time())}"
        processing_data = {
            'status': 'processing',
            'kpi_type': kpi_type,
            'current_value': current_value,
            'display_name': display_name,
            'card_id': card_id,
            'title': f"{display_name} Analysis",
            'start_time': time.time(),
            'result': None,
            'id': processing_id
        }
        
        # Store in global state
        ai_processing_state[processing_id] = processing_data
        
        def process_ai_insights():
            """Background processing function"""
            try:
                print(f"🤖 AI BACKGROUND: Starting AI processing for {kpi_type}...")
                
                # Get AI insights using the insights manager
                insights_manager = AIInsightsManager()
                insights_data = insights_manager.get_kpi_insights_sync(
                    kpi_type=kpi_type,
                    current_value=current_value,
                    additional_context={"ai_enabled": True, "card_id": card_id, "display_name": display_name}
                )
                
                print(f"🤖 AI BACKGROUND: Processing complete, success={insights_data.get('success')}")
                
                # Store result back in global processing state
                if processing_id in ai_processing_state:
                    ai_processing_state[processing_id]['result'] = insights_data
                    ai_processing_state[processing_id]['status'] = 'complete'
                
            except Exception as e:
                print(f"🤖 AI BACKGROUND: ❌ Error during processing: {e}")
                if processing_id in ai_processing_state:
                    ai_processing_state[processing_id]['result'] = {
                        'success': False,
                        'markdown_content': f'# ⚠️ AI Processing Error\n\nAn error occurred while analyzing your data: {str(e)}\n\nPlease try again or contact support.',
                        'kpi_type': kpi_type,
                        'source': 'error'
                    }
                    ai_processing_state[processing_id]['status'] = 'complete'
        
        # Start background processing
        thread = threading.Thread(target=process_ai_insights)
        thread.daemon = True
        thread.start()
        
        # Show modal immediately with loading indicator
        initial_loading_content = f"""
# 🤖 Initializing AI Analysis...

## Preparing to analyze {display_name}

🚀 **Starting AI Engine...**
- Connecting to Advanced AI Analysis Engine
- Preparing enhanced context engine
- Loading historical patterns

*Please wait, this will take just a moment...*

---
*Powered by advanced AI analytics*
        """.strip()
        
        print(f"🤖 AI INFO: Opening modal with loading state")
        
        return (
            True,  # Open modal
            f"{display_name} Analysis",
            initial_loading_content,
            "🤖 Initializing...",
            processing_id,  # Store processing ID
            False,  # Enable interval for status checking
            0       # Reset n_intervals to 0 for fresh start
        )
    
    print(f"🤖 AI INFO: No matching condition, returning no_update")
    raise PreventUpdate

# AI Assistant Chat Callback
@app.callback(
    [Output('chat-messages', 'children'),
     Output('chat-input', 'value'),
     Output('loading-placeholder', 'style')],
    [Input('send-button', 'n_clicks'),
     Input('chat-input', 'n_submit'),
     Input('quick-revenue', 'n_clicks'),
     Input('quick-calls', 'n_clicks'), 
     Input('quick-satisfaction', 'n_clicks'),
     Input('quick-profit', 'n_clicks')],
    [State('chat-messages', 'children'),
     State('chat-input', 'value')]
)
def handle_chat_message(send_clicks, input_submit, revenue_clicks, calls_clicks, 
                       satisfaction_clicks, profit_clicks, current_messages, user_input):
    """Handle AI assistant chat messages with simple stateless approach"""
    from pages.ai_assistant import get_ai_response, create_message
    
    # Check which input triggered the callback
    triggered_id = callback_context.triggered[0]['prop_id'].split('.')[0] if callback_context.triggered else None
    
    # Determine the message to process
    if triggered_id == 'quick-revenue':
        message_text = "What's our current revenue status and growth trends?"
    elif triggered_id == 'quick-calls':
        message_text = "How is our call volume performing today?"
    elif triggered_id == 'quick-satisfaction':
        message_text = "What's our customer satisfaction level?"
    elif triggered_id == 'quick-profit':
        message_text = "How are our profit margins looking?"
    elif triggered_id in ['send-button', 'chat-input'] and user_input and user_input.strip():
        message_text = user_input.strip()
    else:
        raise PreventUpdate
    
    try:
        # Create user message (only show if it was typed, not for quick actions)
        messages_to_add = []
        if triggered_id in ['send-button', 'chat-input']:
            messages_to_add.append(create_message("user", message_text))
        
        # Get AI response with conversation history
        ai_response = get_ai_response(message_text, current_messages or [])
        
        # Create AI message
        messages_to_add.append(create_message("assistant", ai_response))
        
        # Update messages list
        updated_messages = (current_messages or []) + messages_to_add
        
        # Clear input and hide loading
        return updated_messages, "", {"display": "none"}
        
    except Exception as e:
        print(f"Chat Error: {e}")
        error_msg = create_message("assistant", "🤖 I encountered an error. Please try again.")
        updated_messages = (current_messages or []) + [error_msg]
        return updated_messages, "", {"display": "none"}

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8050)
