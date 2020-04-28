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
from . import BASE_URL
from .comments import *

from dateutil import tz
import sys

SOURCES = ['USGS', 'EMSC']

column1 = dbc.Col(
    html.Div([
        dcc.Markdown(
            """


            This shows earthquake history for US zip codes.

            The map at the right shows earthquakes for the specified area below.
            Larger dots are larger earthquakes. Click on an earthquake for additional details.

            Enter your zip code below and use the slider to set the range you would
            like history for.


            Zip Code:
            """
        ),
        html.Div([
            dcc.Dropdown(
                id='source',
                options=[
                    {'label': 'USGS', 'value': 'USGS'},
                    {'label': 'EMSC', 'value': 'EMSC'},
                    {'label': 'BOTH', 'value': 'BOTH'}
                ],
                value='USGS'
            ),

            dcc.Input(
                id='zip',
                type='number',
                minLength=5,
                maxLength=5,
                value=10001
            )]),

        html.Div([
            dcc.Markdown("\n\n\n\n"),
            dcc.Slider(
                id='distance',
                min=0,
                max=100,
                step=10,
                value=20
            ),
            dcc.Markdown(id='distanceOut')
        ])
    ], style={'margin-top': 20}),
    md=3,
)

# fig = go.Figure()


@app.callback(
    dash.dependencies.Output('distanceOut', 'children'),
    [dash.dependencies.Input('distance', 'value')])
def display_min_mag(mag_num):
    return f"distance: {mag_num} KM"


@app.callback(
    dash.dependencies.Output('themapgoeshere', 'children'),
    [dash.dependencies.Input('distance', 'value'),
     dash.dependencies.Input('zip', 'value'),
     dash.dependencies.Input('source', 'value')])
def update_output(dist, zip, source):
    # check for valid zip code
    if len(str(zip)) == 5:
        # check out sources
        if source != 'BOTH':
            print('running zip with one source')
            return single_source(zip, dist, source)
        else:
            print('running zip with two sources')
            return dual_source(zip, dist)
    else:
        # invalid zip code option
        return invalid_zip(zip)


# This creates an answer from one source
def single_source(zip, dist, source):
    location_search = SearchEngine(simple_zipcode=True)
    location = location_search.by_zipcode(str(zip))
    lat = location.to_dict()['lat']
    lon = location.to_dict()['lng']
    if lat == None:
        return invalid_zip(zip)

    api_url = BASE_URL + f'history/{source}/{lat},{lon},{dist}'
    quakes = requests.get(api_url)
    if quakes.json()['num_quakes'] != 0:
        df = pd.DataFrame(quakes.json()['message'])
        df['color'] = 'blue' if source == 'USGS' else 'yellow'
        data, layout = loaded_fig(df, lat, lon)
        title = f'Quakes within {dist} KM of {zip} from {source}'
    else:
        data, layout = empty_fig(lat, lon)
        title = f'No Quakes have occured within {dist} KM of {zip} in {source}'

    return build_fig(data, layout, title, quakes.json()['boundingA'], quakes.json()['boundingB'])


def dual_source(zip, dist):
    # get the lat and lon from zip
    location_search = SearchEngine(simple_zipcode=True)
    location = location_search.by_zipcode(str(zip))
    lat = location.to_dict()['lat']
    lon = location.to_dict()['lng']
    if lat == None:
        return invalid_zip(zip)

    df = pd.DataFrame()
    # load DF with the two sources
    for source in SOURCES:
        api_url = BASE_URL + f'history/{source}/{lat},{lon},{dist}'
        quakes = requests.get(api_url)
        if quakes.json()['num_quakes'] != 0:
            df = df.append(quakes.json()['message'])

    # check that there are any quakes
    if df.shape[0] > 0:
        title = f'Quakes within {dist} KM of {zip} from both USGS and EMSC'
        df['color'] = df['Oceanic'].apply(lambda x: 'yellow' if x != x else 'blue')
        data, layout = loaded_fig(df, lat, lon)
    else:
        title = f'No Quakes have occured within {dist} KM of {zip} in either USGS or EMSC'
        data, layout = empty_fig(lat, lon)

    return build_fig(data, layout, title,  quakes.json()['boundingA'], quakes.json()['boundingB'])


def invalid_zip(zip):
    title = f'{zip} is not a valid US zip code'
    data, layout = empty_fig(39.8283, -98.5795)
    return build_fig(data, layout, title)


def loaded_fig(df, centLat, centLon):
    df['lat'] = df['lat'].apply(lambda x: str(x))
    df['lon'] = df['lon'].apply(lambda x: str(x))
    data = [
        go.Scattermapbox(
            lat=df['lat'],
            lon=df['lon'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=df['mag'] + 9,
                color=df['color'],
            ),

            text=[f"""{x['place']}<br>{datetime.datetime.fromtimestamp(x['time']/1000.0)}<br>{x['mag']}<br>{x['lat']}<br>{x['lon']}<br>{x['color']}<br>{x['id']}"""
                  for _, x in df.iterrows()],
            hoverinfo='none'
        )
    ]

    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=centLat,
                lon=centLon
            ),
            pitch=0,
            zoom=8
        ),
        clickmode='event+select'
    )
    return data, layout


def empty_fig(centLat=None, centLon=None):
    data = [
        go.Scattermapbox(
            lat=[0],
            lon=[0],
            mode='text',
            textposition='middle center'
        )
    ]

    layout = go.Layout(
        autosize=True,
        mapbox=go.layout.Mapbox(
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=centLat if centLat != None else 0,
                lon=centLon if centLon != None else 0
            ),
            pitch=0,
            zoom=3 if centLat == 39.8283 else 8 if centLat != None else 0.5
        ),
    )
    return data, layout


def build_fig(data, layout, title, locA=None, locB=None):
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(mapbox_style='stamen-terrain', height=700, title=title, showlegend=False)
    fig.update_layout(margin={'l': 0, 'r': 0, 'b': 0, 't': 50})
    if locA != None:
        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lon=[locA[1], locB[1], locB[1], locA[1], locA[1]],
            lat=[locA[0], locA[0], locB[0], locB[0], locA[0]],
            marker={'size': 0,
                    'color': 'red'})
        )

    return dcc.Graph(figure=fig, id='mapZone')


column2 = dbc.Col([html.Div(build_fig(*empty_fig(39.8283, -98.5795),''),
                            id='themapgoeshere')
                   ])


layout = html.Div([
    html.Div(dbc.Row(dbc.Col(html.H1('Local Earthquake History'))), style={'text-align': 'center',
                                                                           'margin-top': 40,
                                                                           'margin-bottom': 0}),
    dbc.Row([column1, column2]),
    dbc.Row([details, comments_col])
])
