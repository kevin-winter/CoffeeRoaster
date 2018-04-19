from time import time, sleep
import numpy as np

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from plotly.graph_objs import *

import sensordata

roasttime = 4*60
starttime = 0

refresh_rate = 4 #Hz

def graphdata():
    t, temp = sessiondata()
    return {'x': t,
            'y': temp,
            'name': 'Temp',
            'mode': 'lines+markers',
            'type': 'scatter'}

def sessiondata():
    with sensordata.datalock:
        t = np.array(sensordata.data['t']) - starttime
        temp = np.array(sensordata.data['temp'])
        t = t[t <= roasttime]
    return t, temp

app = dash.Dash(__name__)
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.layout = html.Div(
    html.Div([
        html.H2('Roaster Coaster'),
        dcc.Graph(id='graph1'),
        html.Div(dcc.Input(id='in-roasttime', value=roasttime, type='number')),
        html.Button("Roast", id="btn-start"),
        html.Div(id='lbl-roast', children=''),
        dcc.Interval(id='interval1', interval=1000.0/refresh_rate, n_intervals=0)
    ])
)


@app.callback(Output('btn-start', 'children'), [Input('interval1', 'n_intervals')])
def update_button(n):
    if is_roasting():
        return "Cancel Roast"
    else:
        return "Start Roast"

@app.callback(Output('graph1', 'figure'), [Input('interval1', 'n_intervals')])
def update_graph_live(n):
    fig = Figure()
    fig['data'] = [graphdata()]
    fig['layout'] = {"xaxis": {'range': [0, roasttime]},
                     "yaxis": {'range': [0, 700]}}
    return fig

@app.callback(Output('lbl-roast', 'children'), [Input('btn-start', 'n_clicks')], [State('in-roasttime', 'value')])
def on_click(n, value):
    if is_roasting():
        return stop_roast()
    else:
        return start_roast(value)


def start_roast(t):
    global starttime, roasttime, test
    sensordata.data.clear()
    starttime = time()
    roasttime = t
    return "Roasting for {} seconds".format(t)

def stop_roast():
    global starttime, roasttime
    #get_data().clear()
    #starttime = time()+roasttime+1
    roasttime = time() - starttime
    return "Roasting cancelled"

def is_roasting():
    return starttime < time() < starttime + roasttime


if __name__ == '__main__':
    app.run_server(debug=False)
