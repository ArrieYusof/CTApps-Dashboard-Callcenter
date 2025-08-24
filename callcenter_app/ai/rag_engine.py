# Version: 0.1
# Last Modified: 2025-08-24
# Changes: Enhanced with Malaysian intelligence and better predictions
"""
RAG (Retrieval-Augmented Generation) Engine for Call Center Analytics
Combines historical data retrieval with OpenAI API for contextual insights
Enhanced with Malaysian business intelligence and predictive capabilities
"""
import json
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import numpy as np
from .malaysian_intelligence import MalaysianBusinessCalendar, EnhancedPredictiveEngine

class RAGEngine:
    """RAG engine for contextual data retrieval and analysis"""
    
    def __init__(self):
        self.historical_data = {}
        self.context_window = 30  # days
        # Initialize Malaysian business intelligence
        self.malaysian_calendar = MalaysianBusinessCalendar()
        self.predictive_engine = EnhancedPredictiveEngine(self.malaysian_calendar)
        self.load_knowledge_base()
    
    def load_knowledge_base(self):
        """Load historical data and knowledge base for RAG"""
        # In production, this would connect to your database
        # For now, we'll simulate historical data
        self.historical_data = {
            'call_volume': self._generate_historical_calls(),
            'agent_performance': self._generate_agent_history(),
            'customer_satisfaction': self._generate_csat_history(),
            'sla_metrics': self._generate_sla_history(),
            'seasonal_patterns': self._load_seasonal_patterns(),
            'best_practices': self._load_best_practices()
        }
    
    def retrieve_context_for_kpi(self, kpi_type: str, current_value: Any) -> Dict[str, Any]:
        """Retrieve contextual data for specific KPI type with executive dashboard support"""
        
        # Executive Dashboard KPI handlers
        if kpi_type == 'revenue_growth':
            return self._get_revenue_growth_context(current_value)
        elif kpi_type == 'cost_per_call':
            return self._get_cost_per_call_context(current_value)
        elif kpi_type == 'cash_flow':
            return self._get_cash_flow_context(current_value)
        elif kpi_type == 'profit_margin':
            return self._get_profit_margin_context(current_value)
        elif kpi_type == 'customer_retention':
            return self._get_customer_retention_context(current_value)
        elif kpi_type == 'kpi_performance':
            return self._get_kpi_performance_context(current_value)
            
        # Operational Dashboard KPI handlers (existing)
        elif kpi_type == 'call_volume':
            return self._get_call_volume_context(current_value)
        elif kpi_type == 'agent_availability':
            return self._get_agent_performance_context(current_value)
        elif kpi_type == 'service_level':
            return self._get_service_level_context(current_value)
        elif kpi_type == 'satisfaction_score':
            return self._get_satisfaction_context(current_value)
        elif kpi_type == 'first_call_resolution':
            return self._get_resolution_context(current_value)
        elif kpi_type == 'avg_response_time':
            return self._get_response_time_context(current_value)
        else:
            return self._get_general_context(kpi_type, current_value)
    
    def _get_call_volume_context(self, current_volume: int) -> Dict[str, Any]:
        """Retrieve call volume specific context"""
        historical = self.historical_data['call_volume']
        
        return {
            'historical_trends': historical[-30:],  # Last 30 days
            'comparative_metrics': {
                'yesterday_same_time': historical[-1] if historical else 0,
                'week_ago_same_time': historical[-7] if len(historical) >= 7 else 0,
                'monthly_average': np.mean(historical) if historical else 0,
                'peak_today': max(historical[-1:]) if historical else 0
            },
            'seasonal_patterns': self.historical_data['seasonal_patterns'].get('call_volume', {}),
            'relevant_patterns': [
                "Peak hours typically 10AM-12PM and 2PM-4PM",
                "Monday/Tuesday highest volume days",
                "End of month 15% increase in calls"
            ],
            'best_practices': self.historical_data['best_practices'].get('call_volume', [])
        }
    
    def _get_agent_performance_context(self, current_performance: float) -> Dict[str, Any]:
        """Retrieve agent performance context"""
        return {
            'historical_trends': self.historical_data['agent_performance'][-30:],
            'comparative_metrics': {
                'team_average': 85.2,
                'top_performer': 96.8,
                'industry_benchmark': 82.0,
                'monthly_trend': '+2.3%'
            },
            'relevant_patterns': [
                "Performance dips typically after lunch (1-2PM)",
                "New agents show 15% improvement after 90 days",
                "Training correlation: +0.8 with customer satisfaction"
            ],
            'best_practices': self.historical_data['best_practices'].get('agent_performance', [])
        }
    
    def _get_csat_context(self, current_csat: float) -> Dict[str, Any]:
        """Retrieve customer satisfaction context with Malaysian cultural considerations"""
        return {
            'historical_trends': self.historical_data['customer_satisfaction'][-30:],
            'malaysian_context': {
                'cultural_factors': {
                    'multi_cultural_market': 'Malay (60%), Chinese (22%), Indian (7%), Others (11%)',
                    'language_preferences': 'Bahasa Malaysia, English, Mandarin, Tamil support required',
                    'cultural_sensitivity': 'Respect for Malaysian festivals and religious observances',
                    'service_expectations': 'Malaysian customers value relationship-building and personal service'
                },
                'local_benchmarks': {
                    'malaysian_industry_avg': 4.3,
                    'asean_comparison': 4.4,
                    'local_competitors': [4.2, 4.5, 4.1, 4.6],
                    'government_service_benchmark': 4.0
                },
                'regulatory_compliance': {
                    'consumer_protection': 'Malaysian Consumer Protection Act 1999',
                    'data_privacy': 'Personal Data Protection Act 2010 (PDPA)',
                    'service_standards': 'Malaysian Standards MS ISO 9001:2015'
                }
            },
            'comparative_metrics': {
                'industry_average_malaysia': 4.3,
                'company_target': 4.5,
                'monthly_trend': '+0.2',
                'resolution_correlation': 0.85,
                'cultural_sensitivity_score': 4.1,
                'language_support_rating': 4.4
            },
            'relevant_patterns': [
                "CSAT strongly correlates with first-call resolution (0.85 correlation in Malaysian market)",
                "Malaysian customer satisfaction peaks during festival months (Chinese New Year, Hari Raya, Deepavali)",
                "Multi-language support correlation: Bahasa Malaysia (0.92), English (0.88), Mandarin (0.85)",
                "Cultural sensitivity training improves ratings by average 0.3 points in Malaysian market",
                "Technical issues show 20% lower satisfaction, 25% lower during Malaysian peak seasons",
                "Response time <30s increases CSAT by 15% (18% for Malaysian customers)",
                "Malaysian customers show 23% higher loyalty when cultural preferences are acknowledged"
            ],
            'best_practices': [
                "Implement multi-cultural customer service training for Malaysian market diversity",
                "Provide service in Bahasa Malaysia, English, Mandarin, and Tamil languages", 
                "Schedule adequate staffing during Malaysian festival seasons",
                "Train agents on Malaysian cultural etiquette and business customs",
                "Monitor satisfaction across different Malaysian ethnic communities",
                "Align service hours with Malaysian business culture (9 AM - 6 PM MYT)",
                "Implement Malaysian complaint resolution process within 24-48 hours",
                "Language localization could improve scores by 0.2-0.4 points",
                "Cultural awareness training showing 0.3 point average improvement"
            ] + self.historical_data['best_practices'].get('customer_satisfaction', [])
        }
    
    def _get_sla_context(self, current_sla: float) -> Dict[str, Any]:
        """Retrieve SLA monitoring context"""
        return {
            'historical_trends': self.historical_data['sla_metrics'][-30:],
            'comparative_metrics': {
                'target_sla': 95.0,
                'monthly_average': 89.2,
                'breach_incidents': 12,
                'cost_per_breach': 150
            },
            'relevant_patterns': [
                "SLA breaches increase 300% during peak hours",
                "Monday mornings highest risk period",
                "Queue >45 calls = 80% breach probability"
            ],
            'best_practices': self.historical_data['best_practices'].get('sla_monitoring', [])
        }
    
    def _get_queue_context(self, current_queue: int) -> Dict[str, Any]:
        """Retrieve queue status context"""
        return {
            'historical_trends': [45, 52, 38, 41, 47, 39, 44],  # Last 7 hours
            'comparative_metrics': {
                'average_wait_time': '3.2 min',
                'abandon_rate': '8.5%',
                'agents_available': 12,
                'peak_queue_today': 78
            },
            'relevant_patterns': [
                "Queue >50 calls triggers agent alerts",
                "Abandon rate increases 2x after 5min wait",
                "Lunch hours (12-1PM) show highest queue"
            ],
            'best_practices': self.historical_data['best_practices'].get('queue_management', [])
        }
    
    # Helper methods for generating mock data
    def _generate_historical_calls(self) -> List[int]:
        """Generate realistic call volume history"""
        base = 2800
        return [base + int(np.random.normal(0, 200)) for _ in range(30)]
    
    def _generate_agent_history(self) -> List[float]:
        """Generate agent performance history"""
        base = 85.0
        return [base + np.random.normal(0, 5) for _ in range(30)]
    
    def _generate_csat_history(self) -> List[float]:
        """Generate CSAT history"""
        base = 4.1
        return [max(1.0, min(5.0, base + np.random.normal(0, 0.3))) for _ in range(30)]
    
    def _generate_sla_history(self) -> List[float]:
        """Generate SLA metrics history"""
        base = 88.0
        return [max(60.0, min(100.0, base + np.random.normal(0, 8))) for _ in range(30)]
    
    def _load_seasonal_patterns(self) -> Dict[str, Any]:
        """Load seasonal and temporal patterns"""
        return {
            'call_volume': {
                'hourly_pattern': [0.6, 0.3, 0.2, 0.3, 0.5, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 1.5, 1.0, 1.3, 1.7, 1.9, 1.6, 1.2, 0.9, 0.7, 0.5, 0.4, 0.3, 0.4],
                'daily_pattern': [1.2, 1.3, 1.1, 1.0, 0.9, 0.8, 0.7],  # Mon-Sun
                'monthly_pattern': [1.1, 1.0, 1.2, 1.1, 0.9, 0.8, 0.9, 1.0, 1.1, 1.3, 1.2, 1.4]  # Jan-Dec
            }
        }
    
    def _load_best_practices(self) -> Dict[str, List[str]]:
        """Load best practices knowledge base"""
        return {
            'call_volume': [
                "Add 1 agent per 100 calls above baseline",
                "Monitor queue every 15 minutes during peak",
                "Implement callback option when queue >40"
            ],
            'agent_performance': [
                "Provide real-time coaching for scores <80%",
                "Review call recordings for improvement",
                "Pair low performers with top performers"
            ],
            'customer_satisfaction': [
                "Follow up on CSAT scores <3.0 within 24h",
                "Analyze negative feedback for patterns",
                "Implement proactive communication for delays"
            ],
            'sla_monitoring': [
                "Alert supervisors when SLA drops below 85%",
                "Adjust staffing 30min before predicted peaks",
                "Have overflow process ready for high volumes"
            ]
        }

    # Executive Dashboard Context Methods
    def _get_revenue_growth_context(self, current_value: Any) -> Dict[str, Any]:
        """Get revenue growth specific context with enhanced Malaysian predictions"""
        # Convert from thousands to actual currency values (1000 -> 1,000,000)
        historical_trends = [1000000, 1100000, 1200000, 1300000, 1400000]  # Actual currency values
        target = 1500000.0  # Target growth in actual currency
        industry_avg = 1200000.0  # Industry average in actual currency
        
        # Calculate performance metrics
        performance_gap = target - current_value
        gap_percentage = (performance_gap / target) * 100
        recent_velocity = historical_trends[-1] - historical_trends[-2] if len(historical_trends) >= 2 else 0
        total_growth = historical_trends[-1] - historical_trends[0] if len(historical_trends) >= 2 else 0
        growth_percentage = (total_growth / historical_trends[0]) * 100 if historical_trends[0] != 0 else 0
        periods_to_target = performance_gap / recent_velocity if recent_velocity > 0 else float('inf')
        
        # Generate enhanced predictions using Malaysian intelligence
        context_for_prediction = {
            'kpi_type': 'revenue_growth',
            'current_value': current_value,
            'historical_trends': historical_trends,
            'comparative_metrics': {
                'recent_velocity': recent_velocity,
                'target': target,
                'performance_gap': performance_gap
            }
        }
        
        enhanced_predictions = self.predictive_engine.generate_enhanced_predictions(context_for_prediction)
        malaysian_seasonal = self.malaysian_calendar.get_seasonal_impact('revenue_growth', current_value)
        
        return {
            'kpi_type': 'revenue_growth',
            'current_value': current_value,
            'unit': 'percentage',
            'malaysian_context': {
                'currency': 'RM (Ringgit Malaysia)',
                'business_hours': '9:00 AM - 6:00 PM MYT',
                'regulatory_framework': 'Malaysian Companies Commission (SSM) standards',
                'market_focus': 'Southeast Asian markets with Malaysian base',
                'seasonal_patterns': 'Malaysian festival seasons (CNY, Raya, Deepavali impact)',
                'economic_indicators': 'Bank Negara Malaysia benchmark rates'
            },
            'comparative_metrics': {
                'last_quarter': 10.2,
                'last_year_same_period': 8.7,
                'industry_average_malaysia': industry_avg,
                'target': target,
                'performance_gap': performance_gap,
                'gap_percentage': round(gap_percentage, 1),
                'recent_velocity': recent_velocity,
                'total_growth': total_growth,
                'growth_percentage': round(growth_percentage, 1),
                'periods_to_target': round(periods_to_target, 1) if periods_to_target != float('inf') else None
            },
            'historical_trends': historical_trends,
            'relevant_patterns': [
                "Revenue growth in Malaysia typically accelerates during Q2-Q3 due to corporate budget cycles and mid-year bonuses",
                "Strong correlation with customer acquisition rates (0.85 correlation coefficient) in Malaysian market",
                "Malaysian festival seasons (Chinese New Year, Hari Raya, Deepavali) create 15-20% revenue peaks",
                f"Current velocity of {recent_velocity} points per period indicates {periods_to_target:.1f} periods to reach target based on Malaysian market dynamics" if periods_to_target != float('inf') else "Current stagnant velocity requires immediate intervention aligned with Malaysian business practices",
                "Malaysian consumer spending patterns show strong correlation with government policy announcements and EPF withdrawals"
            ],
            'best_practices': [
                "Focus on customer lifetime value improvement - Malaysian market average RM 7,200 per customer (USD $2,400 equivalent)",
                "Diversify revenue streams to reduce volatility - target 30% from new digital channels popular in Malaysia", 
                "Leverage Malaysian Q2-Q3 corporate spending cycles and government budget announcements for maximum impact",
                "Implement customer retention strategies for Malaysian multicultural customer base",
                "Launch targeted campaigns during Malaysian festival seasons for 18% seasonal uplift",
                "Consider Malaysian business hour optimization (9 AM - 6 PM MYT) for customer engagement",
                "Align strategies with Malaysian regulatory requirements and Bank Negara guidelines"
            ],
            'financial_context': {
                'currency': 'RM',
                'revenue_per_point': 30000,  # RM 30K per revenue growth point (Malaysian market)
                'financial_shortfall': performance_gap * 30000,  # In RM
                'seasonal_opportunity': current_value * 0.18,  # 18% Malaysian festival boost potential
                'market_expansion_potential': 2.5,  # 2.5 point potential from Malaysian market expansion
                'exchange_rate_note': '1 USD ≈ 3.0 RM (for international comparisons)',
                'malaysian_benchmarks': {
                    'avg_customer_value': 7200,  # RM 7,200
                    'market_growth_rate': 8.5,   # Malaysian market average
                    'digital_adoption_rate': 0.75  # 75% digital adoption in Malaysia
                }
            },
            # Enhanced predictions with Malaysian intelligence
            'enhanced_predictions': enhanced_predictions,
            'malaysian_seasonal_intelligence': malaysian_seasonal
        }

    def _get_cost_per_call_context(self, current_value: Any) -> Dict[str, Any]:
        """Get cost per call specific context with Malaysian business considerations"""
        return {
            'kpi_type': 'cost_per_call',
            'current_value': current_value,
            'unit': 'ringgit_malaysia',
            'malaysian_context': {
                'currency': 'RM (Ringgit Malaysia)',
                'cost_structure': {
                    'agent_hourly_rate': 'RM 12-18 per hour (junior to senior)',
                    'technology_costs': 'RM 0.60 per call (telecom + software)',
                    'overhead_allocation': 'RM 0.35 per call (facilities, management)',
                    'training_amortization': 'RM 0.15 per call'
                },
                'local_benchmarks': {
                    'malaysian_industry_avg': 3.40,  # RM 3.40
                    'government_service_cost': 4.20,  # RM 4.20
                    'private_sector_best': 1.80,     # RM 1.80
                    'regional_comparison': 'ASEAN average: RM 3.20'
                },
                'regulatory_considerations': {
                    'minimum_wage': 'RM 1,500/month base requirement',
                    'epf_contribution': '13% EPF + 1.75% SOCSO employer contribution',
                    'service_tax': '6% SST on technology services'
                }
            },
            'comparative_metrics': {
                'last_month': 2.60,  # RM 2.60 
                'industry_benchmark_malaysia': 3.40,  # RM 3.40
                'target': 2.20,  # RM 2.20
                'best_in_class_malaysia': 1.80,  # RM 1.80
                'cost_breakdown': {
                    'agent_cost': 1.50,     # RM 1.50 (61%)
                    'technology': 0.60,      # RM 0.60 (25%)
                    'overhead': 0.35,        # RM 0.35 (14%)
                }
            },
            'historical_trends': [2.90, 2.85, 2.60, 2.67, 2.55],  # All in RM
            'relevant_patterns': [
                "Cost decreases with higher agent efficiency in Malaysian market",
                "Technology investments reduce long-term costs by RM 0.30-0.50 per call over 12 months",
                "Malaysian agent training programs show 3-month ROI with RM 0.20 average cost reduction",
                "Festival season overtime increases costs by 15-20% during Malaysian peak periods",
                "Multi-language support adds RM 0.15 per call but improves resolution by 25%"
            ],
            'best_practices': [
                "Implement self-service options for common issues - reduces cost by RM 0.80-1.20 per avoided call",
                "Optimize call routing to reduce transfer costs in Malaysian market",
                "Invest in Malaysian multi-cultural agent training for first-call resolution",
                "Leverage Malaysian government training grants (HRDF) to reduce training costs",
                "Schedule staffing to align with Malaysian business hours (9 AM - 6 PM MYT)",
                "Implement Bahasa Malaysia IVR to reduce agent routing costs by RM 0.23 per call"
            ],
            'financial_impact': {
                'cost_savings_potential': 0.49,  # RM 0.49 per call with optimization
                'monthly_volume_impact': 12000,  # 12K calls per month
                'annual_savings_opportunity': 235000,  # RM 235K annually
                'roi_timeline': '3-6 months for technology investments',
                'exchange_rate_reference': '1 USD ≈ 3.0 RM for international comparisons'
            }
        }

    def _get_cash_flow_context(self, current_value: Any) -> Dict[str, Any]:
        """Get cash flow specific context with Malaysian business considerations"""
        return {
            'kpi_type': 'cash_flow',
            'current_value': current_value,
            'unit': 'ringgit_malaysia',
            'malaysian_context': {
                'currency': 'RM (Ringgit Malaysia)',
                'business_environment': {
                    'payment_cycles': 'Malaysian B2B typical 30-60 day payment terms',
                    'seasonal_factors': 'Q4 slower collections due to year-end holidays',
                    'regulatory_cash_requirements': 'Maintain minimum 3-month operational buffer',
                    'banking_relationships': 'Local banking partnerships for optimal cash management'
                },
                'economic_factors': {
                    'currency_stability': 'RM exchange rate impacts international collections',
                    'interest_rates': 'OPR (Overnight Policy Rate) affects financing costs',
                    'business_cycles': 'Malaysian economic cycles impact customer payment behavior',
                    'government_policies': 'Tax incentives and grants affect cash timing'
                }
            },
            'comparative_metrics': {
                'last_month': 850000,  # RM 850K (Q3)
                'quarterly_target': 2400000,  # RM 2.4M (annual target / 4 quarters)
                'operating_expenses': 620000,  # RM 620K
                'net_margin': 250000,  # RM 250K
                'working_capital': 400000,  # RM 400K
                'free_cash_flow': 290000,  # RM 290K
                'cash_conversion_cycle': 45,  # days
                'liquidity_ratio': 2.1
            },
            'historical_trends': [750000, 820000, 850000, 870000],  # Q1-Q4 in RM
            'relevant_patterns': [
                "Cash flow peaks during Malaysian Q2-Q3 corporate budget cycles",
                "Seasonal variations during Malaysian festival seasons (CNY, Hari Raya) affect collections",
                "Malaysian customer payment behavior correlates with EPF withdrawal seasons",
                "Government contract payments follow Malaysian fiscal year cycles",
                "Technology investments show 6-month payback in Malaysian market"
            ],
            'best_practices': [
                "Maintain 3-month RM operating expense buffer for Malaysian market volatility",
                "Optimize accounts receivable collection aligned with Malaysian payment cycles",
                "Plan capital expenditures during high-flow Q2-Q3 periods",
                "Leverage Malaysian government grants and tax incentives for cash timing",
                "Implement Malaysian Ringgit hedging for international customer collections",
                "Use local banking relationships for efficient cash management"
            ],
            'financial_impact': {
                'monthly_operating_needs': 650000,  # RM 650K monthly
                'growth_investment_capacity': 180000,  # RM 180K for growth
                'emergency_reserves': 1950000,  # RM 1.95M (3-month buffer)
                'debt_service_capacity': 85000,  # RM 85K monthly
                'roi_investment_threshold': 15.0  # 15% minimum ROI for Malaysian projects
            }
        }

    def _get_profit_margin_context(self, current_value: Any) -> Dict[str, Any]:
        """Get profit margin specific context"""
        return {
            'kpi_type': 'profit_margin',
            'current_value': current_value,
            'unit': 'percentage',
            'comparative_metrics': {
                'last_quarter': 17.1,
                'industry_average': 16.8,
                'target': 20.0,
                'best_performers': 22.5
            },
            'historical_trends': [15.2, 16.1, 17.1, 18.0, 18.3],
            'relevant_patterns': [
                "Margin improvement correlates with operational efficiency",
                "Scale effects become visible above $1M revenue",
                "Technology investments show delayed margin benefits"
            ],
            'best_practices': [
                "Focus on high-margin service offerings",
                "Automate routine processes to reduce costs",
                "Negotiate better supplier contracts annually"
            ]
        }

    def _get_customer_retention_context(self, current_value: Any) -> Dict[str, Any]:
        """Get customer retention specific context"""
        return {
            'kpi_type': 'customer_retention',
            'current_value': current_value,
            'unit': 'percentage',
            'comparative_metrics': {
                'last_month': 93.8,
                'industry_benchmark': 91.2,
                'target': 96.0,
                'churn_cost_per_customer': 450
            },
            'historical_trends': [92.1, 93.2, 93.8, 94.2, 94.7],
            'relevant_patterns': [
                "Retention improves significantly after 6-month mark",
                "Proactive communication reduces churn by 15%",
                "Service quality directly correlates with retention"
            ],
            'best_practices': [
                "Implement early warning churn detection",
                "Create customer success programs",
                "Regular satisfaction surveys and follow-ups"
            ]
        }

    def _get_kpi_performance_context(self, current_value: Any) -> Dict[str, Any]:
        """Get overall KPI performance context"""
        return {
            'kpi_type': 'kpi_performance',
            'current_value': current_value,
            'unit': 'percentage',
            'comparative_metrics': {
                'last_month': 82.7,
                'department_average': 79.3,
                'target': 90.0,
                'top_performers': 93.5
            },
            'historical_trends': [78.2, 80.1, 82.7, 84.5, 85.3],
            'relevant_patterns': [
                "Performance improves with consistent monitoring",
                "Cross-functional collaboration boosts scores",
                "Training investments show 6-8 week delays"
            ],
            'best_practices': [
                "Set clear, measurable KPI targets",
                "Provide real-time performance dashboards",
                "Regular review and adjustment cycles"
            ]
        }

    def _get_general_context(self, kpi_type: str, current_value: Any) -> Dict[str, Any]:
        """Get general context for unknown KPI types"""
        return {
            'kpi_type': kpi_type,
            'current_value': current_value,
            'unit': 'unknown',
            'comparative_metrics': {
                'baseline': current_value * 0.9,
                'target': current_value * 1.1
            },
            'historical_trends': [current_value * 0.95, current_value * 1.02, current_value],
            'relevant_patterns': [
                "Performance metrics require consistent monitoring",
                "Trends emerge over 3-6 month periods"
            ],
            'best_practices': [
                "Establish clear measurement criteria",
                "Regular data quality checks",
                "Benchmarking against industry standards"
            ]
        }
