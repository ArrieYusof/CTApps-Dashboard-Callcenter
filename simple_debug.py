#!/usr/bin/env python3
"""
Simple debug: Check if Agent 3's actual data value is causing the issue
"""

def get_operational_data():
    """Return structured dummy data for operational dashboard"""
    return {
        "agent_performance": [round(3.5 + (i % 10) * 0.1, 2) for i in range(20)],
    }

data = get_operational_data()
agent_performance = data["agent_performance"]

print("=== SIMPLE AGENT 3 DEBUG ===")
print("Raw data (first 10 agents):")
for i in range(10):
    print(f"  Agent {i+1}: {agent_performance[i]}")

print(f"\nAgent 3 specifically:")
print(f"  Index: 2")
print(f"  Value: {agent_performance[2]}")
print(f"  Type: {type(agent_performance[2])}")
print(f"  Is <= 3.8? {agent_performance[2] <= 3.8}")

# Check if there are any NaN or None values
print(f"\nData validation:")
for i, val in enumerate(agent_performance):
    if val is None or str(val) == 'nan':
        print(f"  WARNING: Agent {i+1} has invalid value: {val}")
        
print(f"\nAll agent performance values: {agent_performance}")

# Simple color assignment test
def simple_color(time):
    if time <= 3.8:
        return "GREEN"
    elif time <= 4.2:
        return "AMBER"
    else:
        return "RED"

print(f"\nAgent 3 color test:")
agent3_time = agent_performance[2]
agent3_color = simple_color(agent3_time)
print(f"  Agent 3: {agent3_time} min -> {agent3_color}")

if agent3_color != "GREEN":
    print(f"  *** PROBLEM FOUND: Agent 3 should be GREEN but got {agent3_color} ***")
else:
    print(f"  ✅ Agent 3 color logic is correct")
