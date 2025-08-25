# Version: 0.1
# Last Modified: 2025-08-24
# Changes: Advanced AI analytics module for enhanced insights
"""
Advanced Analytics Module for Enhanced AI Insights
Provides correlation analysis, anomaly detection, and predictive intelligence
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from scipy import stats
import json

class AdvancedAnalyticsEngine:
    """Enhanced analytics engine for deeper AI insights"""
    
    def __init__(self):
        self.correlation_threshold = 0.7
        self.anomaly_threshold = 2.0  # Standard deviations
        self.prediction_confidence_levels = {
            'high': 0.85,
            'moderate': 0.65,
            'low': 0.45
        }
        
    def analyze_cross_kpi_correlations(self, kpi_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze correlations between different KPIs"""
        correlations = {}
        
        # Define KPI relationships based on call center domain knowledge
        kpi_relationships = {
            'call_volume': ['agent_availability', 'service_level', 'satisfaction_score'],
            'agent_availability': ['satisfaction_score', 'first_call_resolution'],
            'service_level': ['satisfaction_score', 'call_volume'],
            'satisfaction_score': ['first_call_resolution', 'avg_response_time'],
            'revenue_growth': ['customer_retention', 'satisfaction_score'],
            'cost_per_call': ['agent_availability', 'first_call_resolution']
        }
        
        current_kpi = kpi_data.get('kpi_type', '')
        related_kpis = kpi_relationships.get(current_kpi, [])
        
        insights = []
        for related_kpi in related_kpis:
            correlation_insight = self._calculate_correlation_insight(
                current_kpi, kpi_data.get('current_value', 0), related_kpi
            )
            if correlation_insight:
                insights.append(correlation_insight)
        
        return {
            'cross_kpi_insights': insights,
            'related_kpis': related_kpis,
            'correlation_strength': 'high' if len(insights) > 2 else 'moderate'
        }
    
    def detect_anomalies(self, kpi_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect anomalies in KPI data using statistical methods"""
        historical_trends = kpi_data.get('historical_trends', [])
        current_value = kpi_data.get('current_value', 0)
        
        # Convert current_value to numeric if it's a string
        if isinstance(current_value, str):
            try:
                if current_value == 'current' or not current_value:
                    # Use the latest historical value if available
                    if historical_trends:
                        current_value = historical_trends[-1]
                    else:
                        return {'anomaly_detected': False, 'reason': 'No current value available'}
                else:
                    current_value = float(current_value)
            except (ValueError, TypeError):
                return {'anomaly_detected': False, 'reason': 'Invalid current value format'}
        
        if len(historical_trends) < 5:
            return {'anomaly_detected': False, 'reason': 'Insufficient historical data'}

        # Filter out non-numeric values from historical trends
        numeric_trends = []
        for val in historical_trends:
            try:
                if isinstance(val, (int, float)):
                    numeric_trends.append(float(val))
                elif isinstance(val, str) and val.replace('.', '').replace('-', '').isdigit():
                    numeric_trends.append(float(val))
            except (ValueError, TypeError):
                continue
        
        if len(numeric_trends) < 5:
            return {'anomaly_detected': False, 'reason': 'Insufficient numeric historical data'}

        # Convert to numpy array for calculations
        data = np.array(numeric_trends)
        mean_val = np.mean(data)
        std_val = np.std(data)
        
        # Calculate Z-score for current value
        if std_val > 0:
            z_score = abs((float(current_value) - mean_val) / std_val)
            is_anomaly = z_score > self.anomaly_threshold
            
            # Determine anomaly type
            anomaly_type = 'positive' if float(current_value) > mean_val else 'negative'
            
            return {
                'anomaly_detected': is_anomaly,
                'z_score': round(z_score, 2),
                'anomaly_type': anomaly_type,
                'severity': self._get_anomaly_severity(z_score),
                'mean_baseline': round(mean_val, 2),
                'deviation_percent': round(((float(current_value) - mean_val) / mean_val) * 100, 1)
            }
        
        return {'anomaly_detected': False, 'reason': 'No variance in historical data'}
    
    def generate_predictive_insights(self, kpi_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate predictive insights based on trends and patterns"""
        historical_trends = kpi_data.get('historical_trends', [])
        kpi_type = kpi_data.get('kpi_type', '')
        current_value = kpi_data.get('current_value', 0)
        
        if len(historical_trends) < 7:
            return {'predictions': [], 'confidence': 'low'}
        
        # Calculate trend direction and strength
        recent_data = historical_trends[-7:]  # Last 7 data points
        trend_direction = self._calculate_trend_direction(recent_data)
        trend_strength = self._calculate_trend_strength(recent_data)
        
        # Generate time-based predictions
        predictions = []
        
        # Short-term prediction (2-4 hours)
        short_term = self._predict_short_term(recent_data, trend_direction, trend_strength)
        predictions.append({
            'timeframe': '2-4 hours',
            'predicted_value': short_term['value'],
            'confidence': short_term['confidence'],
            'factors': short_term['factors']
        })
        
        # Medium-term prediction (24 hours)
        medium_term = self._predict_medium_term(historical_trends, kpi_type)
        predictions.append({
            'timeframe': '24 hours',
            'predicted_value': medium_term['value'],
            'confidence': medium_term['confidence'],
            'factors': medium_term['factors']
        })
        
        return {
            'predictions': predictions,
            'trend_direction': trend_direction,
            'trend_strength': trend_strength,
            'confidence_level': max([p['confidence'] for p in predictions])
        }
    
    def assess_business_impact(self, kpi_data: Dict[str, Any], correlations: Dict[str, Any]) -> Dict[str, Any]:
        """Assess potential business impact of current KPI status"""
        kpi_type = kpi_data.get('kpi_type', '')
        current_value = kpi_data.get('current_value', 0)
        comparative_metrics = kpi_data.get('comparative_metrics', {})
        
        # Define business impact mappings
        impact_mappings = {
            'call_volume': {
                'high_impact_threshold': 20,  # % deviation
                'revenue_correlation': 0.8,
                'customer_satisfaction_impact': 'high'
            },
            'satisfaction_score': {
                'high_impact_threshold': 10,
                'revenue_correlation': 0.9,
                'retention_impact': 'critical'
            },
            'revenue_growth': {
                'high_impact_threshold': 15,
                'business_critical': True,
                'board_visibility': 'high'
            }
        }
        
        impact_assessment = impact_mappings.get(kpi_type, {})
        
        # Calculate impact score
        impact_score = self._calculate_impact_score(kpi_data, impact_assessment)
        
        return {
            'impact_score': impact_score,
            'business_criticality': self._get_business_criticality(impact_score),
            'stakeholder_alerts': self._get_required_alerts(kpi_type, impact_score),
            'financial_impact_estimate': self._estimate_financial_impact(kpi_type, current_value, comparative_metrics)
        }
    
    def _calculate_correlation_insight(self, kpi1: str, value1: float, kpi2: str) -> Optional[str]:
        """Calculate correlation insight between two KPIs"""
        # Simulate correlation calculation (in production, use real data)
        correlation_templates = {
            ('call_volume', 'agent_availability'): "Current call volume may impact agent availability by {impact}%",
            ('satisfaction_score', 'first_call_resolution'): "Customer satisfaction strongly correlates with resolution rates",
            ('revenue_growth', 'customer_retention'): "Revenue growth trends align with customer retention patterns"
        }
        
        template = correlation_templates.get((kpi1, kpi2))
        if template:
            impact = abs(value1 * 0.1)  # Simplified calculation
            return template.format(impact=round(impact, 1))
        
        return None
    
    def _get_anomaly_severity(self, z_score: float) -> str:
        """Determine anomaly severity based on Z-score"""
        if z_score > 3.0:
            return 'critical'
        elif z_score > 2.5:
            return 'high'
        elif z_score > 2.0:
            return 'moderate'
        return 'low'
    
    def _calculate_trend_direction(self, data: List[float]) -> str:
        """Calculate trend direction using linear regression"""
        if len(data) < 3:
            return 'stable'
        
        x = np.arange(len(data))
        slope, _, r_value, _, _ = stats.linregress(x, data)
        
        if abs(r_value) < 0.5:  # Weak correlation
            return 'stable'
        elif slope > 0:
            return 'increasing'
        else:
            return 'decreasing'
    
    def _calculate_trend_strength(self, data: List[float]) -> str:
        """Calculate trend strength"""
        if len(data) < 3:
            return 'weak'
        
        x = np.arange(len(data))
        _, _, r_value, _, _ = stats.linregress(x, data)
        
        if abs(r_value) > 0.8:
            return 'strong'
        elif abs(r_value) > 0.5:
            return 'moderate'
        else:
            return 'weak'
    
    def _predict_short_term(self, data: List[float], trend_direction: str, trend_strength: str) -> Dict[str, Any]:
        """Predict short-term value based on trends"""
        current = data[-1]
        
        if trend_direction == 'increasing':
            if trend_strength == 'strong':
                predicted = current * 1.05  # 5% increase
                confidence = 'high'
            else:
                predicted = current * 1.02  # 2% increase
                confidence = 'moderate'
        elif trend_direction == 'decreasing':
            if trend_strength == 'strong':
                predicted = current * 0.95  # 5% decrease
                confidence = 'high'
            else:
                predicted = current * 0.98  # 2% decrease
                confidence = 'moderate'
        else:
            predicted = current
            confidence = 'moderate'
        
        return {
            'value': round(predicted, 2),
            'confidence': confidence,
            'factors': [f'{trend_strength} {trend_direction} trend', 'Historical patterns', 'Statistical modeling']
        }
    
    def _predict_medium_term(self, data: List[float], kpi_type: str) -> Dict[str, Any]:
        """Predict medium-term value"""
        if len(data) < 14:
            return {
                'value': data[-1],
                'confidence': 'low',
                'factors': ['Insufficient historical data']
            }
        
        # Use simple moving average with trend adjustment
        recent_avg = np.mean(data[-7:])
        older_avg = np.mean(data[-14:-7])
        
        trend_factor = (recent_avg - older_avg) / older_avg if older_avg != 0 else 0
        predicted = recent_avg * (1 + trend_factor * 0.5)  # Dampen the trend for medium-term
        
        return {
            'value': round(predicted, 2),
            'confidence': 'moderate',
            'factors': ['Moving average trend', 'Historical seasonality', 'Business cycle patterns']
        }
    
    def _calculate_impact_score(self, kpi_data: Dict[str, Any], impact_mapping: Dict[str, Any]) -> float:
        """Calculate business impact score (0-100)"""
        current_value = kpi_data.get('current_value', 0)
        comparative_metrics = kpi_data.get('comparative_metrics', {})
        
        # Convert current_value to numeric if it's a string
        if isinstance(current_value, str):
            try:
                if current_value == 'current' or not current_value:
                    # Use a default impact score if no numeric value available
                    return 50.0  # Neutral baseline
                else:
                    current_value = float(current_value)
            except (ValueError, TypeError):
                return 50.0  # Neutral baseline for invalid values
        
        # Base score calculation
        score = 50  # Neutral baseline
        
        # Adjust based on targets/benchmarks
        if 'target' in comparative_metrics:
            target = comparative_metrics['target']
            if target > 0:
                deviation = abs((float(current_value) - target) / target) * 100
                if deviation > impact_mapping.get('high_impact_threshold', 15):
                    score += 30
                elif deviation > 10:
                    score += 15
                elif deviation < 5:
                    score -= 10  # Good performance
        
        return min(100, max(0, score))
    
    def _get_business_criticality(self, impact_score: float) -> str:
        """Determine business criticality level"""
        if impact_score > 80:
            return 'critical'
        elif impact_score > 60:
            return 'high'
        elif impact_score > 40:
            return 'moderate'
        return 'low'
    
    def _get_required_alerts(self, kpi_type: str, impact_score: float) -> List[str]:
        """Determine required stakeholder alerts"""
        alerts = []
        
        if impact_score > 80:
            alerts.extend(['Executive Team', 'Operations Manager', 'Department Heads'])
        elif impact_score > 60:
            alerts.extend(['Operations Manager', 'Team Leads'])
        elif impact_score > 40:
            alerts.extend(['Team Leads', 'Supervisors'])
        
        return alerts
    
    def _estimate_financial_impact(self, kpi_type: str, current_value: float, 
                                 comparative_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate financial impact of KPI deviation"""
        
        # Simplified financial impact calculations
        impact_multipliers = {
            'call_volume': {'cost_per_call': 2.45, 'revenue_per_call': 15.0},
            'satisfaction_score': {'retention_value': 1200, 'acquisition_cost': 150},
            'first_call_resolution': {'cost_savings': 12.0, 'satisfaction_boost': 0.3},
            'revenue_growth': {'direct_impact': True}
        }
        
        multiplier_data = impact_multipliers.get(kpi_type, {})
        
        if not multiplier_data:
            return {'estimated_impact': 'Not quantifiable', 'confidence': 'low'}
        
        if kpi_type == 'revenue_growth':
            # Direct revenue impact
            target = comparative_metrics.get('target', current_value)
            deviation = current_value - target
            return {
                'estimated_impact': f"${abs(deviation * 10000):,.0f} {'above' if deviation > 0 else 'below'} target",
                'confidence': 'high',
                'timeframe': 'monthly'
            }
        
        return {
            'estimated_impact': 'Moderate financial impact expected',
            'confidence': 'moderate',
            'timeframe': 'quarterly'
        }
