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

location_search = SearchEngine(simple_zipcode=True)

SOURCES = ['USGS', 'EMSC']

column1 = dbc.Col(
    [
        dcc.Markdown(
            """

            ## Recent Earthquakes
            The map at the right shows earthquakes for the specified area below.
            Larger dots are larger earthquakes.

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
                max=30,
                step=.5,
                value=5.5
            ),
            dcc.Markdown(id='distanceOut')
        ])
    ],
    md=2,
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
    if source != 'BOTH':
        print('running with one source')
        return single_source(zip, dist, source)
    else:
        print('running with two sources')
        return dual_source(zip, dist)


def single_source(zip, dist, source):
    location = location_search.by_zipcode(str(zip))
    lat = location.to_dict()['lat']
    lon = location.to_dict()['lng']
    api_url = f'http://quake-ds-staging.herokuapp.com/history/{source}/{lat}, {lon}, {dist}'
    data = requests.get(api_url)
    if data.json()['num_quakes'] != 0:
        df = pd.DataFrame(data.json()['message'])
        df['color'] = 'blue' if source == 'USGS' else 'yellow'
        data, layout = loaded_fig(df)
        title = f'Quakes within {dist} KM of {zip}'
    else:
        data, layout = empty_fig()
        title = f'No Quakes have occured within {dist} of {zip}'

    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(mapbox_style='stamen-terrain', height=700, title=title)
    return dcc.Graph(figure=fig)


def loaded_fig(df):
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

            text=[f"""place: {x['place']}<br>UTC time: {datetime.datetime.fromtimestamp(x['time']/1000.0)}<br>mag: {x['mag']}"""
                  for _, x in df.iterrows()],
            hoverinfo='text'
        )
    ]

    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=0,
                lon=0
            ),
            pitch=0,
            zoom=.5
        ),
    )
    return data, layout


def empty_fig():
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
                lat=0,
                lon=0
            ),
            pitch=0,
            zoom=.5
        ),
    )
    return data, layout


column2 = dbc.Col([html.Div(
    id='themapgoeshere')
])

layout = dbc.Row([column1, column2], style={'margin-top': 100, 'height': 1000})
