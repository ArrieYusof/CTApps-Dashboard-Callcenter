#!/usr/bin/env python3
"""
Test SIMPLE chart with plotly directly - no Dash interference
"""
import plotly.graph_objects as go

def test_simple_chart():
    # Same data as the app
    agent_performance = [round(3.5 + (i % 10) * 0.1, 2) for i in range(20)]
    
    # Same processing as the app
    agent_names = [f"Agent {i+1}" for i in range(len(agent_performance))]
    sorted_agents = sorted(zip(agent_names, agent_performance), key=lambda x: x[1])
    sorted_names = [a[0] for a in sorted_agents]
    sorted_times = [a[1] for a in sorted_agents]
    
    # SIMPLE color assignment
    colors = []
    for time in sorted_times:
        if time <= 3.8:
            colors.append("#00FF88")  # Green
        elif time <= 4.2:
            colors.append("#FFB800")  # Amber  
        else:
            colors.append("#FF3366")  # Red
    
    print("=== SIMPLE CHART TEST ===")
    print("Agent 3 details:")
    agent3_index = sorted_names.index("Agent 3")
    print(f"  Position: {agent3_index}")
    print(f"  Time: {sorted_times[agent3_index]}")
    print(f"  Color: {colors[agent3_index]}")
    
    # Create SIMPLE chart
    fig = go.Figure(go.Bar(
        x=sorted_names,
        y=sorted_times,
        marker_color=colors,  # This is the SIMPLEST way
        text=[f"{t:.1f}" for t in sorted_times],
        textposition="outside"
    ))
    
    print(f"\n✅ Chart created successfully")
    print(f"✅ Agent 3 should be: {colors[agent3_index]}")
    
    # Save as HTML to test
    fig.write_html("/Users/obie/Dev/AI/CTApps/CallCenter/test_simple_chart.html")
    print(f"✅ Chart saved to test_simple_chart.html")
    print(f"\nOpen the HTML file in browser to see if Agent 3 is green!")

if __name__ == "__main__":
    test_simple_chart()
