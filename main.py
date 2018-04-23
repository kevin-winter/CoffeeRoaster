from time import time
import numpy as np

import dash
from dash.dependencies import Input, Output, State
from plotly.graph_objs import *

import defaults
import layout
import sensordata

starttime = 0

app = dash.Dash(__name__)
#app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.css.append_css({"external_url": "https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css"})
app.scripts.append_script({"external_url": "https://code.jquery.com/jquery-3.3.1.slim.min.js"})
app.scripts.append_script({"external_url": "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js"})
app.scripts.append_script({"external_url": "https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js"})

app.layout = layout.mainpage


def graphdata():
    t, temp, beantemp = sessiondata()
    return [{'x': t, 'y': temp,
             'name': 'Temp',
             'mode': 'lines+markers',
             'type': 'scatter'},

            {'x': t, 'y': beantemp,
             'name': 'Beantemp',
             'mode': 'lines+markers',
             'type': 'scatter'}]

def sessiondata():
    with sensordata.datalock:
        t = np.array(sensordata.data['t']) - starttime
        temp = np.array(sensordata.data['temp'])
        beantemp = np.array(sensordata.data['beantemp'])
        t = t[t <= defaults.roasttime]
    return t, temp, beantemp

@app.callback(Output('btn-start', 'children'), [Input('interval1', 'n_intervals')])
def update_button(n):
    if is_roasting():
        return "Cancel Roast"
    else:
        return "Start Roast"

@app.callback(Output('graph1', 'figure'), [Input('interval1', 'n_intervals')])
def update_graph_live(n):
    fig = Figure()
    fig['data'] = graphdata()
    fig['layout'] = {
        'title': 'Temperatures',
        "xaxis": {'range': [0, defaults.roasttime]},
        "yaxis": {'range': [0, 700]}
    }
    return fig


@app.callback(Output('lbl-roast', 'children'), [Input('btn-start', 'n_clicks')],
              [State('in-roasttime', 'value'), State('in-roasttemp', 'value')])
def on_click(n, time, temp):
    if not n:
        return ""

    if is_roasting():
        return stop_roast()
    else:
        return start_roast(time, temp)

def start_roast(duration, temp):
    if not defaults.min_roasttime <= duration <= defaults.max_roasttime:
        return "Roast time must be between {} and {} seconds".format(defaults.min_roasttime, defaults.max_roasttime)

    if not defaults.min_roasttemp <= temp <= defaults.max_roasttemp:
        return "Roast temperature must be between {} and {} degrees C".format(defaults.min_roasttemp, defaults.max_roasttemp)

    turn_on_heating(temp)

    sensordata.data.clear()

    global starttime
    starttime = time()
    defaults.roasttime = duration
    return "Roasting for {} seconds".format(duration)

def stop_roast():
    #get_data().clear()
    #starttime = time()+roasttime+1
    defaults.roasttime = time() - starttime
    return "Roasting cancelled"

def turn_on_heating(temp):
    return


def is_roasting():
    return starttime < time() < starttime + defaults.roasttime


if __name__ == '__main__':
    app.run_server(debug=False)
