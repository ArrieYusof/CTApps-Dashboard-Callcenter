# Version: 0.1
# Last Modified: 2025-08-24
# Changes: AI-powered modal component for KPI detailed insights
"""
Modal component for displaying AI-generated KPI insights with RAG context
"""
import dash_bootstrap_components as dbc
from dash import html, dcc
from typing import Dict, Any, Optional

def create_ai_insights_modal() -> dbc.Modal:
    """Create simplified modal for displaying AI-generated markdown insights"""
    return dbc.Modal([
        dbc.ModalHeader([
            html.H4("", id="modal-kpi-title"),
            html.Div([
                html.Span("🤖 AI", className="ai-badge"),
                html.Span("", id="ai-status-indicator", className="ai-subtitle")
            ], className="ai-indicator")
        ], close_button=True),
        
        dbc.ModalBody([
            # Loading state with better styling
            dcc.Loading(
                id="modal-loading",
                children=[
                    # Main markdown content area
                    html.Div([
                        dcc.Markdown(
                            "# 🤖 Loading AI Insights...\n\n**Please wait while we analyze your KPI data...**\n\n*This may take a few moments.*",
                            id="modal-markdown-content",
                            className="ai-insights-markdown",
                            dangerously_allow_html=True
                        )
                    ], id="modal-content-wrapper")
                ],
                type="circle",
                color="var(--accent-blue)",
                style={"minHeight": "200px"}
            )
        ]),
        
        dbc.ModalFooter([
            html.Button([
                html.I(className="fas fa-sync-alt", style={"marginRight": "6px"}),
                "Refresh Analysis"
            ], id="btn-refresh-insights", className="btn-refresh"),
            dbc.Button("Close", id="btn-close-modal", className="btn-close-modal", size="sm")
        ])
        
    ], id="modal-kpi-insights", size="lg", is_open=False, className="ai-insights-modal")

def format_insights_for_display(insights_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format AI insights data for modal display - Simplified for Markdown"""
    
    if not insights_data.get('success', False):
        # Error state
        return {
            'title': f"{insights_data.get('kpi_type', 'KPI')} - Analysis Error",
            'markdown_content': insights_data.get('markdown_content', '# ⚠️ Analysis Unavailable\n\nPlease try again or contact support.'),
            'ai_status': "❌ AI Service Error"
        }
    
    kpi_type = insights_data.get('kpi_type', 'Unknown KPI')
    source = insights_data.get('source', 'unknown')
    
    # Format title
    title = f"{kpi_type.replace('_', ' ').title()} Details"
    
    # Format AI status indicator
    if insights_data.get('ai_enabled', False) and source == 'openai_markdown':
        ai_status = "Powered by OpenAI GPT-4"
    elif source == 'rag_fallback' or source == 'rag_only':
        ai_status = "Data-Driven Analysis"
    else:
        ai_status = "Basic Analysis"
    
    return {
        'title': title,
        'markdown_content': insights_data.get('markdown_content', '# No content available'),
        'ai_status': ai_status,
        'timestamp': insights_data.get('timestamp', ''),
        'source': source
    }
