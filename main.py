from time import time
import numpy as np

import dash
from dash.dependencies import Input, Output, State
from plotly.graph_objs import *

import defaults
from defaults import min_roasttemp, max_roasttemp, min_roasttime, max_roasttime, HEATING, FAN, BEAN_ENTRANCE, BEAN_EXIT, TESTLED
import layout
import sensordata

test = 0
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

    trigger_test_led()
    if is_roasting():
        return stop_roast()
    else:
        return start_roast(time, temp)

def start_roast(duration, temp):
    if not min_roasttime <= duration <= max_roasttime:
        return "Roast time must be between {} and {} seconds".format(min_roasttime, max_roasttime)

    if not min_roasttemp <= temp <= max_roasttemp:
        return "Roast temperature must be between {} and {} degrees C".format(min_roasttemp, max_roasttemp)

    set_heating(temp)
    set_fanspeed(100)

    sensordata.data.clear()

    global starttime
    starttime = time()
    defaults.roasttime = duration
    return "Roasting for {} seconds".format(duration)

def stop_roast():
    defaults.roasttime = time() - starttime
    return "Roasting cancelled"

def set_heating(temp):
    sensordata.tasks.put((HEATING, temp))

def set_fanspeed(speed):
    sensordata.tasks.put((FAN, speed))

def trigger_bean_entrance():
    sensordata.tasks.put((BEAN_ENTRANCE,))

def trigger_bean_exit():
    sensordata.tasks.put((BEAN_EXIT,))

def trigger_test_led():
    global test
    test ^= 1
    sensordata.tasks.put((TESTLED, test))


def is_roasting():
    return starttime < time() < starttime + defaults.roasttime


if __name__ == '__main__':
    app.run_server(debug=False)
