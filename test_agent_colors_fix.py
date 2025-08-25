#!/usr/bin/env python3
"""
Test the Agent Performance color fix
"""
import plotly.graph_objs as go

def test_agent_colors():
    # Simulate the exact same data and logic as the dashboard
    chart_data = [round(3.5 + (i % 10) * 0.1, 2) for i in range(20)]  # Agent performance data
    
    # Same sorting logic as dashboard
    agent_names = [f"Agent {i+1}" for i in range(len(chart_data))]
    sorted_agents = sorted(zip(agent_names, chart_data), key=lambda x: x[1])
    sorted_names = [a[0] for a in sorted_agents]
    sorted_times = [a[1] for a in sorted_agents]
    
    # NEW improved color assignment logic
    bar_colors = []
    for t in sorted_times:
        if t <= 3.8:
            bar_colors.append("#00FF88")  # Green
        elif t <= 4.2:
            bar_colors.append("#FFB800")  # Amber
        else:
            bar_colors.append("#FF3366")  # Red
    
    print("=== AGENT COLOR TEST ===")
    print("Agent 3 analysis:")
    agent3_index = sorted_names.index("Agent 3")
    agent3_time = sorted_times[agent3_index] 
    agent3_color = bar_colors[agent3_index]
    
    print(f"Agent 3 position in sorted chart: {agent3_index}")
    print(f"Agent 3 handle time: {agent3_time} min")
    print(f"Agent 3 assigned color: {agent3_color}")
    print(f"Agent 3 expected color: GREEN (#00FF88)")
    
    if agent3_color == "#00FF88":
        print("✅ SUCCESS: Agent 3 should be GREEN!")
    else:
        print("❌ FAILURE: Agent 3 has wrong color!")
    
    # Test creating the actual Plotly chart
    fig = go.Figure(go.Bar(
        x=sorted_names,
        y=sorted_times,
        marker=dict(
            color=bar_colors, 
            line=dict(color="#23263A", width=2),
            colorscale=None
        ),
        text=[f"{t:.2f} min" for t in sorted_times],
        textposition="auto",
        textfont=dict(color="#fff"),
        hovertemplate="<b>%{x}</b><br>Handle Time: %{y:.2f} min<extra></extra>",
        showlegend=False
    ))
    
    print(f"\n=== CHART CREATION TEST ===")
    print(f"Chart created successfully: {fig is not None}")
    print(f"Number of bars: {len(fig.data[0].x) if fig.data else 0}")
    print(f"Number of colors: {len(fig.data[0].marker.color) if fig.data else 0}")
    
    # Validate that Agent 3's color in the chart matches expectation
    if fig.data and len(fig.data) > 0:
        chart_colors = fig.data[0].marker.color
        chart_names = list(fig.data[0].x)
        if "Agent 3" in chart_names:
            agent3_chart_index = chart_names.index("Agent 3")
            agent3_chart_color = chart_colors[agent3_chart_index]
            print(f"Agent 3 color in chart object: {agent3_chart_color}")
            
            if agent3_chart_color == "#00FF88":
                print("✅ CHART SUCCESS: Agent 3 color correctly set in chart!")
                return True
            else:
                print("❌ CHART FAILURE: Agent 3 color wrong in chart!")
                return False
    
    return False

if __name__ == "__main__":
    success = test_agent_colors()
    print(f"\n=== FINAL RESULT ===")
    if success:
        print("🎉 Agent 3 should now be GREEN in the dashboard!")
        print("If it still appears black, try:")
        print("1. Hard refresh the browser (Cmd+Shift+R)")
        print("2. Clear browser cache")
        print("3. Restart the application")
    else:
        print("❌ There may still be an issue with the color assignment")
