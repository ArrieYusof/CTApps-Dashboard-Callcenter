# Version: 0.1
# Last Modified: 2025-08-24
# Changes: AI insights coordinator combining RAG and OpenAI for contextual analytics
"""
AI Insights Manager - Orchestrates RAG + OpenAI for Call Center Analytics
Main interface for generating contextual AI insights for KPI details
"""
import asyncio
from typing import Dict, Any, Optional
from .rag_engine import RAGEngine
from .openai_service import OpenAIInsightGenerator

class AIInsightsManager:
    """Main orchestrator for AI-powered KPI insights"""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize AI insights manager with RAG engine and OpenAI service"""
        self.rag_engine = RAGEngine()
        
        try:
            self.openai_service = OpenAIInsightGenerator(openai_api_key)
            self.ai_enabled = True
        except ValueError:
            # OpenAI not available, use fallback mode
            self.openai_service = None
            self.ai_enabled = False
            print("Warning: OpenAI API key not found. AI insights will use fallback mode.")
    
    async def get_kpi_insights(self, kpi_type: str, current_value: Any, additional_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Get comprehensive AI insights for a KPI"""
        try:
            # Step 1: RAG - Retrieve relevant context
            rag_context = self.rag_engine.retrieve_context_for_kpi(kpi_type, current_value)
            
            # Add any additional context provided
            if additional_context:
                rag_context.update(additional_context)
            
            # Step 2: Generate AI insights if available
            if self.ai_enabled and self.openai_service:
                ai_insights = await self.openai_service.generate_kpi_insights(rag_context)
            else:
                ai_insights = self._get_enhanced_fallback_insights(rag_context)
            
            # Step 3: Combine RAG context with AI insights
            return {
                'kpi_type': kpi_type,
                'current_value': current_value,
                'ai_insights': ai_insights,
                'context_data': rag_context,
                'ai_enabled': self.ai_enabled,
                'timestamp': rag_context.get('timestamp')
            }
            
        except Exception as e:
            return {
                'kpi_type': kpi_type,
                'current_value': current_value,
                'error': str(e),
                'ai_insights': self._get_error_fallback(kpi_type),
                'ai_enabled': False
            }
    
    def get_kpi_insights_sync(self, kpi_type: str, current_value: Any, additional_context: Optional[Dict] = None) -> Dict[str, Any]:
        """Synchronous version for non-async contexts - Returns Markdown content"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Extract AI enabled flag from additional_context
        ai_enabled = (additional_context or {}).get('ai_enabled', True)
        
        print(f"🤖 AI INFO: Starting insights generation for {kpi_type}")
        print(f"🤖 AI INFO: Current value: {current_value}, AI enabled: {ai_enabled}")
        
        try:
            # Step 1: RAG - Retrieve relevant context (this is synchronous)
            # Get contextual data from RAG
            print(f"🤖 AI INFO: Retrieving RAG context for {kpi_type}...")
            context_data = self.rag_engine.retrieve_context_for_kpi(kpi_type, current_value)
            print(f"🤖 AI INFO: RAG context retrieved - {len(context_data)} context items")
            
            # Add any additional context provided
            if additional_context:
                context_data.update(additional_context)
            
            # Step 2: Generate AI insights in markdown format
            if ai_enabled:
                try:
                    print(f"🤖 AI INFO: Sending query to OpenAI for {kpi_type}...")
                    print(f"🤖 AI INFO: OpenAI Request - KPI: {kpi_type}, Value: {current_value}")
                    
                    # Build context for OpenAI
                    openai_context = {
                        'kpi_type': kpi_type,
                        'current_value': current_value,
                        **context_data  # Include RAG context
                    }
                    
                    result = self.openai_service.generate_markdown_insights(openai_context)
                    markdown_content = result.get('markdown_content', '')
                    
                    if result.get('success') and markdown_content and markdown_content.strip():
                        print(f"🤖 AI INFO: ✅ OpenAI response received ({len(markdown_content)} chars)")
                        print(f"🤖 AI INFO: OpenAI Response Preview: {markdown_content[:200]}...")
                        
                        return {
                            'success': True,
                            'kpi_type': kpi_type,
                            'current_value': current_value,
                            'markdown_content': markdown_content,
                            'source': 'openai_markdown',
                            'ai_enabled': True,
                            'timestamp': timestamp,
                            'context_data': context_data
                        }
                    else:
                        print(f"🤖 AI INFO: ⚠️ OpenAI returned empty response or failed")
                    
                except Exception as openai_error:
                    print(f"🤖 AI INFO: ❌ OpenAI error for {kpi_type}: {str(openai_error)}")
                    # Fall through to RAG fallback
            
            # Fallback to RAG-only markdown generation
            print(f"🤖 AI INFO: Falling back to RAG-only analysis...")
            markdown_content = self._generate_rag_markdown(kpi_type, current_value, context_data)
            print(f"🤖 AI INFO: ✅ RAG fallback generated ({len(markdown_content)} chars)")
            
            return {
                'success': True,
                'kpi_type': kpi_type,
                'current_value': current_value,
                'markdown_content': markdown_content,
                'source': 'rag_fallback' if ai_enabled else 'rag_only',
                'ai_enabled': ai_enabled,
                'timestamp': timestamp,
                'context_data': context_data
            }
            
        except Exception as e:
            print(f"🤖 AI INFO: ❌ Critical error getting insights for {kpi_type}: {str(e)}")
            return self._generate_error_markdown(kpi_type, str(e), timestamp)
    
    def _generate_rag_markdown(self, kpi_type: str, current_value: Any, context: Dict[str, Any]) -> str:
        """Generate markdown insights using RAG data only"""
        kpi_display = kpi_type.replace('_', ' ').title()
        comparative = context.get('comparative_metrics', {})
        patterns = context.get('relevant_patterns', [])
        practices = context.get('best_practices', [])
        
        # Generate status assessment
        status = self._generate_status_from_data(kpi_type, current_value, comparative)
        trends = self._generate_trends_from_data(context.get('historical_trends', []))
        risks = self._assess_risks_from_data(kpi_type, current_value, comparative)
        
        markdown_content = f"""# 📊 {kpi_display} Analysis - {current_value}

## 🔍 Current Status
{status}

## 📈 Trend Analysis  
{trends}

{f"**Key Patterns Observed:**" if patterns else ""}
{chr(10).join(f"- {pattern}" for pattern in patterns[:3]) if patterns else ""}

## 💡 Recommendations
{chr(10).join(f"{i+1}. **{practice.split('.')[0] if '.' in practice else 'Action'}**: {practice}" for i, practice in enumerate(practices[:3])) if practices else "1. **Monitor**: Continue standard monitoring procedures"}

## 🔮 Predictions (Next 2-4 Hours)
🟡 **Based on historical patterns** - {f"Expected continuation of current trend" if trends else "Standard operational patterns expected"}

## ⚠️ Risk Assessment  
{risks}

---
*Analysis generated using enhanced historical data*
"""
        
        return markdown_content
    
    def _generate_error_markdown(self, kpi_type: str, error: str, timestamp: str) -> Dict[str, Any]:
        """Generate error state response with markdown"""
        kpi_display = kpi_type.replace('_', ' ').title()
        
        markdown_content = f"""# 📊 {kpi_display} Analysis Error

## ⚠️ Service Unavailable

AI insights are temporarily unavailable due to a system error.

## 📋 Manual Analysis Required
- **KPI Type**: {kpi_display}
- **Status**: Review manually using operational procedures
- **Action**: Contact system administrator if issue persists

## 🔧 Troubleshooting
```
Error: {error[:100]}{'...' if len(error) > 100 else ''}
Timestamp: {timestamp}
```

---
*Please try again later or contact support if the problem persists*
"""

        return {
            'success': False,
            'kpi_type': kpi_type,
            'current_value': 'N/A',
            'markdown_content': markdown_content,
            'source': 'error',
            'ai_enabled': False,
            'timestamp': timestamp,
            'error': error
        }
    
    def _get_sync_openai_insights(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Get OpenAI insights synchronously"""
        try:
            prompt = self._build_insight_prompt(context)
            response = self.openai_service._call_openai_sync(prompt)
            insights = self.openai_service._parse_insights_response(response, context['kpi_type'])
            
            return {
                'status': insights.get('status', 'Analysis complete'),
                'trends': insights.get('trends', 'Trend analysis available'),
                'recommendations': insights.get('recommendations', ['Review performance metrics']),
                'predictions': insights.get('predictions', 'Predictions based on current trends'),
                'risks': insights.get('risks', 'Standard monitoring recommended')
            }
        except Exception as e:
            return self._get_enhanced_fallback_insights(context)['insights']
    
    def _build_insight_prompt(self, context: Dict[str, Any]) -> str:
        """Build contextual prompt for OpenAI based on RAG data"""
        kpi_type = context['kpi_type']
        current_value = context['current_value']
        
        prompt = f"""
You are an expert call center analytics AI. Analyze this {kpi_type} data and provide actionable insights.

CURRENT METRICS:
- KPI: {kpi_type}
- Current Value: {current_value}
- Timestamp: {context.get('timestamp', 'N/A')}

COMPARATIVE METRICS:
{context.get('comparative_metrics', {})}

KNOWN PATTERNS:
{chr(10).join(f"• {pattern}" for pattern in context.get('relevant_patterns', []))}

Provide:
1. CURRENT STATUS: Brief assessment
2. TREND ANALYSIS: What trends indicate
3. ACTIONABLE RECOMMENDATIONS: 2-3 specific actions
4. PREDICTIONS: Next 2-4 hours
5. RISK ASSESSMENT: Potential issues

Keep responses concise and actionable.
"""
        return prompt
    
    def _get_enhanced_fallback_insights(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Enhanced fallback using RAG data when OpenAI is unavailable"""
        kpi_type = context['kpi_type']
        current_value = context['current_value']
        comparative = context.get('comparative_metrics', {})
        patterns = context.get('relevant_patterns', [])
        practices = context.get('best_practices', [])
        
        # Generate insights based on available data
        insights = {
            'success': True,
            'source': 'rag_fallback',
            'insights': {
                'status': self._generate_status_from_data(kpi_type, current_value, comparative),
                'trends': self._generate_trends_from_data(context.get('historical_trends', [])),
                'recommendations': practices[:3] if practices else [f"Monitor {kpi_type} closely"],
                'predictions': f"Based on patterns: {patterns[0] if patterns else 'Normal operations expected'}",
                'risks': self._assess_risks_from_data(kpi_type, current_value, comparative)
            }
        }
        
        return insights
    
    def _generate_status_from_data(self, kpi_type: str, current: Any, comparative: Dict) -> str:
        """Generate status assessment from comparative data"""
        if not comparative:
            return f"Current {kpi_type}: {current} (baseline assessment)"
        
        # Simple rule-based assessment
        if 'monthly_average' in comparative:
            avg = comparative['monthly_average']
            if isinstance(current, (int, float)) and isinstance(avg, (int, float)):
                if current > avg * 1.1:
                    return f"Above average performance: {current} vs {avg:.1f} average"
                elif current < avg * 0.9:
                    return f"Below average performance: {current} vs {avg:.1f} average"
                else:
                    return f"Normal performance: {current} near {avg:.1f} average"
        
        return f"Current {kpi_type}: {current}"
    
    def _generate_trends_from_data(self, historical: list) -> str:
        """Generate trend analysis from historical data"""
        if not historical or len(historical) < 2:
            return "Insufficient data for trend analysis"
        
        try:
            recent = historical[-3:]  # Last 3 data points
            if all(isinstance(x, (int, float)) for x in recent):
                if recent[-1] > recent[0] * 1.05:
                    return f"Upward trend: {recent[0]:.1f} → {recent[-1]:.1f}"
                elif recent[-1] < recent[0] * 0.95:
                    return f"Downward trend: {recent[0]:.1f} → {recent[-1]:.1f}"
                else:
                    return f"Stable trend: {recent[0]:.1f} → {recent[-1]:.1f}"
        except:
            pass
        
        return "Mixed trend - review historical data"
    
    def _assess_risks_from_data(self, kpi_type: str, current: Any, comparative: Dict) -> str:
        """Assess risks based on current performance vs targets"""
        risk_thresholds = {
            'call_volume': {'high': 3000, 'target_field': 'monthly_average'},
            'customer_satisfaction': {'low': 3.5, 'target_field': 'company_target'},
            'sla_monitoring': {'low': 85.0, 'target_field': 'target_sla'},
            'agent_performance': {'low': 75.0, 'target_field': 'team_average'},
            'queue_status': {'high': 50, 'target_field': 'average_queue'}
        }
        
        if kpi_type not in risk_thresholds:
            return "Standard monitoring recommended"
        
        thresholds = risk_thresholds[kpi_type]
        
        try:
            if isinstance(current, (int, float)):
                if 'high' in thresholds and current > thresholds['high']:
                    return f"⚠️ High risk: {current} exceeds normal range"
                elif 'low' in thresholds and current < thresholds['low']:
                    return f"⚠️ Performance risk: {current} below acceptable threshold"
        except:
            pass
        
        return "Normal risk level - continue monitoring"
    
    def _get_basic_insights(self, kpi_type: str, current_value: Any) -> Dict[str, Any]:
        """Most basic fallback insights"""
        return {
            'kpi_type': kpi_type,
            'current_value': current_value,
            'ai_insights': {
                'success': False,
                'insights': {
                    'status': f"Current {kpi_type}: {current_value}",
                    'recommendations': ["Manual analysis recommended", "Review historical trends", "Consult operational guidelines"],
                    'risks': "Standard monitoring procedures apply"
                }
            },
            'ai_enabled': False,
            'source': 'basic_fallback'
        }
    
    def _get_error_fallback(self, kpi_type: str) -> Dict[str, Any]:
        """Error state fallback"""
        return {
            'success': False,
            'error': 'AI insights temporarily unavailable',
            'insights': {
                'status': 'Analysis service unavailable',
                'recommendations': ['Use manual procedures', 'Contact system administrator'],
                'risks': 'Enhanced manual monitoring recommended'
            }
        }
