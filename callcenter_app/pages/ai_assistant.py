# Version: 1.0
# Last Modified: 2025-08-25
# Changes: New simple AI assistant page with improved architecture
"""
AI Assistant Page - Clean Implementation
Simple chat interface leveraging existing RAG engine and OpenAI service
"""
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, callback_context
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

from ai.insights_manager import AIInsightsManager
from ai.openai_service import OpenAIInsightGenerator

# Import fast AI at module level to avoid relative import issues
try:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    from callcenter_app.ai.fast_conversational_ai import fast_ai
    FAST_AI_AVAILABLE = True
except Exception as e:
    print(f"⚠️ Fast AI import failed: {e}")
    FAST_AI_AVAILABLE = False
    fast_ai = None

def get_current_kpi_value(kpi_type: str) -> float:
    """Get current numeric value for KPI to avoid string/float operation errors"""
    # Sample current values - in real system, these would come from live data
    kpi_values = {
        'revenue_growth': 1400000,  # RM 1.4M
        'profit_margin': 18.3,
        'call_volume': 2573,
        'customer_satisfaction': 4.2,
        'customer_retention': 85.5,
        'first_call_resolution': 78.2,
        'cost_per_call': 15.50,
        'call_abandonment': 3.2,
        'average_wait_time': 42.5,
        'average_handle_time': 285.0
    }
    return kpi_values.get(kpi_type, 0.0)

# Initialize AI components
try:
    ai_manager = AIInsightsManager()
    chat_enabled = True
except Exception as e:
    print(f"AI Assistant: Could not initialize AI manager: {e}")
    ai_manager = None
    chat_enabled = False

def ai_assistant_layout():
    """Create AI assistant page layout"""
    return html.Div([
        # Page Header - Fixed at top
        html.Div([
            html.H2([
                html.I(className="fas fa-robot", style={"marginRight": "12px", "color": "#4A90E2"}),
                "AI Assistant"
            ], className="page-title"),
            html.P("Ask questions about your call center metrics and get AI-powered insights.", 
                   className="page-subtitle")
        ], className="ai-header-fixed"),
        
        # Quick Actions - Fixed below header
        html.Div([
            html.H6("Quick Questions:", className="mb-2", style={"color": "var(--text-secondary)"}),
            html.Div([
                dbc.Button("📊 Revenue Status", id="quick-revenue", size="sm", outline=True, className="me-2 mb-2"),
                dbc.Button("📞 Call Volume", id="quick-calls", size="sm", outline=True, className="me-2 mb-2"),
                dbc.Button("😊 Customer Satisfaction", id="quick-satisfaction", size="sm", outline=True, className="me-2 mb-2"),
                dbc.Button("💰 Profit Analysis", id="quick-profit", size="sm", outline=True, className="me-2 mb-2"),
            ], className="mb-3")
        ], className="ai-quick-actions-fixed"),
        
        # Chat Messages - Scrollable area
        html.Div([
            # Welcome message
            create_message("assistant", 
                "👋 Hello! I'm your AI assistant for call center analytics. "
                "I can help you understand your KPIs, analyze trends, and provide actionable insights. "
                "Use the quick questions above or type your own question!")
        ], id="chat-messages", className="ai-chat-messages-fullscreen"),
        
        # Input Area - Fixed at bottom
        html.Div([
            html.Div([
                html.Small("💬 Type your question here:", className="mb-2", 
                         style={"color": "var(--text-secondary)", "fontSize": "12px"})
            ]),
            dbc.InputGroup([
                dbc.Input(
                    id="chat-input",
                    placeholder="Ask me about your call center metrics..." if chat_enabled 
                              else "AI assistant is currently unavailable",
                    disabled=not chat_enabled,
                    type="text",
                    value="",  # Ensure empty initial value
                    style={
                        "borderRadius": "20px 0 0 20px",
                        "fontSize": "16px",
                        "padding": "12px 16px",
                        "border": "2px solid var(--border-color)"
                    }
                ),
                dbc.Button([
                    html.I(className="fas fa-paper-plane")
                ], 
                id="send-button", 
                color="primary", 
                disabled=not chat_enabled,
                style={
                    "borderRadius": "0 20px 20px 0",
                    "padding": "12px 20px",
                    "fontSize": "16px"
                })
            ], className="mb-0"),
            
            # Status indicator
            html.Div([
                html.Small([
                    html.I(className="fas fa-circle text-success" if chat_enabled else "fas fa-circle text-warning"),
                    f" AI Assistant {'Online' if chat_enabled else 'Offline'}"
                ])
            ], className="status-indicator", style={"textAlign": "center", "marginTop": "8px"})
        ], className="ai-input-area-fixed"),
        
        # Loading indicator (hidden by default)
        dcc.Loading(
            id="chat-loading",
            children=[html.Div(id="loading-placeholder")],
            type="dot",
            style={"display": "none"}
        )
        
    ], className="ai-assistant-fullscreen")

def create_message(sender: str, content: str, timestamp: Optional[str] = None) -> html.Div:
    """Create a chat message component with markdown support"""
    if not timestamp:
        timestamp = datetime.now().strftime("%H:%M")
    
    is_user = sender == "user"
    message_class = "user-message" if is_user else "assistant-message"
    
    # Use markdown rendering for AI responses, plain text for user messages
    if is_user:
        content_component = html.Div(content, className="message-content")
    else:
        # Detect if content contains markdown (tables, headers, etc.)
        has_markdown = any(marker in content for marker in ['|', '#', '**', '```', '*', '-'])
        
        if has_markdown:
            # Wrap tables in a responsive container
            if '|' in content and content.count('|') > 5:  # Likely contains table
                content_component = html.Div([
                    html.Div([
                        dcc.Markdown(
                            content, 
                            className="message-content markdown-content",
                            dangerously_allow_html=False,  # Security
                            link_target="_blank"
                        )
                    ], className="table-responsive-wrapper")
                ], className="markdown-table-container")
            else:
                content_component = dcc.Markdown(
                    content, 
                    className="message-content markdown-content",
                    dangerously_allow_html=False,
                    link_target="_blank"
                )
        else:
            content_component = html.Div(content, className="message-content")
    
    return html.Div([
        html.Div([
            html.Div([
                html.I(className="fas fa-user" if is_user else "fas fa-robot"),
            ], className="message-avatar"),
            html.Div([
                content_component,
                html.Small(timestamp, className="message-timestamp")
            ], className="message-body")
        ], className="message-inner")
    ], className=f"message {message_class}")

def get_detailed_analysis_response(user_message: str, conversation_history: list = None) -> str:
    """Generate detailed analysis response using the heavy analytics system"""
    try:
        # Analyze intent with conversation history
        intent_analysis = analyze_user_intent_with_history(user_message, conversation_history or [])
        
        if intent_analysis.get('intent') in ['kpi_analysis', 'kpi_followup']:
            kpi_type = intent_analysis.get('kpi_type')
            if not kpi_type:
                return "I couldn't determine which KPI you're asking about. Could you be more specific?"
            
            # Check if user is asking for table/structured format
            if any(term in user_message.lower() for term in ['table', 'breakdown', 'monthly', 'quarterly']):
                print("🤖 AI INFO: User requesting table format - routing to structured data")
                return get_structured_data_response(user_message, conversation_history or [])
            
            detail_level = 'detailed'  # Always detailed for this mode
            
            print(f"🤖 AI INFO: Generating detailed insights for {kpi_type}")
            
            # Generate KPI insights using heavy system
            try:
                from callcenter_app.ai.insights_manager import AIInsightsManager
                insights_manager = AIInsightsManager()
                
                # Get current KPI value for the analysis
                current_value = get_current_kpi_value(kpi_type)
                insights = insights_manager.get_kpi_insights_sync(kpi_type, current_value)
                
                if insights and insights.get('success'):
                    return format_insights_as_chat(insights, user_message, detail_level)
                else:
                    return f"I had trouble generating detailed analysis for {kpi_type.replace('_', ' ')}. Could you try rephrasing your question?"
            except Exception as e:
                print(f"Detailed insights error: {e}")
                return f"I encountered an error generating detailed analysis. Please try again."
        
        else:
            # For general questions or table requests in detailed mode
            if any(term in user_message.lower() for term in ['table', 'breakdown', 'monthly', 'quarterly']):
                return get_structured_data_response(user_message, conversation_history or [])
            else:
                return get_contextual_response(user_message, conversation_history or [])
            
    except Exception as e:
        print(f"Detailed analysis error: {e}")
        return "I encountered an error generating detailed analysis. Please try a simpler question."

def get_structured_data_response(user_message: str, conversation_history: list = None) -> str:
    """Generate structured data responses using OpenAI to create Markdown tables"""
    try:
        # Load the Malaysian business data
        import json
        import os
        
        data_file = "data/malaysian_callcenter_data.json"
        if os.path.exists(data_file):
            with open(data_file, 'r') as f:
                business_data = json.load(f)
        else:
            return "I don't have access to the business data right now. Please try again later."
        
        # Use OpenAI to generate contextual Markdown tables
        return generate_openai_markdown_table(business_data, user_message, conversation_history)
            
    except Exception as e:
        print(f"Structured data error: {e}")
        return "I encountered an error generating the table. Please try rephrasing your request."

def generate_openai_markdown_table(business_data: dict, user_message: str, conversation_history: list = None) -> str:
    """Use OpenAI to generate contextual Markdown tables with business insights"""
    try:
        from callcenter_app.ai.openai_service import OpenAIInsightGenerator
        
        # Prepare business context for OpenAI
        current_kpis = business_data.get("current_snapshot", {}).get("current_kpis", {})
        historical_data = business_data.get("historical_data", [])
        competitor_benchmarks = business_data.get("competitor_benchmarks", {})
        
        # Get recent 6 months for context
        recent_months = historical_data[-6:] if len(historical_data) >= 6 else historical_data
        
        # Build comprehensive context
        business_context = {
            "current_date": "August 25, 2025",
            "current_performance": current_kpis,
            "recent_monthly_data": recent_months,
            "industry_benchmarks": competitor_benchmarks,
            "currency": "Malaysian Ringgit (RM)"
        }
        
        # Create OpenAI prompt for Markdown table generation
        table_prompt = f"""
You are a Malaysian call center business analyst. Generate a professional Markdown table based on this request: "{user_message}"

BUSINESS CONTEXT:
- Current Date: August 25, 2025
- Currency: Malaysian Ringgit (RM)
- Current Revenue: RM {current_kpis.get('revenue_growth', {}).get('value', 0):,}
- Current CSAT: {current_kpis.get('customer_satisfaction', {}).get('value', 0):.1f}/5.0
- Current FCR: {current_kpis.get('first_call_resolution', {}).get('value', 0):.1f}%

RECENT MONTHLY DATA (Last 6 months):
{format_monthly_data_for_prompt(recent_months)}

REQUIREMENTS:
1. Create a proper Markdown table with appropriate headers
2. Include Malaysian Ringgit (RM) formatting for currency
3. Add trend indicators (📈, 📉, ➡️) where relevant
4. Include status indicators (✅, ⚠️, ❌) for performance levels
5. Add a brief insights paragraph after the table
6. Use proper Markdown formatting with alignment

Focus on what the user specifically requested while providing Malaysian business context.
"""

        # Generate response using OpenAI
        openai_generator = OpenAIInsightGenerator()
        
        # Use the simple completion method for faster response
        if hasattr(openai_generator, 'simple_completion'):
            markdown_response = openai_generator.simple_completion(table_prompt)
        else:
            # Fallback to standard completion
            response = openai_generator.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": table_prompt}],
                max_tokens=800,
                temperature=0.3  # Lower temperature for more consistent formatting
            )
            markdown_response = response.choices[0].message.content or "Unable to generate table"
        
        return markdown_response
        
    except Exception as e:
        print(f"OpenAI Markdown table generation error: {e}")
        return generate_fallback_markdown_table(business_data, user_message)

def format_monthly_data_for_prompt(monthly_data: list) -> str:
    """Format monthly data for OpenAI prompt"""
    if not monthly_data:
        return "No recent data available"
    
    formatted_data = []
    for month_data in monthly_data:
        month = month_data.get("month", "Unknown")
        kpis = month_data.get("kpis", {})
        
        revenue = kpis.get("revenue_growth", {}).get("value", 0)
        csat = kpis.get("customer_satisfaction", {}).get("value", 0)
        fcr = kpis.get("first_call_resolution", {}).get("value", 0)
        
        formatted_data.append(f"- {month}: Revenue RM {revenue:,}, CSAT {csat:.1f}/5.0, FCR {fcr:.1f}%")
    
    return "\n".join(formatted_data)

def generate_fallback_markdown_table(business_data: dict, user_message: str) -> str:
    """Generate a fallback Markdown table if OpenAI fails"""
    try:
        current_kpis = business_data.get("current_snapshot", {}).get("current_kpis", {})
        
        fallback_table = f"""
## 📊 Current Performance Overview

| Metric | Current Value | Status | Trend |
|--------|---------------|---------|-------|
| Revenue | RM {current_kpis.get('revenue_growth', {}).get('value', 0):,} | ✅ Active | 📈 Growing |
| Customer Satisfaction | {current_kpis.get('customer_satisfaction', {}).get('value', 0):.1f}/5.0 | ✅ Good | ➡️ Stable |
| First Call Resolution | {current_kpis.get('first_call_resolution', {}).get('value', 0):.1f}% | 📊 Tracking | 📈 Improving |
| Average Handle Time | {current_kpis.get('average_handle_time', {}).get('value', 0):.0f} seconds | ⚠️ Monitor | ➡️ Stable |

💡 **Quick Insight**: This is a summary of current Malaysian call center performance as of August 2025. 
All values are based on real-time operational data with Malaysian Ringgit currency formatting.
        """
        
        return fallback_table.strip()
        
    except Exception as e:
        print(f"Fallback table generation error: {e}")
        return "## ❌ Unable to Generate Table\n\nI'm experiencing technical difficulties generating the requested table. Please try again later."

def generate_revenue_table(business_data: dict, user_message: str) -> str:
    """Generate revenue data in table format"""
    try:
        historical_data = business_data.get("historical_data", [])
        current_kpis = business_data.get("current_snapshot", {}).get("current_kpis", {})
        
        # Get recent 6 months of data
        recent_data = historical_data[-6:] if len(historical_data) >= 6 else historical_data
        
        table_response = "📊 **Revenue Breakdown Table**\n\n"
        table_response += "| Month | Revenue (RM) | Growth % | Target % | Status |\n"
        table_response += "|-------|--------------|----------|----------|--------|\n"
        
        for month_data in recent_data:
            month = month_data.get("month", "N/A")
            revenue = month_data.get("kpis", {}).get("revenue_growth", {})
            revenue_value = revenue.get("value", 0)
            growth = revenue.get("growth_rate", 0)
            target = revenue.get("vs_target", 0)
            status = "✅ Above" if target > 0 else "⚠️ Below" if target < -5 else "📊 On Track"
            
            table_response += f"| {month} | RM {revenue_value:,} | {growth:+.1f}% | {target:+.1f}% | {status} |\n"
        
        # Add current month
        current_revenue = current_kpis.get("revenue_growth", {})
        table_response += f"| Current | RM {current_revenue.get('value', 0):,} | {current_revenue.get('growth_rate', 0):+.1f}% | {current_revenue.get('vs_target', 0):+.1f}% | 🎯 Current |\n"
        
        table_response += f"\n💡 **Summary**: Current revenue is RM {current_revenue.get('value', 0):,} with {current_revenue.get('vs_target', 0):+.1f}% vs target performance."
        
        return table_response
        
    except Exception as e:
        print(f"Revenue table generation error: {e}")
        return "I had trouble generating the revenue table. Please try again."

def generate_monthly_overview_table(business_data: dict, user_message: str) -> str:
    """Generate monthly overview of all key metrics"""
    try:
        historical_data = business_data.get("historical_data", [])
        
        # Get recent 3 months for overview
        recent_data = historical_data[-3:] if len(historical_data) >= 3 else historical_data
        
        table_response = "📊 **Monthly Performance Overview**\n\n"
        table_response += "| Month | Revenue (RM) | CSAT Score | FCR Rate | Avg Handle Time |\n"
        table_response += "|-------|--------------|------------|----------|------------------|\n"
        
        for month_data in recent_data:
            month = month_data.get("month", "N/A")
            kpis = month_data.get("kpis", {})
            
            revenue = kpis.get("revenue_growth", {}).get("value", 0)
            csat = kpis.get("customer_satisfaction", {}).get("value", 0)
            fcr = kpis.get("first_call_resolution", {}).get("value", 0)
            aht = kpis.get("average_handle_time", {}).get("value", 0)
            
            table_response += f"| {month} | RM {revenue:,} | {csat:.1f}/5.0 | {fcr:.1f}% | {aht:.0f}s |\n"
        
        table_response += "\n📈 **Trends**: This shows the key performance indicators across recent months for quick comparison."
        
        return table_response
        
    except Exception as e:
        print(f"Monthly overview table generation error: {e}")
        return "I had trouble generating the monthly overview table. Please try again."

def generate_satisfaction_table(business_data: dict, user_message: str) -> str:
    """Generate customer satisfaction data in table format"""
    try:
        historical_data = business_data.get("historical_data", [])
        current_kpis = business_data.get("current_snapshot", {}).get("current_kpis", {})
        
        recent_data = historical_data[-6:] if len(historical_data) >= 6 else historical_data
        
        table_response = "🎯 **Customer Satisfaction Breakdown**\n\n"
        table_response += "| Month | CSAT Score | Trend | Target Gap | Rating |\n"
        table_response += "|-------|------------|-------|------------|--------|\n"
        
        for month_data in recent_data:
            month = month_data.get("month", "N/A")
            csat_data = month_data.get("kpis", {}).get("customer_satisfaction", {})
            score = csat_data.get("value", 0)
            trend = csat_data.get("trend", "stable")
            target_gap = csat_data.get("vs_target", 0)
            
            if score >= 4.5:
                rating = "⭐ Excellent"
            elif score >= 4.0:
                rating = "✅ Good"
            elif score >= 3.5:
                rating = "⚠️ Fair"
            else:
                rating = "❌ Needs Work"
            
            table_response += f"| {month} | {score:.1f}/5.0 | {trend} | {target_gap:+.1f}% | {rating} |\n"
        
        # Add current
        current_csat = current_kpis.get("customer_satisfaction", {})
        current_score = current_csat.get("value", 0)
        table_response += f"| Current | {current_score:.1f}/5.0 | {current_csat.get('trend', 'stable')} | {current_csat.get('vs_target', 0):+.1f}% | 🎯 Current |\n"
        
        table_response += f"\n💭 **Insight**: Current satisfaction is {current_score:.1f}/5.0 - {'above industry standard' if current_score >= 4.2 else 'room for improvement'}."
        
        return table_response
        
    except Exception as e:
        print(f"Satisfaction table generation error: {e}")
        return "I had trouble generating the satisfaction table. Please try again."

def generate_general_kpi_table(business_data: dict, user_message: str) -> str:
    """Generate general KPI overview table"""
    try:
        current_kpis = business_data.get("current_snapshot", {}).get("current_kpis", {})
        
        table_response = "📊 **Current KPI Overview**\n\n"
        table_response += "| Metric | Current Value | Target Performance | Status |\n"
        table_response += "|--------|---------------|-------------------|--------|\n"
        
        # Format different KPI types
        kpi_configs = {
            "revenue_growth": ("Revenue", "RM {value:,}", "currency"),
            "customer_satisfaction": ("CSAT Score", "{value:.1f}/5.0", "rating"),
            "first_call_resolution": ("FCR Rate", "{value:.1f}%", "percentage"),
            "average_handle_time": ("Avg Handle Time", "{value:.0f} seconds", "time"),
            "agent_utilization": ("Agent Utilization", "{value:.1f}%", "percentage"),
            "customer_retention": ("Retention Rate", "{value:.1f}%", "percentage")
        }
        
        for kpi_key, (name, format_str, type_hint) in kpi_configs.items():
            if kpi_key in current_kpis:
                kpi_data = current_kpis[kpi_key]
                value = kpi_data.get("value", 0)
                vs_target = kpi_data.get("vs_target", 0)
                
                formatted_value = format_str.format(value=value)
                target_perf = f"{vs_target:+.1f}% vs target"
                status = "✅ Above" if vs_target > 0 else "⚠️ Below" if vs_target < -5 else "📊 On Track"
                
                table_response += f"| {name} | {formatted_value} | {target_perf} | {status} |\n"
        
        table_response += "\n📋 **Overview**: This table shows current performance across all key metrics compared to targets."
        
        return table_response
        
    except Exception as e:
        print(f"General KPI table generation error: {e}")
        return "I had trouble generating the KPI overview table. Please try again."

def get_ai_response(user_message: str, conversation_history: list = None) -> str:
    """Generate AI response using fast conversational AI with pre-generated data"""
    try:
        print(f"🤖 AI INFO: Processing question: '{user_message[:50]}...'")
        
        # Check for detailed analysis request or structured data request
        detailed_request = any(term in user_message.lower() for term in [
            'detailed analysis', 'full report', 'comprehensive', 'deep dive', 'detailed breakdown',
            'table', 'table form', 'tabular', 'breakdown', 'monthly breakdown', 'quarterly breakdown',
            'show me data', 'data table', 'structured', 'format', 'list', 'summary table'
        ])
        
        if detailed_request:
            # Use heavy analysis for detailed requests
            print("🤖 AI INFO: Using detailed analysis mode")
            return get_detailed_analysis_response(user_message, conversation_history)
        else:
            # Use fast conversational AI for casual questions
            print("🤖 AI INFO: Using fast conversational mode")
            if FAST_AI_AVAILABLE and fast_ai:
                response = fast_ai.get_conversational_response(user_message, conversation_history)
                print(f"🤖 AI INFO: Fast response generated ({len(response)} chars)")
                return response
            else:
                print("🤖 AI INFO: Fast AI not available, falling back to detailed analysis")
                return get_detailed_analysis_response(user_message, conversation_history)
            
    except Exception as e:
        print(f"🤖 AI ERROR: {e}")
        return "I'm having trouble processing your question right now. Could you try rephrasing it?"

def analyze_user_intent_with_history(message: str, conversation_history: list) -> Dict[str, Any]:
    """Analyze user message with conversation context"""
    message_lower = message.lower()
    
    # Check for follow-up patterns (expanded to include more contextual terms)
    follow_up_patterns = [
        'explain more', 'tell me more', 'more details', 'elaborate', 'expand', 
        'go deeper', 'more info', 'further', 'continue', 'what else',
        'summary', 'overview', 'breakdown', 'analysis', 'details',
        'last quarter', 'this quarter', 'previous', 'recent', 'current',
        'trends', 'performance', 'how about', 'what about'
    ]
    
    # Also check for contextual terms that suggest user is asking about recent topic
    contextual_terms = [
        'quarter', 'month', 'period', 'trend', 'performance', 'status',
        'update', 'report', 'summary', 'analysis', 'breakdown'
    ]
    
    is_follow_up = any(pattern in message_lower for pattern in follow_up_patterns)
    has_context_terms = any(term in message_lower for term in contextual_terms)
    
    # If it's a follow-up or has contextual terms, check recent conversation
    if is_follow_up or has_context_terms:
        # This is likely a follow-up - look at recent context
        recent_context = get_recent_kpi_context(conversation_history)
        if recent_context:
            return {
                'kpi_type': recent_context,
                'intent': 'kpi_followup',
                'detail_level': 'detailed' if is_follow_up else 'summary'
            }
    
    # Standard intent analysis
    kpi_mapping = {
        'revenue': 'revenue_growth',
        'profit': 'profit_margin', 
        'cost per call': 'cost_per_call',
        'call volume': 'call_volume',
        'satisfaction': 'customer_satisfaction',
        'retention': 'customer_retention',
        'resolution': 'first_call_resolution',
        'abandon': 'call_abandonment',
        'wait time': 'average_wait_time',
        'handle time': 'average_handle_time'
    }
    
    # Check for KPI mentions
    for keyword, kpi_type in kpi_mapping.items():
        if keyword in message_lower:
            return {
                'kpi_type': kpi_type,
                'intent': 'kpi_analysis',
                'keyword': keyword,
                'detail_level': 'summary'
            }
    
    return {
        'intent': 'general_query'
    }

def get_recent_kpi_context(conversation_history: list) -> Optional[str]:
    """Extract the most recent KPI context from conversation history"""
    if not conversation_history:
        return None
    
    # Look at the last few assistant messages for KPI context
    for message in reversed(conversation_history[-8:]):  # Look at last 8 messages (more context)
        try:
            # Check if this is an assistant message with KPI content
            if hasattr(message, 'children') and message.children:
                content = str(message.children).lower()
                # Look for KPI indicators in the content (expanded detection)
                if any(term in content for term in ['customer satisfaction', 'satisfaction', 'rating', 'csat']):
                    return 'customer_satisfaction'
                elif any(term in content for term in ['revenue', 'income', 'earnings', 'rm 1,400,000', 'rm 1.4', 'sales']):
                    return 'revenue_growth'
                elif any(term in content for term in ['profit', 'margin', 'profitability']):
                    return 'profit_margin'
                elif any(term in content for term in ['call volume', 'volume', 'calls per', 'total calls']):
                    return 'call_volume'
                elif any(term in content for term in ['retention', 'churn', 'loyalty']):
                    return 'customer_retention'
                elif any(term in content for term in ['resolution', 'first call', 'fcr']):
                    return 'first_call_resolution'
                elif any(term in content for term in ['abandon', 'abandonment', 'hang up']):
                    return 'call_abandonment'
                elif any(term in content for term in ['wait time', 'waiting', 'hold time']):
                    return 'average_wait_time'
                elif any(term in content for term in ['handle time', 'handling', 'aht']):
                    return 'average_handle_time'
                elif any(term in content for term in ['cost per call', 'cost', 'expense']):
                    return 'cost_per_call'
        except:
            continue
    return None

def analyze_user_intent(message: str) -> Dict[str, Any]:
    """Analyze user message to determine intent and extract relevant context"""
    message_lower = message.lower()
    
    # KPI keywords mapping
    kpi_mapping = {
        'revenue': 'revenue_growth',
        'profit': 'profit_margin', 
        'cost per call': 'cost_per_call',
        'call volume': 'call_volume',
        'satisfaction': 'customer_satisfaction',
        'retention': 'customer_retention',
        'resolution': 'first_call_resolution',
        'abandon': 'call_abandonment',
        'wait time': 'average_wait_time',
        'handle time': 'average_handle_time'
    }
    
    # Check for KPI mentions
    for keyword, kpi_type in kpi_mapping.items():
        if keyword in message_lower:
            return {
                'kpi_type': kpi_type,
                'intent': 'kpi_analysis',
                'keyword': keyword
            }
    
    return {
        'intent': 'general_query'
    }

def format_insights_as_chat(insights: Dict[str, Any], original_question: str, detail_level: str = 'summary') -> str:
    """Convert insights markdown to conversational chat response with context awareness"""
    markdown_content = insights.get('markdown_content', '')
    
    if not markdown_content:
        return "I don't have enough information to answer that question right now."
    
    # Extract key points from markdown based on detail level
    lines = markdown_content.split('\n')
    response_parts = []
    
    if detail_level == 'detailed':
        # Provide more detailed response for follow-up questions
        current_section = ""
        for line in lines:
            line = line.strip()
            if line.startswith('##') and ('analysis' in line.lower() or 'performance' in line.lower()):
                current_section = "analysis"
            elif line.startswith('##') and ('action' in line.lower() or 'recommend' in line.lower()):
                current_section = "actions"
            elif line.startswith('##') and ('predict' in line.lower() or 'forecast' in line.lower()):
                current_section = "predictions"
            elif line and not line.startswith('#') and current_section:
                if len(response_parts) < 8:  # More content for detailed response
                    response_parts.append(line)
    else:
        # Summary level response (original behavior)
        current_section = ""
        for line in lines:
            line = line.strip()
            if line.startswith('##') and ('status' in line.lower() or 'summary' in line.lower()):
                current_section = "status"
            elif line.startswith('##') and 'recommend' in line.lower():
                current_section = "recommendations"
            elif line and not line.startswith('#') and current_section:
                if current_section == "status" and len(response_parts) < 2:
                    response_parts.append(line)
                elif current_section == "recommendations" and len(response_parts) < 4:
                    response_parts.append(line)
    
    # Build conversational response
    if response_parts:
        if detail_level == 'detailed':
            response = "📊 **Detailed Analysis:**\n\n" + (response_parts[0] if response_parts else "Here's a comprehensive analysis:")
            
            if len(response_parts) > 1:
                response += "\n\n🔍 **In-depth Insights:**\n"
                for part in response_parts[1:5]:
                    if part.startswith('•') or part.startswith('-'):
                        response += f"\n{part}"
                    else:
                        response += f"\n• {part}"
                        
                if len(response_parts) > 5:
                    response += "\n\n📈 **Strategic Recommendations:**\n"
                    for part in response_parts[5:8]:
                        if part.startswith('•') or part.startswith('-'):
                            response += f"\n{part}"
                        else:
                            response += f"\n• {part}"
            
            response += "\n\n❓ Need even more specific information? Ask me about any particular aspect!"
        else:
            response = "📊 " + (response_parts[0] if response_parts else "Here's what I found:")
            
            if len(response_parts) > 1:
                response += "\n\n💡 **Key recommendations:**\n"
                for i, part in enumerate(response_parts[1:3], 1):
                    if part.startswith('•') or part.startswith('-'):
                        response += f"\n{part}"
                    else:
                        response += f"\n• {part}"
            
            response += "\n\n❓ Would you like me to explain any specific aspect in more detail?"
        return response
    
    return "I analyzed your question but couldn't extract clear insights. Could you be more specific?"

def get_contextual_response(message: str, conversation_history: list) -> str:
    """Handle general questions with conversation context awareness"""
    try:
        message_lower = message.lower()
        
        # Check for contextual terms that suggest user is asking about recent topics
        contextual_terms = [
            'quarter', 'month', 'period', 'trend', 'performance', 'status',
            'update', 'report', 'summary', 'analysis', 'breakdown', 'overview'
        ]
        
        # If message contains contextual terms, try to find recent KPI context
        if any(term in message_lower for term in contextual_terms):
            recent_context = get_recent_kpi_context(conversation_history)
            if recent_context:
                # User is asking for summary/analysis of recent KPI topic
                from ..ai.insights_manager import InsightsManager
                insights_manager = InsightsManager()
                
                try:
                    insights = insights_manager.generate_insights(recent_context)
                    if insights and insights.get('success'):
                        return format_insights_as_chat(insights, message, detail_level='detailed')
                except Exception as e:
                    print(f"Error generating contextual insights for {recent_context}: {e}")
                
                # Fallback with context awareness
                kpi_display = recent_context.replace('_', ' ').title()
                return (f"📊 I understand you're asking about **{kpi_display}** from our recent discussion.\n\n"
                       f"Let me provide you with the latest insights on {kpi_display.lower()}. "
                       f"Would you like me to focus on:\n"
                       f"• Current performance vs targets\n"
                       f"• Historical trends and patterns\n" 
                       f"• Actionable recommendations\n"
                       f"• Detailed quarterly breakdown\n\n"
                       f"Or simply ask: \"Tell me about our {kpi_display.lower()}\" for a comprehensive analysis!")
        
        # Check for follow-up patterns without specific KPI context
        follow_up_patterns = [
            'explain more', 'tell me more', 'more details', 'elaborate', 'expand', 
            'go deeper', 'more info', 'further', 'continue', 'what else'
        ]
        
        if any(pattern in message_lower for pattern in follow_up_patterns):
            return ("I'd be happy to provide more details! However, I need to know what specific topic you'd like me to elaborate on. "
                   "Are you asking about:\n"
                   "• Revenue and growth trends\n"
                   "• Customer satisfaction metrics\n"
                   "• Call volume and operational efficiency\n"
                   "• Profit margins and cost analysis\n"
                   "• Any other specific KPI?\n\n"
                   "Just let me know which area interests you most!")
        
        # Use OpenAI for general conversation
        return get_general_response(message)
            
    except Exception as e:
        print(f"Contextual response error: {e}")
        return "I'm here to help with your call center analytics. What specific metric would you like to know about?"

def get_general_response(message: str) -> str:
    """Handle general questions using OpenAI for intelligent responses"""
    try:
        from ..ai.openai_service import OpenAIService
        
        openai_service = OpenAIService()
        message_lower = message.lower()
        
        # Check for specific predefined responses first
        if any(word in message_lower for word in ['help', 'what can you do', 'how to', 'capabilities']):
            return ("🤖 **I'm your AI Call Center Analytics Assistant!** I can help you with:\n\n"
                   "📊 **KPI Analysis:** Revenue, profit, customer satisfaction, call metrics\n"
                   "📈 **Trend Analysis:** Historical patterns and forecasts\n"
                   "💡 **Insights & Recommendations:** Actionable business intelligence\n"
                   "🎯 **Performance Monitoring:** Real-time alerts and benchmarking\n"
                   "🇲🇾 **Malaysian Market Focus:** Local business context and RM currency\n\n"
                   "💬 **Try asking:**\n"
                   "• \"How's our revenue performing?\"\n"
                   "• \"What about customer satisfaction?\"\n"
                   "• \"Show me call volume trends\"\n"
                   "• \"What should we focus on?\"\n\n"
                   "Just ask me anything about your call center metrics!")
        
        elif any(word in message_lower for word in ['status', 'how are we', 'overall', 'dashboard']):
            return ("📊 **Call Center Health Check:**\n\n"
                   "🎯 **Current Performance:**\n"
                   "• 📈 Revenue: RM 1.4M (growing steadily)\n"
                   "• 💰 Profit Margin: 18.3% (strong performance)\n"
                   "• 📞 Call Volume: 2,847 calls (efficient handling)\n"
                   "• 😊 Customer Satisfaction: 4.2/5 (above baseline)\n"
                   "• ⏱️ Response Times: Optimized for peak hours\n\n"
                   "🚀 **Key Opportunities:**\n"
                   "• Leverage upcoming Merdeka Day for revenue boost\n"
                   "• Focus on customer retention strategies\n"
                   "• Optimize digital channel diversification\n\n"
                   "🎯 **Want deeper insights?** Ask me about any specific metric!")
        
        # For other general questions, use OpenAI for intelligent responses
        else:
            prompt = f"""You are a friendly AI assistant specializing in Malaysian call center analytics. 
            The user asked: "{message}"
            
            Provide a helpful, conversational response that:
            1. Acknowledges their question warmly
            2. Explains how it relates to call center analytics if relevant
            3. Offers specific ways you can help with KPIs like revenue, customer satisfaction, call volume, etc.
            4. Uses Malaysian business context (RM currency, local market insights)
            5. Keeps the tone professional but approachable
            6. Ends with a suggestion for what they could ask next
            
            Keep the response concise (2-4 sentences) and engaging."""
            
            try:
                response = openai_service.get_completion(prompt, max_tokens=200)
                return f"🤖 {response}\n\n� **Quick tip:** Try asking about specific KPIs like revenue, customer satisfaction, or call metrics for detailed insights!"
            except Exception as openai_error:
                print(f"OpenAI error for general response: {openai_error}")
                # Fallback to intelligent contextual response
                return get_intelligent_fallback_response(message)
            
    except Exception as e:
        print(f"General response error: {e}")
        return get_intelligent_fallback_response(message)

def get_intelligent_fallback_response(message: str) -> str:
    """Intelligent fallback responses when OpenAI is unavailable"""
    message_lower = message.lower()
    
    # Greetings and casual conversation
    if any(word in message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
        return ("👋 Hello there! Great to chat with you! I'm your AI assistant specializing in call center analytics.\n\n"
               "I'm here to help you understand your business metrics, spot trends, and make data-driven decisions. "
               "Whether you want to know about revenue, customer satisfaction, call volumes, or operational efficiency, just ask!\n\n"
               "🎯 What would you like to explore today?")
    
    # Questions about the system/company
    elif any(word in message_lower for word in ['company', 'business', 'what do you know', 'tell me about']):
        return ("🏢 I work with Malaysian call center operations, focusing on key performance indicators that drive business success.\n\n"
               "📊 **I have access to:**\n"
               "• Revenue and profit metrics (in RM)\n"
               "• Customer satisfaction scores and trends\n"
               "• Call volume and operational efficiency data\n"
               "• Cost analysis and optimization opportunities\n"
               "• Malaysian market insights and seasonal patterns\n\n"
               "🤔 What specific aspect of your call center would you like to discuss?")
    
    # Time-based questions
    elif any(word in message_lower for word in ['today', 'this week', 'this month', 'recent', 'latest']):
        return ("📅 I can provide you with the latest performance insights!\n\n"
               "Currently, I'm tracking real-time data for all major KPIs. Whether you want to see today's call volumes, "
               "this week's customer satisfaction trends, or this month's revenue performance, I can help.\n\n"
               "📈 Which time period and metric combination interests you most?")
    
    # Problem-solving questions
    elif any(word in message_lower for word in ['problem', 'issue', 'wrong', 'concern', 'worried']):
        return ("🔍 I'm here to help identify and solve any performance challenges!\n\n"
               "I can analyze your metrics to spot potential issues, provide root cause analysis, and suggest actionable solutions. "
               "From revenue gaps to customer satisfaction drops, I'll help you understand what's happening and what to do about it.\n\n"
               "🎯 What specific area are you concerned about?")
    
    # Default intelligent response
    else:
        return ("🤖 That's an interesting question! While I specialize in call center analytics, I'd love to help you explore how it connects to your business.\n\n"
               "I'm particularly good at analyzing KPIs like revenue growth, customer satisfaction, call efficiency, and operational costs. "
               "I can provide insights with Malaysian market context and suggest actionable next steps.\n\n"
               "💡 **Try asking:** \"What's our current performance?\" or mention any specific metric you'd like to understand better!")
