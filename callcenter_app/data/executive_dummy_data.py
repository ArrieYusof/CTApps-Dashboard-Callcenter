# Version: 0.2
# Last Modified: 2025-08-23
# Changes: Enhanced dummy data structure for executive dashboard
"""
All data in this file is for wireframe/mockup only. Remove and replace with DB queries in production.
"""

def get_executive_data():
    """Return structured dummy data for executive dashboard"""
    return {
        "revenue_growth": [1000, 1100, 950, 1200, 1350, 1250, 1400],  # 7-point trend
        "cost_per_call": [2.8, 2.7, 2.9, 2.6, 2.5, 2.4, 2.45],      # Decreasing cost trend
        "cash_flow": [750, 820, 850, 870, 890, 890, 890],             # Cash flow in thousands (RM)
        "efficiency": [88, 89, 91, 92, 93, 94, 94.2],                 # Improving efficiency
        "retention": [91, 90, 89.5, 89, 89.2, 89.5, 89.4],           # Slight decline
        "summary_data": [75, 78, 82, 85, 88, 90, 92]                  # Overall trend
    }

# Legacy data for backward compatibility
revenue_growth = [300, 400, 250, 250]  # Q1-Q4
cost_per_call = [2.5, 2.7, 2.4]        # Jan-Mar
customer_retention = [85, 87, 88]      # 2023-2025
