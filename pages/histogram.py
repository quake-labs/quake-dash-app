import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import requests
import pandas as pd

from app import app



column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## Plots


            """
        ),
        html.Div([
            dcc.Dropdown(
                id='timeFrame',
                options=[
                    {'label': 'Last Quake', 'value': 'lastQuake'},
                    {'label': 'Last Hour', 'value': 'last/hour'},
                    {'label': 'Last Day', 'value': 'last/day'},
                    {'label': 'Last Week', 'value': 'last/week'},
                    {'label': 'Last Month', 'value': 'last/month'}
                ],
                value='lastQuake'
            ),
            html.Div(id='menuItems')
        ])
    ],
    md=4,
)

@app.callback(
    Output('histogram_plot', 'figure'),
    [Input('timeFrame', 'value')])
def update_output(value):
    data = requests.get(f'https://quake-ds-production.herokuapp.com/{value}')
    df = pd.DataFrame(data.json()['message']) if value != 'lastQuake' else \
        pd.DataFrame(data.json()['message'], index=[0])
    
    fig = px.histogram(df, x='mag')
    return fig


column2 = dbc.Col([
    dcc.Graph(id='histogram_plot'),
])

layout = dbc.Row([column1, column2], style={'margin-top': 100, 'height': 1000})
