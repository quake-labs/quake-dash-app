import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import requests
import pandas as pd
import numpy as np
import datetime
from app import app

title = html.Div(html.H1('Search Earthquakes'), style={'text-align': 'center',
                                                       'margin-top': '40px'})


source_col = dbc.Col([
    dcc.Markdown('Choose a source'),
    html.Div([
        dcc.Dropdown(
            id='source',
            options=[
                {'label': 'USGS', 'value': 'USGS'},
                {'label': 'EMSC', 'value': 'EMSC'},
            ],
            value='USGS'
        ),  # ends dropdown
    ])  # ends div
])  # ends col1

type_col = dbc.Col([
    dcc.Markdown('Search By:'),
    html.Div(
        dcc.Dropdown(
            id='searchtype',
            options=[
                {'label': 'Zipcode', 'value': 'zip'},
                {'label': 'Time', 'value': 'time'}
            ],
            value='zip'
        )
    )
])  # ends col2


@app.callback(
    dash.dependencies.Output('searchArea', 'children'),
    [dash.dependencies.Input('searchtype', 'value')])
def search_type(search):
    if search == 'time':
        search_fields = dbc.Col([
            html.Div([
                dcc.Dropdown(
                     id='timeFrame',
                     options=[
                         {'label': 'Last Quake', 'value': 'Quake'},
                         {'label': 'Last Hour', 'value': '/hour'},
                         {'label': 'Last Day', 'value': '/day'},
                         {'label': 'Last Week', 'value': '/week'},
                         {'label': 'Last Month', 'value': '/month'}
                     ],
                     value='Quake'
                     ),
                html.Div(id='menuItems')
            ]),
            html.Div([
                dcc.Markdown("\n\n\n\n"),
                dcc.Slider(
                     id='magnitude',
                     min=0,
                     max=10,
                     step=.5,
                     value=5.5
                     ),
                dcc.Markdown(id='sliderOutput')
            ])
        ])
    else:
        search_fields = [
            dbc.Col([dcc.Markdown('Enter Zipcode:'),

                     dcc.Input(
                id='zip',
                type='number',
                minLength=5,
                maxLength=5,
                value=10001
            )]),
            dbc.Col([
                dcc.Markdown('Select Distance:'),
                dcc.Slider(
                    id='distance',
                    min=0,
                    max=100,
                    step=10,
                    value=20
                )]),
        ]

    return search_fields


layout = dbc.Col([
    title,
    dbc.Row([type_col, source_col]),
    html.Div(style={'margin': '20px'}),
    dbc.Row(id='searchArea', style={'width': '100%'}),
    html.Div(id='searchResults')
])
