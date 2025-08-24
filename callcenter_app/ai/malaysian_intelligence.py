# Version: 0.2
# Last Modified: 2025-08-24
# Changes: Enhanced Malaysian calendar and improved predictive intelligence
"""
Malaysian Business Calendar and Enhanced Predictions Module
Provides Malaysian cultural, economic, and business event intelligence
"""
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import calendar
import numpy as np

class MalaysianBusinessCalendar:
    """Malaysian business calendar with cultural and economic events"""
    
    def __init__(self):
        self.current_date = datetime.now()
        self.malaysian_events = self._load_malaysian_calendar()
        self.economic_indicators = self._load_economic_calendar()
        
    def _load_malaysian_calendar(self) -> Dict[str, Any]:
        """Load Malaysian cultural and business events"""
        return {
            '2025': {
                'chinese_new_year': {
                    'date': '2025-01-29',
                    'impact': 'high',
                    'revenue_multiplier': 1.18,
                    'duration_days': 15,
                    'description': 'Chinese New Year period - highest consumer spending'
                },
                'hari_raya_puasa': {
                    'date': '2025-03-30',
                    'impact': 'high', 
                    'revenue_multiplier': 1.15,
                    'duration_days': 10,
                    'description': 'Eid al-Fitr - major Muslim celebration, high spending'
                },
                'wesak_day': {
                    'date': '2025-05-12',
                    'impact': 'medium',
                    'revenue_multiplier': 1.08,
                    'duration_days': 3,
                    'description': 'Buddhist holiday - moderate spending increase'
                },
                'hari_raya_haji': {
                    'date': '2025-06-07',
                    'impact': 'medium',
                    'revenue_multiplier': 1.12,
                    'duration_days': 7,
                    'description': 'Eid al-Adha - Muslim pilgrimage season'
                },
                'merdeka_day': {
                    'date': '2025-08-31',
                    'impact': 'medium',
                    'revenue_multiplier': 1.10,
                    'duration_days': 5,
                    'description': 'Independence Day - patriotic spending surge'
                },
                'malaysia_day': {
                    'date': '2025-09-16',
                    'impact': 'medium',
                    'revenue_multiplier': 1.08,
                    'duration_days': 3,
                    'description': 'Malaysia Day - national celebration'
                },
                'deepavali': {
                    'date': '2025-10-20',
                    'impact': 'high',
                    'revenue_multiplier': 1.16,
                    'duration_days': 7,
                    'description': 'Hindu festival of lights - major Indian Malaysian celebration'
                },
                'year_end_sales': {
                    'date': '2025-12-01',
                    'impact': 'very_high',
                    'revenue_multiplier': 1.25,
                    'duration_days': 31,
                    'description': 'Year-end shopping season - highest revenue period'
                }
            },
            '2026': {
                'chinese_new_year': {
                    'date': '2026-02-17',
                    'impact': 'high',
                    'revenue_multiplier': 1.18,
                    'duration_days': 15,
                    'description': 'Chinese New Year period - highest consumer spending'
                }
                # Additional 2026 events would be added here
            }
        }
    
    def _load_economic_calendar(self) -> Dict[str, Any]:
        """Load Malaysian economic events and indicators"""
        return {
            'quarterly_events': {
                'q1': {
                    'epf_withdrawal': {
                        'typical_date': 'March 15',
                        'impact': 'Consumer spending increase 10-15%',
                        'revenue_effect': 1.12
                    },
                    'budget_announcement': {
                        'typical_date': 'March 30',
                        'impact': 'Corporate spending alignment',
                        'revenue_effect': 1.08
                    }
                },
                'q2': {
                    'corporate_budgets': {
                        'typical_date': 'April-June',
                        'impact': 'B2B spending acceleration',
                        'revenue_effect': 1.15
                    },
                    'mid_year_bonuses': {
                        'typical_date': 'June 15',
                        'impact': 'Consumer discretionary spending',
                        'revenue_effect': 1.10
                    }
                },
                'q3': {
                    'harvest_season': {
                        'typical_date': 'July-September',
                        'impact': 'Agricultural sector spending',
                        'revenue_effect': 1.05
                    },
                    'back_to_school': {
                        'typical_date': 'August',
                        'impact': 'Family spending on education',
                        'revenue_effect': 1.12
                    }
                },
                'q4': {
                    'year_end_budgets': {
                        'typical_date': 'October-December',
                        'impact': 'Corporate budget exhaustion',
                        'revenue_effect': 1.20
                    },
                    'bonus_season': {
                        'typical_date': 'December',
                        'impact': 'Highest consumer spending period',
                        'revenue_effect': 1.25
                    }
                }
            },
            'monthly_patterns': {
                'salary_days': [25, 28, 30],  # Common Malaysian salary dates
                'school_holidays': {
                    'march': {'days': [9, 23], 'effect': 1.08},
                    'june': {'days': [1, 30], 'effect': 1.15},
                    'august': {'days': [31], 'effect': 1.10},
                    'november': {'days': [16, 30], 'effect': 1.12}
                }
            }
        }

    def get_upcoming_events(self, days_ahead: int = 90) -> List[Dict[str, Any]]:
        """Get upcoming Malaysian events within specified timeframe"""
        upcoming = []
        current_year = str(self.current_date.year)
        next_year = str(self.current_date.year + 1)
        
        # Check current and next year events
        for year in [current_year, next_year]:
            if year in self.malaysian_events:
                for event_name, event_data in self.malaysian_events[year].items():
                    event_date = datetime.strptime(event_data['date'], '%Y-%m-%d')
                    days_until = (event_date - self.current_date).days
                    
                    if 0 <= days_until <= days_ahead:
                        upcoming.append({
                            'name': event_name,
                            'date': event_data['date'],
                            'days_until': days_until,
                            'impact': event_data['impact'],
                            'revenue_multiplier': event_data['revenue_multiplier'],
                            'duration': event_data['duration_days'],
                            'description': event_data['description']
                        })
        
        # Sort by date
        upcoming.sort(key=lambda x: x['days_until'])
        return upcoming

    def get_seasonal_impact(self, kpi_type: str, current_value: float) -> Dict[str, Any]:
        """Calculate seasonal impact on KPI based on Malaysian calendar"""
        upcoming_events = self.get_upcoming_events(30)
        current_quarter = f"q{(self.current_date.month - 1) // 3 + 1}"
        
        seasonal_analysis = {
            'upcoming_catalysts': [],
            'quarterly_trend': None,
            'next_major_event': None,
            'seasonal_prediction': None
        }
        
        # Analyze upcoming events
        for event in upcoming_events:
            if event['days_until'] <= 30:
                predicted_impact = current_value * event['revenue_multiplier']
                seasonal_analysis['upcoming_catalysts'].append({
                    'event': event['name'].replace('_', ' ').title(),
                    'date': event['date'],
                    'days_until': event['days_until'],
                    'predicted_value': round(predicted_impact, 1),
                    'uplift_percentage': round((event['revenue_multiplier'] - 1) * 100, 1),
                    'description': event['description']
                })
        
        # Quarterly analysis
        if current_quarter in self.economic_indicators['quarterly_events']:
            q_data = self.economic_indicators['quarterly_events'][current_quarter]
            seasonal_analysis['quarterly_trend'] = {
                'quarter': current_quarter.upper(),
                'events': list(q_data.keys()),
                'average_multiplier': round(np.mean([v['revenue_effect'] for v in q_data.values()]), 2),
                'description': f"Q{current_quarter[-1]} typically shows enhanced business activity in Malaysia"
            }
        
        # Next major event
        if upcoming_events:
            next_event = upcoming_events[0]
            seasonal_analysis['next_major_event'] = {
                'name': next_event['name'].replace('_', ' ').title(),
                'date': next_event['date'],
                'impact_level': next_event['impact'],
                'predicted_uplift': f"{round((next_event['revenue_multiplier'] - 1) * 100, 1)}%"
            }
        
        return seasonal_analysis

class EnhancedPredictiveEngine:
    """Enhanced predictions using velocity analysis and Malaysian context"""
    
    def __init__(self, malaysian_calendar: MalaysianBusinessCalendar):
        self.calendar = malaysian_calendar
    
    def generate_enhanced_predictions(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate enhanced predictions with Malaysian context"""
        current_value = context.get('current_value', 0)
        historical_trends = context.get('historical_trends', [])
        comparative_metrics = context.get('comparative_metrics', {})
        
        # Calculate velocity and trend
        velocity = comparative_metrics.get('recent_velocity', 0)
        target = comparative_metrics.get('target', current_value)
        
        # Generate time-based predictions
        predictions = {
            'short_term': self._predict_short_term(current_value, velocity, historical_trends),
            'medium_term': self._predict_medium_term(current_value, velocity, target),
            'seasonal_impact': self.calendar.get_seasonal_impact(context.get('kpi_type', ''), current_value),
            'confidence_factors': self._calculate_confidence(historical_trends, velocity)
        }
        
        return predictions
    
    def _predict_short_term(self, current_value: float, velocity: float, historical_trends: List[float]) -> Dict[str, Any]:
        """Predict 2-4 hour performance based on velocity"""
        if not velocity or not historical_trends:
            return {'predicted_value': 'Insufficient data', 'confidence': 'Low'}
        
        # Calculate micro-trend for short-term prediction
        micro_velocity = velocity * 0.1  # Assume 10% of period velocity for 2-4 hours
        predicted_short = current_value + micro_velocity
        
        # Calculate confidence based on trend stability
        recent_variance = np.var(historical_trends[-3:]) if len(historical_trends) >= 3 else 0
        confidence = 'High' if recent_variance < 1.0 else 'Medium' if recent_variance < 2.0 else 'Low'
        
        return {
            'predicted_value': round(predicted_short, 2),
            'confidence': confidence,
            'change_direction': 'Increase' if micro_velocity > 0 else 'Decrease' if micro_velocity < 0 else 'Stable',
            'basis': f"Based on recent velocity of {velocity:.2f} points per period"
        }
    
    def _predict_medium_term(self, current_value: float, velocity: float, target: float) -> Dict[str, Any]:
        """Predict 24-48 hour performance with Malaysian business context"""
        if not velocity:
            return {'predicted_value': 'Insufficient velocity data', 'confidence': 'Low'}
        
        # Predict based on 1-2 day velocity
        daily_velocity = velocity * 0.5  # Assume half period velocity per day
        predicted_medium = current_value + (daily_velocity * 1.5)  # 1.5 days average
        
        # Adjust for Malaysian business patterns
        current_hour = datetime.now().hour
        if 9 <= current_hour <= 18:  # Malaysian business hours
            predicted_medium *= 1.05  # 5% boost during business hours
        
        # Weekend adjustment
        if datetime.now().weekday() >= 5:  # Weekend
            predicted_medium *= 0.95  # 5% reduction for weekend
        
        confidence = self._assess_medium_confidence(velocity, target, predicted_medium)
        
        return {
            'predicted_value': round(predicted_medium, 2),
            'confidence': confidence,
            'target_progress': round(((predicted_medium - current_value) / (target - current_value)) * 100, 1) if target != current_value else 0,
            'business_context': 'Adjusted for Malaysian business hours and patterns'
        }
    
    def _assess_medium_confidence(self, velocity: float, target: float, predicted: float) -> str:
        """Assess confidence level for medium-term predictions"""
        if abs(velocity) < 0.1:
            return 'Low'  # Very slow movement
        elif abs(predicted - target) < 1.0:
            return 'High'  # Close to target
        else:
            return 'Medium'  # Standard prediction
    
    def _calculate_confidence(self, historical_trends: List[float], velocity: float) -> Dict[str, Any]:
        """Calculate confidence factors for predictions"""
        if not historical_trends or len(historical_trends) < 3:
            return {'overall': 'Low', 'factors': ['Insufficient historical data']}
        
        factors = []
        confidence_score = 0
        
        # Data quality factor
        if len(historical_trends) >= 5:
            factors.append('Sufficient historical data (5+ periods)')
            confidence_score += 30
        
        # Trend stability
        variance = np.var(historical_trends)
        if variance < 1.0:
            factors.append('Stable trend pattern')
            confidence_score += 25
        elif variance < 2.0:
            factors.append('Moderate trend stability')
            confidence_score += 15
        
        # Velocity reliability
        if abs(velocity) > 0.5:
            factors.append('Strong directional momentum')
            confidence_score += 25
        elif abs(velocity) > 0.1:
            factors.append('Moderate directional momentum')
            confidence_score += 15
        
        # Malaysian business context
        factors.append('Malaysian business patterns integrated')
        confidence_score += 20
        
        # Determine overall confidence
        if confidence_score >= 80:
            overall = 'High'
        elif confidence_score >= 60:
            overall = 'Medium'
        else:
            overall = 'Low'
        
        return {
            'overall': overall,
            'score': confidence_score,
            'factors': factors
        }
