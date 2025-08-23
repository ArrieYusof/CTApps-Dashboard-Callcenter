# Version: 0.2
# Last Modified: 2025-08-23
# Changes: Enhanced dummy data structure for operational dashboard
"""
All data in this file is for wireframe/mockup only. Remove and replace with DB queries in production.
"""

def get_operational_data():
    """Return structured dummy data for operational dashboard"""
    return {
        "queue_status": [12, 25, 47],  # Calls in Queue 1, 2, 3
        # Simulate 20 agents with random handle times between 3.5 and 4.5 min
        "agent_performance": [round(3.5 + (i % 10) * 0.1, 2) for i in range(20)],
        "sla_monitoring": [85, 82, 78, 75, 78, 79, 78.5],  # SLA percentage over time
        "customer_satisfaction": [4.2, 4.0, 4.1, 3.9, 4.0, 4.1, 4.1],  # CSAT scores
        "call_outcomes": [88, 89, 87, 89, 90, 89, 89],  # Resolution rate
        "resource_utilization": [90, 91, 94, 92, 89, 91, 92]  # Staff utilization %
    }

def get_agent_availability():
    """Return dummy data for agent availability status"""
    return {
        "Online": 14,
        "On Break": 4,
        "In Training": 2
    }

# Legacy data for backward compatibility
queue_status = [12, 8, 5]              # Queue 1-3
agent_performance = [40, 35, 45]       # Agent A-C
sla_monitoring = [98, 97, 96]          # Mon-Wed
