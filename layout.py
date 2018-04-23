import dash_core_components as dcc
import dash_html_components as html

import defaults

mainpage = html.Div([
    html.Div(html.H2('Roaster Coaster'), className="jumbotron"),
    dcc.Graph(id='graph1'),
    html.Form([
        html.Div([
            html.Label("Roast Temperature (°C)", htmlFor="in-roasttemp"),
            dcc.Input(id='in-roasttemp', value=defaults.roasttemp, type='number',
                      max=defaults.max_roasttemp, min=defaults.min_roasttemp, className="form-control"),
        ], className="form-group"),
        html.Div([
            html.Label("Roast Time (s)", htmlFor="in-roasttime"),
            dcc.Input(id='in-roasttime', value=defaults.roasttime, type='number',
                      max=defaults.max_roasttime, min=defaults.min_roasttime, className="form-control")
        ], className="form-group"),
        html.Button("Roast", id="btn-start", type="button", className="btn btn-primary"),
        html.Small(id='lbl-roast', children='', className="form-text text-muted"),
        dcc.Interval(id='interval1', interval=1000.0/defaults.refresh_rate, n_intervals=0)
    ], className ="was-validated"),
], className="container")