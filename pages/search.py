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
from uszipcode import SearchEngine
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML as rawHtml
from . import BASE_URL

TITLE = html.Div(html.H1('Search Earthquakes'), style={'text-align': 'center',
                                                       'margin-top': '40px'})


source_col = dbc.Col([
    dcc.Markdown('Choose a source'),
    html.Div([
        dcc.Dropdown(
            id='Searchsource',
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
search_fields = [
    dbc.Col([dcc.Markdown('Enter Zipcode:'),

             dcc.Input(
        id='frame',
        type='number',
        minLength=5,
        maxLength=5,
        value=10001
    )]),
    dbc.Col([
        dcc.Markdown('Select Distance:'),
        dcc.Slider(
            id='amount',
            min=0,
            max=100,
            step=10,
            value=20
        ),
        html.Div(id='amountCol')]),
]

# sets the two search parameters based on selection


@app.callback(
    dash.dependencies.Output('searchArea', 'children'),
    [dash.dependencies.Input('searchtype', 'value')])
def search_type(search):
    if search == 'time':
        search_fields = [
            dbc.Col([dcc.Markdown('Select Timeframe:'),
                     dcc.Dropdown(
                    id='frame',
                    options=[
                        {'label': 'Last Quake', 'value': 'Quake'},
                        {'label': 'Last Hour', 'value': '/hour'},
                        {'label': 'Last Day', 'value': '/day'},
                        {'label': 'Last Week', 'value': '/week'},
                        {'label': 'Last Month', 'value': '/month'}
                    ],
                    value='Quake'
                    )]),
            dbc.Col([dcc.Markdown('Minimum Magnitude:'),
                     dcc.Slider(
                    id='amount',
                    min=0,
                    max=10,
                    step=.5,
                    value=5.5
                    ),
                html.Div(id='amountCol')]),

        ]
    else:
        search_fields = [
            dbc.Col([dcc.Markdown('Enter Zipcode:'),

                     dcc.Input(
                id='frame',
                type='number',
                minLength=5,
                maxLength=5,
                value=10001
            )]),
            dbc.Col([
                dcc.Markdown('Select Distance:'),
                dcc.Slider(
                    id='amount',
                    min=0,
                    max=100,
                    step=10,
                    value=20
                ),
                html.Div(id='amountCol')]),
        ]

    return search_fields


@app.callback(
    dash.dependencies.Output('amountCol', 'children'),
    [dash.dependencies.Input('amount', 'value'),
     dash.dependencies.Input('searchtype', 'value')])
def place_ammount(amount, search):
    if search == 'Time':
        return dcc.Markdown(f'Minimum Magnitude: {amount}')
    else:
        return dcc.Markdown(f'Maximum Distance: {amount}')


@app.callback(
    dash.dependencies.Output('searchResults', 'children'),
    [dash.dependencies.Input('searchtype', 'value'),
     dash.dependencies.Input('frame', 'value'),
     dash.dependencies.Input('amount', 'value'),
     dash.dependencies.Input('Searchsource', 'value')])
def search_results(search, frame, amount, source):
    '''
    Search is the type os search
    Frame is either zip code or time Frame
    Amount is either distance or min mag
    source is USGS or EMSC
    '''
    if search == 'time':
        try:
            float(frame)
        except:
            return search_time(frame, amount, source)
    else:
        try:
            float(frame)
            return search_zip(frame, amount, source)
        except:
            return None


def search_time(frame, amount, source):
    if frame == 'Quake':
        api_url = BASE_URL + f'last{frame}/{source}/{float(amount)}'
    else:
        api_url = BASE_URL + f'last/{source}/{frame}/{float(amount)}'
    print(api_url)
    data = requests.get(api_url)
    if data.json()['num_quakes'] != 0:
        df = pd.DataFrame(data.json()['message']) if frame != 'Quake' else \
            pd.DataFrame(data.json()['message'], index=[0])
        if frame == 'Quake':
            title = f'Last Quake over {amount} in {source}'
        else:
            title = f"Quakes over {amount} in the last {frame.strip('last/')} in {source}"

        return display_table(df, title)

    else:
        if frame == 'Quake':
            display_text = f'No Quakes over {amount} to display in {source}'
        else:
            display_text = f"No Quakes over {amount} in the last {frame.strip('last/')} to display in {source}"

        return dcc.Markdown(display_text)


def search_zip(zip, dist, source):
    location_search = SearchEngine(simple_zipcode=True)
    location = location_search.by_zipcode(str(zip))
    lat = location.to_dict()['lat']
    lon = location.to_dict()['lng']
    if lat == None:
        return dcc.Markdown(f'{zip} is not a valid US zip code')

    api_url = BASE_URL + f'history/{source}/{lat},{lon},{dist}'
    quakes = requests.get(api_url)
    if quakes.json()['num_quakes'] != 0:
        df = pd.DataFrame(quakes.json()['message'])
        title = f'Quakes within {dist} KM of {zip} from {source}'
        return display_table(df, title)
    else:
        return dcc.Markdown(f'No Quakes have occured within {dist} KM of {zip} in {source}')


def display_table(df, title):
    html = '<table cellpadding=20><tr>'
    df = df[['id', 'time', 'place', 'lat', 'lon', 'mag']]
    col_names = df.columns
    for col in col_names:
        html = html + f'<td>{col.upper()}</td>'
    html += '</tr>'
    for row in df.iterrows():
        print(row[1]['id'])
        html += f"<tr class='hoverable'><td>{row[1]['id']}</td><td>{row[1]['time']}</td><td>{row[1]['place']}</td><td>{row[1]['lat']}</td><td>{row[1]['lon']}</td><td>{row[1]['mag']}</td></tr>"

    return rawHtml(html)


hightlight_on_hover = '''<style>
.hoverable:hover {
          background-color: #ffff99;
        }
</style>
'''

layout = dbc.Col([
    TITLE,
    dbc.Row([type_col, source_col]),
    dbc.Row(search_fields, id='searchArea', style={'width': '100%'}),
    dbc.Row(id='searchResults'),
    rawHtml(hightlight_on_hover)
])
