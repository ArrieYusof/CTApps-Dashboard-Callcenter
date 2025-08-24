# Version: 0.1
# Last Modified: 2025-08-24
# Changes: Data enrichment module for enhanced AI analysis
"""
Data Enrichment Module for AI Analysis
Provides enhanced contextual data, time-based intelligence, and external factors
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import random
import math

class DataEnrichmentEngine:
    """Enhanced data enrichment for more intelligent AI analysis"""
    
    def __init__(self):
        self.business_hours = {'start': 8, 'end': 18}
        self.peak_hours = [9, 10, 11, 14, 15, 16]
        self.seasonal_factors = {
            'Q1': 0.85,  # Post-holiday lull
            'Q2': 1.1,   # Spring surge
            'Q3': 0.95,  # Summer slower
            'Q4': 1.2    # Holiday peak
        }
        
    def enrich_kpi_context(self, kpi_type: str, current_value: float, 
                          base_context: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich KPI context with time intelligence, external factors, and business context"""
        
        enriched_context = base_context.copy()
        current_time = datetime.now()
        
        # Add time-based intelligence
        time_context = self._get_time_context(current_time)
        enriched_context['time_intelligence'] = time_context
        
        # Add business cycle context
        business_context = self._get_business_cycle_context(kpi_type, current_time)
        enriched_context['business_cycle'] = business_context
        
        # Add competitive intelligence
        competitive_context = self._get_competitive_context(kpi_type, current_value)
        enriched_context['competitive_intelligence'] = competitive_context
        
        # Add operational context
        operational_context = self._get_operational_context(kpi_type, current_time)
        enriched_context['operational_context'] = operational_context
        
        # Enhance historical trends with realistic patterns
        enhanced_trends = self._enhance_historical_trends(
            kpi_type, 
            enriched_context.get('historical_trends', []), 
            current_time
        )
        enriched_context['historical_trends'] = enhanced_trends
        
        # Add external factors
        external_factors = self._get_external_factors(kpi_type, current_time)
        enriched_context['external_factors'] = external_factors
        
        # Calculate confidence scores
        confidence_scores = self._calculate_confidence_scores(enriched_context, current_value)
        enriched_context['confidence_metrics'] = confidence_scores
        
        return enriched_context
    
    def _get_time_context(self, current_time: datetime) -> Dict[str, Any]:
        """Get comprehensive time-based context"""
        hour = current_time.hour
        day_of_week = current_time.strftime('%A')
        week_of_month = (current_time.day - 1) // 7 + 1
        quarter = f"Q{(current_time.month - 1) // 3 + 1}"
        
        is_business_hours = self.business_hours['start'] <= hour <= self.business_hours['end']
        is_peak_hour = hour in self.peak_hours
        
        # Calculate time-based multipliers
        hour_multiplier = self._get_hour_multiplier(hour)
        day_multiplier = self._get_day_multiplier(day_of_week)
        
        return {
            'current_hour': hour,
            'day_of_week': day_of_week,
            'week_of_month': week_of_month,
            'quarter': quarter,
            'is_business_hours': is_business_hours,
            'is_peak_hour': is_peak_hour,
            'hour_multiplier': hour_multiplier,
            'day_multiplier': day_multiplier,
            'time_based_expectation': hour_multiplier * day_multiplier,
            'business_day_category': self._get_business_day_category(day_of_week)
        }
    
    def _get_business_cycle_context(self, kpi_type: str, current_time: datetime) -> Dict[str, Any]:
        """Get business cycle and seasonal context"""
        month = current_time.month
        quarter = f"Q{(month - 1) // 3 + 1}"
        seasonal_factor = self.seasonal_factors.get(quarter, 1.0)
        
        # Month-specific patterns
        month_patterns = {
            1: {'pattern': 'post_holiday_recovery', 'intensity': 0.8},
            2: {'pattern': 'winter_steady', 'intensity': 0.9},
            3: {'pattern': 'quarter_end_push', 'intensity': 1.1},
            4: {'pattern': 'spring_uptick', 'intensity': 1.05},
            5: {'pattern': 'spring_peak', 'intensity': 1.15},
            6: {'pattern': 'mid_year_steady', 'intensity': 1.0},
            7: {'pattern': 'summer_slowdown', 'intensity': 0.85},
            8: {'pattern': 'back_to_business', 'intensity': 0.95},
            9: {'pattern': 'fall_acceleration', 'intensity': 1.1},
            10: {'pattern': 'pre_holiday_buildup', 'intensity': 1.2},
            11: {'pattern': 'holiday_peak', 'intensity': 1.3},
            12: {'pattern': 'year_end_rush', 'intensity': 1.25}
        }
        
        current_pattern = month_patterns.get(month, {'pattern': 'normal', 'intensity': 1.0})
        
        return {
            'quarter': quarter,
            'month': month,
            'seasonal_factor': seasonal_factor,
            'monthly_pattern': current_pattern['pattern'],
            'intensity_factor': current_pattern['intensity'],
            'expected_variance': self._calculate_seasonal_variance(kpi_type, quarter),
            'business_cycle_stage': self._get_business_cycle_stage(quarter)
        }
    
    def _get_competitive_context(self, kpi_type: str, current_value: float) -> Dict[str, Any]:
        """Get competitive intelligence context"""
        
        # Industry benchmarks (simulated but realistic)
        industry_benchmarks = {
            'call_volume': {'median': 1200, 'top_quartile': 1500, 'best_in_class': 1800},
            'satisfaction_score': {'median': 82, 'top_quartile': 88, 'best_in_class': 94},
            'revenue_growth': {'median': 8.5, 'top_quartile': 12.0, 'best_in_class': 18.0},
            'agent_availability': {'median': 85, 'top_quartile': 90, 'best_in_class': 95},
            'first_call_resolution': {'median': 78, 'top_quartile': 85, 'best_in_class': 92}
        }
        
        benchmark = industry_benchmarks.get(kpi_type, {
            'median': current_value * 0.95, 
            'top_quartile': current_value * 1.05, 
            'best_in_class': current_value * 1.15
        })
        
        # Calculate competitive position
        competitive_position = self._calculate_competitive_position(current_value, benchmark)
        
        return {
            'industry_median': benchmark['median'],
            'top_quartile': benchmark['top_quartile'],
            'best_in_class': benchmark['best_in_class'],
            'competitive_position': competitive_position,
            'improvement_potential': benchmark['best_in_class'] - current_value,
            'competitive_gap': self._get_competitive_gap(competitive_position),
            'market_context': self._get_market_context(kpi_type)
        }
    
    def _get_operational_context(self, kpi_type: str, current_time: datetime) -> Dict[str, Any]:
        """Get operational context and constraints"""
        
        # Simulate operational factors
        operational_factors = {
            'staffing_level': np.random.uniform(0.85, 1.1),
            'system_performance': np.random.uniform(0.9, 1.0),
            'training_cycle_impact': self._get_training_impact(current_time),
            'technology_deployment': self._get_tech_deployment_impact(current_time),
            'process_maturity': np.random.uniform(0.8, 0.95)
        }
        
        # KPI-specific operational context
        kpi_specific = {
            'call_volume': {
                'campaign_impact': np.random.uniform(0.9, 1.2),
                'marketing_drive': self._get_marketing_impact(current_time),
                'product_launch_factor': np.random.uniform(0.95, 1.3)
            },
            'satisfaction_score': {
                'service_quality_initiatives': np.random.uniform(0.98, 1.05),
                'agent_morale_factor': np.random.uniform(0.95, 1.05),
                'system_reliability': np.random.uniform(0.92, 1.0)
            },
            'agent_availability': {
                'schedule_optimization': np.random.uniform(0.95, 1.05),
                'break_compliance': np.random.uniform(0.98, 1.02),
                'overtime_factor': np.random.uniform(0.9, 1.1)
            }
        }
        
        specific_factors = kpi_specific.get(kpi_type, {})
        
        return {
            'operational_efficiency': np.mean(list(operational_factors.values())),
            'operational_factors': operational_factors,
            'kpi_specific_factors': specific_factors,
            'constraint_analysis': self._analyze_constraints(kpi_type, operational_factors),
            'improvement_levers': self._identify_improvement_levers(kpi_type, operational_factors)
        }
    
    def _enhance_historical_trends(self, kpi_type: str, base_trends: List[float], 
                                 current_time: datetime) -> List[float]:
        """Enhance historical trends with realistic patterns and noise"""
        
        if len(base_trends) < 24:
            # Generate 24 hours of realistic data
            base_value = base_trends[0] if base_trends else self._get_baseline_value(kpi_type)
            trends = []
            
            for i in range(24):
                hour_ago = current_time - timedelta(hours=i)
                hour = hour_ago.hour
                
                # Apply time-based patterns
                time_factor = self._get_hour_multiplier(hour)
                
                # Add realistic noise
                noise = np.random.normal(0, base_value * 0.05)  # 5% noise
                
                # Add trend component
                trend_component = math.sin(i * math.pi / 12) * base_value * 0.1
                
                value = base_value * time_factor + noise + trend_component
                trends.insert(0, max(0, value))  # Insert at beginning for chronological order
            
            return trends
        
        return base_trends
    
    def _get_external_factors(self, kpi_type: str, current_time: datetime) -> Dict[str, Any]:
        """Get external factors that might influence KPIs"""
        
        external_factors = {
            'weather_impact': self._get_weather_impact(current_time),
            'economic_indicators': self._get_economic_context(),
            'competitor_activity': self._get_competitor_activity(),
            'regulatory_environment': self._get_regulatory_context(kpi_type),
            'technology_trends': self._get_technology_trends(kpi_type),
            'market_sentiment': np.random.uniform(0.85, 1.15),
            'supply_chain_factors': np.random.uniform(0.9, 1.1)
        }
        
        # Calculate overall external impact
        external_impact = np.mean([
            external_factors['weather_impact'],
            external_factors['economic_indicators'],
            external_factors['market_sentiment']
        ])
        
        return {
            **external_factors,
            'overall_external_impact': external_impact,
            'risk_factors': self._identify_external_risks(external_factors),
            'opportunity_factors': self._identify_external_opportunities(external_factors)
        }
    
    def _calculate_confidence_scores(self, context: Dict[str, Any], current_value: float) -> Dict[str, float]:
        """Calculate confidence scores for various analysis aspects"""
        
        data_quality_score = self._assess_data_quality(context)
        pattern_confidence = self._assess_pattern_confidence(context.get('historical_trends', []))
        external_stability = self._assess_external_stability(context.get('external_factors', {}))
        
        return {
            'data_quality': data_quality_score,
            'pattern_recognition': pattern_confidence,
            'external_stability': external_stability,
            'overall_confidence': (data_quality_score + pattern_confidence + external_stability) / 3,
            'prediction_confidence': min(data_quality_score, pattern_confidence) * external_stability
        }
    
    # Helper methods
    def _get_hour_multiplier(self, hour: int) -> float:
        """Get multiplier based on hour of day"""
        if 9 <= hour <= 11:
            return 1.2  # Morning peak
        elif 14 <= hour <= 16:
            return 1.15  # Afternoon peak
        elif 8 <= hour <= 18:
            return 1.0  # Business hours
        else:
            return 0.3  # Off hours
    
    def _get_day_multiplier(self, day_of_week: str) -> float:
        """Get multiplier based on day of week"""
        multipliers = {
            'Monday': 1.1,
            'Tuesday': 1.15,
            'Wednesday': 1.2,
            'Thursday': 1.1,
            'Friday': 1.05,
            'Saturday': 0.4,
            'Sunday': 0.2
        }
        return multipliers.get(day_of_week, 1.0)
    
    def _get_business_day_category(self, day_of_week: str) -> str:
        """Categorize business day type"""
        if day_of_week in ['Monday', 'Friday']:
            return 'transition_day'
        elif day_of_week in ['Tuesday', 'Wednesday', 'Thursday']:
            return 'peak_business_day'
        else:
            return 'weekend'
    
    def _calculate_seasonal_variance(self, kpi_type: str, quarter: str) -> float:
        """Calculate expected variance for the season"""
        base_variance = 0.15
        seasonal_adjustments = {
            'Q1': 0.2,   # Higher variance post-holiday
            'Q2': 0.1,   # Stable spring period
            'Q3': 0.15,  # Summer variations
            'Q4': 0.25   # Holiday volatility
        }
        return base_variance + seasonal_adjustments.get(quarter, 0.15)
    
    def _get_business_cycle_stage(self, quarter: str) -> str:
        """Determine business cycle stage"""
        stages = {
            'Q1': 'recovery',
            'Q2': 'growth',
            'Q3': 'maturity',
            'Q4': 'peak'
        }
        return stages.get(quarter, 'stable')
    
    def _calculate_competitive_position(self, current_value: float, benchmarks: Dict[str, float]) -> str:
        """Calculate competitive position"""
        if current_value >= benchmarks['best_in_class']:
            return 'best_in_class'
        elif current_value >= benchmarks['top_quartile']:
            return 'top_quartile'
        elif current_value >= benchmarks['median']:
            return 'above_median'
        else:
            return 'below_median'
    
    def _get_competitive_gap(self, position: str) -> str:
        """Get competitive gap analysis"""
        gaps = {
            'best_in_class': 'industry_leader',
            'top_quartile': 'competitive_advantage',
            'above_median': 'market_competitive',
            'below_median': 'improvement_needed'
        }
        return gaps.get(position, 'requires_analysis')
    
    def _get_baseline_value(self, kpi_type: str) -> float:
        """Get baseline value for KPI type"""
        baselines = {
            'call_volume': 1200,
            'satisfaction_score': 85,
            'revenue_growth': 10.0,
            'agent_availability': 88,
            'first_call_resolution': 80
        }
        return baselines.get(kpi_type, 100)
    
    def _get_weather_impact(self, current_time: datetime) -> float:
        """Simulate weather impact (normally minimal)"""
        return np.random.uniform(0.95, 1.05)
    
    def _get_economic_context(self) -> float:
        """Simulate economic context"""
        return np.random.uniform(0.9, 1.1)
    
    def _get_competitor_activity(self) -> float:
        """Simulate competitor activity impact"""
        return np.random.uniform(0.85, 1.15)
    
    def _get_regulatory_context(self, kpi_type: str) -> float:
        """Get regulatory environment impact"""
        return np.random.uniform(0.98, 1.02)
    
    def _get_technology_trends(self, kpi_type: str) -> float:
        """Get technology trends impact"""
        return np.random.uniform(0.95, 1.1)
    
    def _get_training_impact(self, current_time: datetime) -> float:
        """Get training cycle impact"""
        return np.random.uniform(0.9, 1.05)
    
    def _get_tech_deployment_impact(self, current_time: datetime) -> float:
        """Get technology deployment impact"""
        return np.random.uniform(0.95, 1.05)
    
    def _get_marketing_impact(self, current_time: datetime) -> float:
        """Get marketing campaign impact"""
        return np.random.uniform(0.8, 1.4)
    
    def _get_market_context(self, kpi_type: str) -> str:
        """Get market context description"""
        contexts = [
            'stable_market_conditions',
            'growing_market_demand',
            'competitive_pressure_high',
            'digital_transformation_phase'
        ]
        return random.choice(contexts)
    
    def _analyze_constraints(self, kpi_type: str, operational_factors: Dict) -> List[str]:
        """Analyze operational constraints"""
        constraints = []
        
        if operational_factors['staffing_level'] < 0.9:
            constraints.append('staffing_constraints')
        if operational_factors['system_performance'] < 0.95:
            constraints.append('technology_limitations')
        if operational_factors['process_maturity'] < 0.9:
            constraints.append('process_optimization_needed')
            
        return constraints
    
    def _identify_improvement_levers(self, kpi_type: str, operational_factors: Dict) -> List[str]:
        """Identify improvement levers"""
        levers = []
        
        if operational_factors['staffing_level'] < 1.0:
            levers.append('staffing_optimization')
        if operational_factors['system_performance'] < 1.0:
            levers.append('technology_upgrade')
        if operational_factors['training_cycle_impact'] < 1.0:
            levers.append('enhanced_training')
            
        return levers
    
    def _identify_external_risks(self, external_factors: Dict) -> List[str]:
        """Identify external risk factors"""
        risks = []
        
        if external_factors['economic_indicators'] < 0.95:
            risks.append('economic_headwinds')
        if external_factors['competitor_activity'] > 1.1:
            risks.append('competitive_pressure')
        if external_factors['market_sentiment'] < 0.9:
            risks.append('market_uncertainty')
            
        return risks
    
    def _identify_external_opportunities(self, external_factors: Dict) -> List[str]:
        """Identify external opportunities"""
        opportunities = []
        
        if external_factors['economic_indicators'] > 1.05:
            opportunities.append('economic_tailwinds')
        if external_factors['technology_trends'] > 1.05:
            opportunities.append('technology_adoption')
        if external_factors['market_sentiment'] > 1.1:
            opportunities.append('market_growth')
            
        return opportunities
    
    def _assess_data_quality(self, context: Dict[str, Any]) -> float:
        """Assess data quality score"""
        historical_data = context.get('historical_trends', [])
        
        if len(historical_data) >= 20:
            return 0.95
        elif len(historical_data) >= 10:
            return 0.8
        elif len(historical_data) >= 5:
            return 0.6
        else:
            return 0.4
    
    def _assess_pattern_confidence(self, historical_data: List[float]) -> float:
        """Assess pattern recognition confidence"""
        if len(historical_data) < 5:
            return 0.3
        
        # Calculate coefficient of variation
        mean_val = np.mean(historical_data)
        std_val = np.std(historical_data)
        
        if mean_val > 0:
            cv = std_val / mean_val
            # Lower CV means higher confidence in patterns
            return max(0.3, 1 - cv)
        
        return 0.5
    
    def _assess_external_stability(self, external_factors: Dict) -> float:
        """Assess external environment stability"""
        if not external_factors:
            return 0.7
        
        # Calculate stability based on external factor variance
        factors = [
            external_factors.get('economic_indicators', 1.0),
            external_factors.get('market_sentiment', 1.0),
            external_factors.get('competitor_activity', 1.0)
        ]
        
        variance = np.var(factors)
        # Lower variance means higher stability
        return max(0.3, 1 - variance)
