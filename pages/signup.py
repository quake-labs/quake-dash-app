import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

phonenumber = dbc.FormGroup(
    [
        dbc.Label("Phone Number", html_for="signup-phonenumber"),
        dbc.Input(
            type="tel", id="phonenumber", placeholder="Enter valid US Phone Number"
        ),
    ]
)

zipcode = dbc.FormGroup(
    [
        dbc.Label("Zipcode", html_for="signup-zipcode"),
        dbc.Input(
            type="number", id="zipcode", placeholder="Enter valid 5 digit zipcode",
        ),
    ]
)

form = dbc.Form([phonenumber, zipcode])

column1 = dbc.Col([html.Div([html.Img(src="assets/sms.png")], className="phone-image")])

column2 = dbc.Col([form])

layout = dbc.Row([column1, column2], style={"margin-top": 100, "height": 1000})
