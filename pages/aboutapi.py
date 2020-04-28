import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML as rawHtml
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
from app import app
from .readmetables import team, routes


readme = dbc.Col([
    html.Div(html.H1('Quake Labs API'), style={'margin-top': 20, 'margin-bottom': 20}),

    html.Div([html.H2('Project Overview'),
              dcc.Markdown(
        '''Quake Labs is powered by the Quake Labs API. The API is publicly available at the link below.
        The Quake Labs API is powered by two AWS Lambda functions which collect data from USGS and EMSC's publicly
        available earthquake data and stores it in an AWS RDS instance. The fucntion of this app is to provide easy access
        to earthquake information and provide alerts to affected individuals who sign up for text alerts.
        '''
    )
    ]),  # closes project overview div

    html.Div([html.H2('Team Members'),
              dcc.Markdown('The Quake Labs API and Dashboard were designed and built by:'),
              html.Div(rawHtml(team), style={'text-align': 'center'})
              ]),  # closes team members div
    html.Div([html.H2('Accessing the API'),
              dcc.Markdown(
                  'Base route 👉 https://quake-ds-production.herokuapp.com/ (Returns no data, just a confirmation that the API is running)'),
              html.H3('Routes:'),
              rawHtml(routes)
              ], style={'margin-top': 10}),  # closes accessing the API div
    html.Div([html.H2('Route Usage'),
              dcc.Markdown('''
            1. `/lastQuake/SOURCE/MAGNITUDE` - Returns the last quake over the given magnitude from the source

            `SOURCE`: choice of 'USGS' or 'EMSC' depending on which datasource to pull from

            `MAGNITUDE`: a number 0-11 (accepts floats and ints) defaults to 5.5

            2. `/last/SOURCE/TIME/MAGNITUDE` - Gets the quakes over the given timeframe

            `SOURCE`: choice of 'USGS' or 'EMSC' depending on which datasource to pull from

            `TIME`: choice of 'hour', 'day', 'week' or 'month', returns quakes over the given time period

            `MAGNITUDE`: a number 0-11 (accepts floats and ints) defaults to 5.5

            3. `/history/SOURCE/LAT,LON,DIST` - Returns all quakes in a given area

            `SOURCE`: choice of 'USGS' or 'EMSC' depending on which datasource to pull from

            `LAT` and `LON` are the central latitude and longitude

            `DIST` is the distance in miles from the center to search from

            4. `/zip/ZIPCODE/DIST` - reutrns last quake around a given zip code

            `ZIPCODE`: a US 5 digit zip code

            `DIST`: the distance out to check for the last quake, defaults to 20km

            5. `/comments/SOURCE/QUAKE` - gets or posts comments about quakes

            `SOURCE`: choice of 'USGS' or 'EMSC' depending on which datasource the quake is in

            `QUAKE`: the earthquake's ID number''')
              ], style={'margin-top': 20}),  # closes route usage div
    html.Div([html.H2('Response Format'),
              dcc.Markdown('''
The history routes will return data in the following format:
```
 "message": Contains the quakes returned in format:
         "Oceanic": a boolean value for if the quake was in the ocean (only for USGS quakes, not reliable),
         "id": A numerical id of the quake in our database (unique per quake),
         "lat": lattitude in degrees
         "lon": longitude in degrees
         "mag": Magnitude of the earthquake
         "place": a Human readable representation of approximatly where the quake is
         "time": the time that the quake occured in UTC in ms since Epoch}
 "num_quakes": the number of quakes returned
 "status_code": standard web status codes
 "boundingA": Only returned on history route, Northwest corner of the bounding box
 "boundingB": Only returned on history route, Southeast corner of the bounding box
 ```

 The comments route will return data in the following format:

 ```
 "message": contains a list of comments in the format:
        "name": the display name of the User
        "comment": the comment
"num_comments": the number of comments returned
"status_code": web status codes
        ''')
              ]),  # closes response format div
    html.Div([html.H2('Tech Stack'),
              dcc.Markdown('''
            - [Flask](https://flask.palletsprojects.com/en/1.1.x/)
            - [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
            - [AWS Lambda](https://docs.aws.amazon.com/lambda/index.html)
            - [AWS RDS](https://docs.aws.amazon.com/rds/index.html)
            - [Heroku](https://devcenter.heroku.com)
            ''')
              ]),  # closes tech stack div
    html.Div([html.H2('Architecture'),
              dcc.Markdown('''
    ![architecture](https://www.notion.so/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2F1b61d2ba-287a-4a01-8c6f-98ae376dc2c9%2Fquake-architect-diagram.jpg)
    ''')
              ]),  # closes Architecture div
    html.Div([html.H2('Data Sources'),
              dcc.Markdown('''
    Our primary data source is the USGS geojson feed. [View the documentation](https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php), or [search their data](https://earthquake.usgs.gov/earthquakes/search/).

    For a further history of earthquakes we also collected the data available on [EMSC](https://www.emsc-csem.org/Earthquake/).
    ''')
              ]),  # closes Data Sources div
    html.Div([html.H2('Feature Requests and Contributions'),
              dcc.Markdown('''
        Source code for the API is available on [GitHub](https://github.com/quake-labs/quake-ds)

        Source code for the Dashboard is also available on [GitHub](https://github.com/quake-labs/quake-dash-app)

        We would love to hear from you about new features which would improve this app and further the aims of our project. Please provide as much detail and information as possible to show us why you think your new feature should be implemented.

        If you have developed a patch, bug fix, or new feature that would improve this app, please submit a pull request. It is best to communicate your ideas with the developers first before investing a great deal of time into a pull request to ensure that it will mesh smoothly with the project.

        Remember that this project is licensed under the MIT license, and by submitting a pull request, you agree that your work will be, too.

        ''')
              ]),  # closes feature requests div
    html.Div(html.P('Please feel free to contact our team with any questions at quakelabs@gmail.com'))
])  # closes readme column


layout = html.Div(readme)
