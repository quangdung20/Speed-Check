from flask import Flask, request, jsonify
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Output, Input
import threading

# Create Flask app
server = Flask(__name__)

# Create Dash app
app = dash.Dash(__name__, server=server)
app.layout = html.Div([
    html.Div([
        dcc.Graph(id='live-update-graph-left')
    ], style={'width': '48%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='live-update-graph-right')
    ], style={'width': '48%', 'display': 'inline-block'}),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    )
])

data = {
    'time': [],
    'left1': [],
    'left2': [],
    'right1': [],
    'right2': []
}

@server.route('/data', methods=['POST'])
def receive_data():
    global data
    content = request.json
    data['time'].append(content['time'])
    data['left1'].append(content['left1'])
    data['left2'].append(content['left2'])
    data['right1'].append(content['right1'])
    data['right2'].append(content['right2'])
    return jsonify(success=True)

@app.callback(Output('live-update-graph-left', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_left(n):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['time'], y=data['left1'], mode='lines', name='Left 1'))
    fig.add_trace(go.Scatter(x=data['time'], y=data['left2'], mode='lines', name='Left 2'))
    fig.update_layout(title='Left Graph', xaxis_title='Time', yaxis_title='Value')
    return fig

@app.callback(Output('live-update-graph-right', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_right(n):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['time'], y=data['right1'], mode='lines', name='Right 1'))
    fig.add_trace(go.Scatter(x=data['time'], y=data['right2'], mode='lines', name='Right 2'))
    fig.update_layout(title='Right Graph', xaxis_title='Time', yaxis_title='Value')
    return fig

def run_dash():
    app.run_server(debug=True, use_reloader=False)

if __name__ == '__main__':
    dash_thread = threading.Thread(target=run_dash)
    dash_thread.start()
    server.run(port=8050, debug=True, use_reloader=False)
