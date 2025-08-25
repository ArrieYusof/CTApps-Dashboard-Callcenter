// Client-side callback to force chart refresh when sidebar toggles
window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        refresh_charts_on_sidebar_toggle: function(n_clicks) {
            // Force a refresh of all Plotly charts after sidebar animation completes
            setTimeout(function() {
                var charts = document.querySelectorAll('.js-plotly-plot');
                charts.forEach(function(chart) {
                    if (window.Plotly && chart._fullLayout) {
                        window.Plotly.Plots.resize(chart);
                        // Force a redraw to ensure colors are correct
                        window.Plotly.redraw(chart);
                    }
                });
            }, 350); // Wait for transition to complete (300ms + buffer)
            
            return window.dash_clientside.no_update;
        }
    }
});
