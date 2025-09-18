import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from datetime import datetime, timezone

# Import our modules
from arduino import SmoothArduinoCloudClient
from smooth_dash_wrapper import create_smooth_dash_app

# Initialize the cloud client
DEVICE_ID = "f9be03ce-1809-4bf5-93c1-b3a4cc67a3e4"
SECRET_KEY = "7L4y@Ol4!jggkGIFrk2pKONxL"
WINDOW_SIZE = 20

cloud_client = SmoothArduinoCloudClient(DEVICE_ID, SECRET_KEY, WINDOW_SIZE)
cloud_client.start_client()

# Define trace configuration for accelerometer data
# Define trace configuration for accelerometer data
traces_config = [
    {'name': 'x', 'color': '#FF4B4B', 'title': 'X-Acceleration'},
    {'name': 'y', 'color': '#4BFF4B', 'title': 'Y-Acceleration'},
    {'name': 'z', 'color': '#4B4BFF', 'title': 'Z-Acceleration'}
]

# Create the data callback function
def accelerometer_callback():
    return cloud_client.get_latest()

# Create the Dash app using our wrapper
app = create_smooth_dash_app(
    data_callback=accelerometer_callback,
    traces_config=traces_config,   # <-- THIS must be present
    update_interval=1000,
    window_size=WINDOW_SIZE,
    title="Smooth Accelerometer Dashboard"
)

# Add additional functionality for saving data windows
@app.callback(
    Output('save-status', 'children'),
    Input('save-button', 'n_clicks'),
    prevent_initial_call=True
)
def save_data(n_clicks):
    if n_clicks:
        buffers = cloud_client.get_buffers()
        # Here you would add code to save the data to a file
        # For example: save to CSV, database, etc.
        return "Data saved successfully!"
    return ""

# Add a save button to the layout
app.layout.children.append(
    html.Div([
        html.Button('Save Current Data', id='save-button', n_clicks=0,
                   style={'margin': '20px', 'padding': '10px 20px'}),
        html.Div(id='save-status', style={'margin': '10px'})
    ], style={'textAlign': 'center'})
)

if __name__ == '__main__':
    print("Starting Smooth Accelerometer Dashboard...")
    print("Open http://127.0.0.1:8051 in your browser")
    app.run(debug=True, host='127.0.0.1', port=8051)