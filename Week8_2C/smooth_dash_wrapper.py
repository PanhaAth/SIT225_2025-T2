# smooth_dash_wrapper.py
import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from collections import deque
from datetime import datetime, timezone
from typing import Callable, List, Dict, Any

def create_smooth_dash_app(
    data_callback: Callable[[], Dict[str, Any]],
    traces_config: List[Dict[str, Any]],
    update_interval: int = 100,
    window_size: int = 200,
    title: str = "Smooth Live Data Dashboard"
) -> dash.Dash:
    """
    Creates a Dash application with smooth, real-time graph updates.
    
    Parameters:
    -----------
    data_callback : Callable[[], Dict[str, Any]]
        A function that returns a dictionary with the latest data values.
        Keys should match the 'name' fields in traces_config.
    traces_config : List[Dict[str, Any]]
        Configuration for each trace. Each dictionary should contain:
        - 'name': The name of the trace (must match data_callback keys)
        - 'color': The color for the trace
        - 'title': The subtitle for the trace
    update_interval : int, optional
        How often to update the graph (in milliseconds). Default is 100ms.
    window_size : int, optional
        Number of data points to keep in the buffer. Default is 200.
    title : str, optional
        Title of the dashboard. Default is "Smooth Live Data Dashboard".
    
    Returns:
    --------
    dash.Dash
        A configured Dash application with smooth updating.
    """
    
    # Initialize the Dash app
    app = dash.Dash(__name__)
    app.title = title
    
    # Create the figure with subplots
    fig = make_subplots(
    rows=len(traces_config),
    cols=1,
    shared_xaxes=True,   # ← fix
    subplot_titles=[trace['title'] for trace in traces_config]
)
    
    # Add initial empty traces to the figure
    for i, trace in enumerate(traces_config):
        fig.add_trace(
            go.Scatter(
                x=[],
                y=[],
                name=trace['name'],
                line=dict(color=trace['color'])
            ), 
            row=i+1, 
            col=1
        )
    
    # Update layout
    fig.update_layout(
        height=200 * len(traces_config), 
        showlegend=False,
        template="plotly_dark",
        margin=dict(l=50, r=50, t=80, b=50)
    )
    fig.update_xaxes(title_text="Time", row=len(traces_config), col=1)
    
    # Define the app layout
    app.layout = html.Div([
        html.H1(
            title, 
            style={
                'textAlign': 'center', 
                'color': 'white', 
                'backgroundColor': '#2c3e50', 
                'padding': '15px',
                'marginBottom': '20px'
            }
        ),
        dcc.Graph(id='live-graph', figure=fig),
        dcc.Interval(
            id='graph-update-interval',
            interval=update_interval,
            n_intervals=0
        )
    ])
    
    # Define the callback for smooth updates
    @app.callback(
        Output('live-graph', 'extendData'),
        Input('graph-update-interval', 'n_intervals'),
        prevent_initial_call=True
    )
    def update_graph(n):
        new_data = data_callback()
        current_time = datetime.now(timezone.utc).astimezone()

        if not new_data:
            return dash.no_update

        return (
            {
                "x": [[current_time], [current_time], [current_time]],
                "y": [[new_data.get("x")], [new_data.get("y")], [new_data.get("z")]]
            },
            [0, 1, 2],      # update all three traces
            window_size     # cap number of visible points
        )

    
    return app