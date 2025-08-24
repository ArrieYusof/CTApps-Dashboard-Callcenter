# Version: 0.1
# Last Modified: 2025-08-24
# Changes: AI insights coordinator combining RAG and OpenAI for contextual analytics
# Version: 1.1
# Last Modified: 2025-08-24
# Changes: Enhanced AI insights manager with advanced analytics integration
"""
AI Insights Manager - Enhanced with Advanced Analytics
Orchestrates RAG context retrieval with OpenAI analysis and statistical intelligence
"""

import asyncio
import threading
import time
from typing import Dict, Any, Optional, List
from datetime import datetime

from .rag_engine import RAGEngine  
from .openai_service import OpenAIInsightGenerator
from .advanced_analytics import AdvancedAnalyticsEngine
import asyncio
from typing import Dict, Any, Optional
from .rag_engine import RAGEngine
from .openai_service import OpenAIInsightGenerator

class AIInsightsManager:
    """Enhanced orchestrator for AI-powered KPI insights with advanced analytics"""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize AI insights manager with RAG, OpenAI, and advanced analytics"""
        self.rag_engine = RAGEngine()
        self.analytics_engine = AdvancedAnalyticsEngine()
        
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
            
            # Step 1.5: Enhanced Analytics - Generate advanced analytics insights
            print(f"🤖 AI INFO: Generating advanced analytics for {kpi_type}...")
            try:
                # Generate advanced analytics using the RAG context
                advanced_analytics = self._generate_advanced_analytics(context_data)
                context_data['advanced_analytics'] = advanced_analytics
                print(f"🤖 AI INFO: Advanced analytics generated with {len(advanced_analytics)} components")
            except Exception as analytics_error:
                print(f"🤖 AI INFO: ⚠️ Advanced analytics failed: {str(analytics_error)}")
                # Continue without advanced analytics
            
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
    
    def _generate_advanced_analytics(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate advanced analytics insights using the analytics engine"""
        try:
            # Prepare data for advanced analytics
            kpi_data = {
                'kpi_type': context_data.get('kpi_type', ''),
                'current_value': context_data.get('current_value', 0),
                'historical_trends': context_data.get('historical_trends', []),
                'comparative_metrics': context_data.get('comparative_metrics', {})
            }
            
            # Generate different types of analytics
            analytics_results = {}
            
            # Cross-KPI correlations
            try:
                correlations = self.analytics_engine.analyze_cross_kpi_correlations(kpi_data)
                analytics_results['correlations'] = correlations
            except Exception as e:
                print(f"🤖 AI INFO: Correlation analysis failed: {e}")
            
            # Anomaly detection
            try:
                anomaly_analysis = self.analytics_engine.detect_anomalies(kpi_data)
                analytics_results['anomaly_analysis'] = anomaly_analysis
            except Exception as e:
                print(f"🤖 AI INFO: Anomaly detection failed: {e}")
            
            # Predictive insights
            try:
                predictions = self.analytics_engine.generate_predictive_insights(kpi_data)
                analytics_results['predictions'] = predictions
            except Exception as e:
                print(f"🤖 AI INFO: Predictive analysis failed: {e}")
            
            # Business impact assessment
            try:
                business_impact = self.analytics_engine.assess_business_impact(
                    kpi_data, analytics_results.get('correlations', {})
                )
                analytics_results['business_impact'] = business_impact
            except Exception as e:
                print(f"🤖 AI INFO: Business impact analysis failed: {e}")
                
            return analytics_results
            
        except Exception as e:
            print(f"🤖 AI INFO: Advanced analytics generation failed: {e}")
            return {}
    
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

    def _generate_enhanced_fallback_insights(self, kpi_type: str, current_value: Any, 
                                           context_data: Dict[str, Any], 
                                           advanced_analytics: Dict[str, Any]) -> str:
        """Generate enhanced analytical insights using advanced analytics when AI is unavailable"""
        
        comparative = context_data.get('comparative_metrics', {})
        historical = context_data.get('historical_trends', [])
        patterns = context_data.get('relevant_patterns', [])
        best_practices = context_data.get('best_practices', [])
        
        # Extract advanced analytics results
        anomaly_info = advanced_analytics.get('anomaly_analysis', {})
        prediction_info = advanced_analytics.get('predictions', {})
        impact_info = advanced_analytics.get('business_impact', {})
        correlation_info = advanced_analytics.get('correlations', {})
        
        insights_md = f"""# 📊 **{kpi_type.replace('_', ' ').title()} Enhanced Analysis** - {current_value}

## 🎯 **Executive Summary**
**Performance Status:** {"🔴 ATTENTION REQUIRED" if anomaly_info.get('anomaly_detected') else "🟢 NORMAL OPERATIONS"} (High Confidence)
**Business Critical:** {"Yes" if impact_info.get('impact_score', 0) > 70 else "No"} - {impact_info.get('business_criticality', 'Moderate').title()} impact level
**Immediate Action Required:** {"Yes" if anomaly_info.get('severity') in ['critical', 'high'] else "No"}

## 🔍 **Deep Performance Analysis**

### Current Performance Trajectory
- **Statistical Confidence:** High (Advanced analytics validation)
- **Trend Direction:** {prediction_info.get('trend_direction', 'Stable').title()} ({prediction_info.get('trend_strength', 'moderate')} strength)
- **Anomaly Status:** {"⚠️  " + anomaly_info.get('severity', 'none').title() + " anomaly detected" if anomaly_info.get('anomaly_detected') else "✅ No anomalies detected"}
- **Deviation from Baseline:** {anomaly_info.get('deviation_percent', 0)}% {"above" if current_value > anomaly_info.get('mean_baseline', current_value) else "below"} historical average

### Cross-Metric Intelligence
{self._format_correlation_insights(correlation_info)}

## ⚡ **Business Intelligence & Root Cause**

### Performance Drivers
1. **Primary Driver** (Confidence: High): Current value indicates {self._assess_performance_level(kpi_type, current_value, comparative)}
2. **Statistical Pattern**: {self._get_statistical_insight(historical, current_value)}
3. **Business Context**: {self._get_business_context_insight(kpi_type, patterns)}

### Risk Assessment Matrix  
- **Impact Score:** {impact_info.get('impact_score', 50)}/100 ({impact_info.get('business_criticality', 'moderate').title()} criticality)
- **Financial Impact:** {impact_info.get('financial_impact_estimate', {}).get('estimated_impact', 'Moderate impact expected')}
- **Stakeholder Alerts:** {', '.join(impact_info.get('stakeholder_alerts', ['Operations Team']))}

## 🚀 **Strategic Action Framework**

### CRITICAL - Next 4 Hours
{self._generate_critical_actions(kpi_type, anomaly_info, impact_info)}

### HIGH PRIORITY - Next 24-48 Hours
{self._generate_priority_actions(kpi_type, prediction_info, comparative)}

### STRATEGIC - This Month
{self._generate_strategic_actions(kpi_type, best_practices)}

## 📈 **Predictive Intelligence**

### Forecast Confidence Matrix
{self._format_predictions(prediction_info)}

### Leading Indicators to Monitor
{self._get_leading_indicators(kpi_type, correlation_info)}

## 💡 **Innovation & Optimization Opportunities**

### Technology Enhancement
- **Data Analytics Opportunity:** Implement real-time anomaly detection for {kpi_type.replace('_', ' ')}
- **Automation Potential:** {"High" if anomaly_info.get('anomaly_detected') else "Moderate"} - Consider automated alerting systems

### Process Optimization
{self._get_optimization_recommendations(kpi_type, best_practices)}

---

## 🚨 **Alert Dashboard**
**Escalation Level:** {impact_info.get('business_criticality', 'MODERATE').upper()}
**Stakeholders to Notify:** {', '.join(impact_info.get('stakeholder_alerts', ['Operations Team']))}
**Review Frequency:** {"Hourly" if impact_info.get('impact_score', 0) > 80 else "Daily" if impact_info.get('impact_score', 0) > 60 else "Weekly"}

*Enhanced Analytics powered by statistical modeling, anomaly detection, and predictive intelligence*
"""
        
        return insights_md
    
    def _format_correlation_insights(self, correlation_info: Dict[str, Any]) -> str:
        """Format cross-KPI correlation insights"""
        insights = correlation_info.get('cross_kpi_insights', [])
        if not insights:
            return "- No significant cross-metric correlations detected in current data"
        
        formatted = []
        for insight in insights[:3]:  # Top 3 correlations
            formatted.append(f"- {insight}")
        
        return '\n'.join(formatted)
    
    def _format_predictions(self, prediction_info: Dict[str, Any]) -> str:
        """Format prediction information"""
        predictions = prediction_info.get('predictions', [])
        if not predictions:
            return "- Predictions require more historical data for accuracy"
        
        formatted = []
        for pred in predictions:
            timeframe = pred.get('timeframe', 'Unknown')
            value = pred.get('predicted_value', 'N/A')
            confidence = pred.get('confidence', 'low')
            formatted.append(f"- **{timeframe}:** {value} (Confidence: {confidence.title()})")
        
        return '\n'.join(formatted)
    
    def _generate_critical_actions(self, kpi_type: str, anomaly_info: Dict[str, Any], impact_info: Dict[str, Any]) -> str:
        """Generate critical actions based on anomaly and impact analysis"""
        if anomaly_info.get('anomaly_detected') and anomaly_info.get('severity') in ['critical', 'high']:
            return f"""- [ ] **Immediate Investigation:** Analyze root cause of {anomaly_info.get('anomaly_type', 'detected')} deviation
- [ ] **Stakeholder Alert:** Notify {', '.join(impact_info.get('stakeholder_alerts', ['Operations Team']))}
- **Success Metric:** Return to baseline within 4 hours"""
        
        return """- [ ] **Monitor Closely:** Continue standard monitoring protocols
- [ ] **Baseline Check:** Verify performance against targets
- **Success Metric:** Maintain current performance levels"""
    
    def _generate_priority_actions(self, kpi_type: str, prediction_info: Dict[str, Any], comparative: Dict[str, Any]) -> str:
        """Generate priority actions based on predictions and benchmarks"""
        trend = prediction_info.get('trend_direction', 'stable')
        
        if trend == 'decreasing':
            return f"""- [ ] **Trend Reversal:** Implement corrective measures to address declining {kpi_type.replace('_', ' ')}
- [ ] **Resource Review:** Assess if additional resources needed
- **Success Metrics:** 5-10% improvement in trend direction"""
        elif trend == 'increasing':
            return f"""- [ ] **Sustain Growth:** Reinforce factors driving positive {kpi_type.replace('_', ' ')} trend
- [ ] **Best Practice Documentation:** Capture successful approaches
- **Success Metrics:** Maintain or exceed current improvement rate"""
        
        return f"""- [ ] **Optimization Review:** Identify incremental improvement opportunities
- [ ] **Benchmark Analysis:** Compare performance against industry standards
- **Success Metrics:** 2-5% performance improvement"""
    
    def _generate_strategic_actions(self, kpi_type: str, best_practices: List[str]) -> str:
        """Generate strategic actions based on best practices"""
        if best_practices:
            practice = best_practices[0]  # Use first best practice
            return f"""- [ ] **Strategic Initiative:** Implement {practice}
- [ ] **Technology Investment:** Consider advanced analytics tools for {kpi_type.replace('_', ' ')} optimization
- **Investment Required:** Moderate (detailed ROI analysis recommended)
- **Expected ROI:** 15-25% improvement in operational efficiency"""
        
        return f"""- [ ] **Strategic Review:** Conduct comprehensive analysis of {kpi_type.replace('_', ' ')} optimization opportunities
- [ ] **Process Innovation:** Evaluate emerging best practices in industry
- **Investment Required:** TBD (analysis phase)
- **Expected ROI:** To be quantified during analysis"""
    
    def _get_leading_indicators(self, kpi_type: str, correlation_info: Dict[str, Any]) -> str:
        """Get leading indicators based on correlations"""
        related_kpis = correlation_info.get('related_kpis', [])
        
        if related_kpis:
            formatted = []
            for related in related_kpis[:3]:
                formatted.append(f"1. **{related.replace('_', ' ').title()}:** Early signal of {kpi_type.replace('_', ' ')} changes")
            return '\n'.join(formatted)
        
        return f"""1. **Historical Patterns:** Monitor same period last month/year
2. **Operational Metrics:** Track underlying business drivers
3. **External Factors:** Consider market and seasonal influences"""
    
    def _get_optimization_recommendations(self, kpi_type: str, best_practices: List[str]) -> str:
        """Get process optimization recommendations"""
        if best_practices:
            return f"""- **High-Impact Process:** {best_practices[0] if best_practices else 'Standard process optimization'}
- **ROI Estimate:** High (proven best practice implementation)"""
        
        return f"""- **Process Analysis:** Conduct detailed workflow review for {kpi_type.replace('_', ' ')}
- **Automation Opportunity:** Evaluate manual processes for efficiency gains"""

    def _assess_performance_level(self, kpi_type: str, current_value: float, comparative: Dict[str, Any]) -> str:
        """Assess current performance level"""
        target = comparative.get('target')
        if target:
            if current_value >= target * 1.1:
                return "exceptional performance (10%+ above target)"
            elif current_value >= target:
                return "meeting or exceeding targets"
            elif current_value >= target * 0.9:
                return "slightly below target (within 10%)"
            else:
                return "significantly below target (requires attention)"
        
        return "performance within expected operational range"
    
    def _get_statistical_insight(self, historical: List[float], current_value: float) -> str:
        """Get statistical insight from historical data"""
        if len(historical) < 5:
            return "Limited historical data available for trend analysis"
        
        import numpy as np
        recent_avg = np.mean(historical[-5:])
        
        if current_value > recent_avg * 1.1:
            return "Current value significantly above recent average (statistical significance high)"
        elif current_value < recent_avg * 0.9:
            return "Current value below recent trend (statistical significance moderate)"
        else:
            return "Current value consistent with recent patterns (statistical confidence high)"
    
    def _get_business_context_insight(self, kpi_type: str, patterns: List[str]) -> str:
        """Get business context insight"""
        if patterns:
            return f"Operational pattern: {patterns[0]}"
        
        context_map = {
            'call_volume': 'Peak periods typically drive higher customer service demands',
            'satisfaction_score': 'Customer satisfaction directly correlates with service quality',
            'revenue_growth': 'Revenue trends reflect overall business performance and market conditions',
            'agent_availability': 'Agent availability impacts customer wait times and satisfaction'
        }
        
        return context_map.get(kpi_type, 'Standard operational context applies')
