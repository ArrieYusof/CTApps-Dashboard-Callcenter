import dash
from dash import dcc, html
import plotly.graph_objects as go

# Create a super simple test app
app = dash.Dash(__name__)

# Simple figure with text labels - exact same as working HTML
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=[1, 2, 3, 4],
    y=[10, 20, 15, 25],
    mode='lines+markers+text',
    text=['$10K', '$20K', '$15K', '$25K'],
    textposition='top center',
    textfont=dict(size=20, color='red', family='Arial')
))

fig.update_layout(
    title="Simple Test - Should Show Text Labels",
    plot_bgcolor='white',
    paper_bgcolor='white',
    height=400,
    margin=dict(t=100, b=50, l=50, r=50)
)

app.layout = html.Div([
    html.H1("Text Label Test"),
    html.P("You should see red text labels above each data point"),
    dcc.Graph(
        figure=fig,
        config={'displayModeBar': True}  # Show all controls for debugging
    )
])

if __name__ == '__main__':
    app.run(debug=True, port=8051)  # Different port
