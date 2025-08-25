#!/usr/bin/env python3
"""
Malaysian Call Center Business Data Generator
Generates realistic 24-month business data with Malaysian context
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
import math

class MalaysianBusinessDataGenerator:
    def __init__(self):
        self.current_date = datetime(2025, 8, 25)  # August 25, 2025
        self.base_kpis = {
            "revenue_growth": 1400000,      # RM 1.4M current
            "customer_satisfaction": 4.2,   # Current rating
            "call_volume": 8500,            # Calls per month
            "cost_per_call": 12.50,         # RM per call
            "first_call_resolution": 78.5,  # Percentage
            "customer_retention": 89.2,     # Percentage
            "average_handle_time": 285,     # Seconds
            "average_wait_time": 45,        # Seconds
            "call_abandonment": 6.8,        # Percentage
            "profit_margin": 23.5           # Percentage
        }
        
        # Malaysian seasonal patterns (impact %)
        self.seasonal_patterns = {
            1: {"name": "January", "revenue": -5, "satisfaction": 0, "volume": -10, "pattern": "post_holiday_dip"},
            2: {"name": "February", "revenue": 20, "satisfaction": 5, "volume": 15, "pattern": "chinese_new_year_surge"},
            3: {"name": "March", "revenue": -8, "satisfaction": -2, "volume": -5, "pattern": "post_cny_normalization"},
            4: {"name": "April", "revenue": 15, "satisfaction": 3, "volume": 10, "pattern": "ramadan_preparation_boost"},
            5: {"name": "May", "revenue": -12, "satisfaction": -3, "volume": -8, "pattern": "ramadan_business_slowdown"},
            6: {"name": "June", "revenue": 25, "satisfaction": 8, "volume": 20, "pattern": "raya_celebration_surge"},
            7: {"name": "July", "revenue": 12, "satisfaction": 4, "volume": 8, "pattern": "mid_year_corporate_budgets"},
            8: {"name": "August", "revenue": 10, "satisfaction": 2, "volume": 5, "pattern": "merdeka_patriotic_spending"},
            9: {"name": "September", "revenue": 8, "satisfaction": 1, "volume": 3, "pattern": "malaysia_day_boost"},
            10: {"name": "October", "revenue": -6, "satisfaction": -1, "volume": -4, "pattern": "monsoon_season_dip"},
            11: {"name": "November", "revenue": 18, "satisfaction": 6, "volume": 12, "pattern": "deepavali_festival_boost"},
            12: {"name": "December", "revenue": -3, "satisfaction": 1, "volume": -2, "pattern": "year_end_mixed_activity"}
        }
        
        # Competitor benchmarks (Malaysian call center industry)
        self.competitor_benchmarks = {
            "industry_average": {
                "revenue_per_month": 1200000,  # RM 1.2M
                "customer_satisfaction": 3.8,
                "call_volume": 7200,
                "cost_per_call": 14.20,
                "first_call_resolution": 72.0,
                "customer_retention": 84.5,
                "average_handle_time": 320,
                "average_wait_time": 55,
                "call_abandonment": 8.5,
                "profit_margin": 19.8
            },
            "top_performer": {
                "revenue_per_month": 1800000,  # RM 1.8M
                "customer_satisfaction": 4.6,
                "call_volume": 12000,
                "cost_per_call": 10.80,
                "first_call_resolution": 85.0,
                "customer_retention": 92.5,
                "average_handle_time": 245,
                "average_wait_time": 35,
                "call_abandonment": 4.2,
                "profit_margin": 28.5
            },
            "market_leader": {
                "company": "TM Contact Center",
                "revenue_per_month": 2500000,  # RM 2.5M
                "customer_satisfaction": 4.8,
                "market_share": 25.5
            }
        }

    def generate_monthly_data(self, month: int, year: int, is_future: bool = False) -> Dict[str, Any]:
        """Generate realistic monthly data with Malaysian patterns"""
        
        seasonal = self.seasonal_patterns.get(month, {"revenue": 0, "satisfaction": 0, "volume": 0})
        
        # Add some randomness but keep it realistic
        random_factor = random.uniform(0.85, 1.15)  # ±15% variation
        
        # Calculate growth trend (future projections show modest growth)
        months_from_current = self._months_difference(year, month, self.current_date.year, self.current_date.month)
        growth_factor = 1 + (months_from_current * 0.02) if is_future else 1 - (abs(months_from_current) * 0.01)
        
        # Generate data for each KPI
        data = {
            "date": f"{year}-{month:02d}-01",
            "month_name": seasonal["name"],
            "is_projection": is_future,
            "kpis": {}
        }
        
        # Revenue Growth
        base_revenue = self.base_kpis["revenue_growth"]
        seasonal_impact = seasonal["revenue"] / 100
        revenue = base_revenue * (1 + seasonal_impact) * growth_factor * random_factor
        data["kpis"]["revenue_growth"] = {
            "value": round(revenue, 0),
            "currency": "RM",
            "vs_target": round(((revenue - 1500000) / 1500000) * 100, 1),
            "vs_previous_month": round(random.uniform(-8, 12), 1),
            "seasonal_factor": seasonal["pattern"]
        }
        
        # Customer Satisfaction
        base_satisfaction = self.base_kpis["customer_satisfaction"]
        satisfaction_impact = seasonal["satisfaction"] / 100 * 0.5  # Smaller impact for satisfaction
        satisfaction = base_satisfaction + satisfaction_impact + random.uniform(-0.2, 0.3)
        satisfaction = max(1.0, min(5.0, satisfaction))  # Clamp between 1-5
        data["kpis"]["customer_satisfaction"] = {
            "value": round(satisfaction, 1),
            "scale": "1-5",
            "vs_target": round(((satisfaction - 4.62) / 4.62) * 100, 1),
            "trend": "improving" if satisfaction > base_satisfaction else "declining",
            "seasonal_factor": seasonal["pattern"]
        }
        
        # Call Volume
        base_volume = self.base_kpis["call_volume"]
        volume_impact = seasonal["volume"] / 100
        volume = base_volume * (1 + volume_impact) * growth_factor * random_factor
        data["kpis"]["call_volume"] = {
            "value": round(volume, 0),
            "unit": "calls",
            "daily_average": round(volume / 30, 0),
            "peak_hours": "9AM-11AM, 2PM-4PM MYT",
            "seasonal_factor": seasonal["pattern"]
        }
        
        # Cost per Call
        base_cost = self.base_kpis["cost_per_call"]
        # Costs generally increase over time but improve with volume
        cost_efficiency = 1 - (volume_impact * 0.1)  # Higher volume = lower cost per call
        cost = base_cost * cost_efficiency * (1 + months_from_current * 0.005)
        data["kpis"]["cost_per_call"] = {
            "value": round(cost, 2),
            "currency": "RM",
            "vs_industry": round(((cost - 14.20) / 14.20) * 100, 1),
            "efficiency_trend": "improving" if cost < base_cost else "declining"
        }
        
        # First Call Resolution
        base_fcr = self.base_kpis["first_call_resolution"]
        fcr_improvement = satisfaction_impact * 10  # Good satisfaction correlates with FCR
        fcr = base_fcr + fcr_improvement + random.uniform(-2, 3)
        fcr = max(60, min(95, fcr))  # Realistic bounds
        data["kpis"]["first_call_resolution"] = {
            "value": round(fcr, 1),
            "unit": "percentage",
            "vs_target": round(fcr - 80, 1),
            "impact_on_satisfaction": "high_correlation"
        }
        
        # Customer Retention
        base_retention = self.base_kpis["customer_retention"]
        retention_seasonal = seasonal_impact * 2  # Seasonal events affect retention
        retention = base_retention + retention_seasonal + random.uniform(-1, 2)
        retention = max(75, min(98, retention))
        data["kpis"]["customer_retention"] = {
            "value": round(retention, 1),
            "unit": "percentage", 
            "churn_rate": round(100 - retention, 1),
            "vs_industry": round(retention - 84.5, 1)
        }
        
        # Average Handle Time
        base_aht = self.base_kpis["average_handle_time"]
        aht_variation = random.uniform(-15, 20)  # AHT can vary significantly
        aht = base_aht + aht_variation
        data["kpis"]["average_handle_time"] = {
            "value": round(aht, 0),
            "unit": "seconds",
            "minutes": round(aht / 60, 1),
            "vs_target": round(aht - 300, 0),
            "efficiency_indicator": "good" if aht < 300 else "needs_improvement"
        }
        
        # Average Wait Time
        base_wait = self.base_kpis["average_wait_time"]
        wait_volume_impact = (volume / base_volume - 1) * 20  # Higher volume = longer waits
        wait = base_wait + wait_volume_impact + random.uniform(-5, 10)
        wait = max(15, wait)
        data["kpis"]["average_wait_time"] = {
            "value": round(wait, 0),
            "unit": "seconds",
            "vs_target": round(wait - 30, 0),
            "customer_impact": "high" if wait > 60 else "moderate"
        }
        
        # Call Abandonment
        base_abandon = self.base_kpis["call_abandonment"]
        abandon_wait_correlation = (wait - 30) / 10  # Higher wait = higher abandonment
        abandon = base_abandon + abandon_wait_correlation + random.uniform(-1, 2)
        abandon = max(2, min(15, abandon))
        data["kpis"]["call_abandonment"] = {
            "value": round(abandon, 1),
            "unit": "percentage",
            "vs_target": round(abandon - 5.0, 1),
            "correlation_with_wait_time": "strong_positive"
        }
        
        # Profit Margin
        base_profit = self.base_kpis["profit_margin"]
        profit_efficiency = (1 - cost / base_cost) * 10  # Lower costs = higher profit
        profit_seasonal = seasonal_impact * 5  # Seasonal revenue affects profit
        profit = base_profit + profit_efficiency + profit_seasonal + random.uniform(-2, 3)
        profit = max(5, min(40, profit))
        data["kpis"]["profit_margin"] = {
            "value": round(profit, 1),
            "unit": "percentage",
            "vs_industry": round(profit - 19.8, 1),
            "revenue_impact": round(revenue * (profit / 100), 0)
        }
        
        # Add business context
        data["business_context"] = {
            "malaysian_events": self._get_malaysian_events(month),
            "economic_factors": self._get_economic_context(month, year),
            "competitive_landscape": "Moderate competition, stable market share"
        }
        
        return data
    
    def _months_difference(self, year1: int, month1: int, year2: int, month2: int) -> int:
        """Calculate difference in months between two dates"""
        return (year1 - year2) * 12 + (month1 - month2)
    
    def _get_malaysian_events(self, month: int) -> List[str]:
        """Get relevant Malaysian events for the month"""
        events_map = {
            1: ["New Year holidays impact"],
            2: ["Chinese New Year celebrations", "Increased consumer spending"],
            3: ["Post-CNY normalization period"],
            4: ["Ramadan preparation period"],
            5: ["Ramadan fasting month", "Reduced business activity"],
            6: ["Hari Raya celebrations", "Major spending surge"],
            7: ["Mid-year corporate budget reviews"],
            8: ["Merdeka Day preparations", "Patriotic spending"],
            9: ["Malaysia Day celebrations"],
            10: ["Monsoon season begins", "Reduced activity"],
            11: ["Deepavali celebrations", "Hindu community spending"],
            12: ["Year-end activities", "Mixed business patterns"]
        }
        return events_map.get(month, [])
    
    def _get_economic_context(self, month: int, year: int) -> Dict[str, str]:
        """Get economic context for Malaysian business environment"""
        return {
            "currency": "RM (Ringgit Malaysia)",
            "business_hours": "9AM-6PM MYT",
            "market_maturity": "Developing digital services sector",
            "regulatory_environment": "Bank Negara Malaysia oversight",
            "economic_outlook": "Stable growth with digital transformation focus"
        }
    
    def generate_full_dataset(self) -> Dict[str, Any]:
        """Generate complete 24-month dataset"""
        
        # Generate 12 months historical data
        historical_data = []
        for i in range(12, 0, -1):  # 12 months back to 1 month back
            target_date = self.current_date - timedelta(days=30 * i)
            monthly_data = self.generate_monthly_data(target_date.month, target_date.year, is_future=False)
            historical_data.append(monthly_data)
        
        # Add current month
        current_data = self.generate_monthly_data(self.current_date.month, self.current_date.year, is_future=False)
        
        # Generate 12 months future projections
        future_data = []
        for i in range(1, 13):  # Next 12 months
            target_date = self.current_date + timedelta(days=30 * i)
            monthly_data = self.generate_monthly_data(target_date.month, target_date.year, is_future=True)
            future_data.append(monthly_data)
        
        # Compile complete dataset
        complete_dataset = {
            "metadata": {
                "generated_at": self.current_date.isoformat(),
                "data_range": "24 months (12 historical + current + 12 projections)",
                "country": "Malaysia",
                "currency": "RM",
                "business_type": "Call Center Operations",
                "data_quality": "Realistic simulation with Malaysian business patterns"
            },
            "current_snapshot": {
                "date": self.current_date.strftime("%Y-%m-%d"),
                "current_kpis": current_data["kpis"],
                "business_status": "Operational - Meeting most targets with room for improvement"
            },
            "historical_data": historical_data,
            "future_projections": future_data,
            "competitor_benchmarks": self.competitor_benchmarks,
            "trend_analysis": self._generate_trend_analysis(historical_data + [current_data]),
            "malaysian_business_calendar": self._generate_business_calendar()
        }
        
        return complete_dataset
    
    def _generate_trend_analysis(self, data: List[Dict]) -> Dict[str, Any]:
        """Generate trend analysis from historical data"""
        if len(data) < 2:
            return {}
        
        # Calculate trends for key metrics
        revenues = [d["kpis"]["revenue_growth"]["value"] for d in data[-6:]]  # Last 6 months
        satisfactions = [d["kpis"]["customer_satisfaction"]["value"] for d in data[-6:]]
        
        revenue_trend = "growing" if revenues[-1] > revenues[0] else "declining"
        satisfaction_trend = "improving" if satisfactions[-1] > satisfactions[0] else "declining"
        
        return {
            "revenue_trend": {
                "direction": revenue_trend,
                "6_month_change": round(((revenues[-1] - revenues[0]) / revenues[0]) * 100, 1),
                "average_monthly_revenue": round(sum(revenues) / len(revenues), 0)
            },
            "satisfaction_trend": {
                "direction": satisfaction_trend,
                "6_month_change": round(satisfactions[-1] - satisfactions[0], 2),
                "average_satisfaction": round(sum(satisfactions) / len(satisfactions), 2)
            },
            "business_momentum": "positive" if revenue_trend == "growing" and satisfaction_trend == "improving" else "mixed",
            "key_insights": [
                f"Revenue has been {revenue_trend} over the last 6 months",
                f"Customer satisfaction is {satisfaction_trend}",
                "Seasonal patterns strongly influence performance",
                "Malaysian festivals create significant business opportunities"
            ]
        }
    
    def _generate_business_calendar(self) -> Dict[str, List[str]]:
        """Generate Malaysian business calendar with key events"""
        return {
            "Q1": ["Chinese New Year (Jan/Feb)", "Post-holiday recovery", "Ramadan preparation"],
            "Q2": ["Ramadan period", "Hari Raya celebrations", "Mid-year corporate budgets"],
            "Q3": ["Merdeka Day (Aug 31)", "Malaysia Day (Sep 16)", "Corporate Q3 reviews"],
            "Q4": ["Deepavali celebrations", "Year-end planning", "Monsoon season impact"]
        }

def main():
    """Generate and save business data"""
    print("🇲🇾 Generating Malaysian Call Center Business Data...")
    print("=" * 60)
    
    generator = MalaysianBusinessDataGenerator()
    
    # Generate complete dataset
    print("📊 Creating 24-month realistic dataset...")
    dataset = generator.generate_full_dataset()
    
    # Create data directory
    import os
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"📁 Created directory: {data_dir}")
    
    # Save complete dataset
    output_file = f"{data_dir}/malaysian_callcenter_data.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Generated comprehensive business data: {output_file}")
    print(f"📈 Data includes:")
    print(f"   • 24 months of data (12 historical + current + 12 projections)")
    print(f"   • 10 key KPIs with Malaysian business context")
    print(f"   • Seasonal patterns and Malaysian events")
    print(f"   • Competitor benchmarks")
    print(f"   • Trend analysis and insights")
    
    # Display sample data
    current_revenue = dataset["current_snapshot"]["current_kpis"]["revenue_growth"]["value"]
    current_satisfaction = dataset["current_snapshot"]["current_kpis"]["customer_satisfaction"]["value"]
    
    print(f"\n📊 Current Performance Snapshot:")
    print(f"   💰 Revenue: RM {current_revenue:,}")
    print(f"   😊 Customer Satisfaction: {current_satisfaction}/5.0")
    print(f"   📅 Data as of: {dataset['metadata']['generated_at'][:10]}")
    
    print(f"\n🚀 Ready for lightning-fast AI responses!")
    print("=" * 60)

if __name__ == "__main__":
    main()
