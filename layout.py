import dash_core_components as dcc
import dash_html_components as html

import defaults

mainpage = html.Div([
    html.Div(html.H2('Roaster Coaster'), className="jumbotron"),
    html.Div([
        dcc.Graph(id='graph1'),
        dcc.Interval(id='interval1', interval=1000.0/defaults.refresh_rate, n_intervals=0),
    ]),
    html.Div(html.Form([

        html.Div([
            html.Label("Roast Profile", htmlFor="sl-profile"),
            dcc.Slider(id='sl-profile', value=defaults.profile,
                       max=defaults.nr_profiles-1, min=0,
                       marks={k: v[0] for k, v in defaults.profiles.items()},
                       className="custom-range"),
        ], className="form-group", style={"height":100}),

        html.Div([
            html.Label("Roast Temperature (°C)", htmlFor="in-roasttemp"),
            dcc.Input(id='in-roasttemp', value=defaults.roasttemp, type='number',
                      max=defaults.max_roasttemp, min=defaults.min_roasttemp, className="form-control", readonly="readonly"),
        ], className="form-group"),

        html.Div([
            html.Label("Roast Time (s)", htmlFor="in-roasttime"),
            dcc.Input(id='in-roasttime', value=defaults.roasttime, type='number',
                      max=defaults.max_roasttime, min=defaults.min_roasttime, className="form-control")
        ], className="form-group"),

        dcc.Checklist(id="cb-preheat", options=[{"label": "Preheat", "value": "PH"}], values=[defaults.preheat]),

        html.Button("Roast", id="btn-start", type="button", className="btn btn-primary"),
        html.Small(id='lbl-roast', children='', className="form-text text-muted")
    ], className ="was-validated")),
], className="container")