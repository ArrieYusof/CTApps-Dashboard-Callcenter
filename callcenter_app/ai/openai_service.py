# Version: 0.2
# Last Modified: 2025-08-25
# Changes: Added chat response functionality for AI chat interface
"""
OpenAI Integration Service for Call Center AI Analytics
Handles prompt engineering and API communication for contextual insights and chat responses
"""
from openai import OpenAI
import json
import os
from typing import Dict, Any, Optional
from datetime import datetime
import asyncio

class OpenAIInsightGenerator:
    """OpenAI integration for generating contextual KPI insights"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize OpenAI client with API key"""
        api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=api_key)
        
        # Configuration for Malaysian business context (now configurable via environment)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "2500"))  # Increased to handle comprehensive analysis
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))  # Balanced creativity with consistency
    
    async def generate_kpi_insights(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI insights based on RAG context"""
        kpi_type = context.get('kpi_type', 'unknown')  # Define at the start for error handling
        try:
            # Log AI analysis start with model info
            print(f"🤖 AI INFO: Starting AI analysis for '{kpi_type}' KPI...")
            
            # Build contextual prompt
            prompt = self._build_insight_prompt(context)
            
            # Call OpenAI API (sync for now, can be made async later)
            response = self._call_openai_sync(prompt)
            
            print(f"🤖 AI INFO: ✅ AI analysis completed successfully for '{kpi_type}' KPI")
            
            # Parse and structure response
            insights = self._parse_insights_response(response, context['kpi_type'])
            
            return {
                'success': True,
                'insights': insights,
                'generated_at': datetime.now().isoformat(),
                'model_used': self.model
            }
            
        except Exception as e:
            print(f"🤖 AI INFO: ❌ AI analysis failed for '{kpi_type}' KPI: {str(e)}")
            print(f"🤖 AI INFO: Using fallback insights for '{kpi_type}' KPI")
            return {
                'success': False,
                'error': str(e),
                'fallback_insights': self._get_fallback_insights(context['kpi_type'])
            }
    
    def _build_insight_prompt(self, context: Dict[str, Any]) -> str:
        """Build enhanced contextual prompt for OpenAI with advanced analytics integration"""
        kpi_type = context['kpi_type']
        current_value = context['current_value']
        
        # Get comparative metrics and advanced analytics
        comp_metrics = context.get('comparative_metrics', {})
        patterns = context.get('relevant_patterns', [])
        best_practices = context.get('best_practices', [])
        historical_trends = context.get('historical_trends', [])
        
        # Enhanced context with advanced analytics and Malaysian predictions
        advanced_context = context.get('advanced_analytics', {})
        anomaly_info = advanced_context.get('anomaly_analysis', {})
        prediction_info = advanced_context.get('predictions', {})
        impact_info = advanced_context.get('business_impact', {})
        correlation_info = advanced_context.get('correlations', {})
        
        # Enhanced Malaysian predictions
        enhanced_predictions = context.get('enhanced_predictions', {})
        malaysian_seasonal = context.get('malaysian_seasonal_intelligence', {})
        
        # Safe access to predictions - handle both old and new format
        predictions = prediction_info.get('predictions', [])
        print(f"🤖 AI INFO: Debug - predictions list: {predictions}, length: {len(predictions)}")
        
        # Enhanced predictions from Malaysian intelligence
        short_term_pred = enhanced_predictions.get('short_term', {})
        medium_term_pred = enhanced_predictions.get('medium_term', {})
        seasonal_impact = enhanced_predictions.get('seasonal_impact', {})
        confidence_factors = enhanced_predictions.get('confidence_factors', {})
        
        print(f"🤖 AI INFO: Enhanced predictions - short_term: {short_term_pred}")
        print(f"🤖 AI INFO: Enhanced predictions - medium_term: {medium_term_pred}")
        print(f"🤖 AI INFO: Malaysian seasonal intelligence: {malaysian_seasonal}")
        
        # Build enhanced analytics section with Malaysian intelligence
        advanced_section = ""
        if advanced_context or enhanced_predictions:
            advanced_section = f"""
ADVANCED ANALYTICS INSIGHTS:
- Anomaly Detection: {anomaly_info.get('anomaly_detected', 'Normal patterns detected')}
- Statistical Confidence: {anomaly_info.get('z_score', 'N/A')} standard deviations from baseline
- Trend Direction: {prediction_info.get('trend_direction', 'Stable')} ({prediction_info.get('trend_strength', 'moderate')} strength)
- Business Impact Score: {impact_info.get('impact_score', 'N/A')}/100 ({impact_info.get('business_criticality', 'moderate')} criticality)
- Cross-KPI Correlations: {len(correlation_info.get('cross_kpi_insights', []))} insights identified
- Financial Impact: {impact_info.get('financial_impact_estimate', {}).get('estimated_impact', 'Under assessment')}
- Stakeholder Alerts Required: {', '.join(impact_info.get('stakeholder_alerts', []))}

ENHANCED MALAYSIAN PREDICTIONS:
- Short-term (2-4 hours): {short_term_pred.get('predicted_value', 'Calculating...')} (Confidence: {short_term_pred.get('confidence', 'Medium')})
- Medium-term (24-48 hours): {medium_term_pred.get('predicted_value', 'Calculating...')} (Confidence: {medium_term_pred.get('confidence', 'Medium')})
- Business Context: {medium_term_pred.get('business_context', 'Malaysian business patterns applied')}
- Prediction Confidence Score: {confidence_factors.get('score', 'N/A')}/100
- Confidence Factors: {', '.join(confidence_factors.get('factors', ['Standard analysis']))}
"""
        
        # Malaysian seasonal intelligence section
        seasonal_section = ""
        if malaysian_seasonal:
            upcoming_catalysts = malaysian_seasonal.get('upcoming_catalysts', [])
            quarterly_trend = malaysian_seasonal.get('quarterly_trend', {})
            next_major_event = malaysian_seasonal.get('next_major_event', {})
            
            seasonal_section = f"""
MALAYSIAN SEASONAL INTELLIGENCE:
- Next Major Event: {next_major_event.get('name', 'None scheduled')} ({next_major_event.get('date', 'TBD')})
- Predicted Impact: {next_major_event.get('predicted_uplift', 'N/A')} uplift expected
- Quarterly Trend: {quarterly_trend.get('quarter', 'Current')} - {quarterly_trend.get('description', 'Standard business cycle')}
"""
            
            if upcoming_catalysts:
                catalyst_text = []
                for catalyst in upcoming_catalysts[:3]:  # Show top 3
                    catalyst_text.append(f"  • {catalyst.get('event', 'Event')} ({catalyst.get('days_until', 0)} days): {catalyst.get('uplift_percentage', 0)}% expected uplift")
                
                seasonal_section += f"""
- Upcoming Catalysts (Next 30 Days):
{chr(10).join(catalyst_text)}
"""
        
        base_prompt = f"""
You are a senior Malaysian call center analytics consultant with 15+ years of experience in Southeast Asian markets, specifically Malaysia's business environment. Your analysis focuses on Malaysian business practices, Ringgit Malaysia (RM) currency, Malaysian regulatory standards, and local market dynamics. You understand Malaysian corporate culture, business hours, and seasonal patterns specific to Malaysia.

MALAYSIAN BUSINESS CONTEXT:
- Currency: All financial figures in Ringgit Malaysia (RM)
- Business Hours: Malaysian standard (9 AM - 6 PM MYT)
- Market: Focus on Malaysian consumer behavior and business practices
- Regulatory: Comply with Malaysian business standards and practices
- Cultural: Consider Malaysian multicultural business environment
- Economic: Reference Malaysian economic indicators and benchmarks

CURRENT SITUATION ANALYSIS:
- KPI: {kpi_type.replace('_', ' ').title()}
- Current Value: {current_value}
- Analysis Timestamp: {context.get('timestamp', 'N/A')} (Malaysia Time)
- Data Confidence: High (Real-time operational data from Malaysian operations)

COMPARATIVE INTELLIGENCE:
{json.dumps(comp_metrics, indent=2) if comp_metrics else 'No comparative benchmarks available'}

HISTORICAL CONTEXT:
Recent Trend Data: {historical_trends[-10:] if len(historical_trends) >= 10 else historical_trends}

PATTERN RECOGNITION:
{chr(10).join(f"• {pattern}" for pattern in patterns) if patterns else 'No significant patterns detected'}

OPERATIONAL BEST PRACTICES (Malaysian Context):
{chr(10).join(f"• {practice}" for practice in best_practices) if best_practices else 'Malaysian industry standard practices apply'}
{advanced_section}
{seasonal_section}

ANALYSIS FRAMEWORK - Provide comprehensive insights using this EXACT markdown structure with Malaysian business context:

# 📊 **{kpi_type.replace('_', ' ').title()} Intelligence Report** - {current_value}

## 🎯 **Executive Summary**

**Performance Status:** [One-sentence executive summary with confidence level]

**Business Critical:** [Yes/No] - [Brief reason if Yes]

**Immediate Action Required:** [Yes/No] - [What action if Yes]

## � **Deep Performance Analysis**
### Current Performance Trajectory
- **Statistical Confidence:** [High/Medium/Low] based on data quality and sample size
- **Trend Direction:** [Specific trend with magnitude and time horizon]
- **Comparative Position:** [Multi-dimensional comparison: target, industry, historical]
- **Data Reliability:** [Assessment of data accuracy and completeness]

### Cross-Metric Intelligence
- **Primary Correlation:** [How this KPI impacts/correlates with other key metrics]
- **Cascade Effects:** [Downstream impacts on customer satisfaction, revenue, operations]
- **Leading Indicators:** [Earlier warning signs that predict this KPI's movement]

## ⚡ **Business Intelligence & Root Cause**
### Performance Drivers (Ranked by Impact)
1. **Primary Driver** (Confidence: [High/Medium/Low]): [Specific factor with quantified impact]
2. **Secondary Driver** (Confidence: [High/Medium/Low]): [Supporting factor]
3. **Contributing Factor**: [Additional influence]

### Risk Assessment Matrix
- **Immediate Risk (0-4 hours):** [Level] - [Specific risks and probability]
- **Short-term Risk (24-48 hours):** [Level] - [Projected challenges]
- **Strategic Risk (30+ days):** [Level] - [Long-term implications]

## 🚀 **Strategic Action Framework**
### CRITICAL - Next 4 Hours
- **☐ Action 1:** [Specific intervention with owner and success metric]
- **☐ Action 2:** [Emergency response if needed]
- **Success Metric:** [How to measure immediate success]

### HIGH PRIORITY - Next 24-48 Hours  
- **☐ Tactical Action 1:** [Operational improvement with timeline]
- **☐ Tactical Action 2:** [Resource reallocation or process change]
- **Success Metrics:** [Quantified improvements expected]

### STRATEGIC - This Month
- **☐ Strategic Initiative 1:** [Systemic improvement with ROI projection]
- **☐ Strategic Initiative 2:** [Technology or process transformation]
- **Investment Required:** [Budget/resource estimate]
- **Expected ROI:** [Quantified business value]

## � **Predictive Intelligence**
### Forecast Confidence Matrix
- **2-4 Hour Prediction:** {short_term_pred.get('predicted_value', 'Calculating based on velocity analysis')} (Confidence: {short_term_pred.get('confidence', 'Medium')})
- **24-Hour Projection:** {medium_term_pred.get('predicted_value', 'Calculating based on Malaysian business patterns')} (Confidence: {medium_term_pred.get('confidence', 'Medium')})
- **Key Assumption:** {short_term_pred.get('basis', 'Malaysian business patterns and velocity analysis applied')}

### Leading Indicators to Monitor
1. **Primary Indicator:** [Most important early warning signal]
2. **Secondary Indicator:** [Supporting prediction metric]
3. **Validation Metric:** [Confirming measurement]

## 💡 **Innovation & Optimization Opportunities**
### Technology Enhancement
- **AI/Automation Opportunity:** [Specific technology solution with impact estimate]
- **Data Enhancement:** [Additional data sources that would improve insights]

### Process Optimization  
- **High-Leverage Process:** [Process change with highest ROI potential]
- **Training Gap:** [Skill development opportunity with impact projection]

### Strategic Positioning
- **Competitive Advantage:** [How improvement creates market differentiation]
- **Customer Experience Impact:** [Direct customer benefit quantification]

---

## 🚨 **Alert Dashboard**

**Escalation Level:** [{impact_info.get('business_criticality', 'MODERATE').upper()}]

**Stakeholders to Notify:** {', '.join(impact_info.get('stakeholder_alerts', ['Operations Team']))}

**Review Frequency:** [Recommended monitoring cadence based on volatility]

*Advanced AI Analysis powered by statistical modeling, predictive analytics, and cross-metric correlation intelligence*

RESPONSE REQUIREMENTS - CRITICAL COMPLIANCE NEEDED:
- MANDATORY: Use specific numbers, percentages, and calculations from the actual data provided
- MANDATORY: Calculate performance gaps with exact numbers (e.g., "current 12.5 vs target 15.0 = 2.5 point gap = 16.7% shortfall")  
- MANDATORY: Reference historical trend data with exact values and calculated changes (e.g., "[8.1, 9.3, 10.2, 11.8, 12.5] shows 4.4 point growth = 54% improvement over period")
- MANDATORY: Calculate trend velocity with specific math (e.g., "Recent velocity: (12.5-11.8)/1 period = 0.7 points per period")
- MANDATORY: Show prediction mathematics (e.g., "At velocity 0.7 points/period, reaching 15.0 target requires (15.0-12.5)/0.7 = 3.6 periods")
- MANDATORY: Provide quantified financial impact with dollar estimates where possible
- MANDATORY: Give specific, actionable recommendations with named owners, timelines, and measurable success metrics
- MANDATORY: All investment and ROI figures must be justified with calculations or industry benchmarks
- MANDATORY: Reference seasonal patterns from RAG data (e.g., "Based on Q2-Q3 acceleration pattern from historical data")
- MANDATORY: Realistic timelines - no "10% increases in 4 hours" unless truly achievable
- MANDATORY FORMATTING: Use proper markdown with blank lines between ALL fields in ALL sections
- MANDATORY FORMATTING: Each field in Executive Summary AND Alert Dashboard must be on separate lines with blank line spacing
- MANDATORY FORMATTING: Never concatenate fields without proper line breaks
- FORBIDDEN: Generic phrases like "customer acquisition strategies" - be specific to the actual situation
- FORBIDDEN: Vague recommendations - every recommendation must have owner, timeline, and success metric
- FORBIDDEN: "N/A" responses when data is available - calculate meaningful insights from provided data
- FORBIDDEN: Concatenating any fields without proper line breaks in any section
- FORBIDDEN: Investment/ROI numbers without justification or calculation basis
- FORBIDDEN: Unrealistic short-term percentage improvements
- REQUIRED TONE: Senior consultant with 15+ years experience providing C-level recommendations

CALCULATION EXAMPLES - FOLLOW THESE PATTERNS:
Performance Gap: "Current 12.5 vs target 15.0 = 2.5 point shortfall = (2.5/15.0) × 100 = 16.7% below target"
Historical Analysis: "Trend [8.1→9.3→10.2→11.8→12.5] = 4.4 total growth = (12.5-8.1)/8.1 × 100 = 54% improvement"
Velocity Calculation: "Recent velocity: (12.5-11.8) = 0.7 points per period"
Target Timeline: "To reach 15.0 from 12.5 at 0.7 velocity = (15.0-12.5)/0.7 = 3.6 periods required"
Financial Impact: "2.5 point gap × $10K per point = $25K revenue shortfall"

SPECIFIC ACTION REQUIREMENTS:
- Instead of "implement strategies": "Launch Q3 seasonal marketing campaign leveraging historical Q2-Q3 acceleration pattern"
- Instead of "increase customer acquisition": "Deploy targeted email campaign to high-value prospect segments identified in CRM analysis"
- Instead of "10% in 4 hours": "2-3% improvement within 24-48 hours through immediate process optimization"
- Instead of "$50,000 investment": "Investment of $X based on industry benchmark of $Y per point improvement"

CRITICAL MARKDOWN FORMATTING EXAMPLES:

EXECUTIVE SUMMARY FORMAT:
**Performance Status:** [Specific analysis with calculations]

**Business Critical:** [Yes/No] - [Specific reason with quantified impact]

**Immediate Action Required:** [Yes/No] - [Specific action with timeline and owner]

ALERT DASHBOARD FORMAT:
**Escalation Level:** [LEVEL]

**Stakeholders to Notify:** [Specific stakeholders with roles]

**Review Frequency:** [Specific frequency with business justification]

ACTION ITEM FORMATTING - CRITICAL:
Use this EXACT format for all action items (NO line breaks between checkbox and text):
- **☐ Action Name:** Description with owner and timeline
- **☐ Next Action:** Another description with metrics

FORBIDDEN CHECKBOX FORMATS:
❌ Never use: "- [ ] **Action:**" (causes line break issues)
❌ Never use: "☐ Action:" without bullet point
✅ Always use: "- **☐ Action:**" (inline formatting)

CONTEXT VALIDATION: If you receive insufficient data, state exactly what additional data you need rather than giving generic responses.
"""
        
        return base_prompt
    
    def generate_markdown_insights(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI insights in markdown format - Enhanced with detailed logging"""
        
        print(f"\n🤖 AI INFO: ===== OPENAI REQUEST DETAILS =====")
        print(f"🤖 AI INFO: Context received:")
        print(f"🤖 AI INFO: - KPI Type: {context.get('kpi_type', 'Unknown')}")
        print(f"🤖 AI INFO: - Current Value: {context.get('current_value', 'N/A')}")
        print(f"🤖 AI INFO: - Context Data Keys: {list(context.keys())}")
        
        # Log RAG context details
        if 'comparative_metrics' in context:
            print(f"🤖 AI INFO: - Comparative Metrics: {context['comparative_metrics']}")
        if 'historical_trends' in context:
            print(f"🤖 AI INFO: - Historical Trends: {context['historical_trends']}")
        if 'relevant_patterns' in context:
            print(f"🤖 AI INFO: - Relevant Patterns: {context['relevant_patterns']}")
        
        try:
            # Build the complete prompt
            prompt = self._build_insight_prompt(context)
            
            print(f"\n🤖 AI INFO: ===== FULL OPENAI PROMPT =====")
            print(f"🤖 AI INFO: Prompt Length: {len(prompt)} characters")
            print(f"🤖 AI INFO: Full Prompt:")
            print(f"🤖 AI INFO: {'-'*60}")
            print(prompt)
            print(f"🤖 AI INFO: {'-'*60}")
            print(f"🤖 AI INFO: ===== END OF PROMPT =====\n")
            
            # Make API call
            print(f"🤖 AI INFO: Making OpenAI API call...")
            response = self._call_openai_sync(prompt)
            
            if response and response.strip():
                print(f"\n🤖 AI INFO: ===== OPENAI RESPONSE =====")
                print(f"🤖 AI INFO: Response Length: {len(response)} characters")
                print(f"🤖 AI INFO: Full Response:")
                print(f"🤖 AI INFO: {'-'*60}")
                print(response)
                print(f"🤖 AI INFO: {'-'*60}")
                print(f"🤖 AI INFO: ===== END OF RESPONSE =====\n")
                
                return {
                    'success': True,
                    'markdown_content': response,
                    'source': 'openai_api',
                    'model': self.model,
                    'timestamp': self._get_current_timestamp()
                }
            else:
                print(f"🤖 AI INFO: ❌ Empty response from OpenAI")
                fallback_content = self._get_markdown_fallback(context.get('kpi_type', 'unknown'), context.get('current_value', 0))
                return {
                    'success': False,
                    'markdown_content': fallback_content,
                    'source': 'fallback',
                    'timestamp': self._get_current_timestamp()
                }
                
        except Exception as e:
            print(f"🤖 AI INFO: ❌ OpenAI API error: {str(e)}")
            fallback_content = self._get_markdown_fallback(context.get('kpi_type', 'unknown'), context.get('current_value', 0), str(e))
            return {
                'success': False,
                'markdown_content': fallback_content,
                'source': 'error_fallback',
                'timestamp': self._get_current_timestamp(),
                'error': str(e)
            }

    def _get_current_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def _get_markdown_fallback(self, kpi_type: str, current_value: Any, error: str = "") -> str:
        """Generate markdown fallback when OpenAI is unavailable"""
        kpi_display = kpi_type.replace('_', ' ').title()
        
        fallback_content = f"""# 📊 {kpi_display} Analysis - {current_value}

## 🔍 Current Status
AI analysis service is temporarily unavailable. Current {kpi_display.lower()} value is **{current_value}**.

## 📈 Trend Analysis  
- **Data Source**: Historical patterns and operational knowledge
- **Status**: Manual analysis recommended
- **Context**: Using fallback insights based on best practices

## 💡 Recommendations
1. **Immediate Action**: Monitor current performance closely
2. **Short-term**: Review historical trends manually  
3. **Monitoring**: Use standard operational procedures

## 🔮 Predictions (Next 2-4 Hours)
🟡 **MODERATE CONFIDENCE** - Use historical averages and operational experience for forecasting

## ⚠️ Risk Assessment
**RISK LEVEL**: MODERATE - Enhanced manual monitoring recommended during AI service outage

---
*Fallback analysis - AI service temporarily unavailable*
{f"*Error: {error}*" if error else ""}
"""
        
        return fallback_content
    
    def _call_openai_sync(self, prompt: str) -> str:
        """Synchronous call to OpenAI API using new v1.x format"""
        try:
            # Log AI model information before making the API call
            print(f"🤖 AI INFO: Using model '{self.model}' with {self.max_tokens} max tokens, temperature {self.temperature}")
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert call center analytics AI that provides actionable insights based on data analysis. Always be specific, concise, and focus on actionable recommendations."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=0.9
            )
            
            # Check if response has choices
            if not response.choices or len(response.choices) == 0:
                raise Exception("OpenAI returned no response choices")
            
            content = response.choices[0].message.content
            if not content:
                raise Exception("OpenAI returned empty content")
                
            return content
            
        except Exception as e:
            raise Exception(f"OpenAI API call failed: {str(e)}")
    
    def get_completion(self, prompt: str, max_tokens: int = 200) -> str:
        """Simple completion method for general chat responses"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a friendly AI assistant specializing in Malaysian call center analytics. Be conversational, helpful, and professional."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=0.7,  # More creative for general chat
                top_p=0.9
            )
            
            if not response.choices or len(response.choices) == 0:
                raise Exception("OpenAI returned no response choices")
            
            content = response.choices[0].message.content
            if not content:
                raise Exception("OpenAI returned empty content")
                
            return content.strip()
            
        except Exception as e:
            raise Exception(f"OpenAI completion failed: {str(e)}")
    
    def _parse_insights_response(self, response: str, kpi_type: str) -> Dict[str, Any]:
        """Parse OpenAI response into structured insights"""
        sections = {
            'status': '',
            'trends': '',
            'recommendations': [],
            'predictions': '',
            'risks': '',
            'raw_response': response
        }
        
        # Simple parsing based on headers (could be improved with regex)
        lines = response.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if 'CURRENT STATUS' in line.upper():
                current_section = 'status'
            elif 'TREND ANALYSIS' in line.upper():
                current_section = 'trends'
            elif 'RECOMMENDATIONS' in line.upper() or 'ACTIONABLE' in line.upper():
                current_section = 'recommendations'
            elif 'PREDICTIONS' in line.upper():
                current_section = 'predictions'
            elif 'RISK' in line.upper():
                current_section = 'risks'
            elif current_section and line.startswith('•') or line.startswith('-'):
                if current_section == 'recommendations':
                    sections['recommendations'].append(line.lstrip('•- '))
                else:
                    sections[current_section] += line + '\n'
            elif current_section and line:
                sections[current_section] += line + ' '
        
        return sections
    
    def _get_fallback_insights(self, kpi_type: str) -> Dict[str, Any]:
        """Provide fallback insights when OpenAI is unavailable"""
        fallbacks = {
            'call_volume': {
                'status': 'Current call volume analysis unavailable',
                'recommendations': [
                    'Monitor queue levels closely',
                    'Consider adjusting staffing for peak hours',
                    'Review historical patterns for capacity planning'
                ],
                'risks': 'Unable to generate AI predictions. Use historical averages.'
            },
            'customer_satisfaction': {
                'status': 'CSAT analysis service temporarily unavailable',
                'recommendations': [
                    'Review recent customer feedback',
                    'Focus on first-call resolution improvement',
                    'Monitor response times closely'
                ],
                'risks': 'Manual review of satisfaction trends recommended.'
            },
            'sla_monitoring': {
                'status': 'SLA analysis service unavailable',
                'recommendations': [
                    'Monitor current performance against targets',
                    'Prepare contingency staffing plans',
                    'Review breach prevention protocols'
                ],
                'risks': 'Enhanced manual monitoring recommended during peak hours.'
            }
        }
        
        return fallbacks.get(kpi_type, {
            'status': 'AI insights temporarily unavailable',
            'recommendations': ['Manual analysis recommended'],
            'risks': 'Use standard operational procedures'
        })

# Create alias for backward compatibility and chat interface
OpenAIService = OpenAIInsightGenerator
