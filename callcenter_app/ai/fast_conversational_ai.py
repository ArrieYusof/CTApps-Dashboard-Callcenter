"""
Fast Conversational AI Service for Malaysian Call Center
Uses pre-generated data for lightning-fast responses
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

class FastBusinessAI:
    def __init__(self):
        self.data_file = "data/malaysian_callcenter_data.json"
        self.business_data = self._load_business_data()
        self.current_kpis = self.business_data.get("current_snapshot", {}).get("current_kpis", {})
        self.historical_data = self.business_data.get("historical_data", [])
        self.future_projections = self.business_data.get("future_projections", [])
        self.competitor_benchmarks = self.business_data.get("competitor_benchmarks", {})
        
    def _load_business_data(self) -> Dict[str, Any]:
        """Load pre-generated business data"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                print(f"⚠️ Data file not found: {self.data_file}")
                return {}
        except Exception as e:
            print(f"❌ Error loading business data: {e}")
            return {}
    
    def get_conversational_response(self, user_message: str, conversation_history: Optional[List] = None) -> str:
        """Generate fast conversational response using pre-generated data"""
        try:
            from callcenter_app.ai.openai_service import OpenAIService
            
            # Prepare lightweight business context
            business_context = self._prepare_context(user_message)
            
            # Create conversational system prompt
            system_prompt = self._create_system_prompt(business_context)
            
            # Prepare conversation context
            recent_messages = self._format_conversation_history(conversation_history or [])
            
            # Generate conversational response
            openai_service = OpenAIService()
            
            # Use the simple completion method for speed
            full_prompt = f"{system_prompt}\n\nUser: {user_message}"
            
            if hasattr(openai_service, 'simple_completion'):
                response = openai_service.simple_completion(full_prompt)
            else:
                # Fallback to basic OpenAI call
                response = self._fallback_openai_call(full_prompt)
            
            return response
            
        except Exception as e:
            print(f"Fast AI Error: {e}")
            return self._get_fallback_response(user_message)
    
    def _prepare_context(self, user_message: str) -> Dict[str, Any]:
        """Prepare relevant business context based on user question"""
        message_lower = user_message.lower()
        
        # Smart context selection for speed
        context = {
            "current_date": "August 25, 2025",
            "malaysian_context": True,
            "currency": "RM"
        }
        
        # Add relevant KPI data based on question
        if any(term in message_lower for term in ['revenue', 'sales', 'income', 'money', 'rm']):
            context["revenue"] = self.current_kpis.get("revenue_growth", {})
            context["monthly_revenue"] = self._get_recent_monthly_data("revenue_growth", 6)
            
            # Check for quarterly requests  
            if any(term in message_lower for term in ['quarter', 'quarterly', 'q1', 'q2', 'q3', 'q4', 'last quarter']):
                # Determine which quarter to get (default to last completed quarter)
                current_month = 8  # August (current date from metadata)
                if current_month <= 3:
                    quarter_year, quarter_num = 2024, 4  # Previous Q4
                elif current_month <= 6:
                    quarter_year, quarter_num = 2025, 1  # Q1 2025
                elif current_month <= 9:
                    quarter_year, quarter_num = 2025, 2  # Q2 2025 (last completed)
                else:
                    quarter_year, quarter_num = 2025, 3  # Q3 2025
                    
                context["quarterly_data"] = self._get_quarterly_data(quarter_year, quarter_num)
                context["is_quarterly_request"] = True
            
        if any(term in message_lower for term in ['satisfaction', 'happy', 'customer', 'rating']):
            context["satisfaction"] = self.current_kpis.get("customer_satisfaction", {})
            context["satisfaction_trend"] = self._get_recent_monthly_data("customer_satisfaction", 3)
            
        if any(term in message_lower for term in ['call', 'volume', 'busy', 'traffic']):
            context["call_volume"] = self.current_kpis.get("call_volume", {})
            
        if any(term in message_lower for term in ['cost', 'expense', 'budget', 'spend']):
            context["cost_per_call"] = self.current_kpis.get("cost_per_call", {})
            
        # Add competitive context if requested
        if any(term in message_lower for term in ['competitor', 'industry', 'benchmark', 'compare']):
            context["benchmarks"] = self.competitor_benchmarks.get("industry_average", {})
            
        # Add monthly breakdown for detailed requests
        if any(term in message_lower for term in ['month', 'breakdown', 'detail', 'history', 'trend']):
            context["monthly_data"] = self._get_recent_monthly_data("revenue_growth", 12)
            context["projections"] = self.future_projections[:3]  # Next 3 months
            
        return context
    
    def _get_recent_monthly_data(self, kpi_name: str, months: int = 6) -> List[Dict[str, Any]]:
        """Get recent monthly data for specific KPI"""
        recent_data = []
        
        # Get from historical data
        for month_data in self.historical_data[-months:]:
            if kpi_name in month_data.get("kpis", {}):
                recent_data.append({
                    "month": month_data.get("month_name", ""),
                    "date": month_data.get("date", ""),
                    "value": month_data["kpis"][kpi_name].get("value", 0),
                    "seasonal_factor": month_data["kpis"][kpi_name].get("seasonal_factor", "")
                })
        
        return recent_data
    
    def _get_quarterly_data(self, year: int, quarter: int) -> Dict[str, Any]:
        """Get quarterly aggregated data"""
        # Define quarter months
        quarter_months = {
            1: ['01', '02', '03'],  # Q1: Jan, Feb, Mar
            2: ['04', '05', '06'],  # Q2: Apr, May, Jun  
            3: ['07', '08', '09'],  # Q3: Jul, Aug, Sep
            4: ['10', '11', '12']   # Q4: Oct, Nov, Dec
        }
        
        if quarter not in quarter_months:
            return {}
            
        target_months = [f"{year}-{month}" for month in quarter_months[quarter]]
        quarterly_data = []
        
        # Get data for the quarter months
        for month_data in self.historical_data:
            month_date = month_data.get("date", "")[:7]  # Get YYYY-MM part
            if month_date in target_months:
                quarterly_data.append(month_data)
        
        if not quarterly_data:
            return {}
            
        # Calculate quarterly totals/averages
        total_revenue = sum(month.get("kpis", {}).get("revenue_growth", {}).get("value", 0) 
                          for month in quarterly_data)
        avg_satisfaction = sum(month.get("kpis", {}).get("customer_satisfaction", {}).get("value", 0) 
                             for month in quarterly_data) / len(quarterly_data)
        total_calls = sum(month.get("kpis", {}).get("call_volume", {}).get("value", 0) 
                        for month in quarterly_data)
        
        # Calculate targets and variances
        revenue_targets = [month.get("kpis", {}).get("revenue_growth", {}).get("vs_target", 0) 
                          for month in quarterly_data]
        avg_vs_target = sum(revenue_targets) / len(revenue_targets) if revenue_targets else 0
        
        return {
            "quarter": f"Q{quarter} {year}",
            "months": [month.get("month_name", "") for month in quarterly_data],
            "total_revenue": total_revenue,
            "avg_satisfaction": avg_satisfaction,
            "total_calls": total_calls,
            "avg_vs_target": avg_vs_target,
            "monthly_breakdown": quarterly_data
        }
    
    def _create_system_prompt(self, context: Dict[str, Any]) -> str:
        """Create system prompt for conversational AI"""
        
        base_prompt = """You are a friendly, knowledgeable Malaysian call center business analyst having a natural conversation with a manager. 

Key Guidelines:
- Speak conversationally like a professional colleague, not a formal report
- Use RM currency and Malaysian business context
- Be insightful but casual unless detailed analysis is requested
- Reference real data and seasonal patterns when relevant
- Ask follow-up questions to keep conversation engaging
- Be transparent about data limitations while providing valuable insights

Malaysian Context:
- Business hours: 9AM-6PM MYT
- Current date: August 25, 2025
- Merdeka Day coming up (Aug 31) - patriotic spending period
- Call center industry is competitive with digital transformation focus"""

        # Add relevant business data to prompt
        if "quarterly_data" in context and context["quarterly_data"]:
            quarterly = context["quarterly_data"]
            base_prompt += f"\n\n{quarterly.get('quarter', 'Quarter')} Performance:"
            base_prompt += f"\n- Total Revenue: RM {quarterly.get('total_revenue', 0):,.0f}"
            base_prompt += f"\n- Performance vs Target: {quarterly.get('avg_vs_target', 0):+.1f}%"
            base_prompt += f"\n- Months included: {', '.join(quarterly.get('months', []))}"
            base_prompt += f"\n- Customer Satisfaction: {quarterly.get('avg_satisfaction', 0):.1f}/5.0"
            
        elif "revenue" in context:
            revenue_data = context["revenue"]
            base_prompt += f"\n\nCurrent Revenue: RM {revenue_data.get('value', 0):,} ({revenue_data.get('vs_target', 0):+.1f}% vs target)"
            
        if "satisfaction" in context:
            sat_data = context["satisfaction"]
            base_prompt += f"\nCustomer Satisfaction: {sat_data.get('value', 0)}/5.0 ({sat_data.get('trend', 'stable')} trend)"
            
        if "monthly_data" in context and context["monthly_data"]:
            base_prompt += f"\nRecent monthly performance available for detailed discussions"
            
        if "benchmarks" in context:
            benchmark = context["benchmarks"]
            base_prompt += f"\nIndustry average revenue: RM {benchmark.get('revenue_per_month', 0):,}"
        
        base_prompt += "\n\nRespond naturally as if chatting with a colleague about the business."
        
        return base_prompt
    
    def _format_conversation_history(self, conversation_history: List) -> str:
        """Format recent conversation for context"""
        if not conversation_history:
            return ""
        
        # Get last few messages for context
        recent_messages = conversation_history[-4:]  # Last 4 messages for speed
        formatted = "\n\nRecent conversation:\n"
        
        for msg in recent_messages:
            # Simple message extraction
            try:
                if hasattr(msg, 'children') and msg.children:
                    content = str(msg.children)[:200]  # Limit length
                    formatted += f"- {content}\n"
            except:
                continue
                
        return formatted
    
    def _fallback_openai_call(self, prompt: str) -> str:
        """Fallback OpenAI API call if service unavailable"""
        try:
            from callcenter_app.ai.openai_service import OpenAIService
            openai_service = OpenAIService()
            
            # Use the OpenAI service's method directly
            response = openai_service.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,  # Shorter for speed
                temperature=0.7
            )
            
            return response.choices[0].message.content or "I'm having trouble generating a response right now."
            
        except Exception as e:
            print(f"OpenAI fallback error: {e}")
            return self._get_fallback_response("general")
    
    def _get_fallback_response(self, user_message: str) -> str:
        """Generate fallback response when AI services are unavailable"""
        message_lower = user_message.lower()
        
        if any(term in message_lower for term in ['revenue', 'money', 'rm']):
            revenue = self.current_kpis.get("revenue_growth", {}).get("value", 1400000)
            return f"Looking at our revenue, we're currently at RM {revenue:,}. We've been tracking steady growth with some seasonal variations. What specific aspect would you like to dive into?"
            
        elif any(term in message_lower for term in ['satisfaction', 'customer', 'happy']):
            satisfaction = self.current_kpis.get("customer_satisfaction", {}).get("value", 4.2)
            return f"Customer satisfaction is sitting at {satisfaction}/5.0 right now. We've seen some interesting patterns tied to our seasonal business cycles. Want to explore what's driving the current rating?"
            
        elif any(term in message_lower for term in ['call', 'volume']):
            volume = self.current_kpis.get("call_volume", {}).get("value", 8500)
            return f"Call volume is averaging around {volume:,} calls per month, with peak hours typically 9AM-11AM and 2PM-4PM MYT. How can I help you analyze the volume patterns?"
            
        else:
            return ("I'm here to chat about our call center performance! I have all the latest data on revenue, customer satisfaction, call volumes, and more. "
                   "With Merdeka Day coming up, there might be some interesting trends to discuss. What would you like to explore?")

# Create global instance for fast access
fast_ai = FastBusinessAI()
