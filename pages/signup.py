import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app, location_search
from dash.dependencies import Input, Output
import requests
import json
import re

phonenumber = dbc.FormGroup(
    [
        dbc.Label("Phone Number", html_for="signup-phonenumber"),
        dbc.Input(
            type="tel", id="phonenumber-input", placeholder="Enter valid US Phone Number", pattern="^(?:\(\d{3}\)|\d{3})[- ]?\d{3}[- ]?\d{4}$", maxLength=14
        ),
        dbc.FormFeedback(
            "That looks like a valid U.S. phone number :-)", valid=True
        ),
        dbc.FormFeedback(
            "Sorry, we only accept valid U.S. phone number",
            valid=False,
        ),
    ]
)

zipcode = dbc.FormGroup(
    [
        dbc.Label("Zipcode", html_for="signup-zipcode"),
        dbc.Input(
            type="text", id="zipcode-input", placeholder="Enter valid 5 digit zipcode", pattern="[0-9]{5}$", maxLength=5
        ),
        dbc.FormFeedback(
            "That looks like a valid U.S. 5 digit ZIP code :-)", valid=True
        ),
        dbc.FormFeedback(
            "Sorry, we only accept valid 5 digit U.S. ZIP code",
            valid=False,
        ),
    ]
)

submit_btn = html.Div(
    [
        dbc.Button("Get Notified", color="primary", id="get-notified-btn"),
    ]
)

result_notf = html.Div([
    html.Span(id="get-notified-btn-output"
              ),
], style={"marginTop": "2%"})

form = dbc.Form([phonenumber, zipcode, submit_btn, result_notf])

column1 = dbc.Col(
    [
        html.Div(
            [html.Img(src="assets/sms.png",
                      className="img-responsive", width="80%")],
            className="phone-image",
        )
    ]
)

column2 = dbc.Col([form])

layout = dbc.Row([column1, column2], style={"margin-top": 100})


# --- Callbacks --- #
@app.callback(
    [Output("phonenumber-input", "valid"),
     Output("phonenumber-input", "invalid")],
    [Input("phonenumber-input", "value")],
)
def check_phone_number_validity(phonenumber):
    print(phonenumber)
    if phonenumber:
        if bool(re.match("^(?:\(\d{3}\)|\d{3})[- ]?\d{3}[- ]?\d{4}$", phonenumber)):
            is_valid = True
        else:
            is_valid = False
        return is_valid, not is_valid
    return False, False


@app.callback(
    [Output("zipcode-input", "valid"),
     Output("zipcode-input", "invalid")],
    [Input("zipcode-input", "value")],
)
def check_zipcode_validity(zipcode):
    if zipcode:
        is_valid = len(zipcode) == 5
        return is_valid, not is_valid
    return False, False


@app.callback(
    Output("get-notified-btn-output", "children"),
    [Input("get-notified-btn", "n_clicks"), Input("phonenumber-input",
                                                  "value"), Input("zipcode-input", "value"), Input("phonenumber-input", "valid"), Input("zipcode-input", "valid")],
)
def on_button_click(n, phonenumber, zipcode, is_phone_valid, is_zip_valid):
    if n is not None:
        if int(n) > 0:
            if is_phone_valid and is_zip_valid:
                phonenumber = re.sub(r"[^\d]", "", phonenumber)
                print(f"Phone number is: {phonenumber}")
                print(f"Zipcode is: {zipcode}")
                payload = {"phonenumber": phonenumber, "zipcode": zipcode}
                print(f"Sending payload: {payload}")
                try:
                    res = requests.post(
                        "https://quakelabs-sms-app.herokuapp.com/web", json=payload)
                    print(res.text)
                except Exception as ex:
                    print(ex)
                    print("Something happened")
                return ""
            elif is_phone_valid:
                return "Please make sure ZIP code is valid."
            elif is_zip_valid:
                return "Please make sure Phone Number is valid."
            else:
                return "Please fill out Phone Number and ZIP code."
