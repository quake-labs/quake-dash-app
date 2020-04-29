import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from app import app
import sys
from . import *
import requests
import pandas as pd
import numpy as np
import datetime
from uszipcode import SearchEngine
from dateutil import tz
from timezonefinder import TimezoneFinder


@app.callback(
    dash.dependencies.Output('Details', 'children'),
    [dash.dependencies.Input('mapZone', 'clickData')])
def show_details(clickData):
    try:
        text = clickData['points'][0]['text'].split('<br>')
        time = text[1]
        local_time, your_time = get_local_time(time, text[3], text[4])
        display = [html.H4('Details:'),
                   dcc.Markdown(f'''
            **Place:** {text[0]}

            UTC time: {text[1]}

            Local time: {local_time}

            Your time: {your_time}

            Magnitude: {text[2]}

            Latitude: {text[3]}

            Longitude: {text[4]}
        '''),
                   comments_box(text[5], text[6])]

        return display
    except:
        e = sys.exc_info()
        print(e)


@app.callback(
    dash.dependencies.Output('Comments', 'children'),
    [dash.dependencies.Input('mapZone', 'clickData')])
def show_details(clickData):
    title = html.H4('Comments:')
    try:
        print('start of try')
        text = clickData['points'][0]['text'].split('<br>')
        print('got text')
        api_url = BASE_URL + f"comments/{'USGS' if text[5]=='blue' else 'EMSC'}/{text[6]}"
        print(api_url)
        data = requests.get(api_url).json()
        print(data)
        if data['num_comments'] == 0:
            return [title, dcc.Markdown('No comments on this quake to display. Add one on the left!')]
        else:
            return [title, comments_area(data)]

    except:
        e = sys.exc_info()
        print(e)


def get_local_time(utc_time, lat, lon):
    from_zone = tz.gettz('UTC')
    tf = TimezoneFinder()
    to_zone = tz.gettz(tf.timezone_at(lng=float(lon), lat=float(lat)))
    your_zone = tz.tzlocal()
    utc = datetime.datetime.strptime(utc_time, '%Y-%m-%d %H:%M:%S.%f')  # set the UTC time
    utc = utc.replace(tzinfo=from_zone)  # set the utc timezone
    local_time = utc.astimezone(to_zone)
    your_time = utc.astimezone(your_zone)
    return local_time, your_time


def comments_box(source, quakeID):
    source = 'USGS' if source == 'blue' else 'EMSC'
    content = html.Div([html.H4('Add a Public Comment'),
                        dcc.Markdown('Display Name:'),
                        dcc.Input(name='display_name', id='display_name'),
                        dcc.Markdown('What was it like?'),
                        dcc.Textarea(name='comment', id='comment', spellCheck=True, style={
                            'height': '100px', 'width': '75%'}),
                        html.Div(dbc.Button('Submit Comment', outline=True,
                                            size='sm', id='submit_button', n_clicks=0)),
                        html.Div(id='dumpzone')], id='comments_box')
    return content


def comments_area(data):
    comments_area = []
    for comment in data['message']:
        comments_area.append(dbc.Card([
            dbc.CardHeader(f'{comment["name"]}'),
            dbc.CardBody(
                html.P(f'{comment["comment"]}', className="card-text"))],
            className='mb-3', style={'width': '85%'}))
    return html.Div(comments_area)


last_click = 0
# setting up the ability to submit comments


@app.callback(dash.dependencies.Output('dumpzone', 'children'),
              [dash.dependencies.Input('submit_button', 'n_clicks'),
               dash.dependencies.Input('display_name', 'value'),
               dash.dependencies.Input('comment', 'value'),
               dash.dependencies.Input('mapZone', 'clickData')])
def submit_comment(clicks, name, comment, clickData):
    global last_click
    text = clickData['points'][0]['text'].split('<br>')
    source = 'USGS' if text[5] == 'blue' else 'EMSC'
    id = text[6]
    if clicks > last_click:
        if name != None and comment != None:
            payload = {'display_name': name, 'comment': comment}
            api_url = BASE_URL + f'comments/{source}/{id}'
            print('sent request', payload)
            # requests.post(api_url, data=payload)
        last_click = clicks
    else:
        print('tried to run')


details = dbc.Col(id='Details')
comments_col = dbc.Col(id='Comments')
