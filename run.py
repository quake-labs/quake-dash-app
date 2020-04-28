# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app, server
from pages import history, map, histogram, aboutapi, tips, search, signup

# Import RE for dynamic URLs for quake details
import re

"""
https://dash-bootstrap-components.opensource.faculty.ai/l/components/navbar

NavbarSimple consists of a 'brand' on the left, to which you can attach a link
with brand_href, and a number nav items as its children. NavbarSimple will
collapse on smaller screens, and add a toggle for revealing navigation items.

brand (string, optional): Brand text, to go top left of the navbar.
brand_href (string, optional): Link to attach to brand.
children (a list of or a singular dash component, string or number, optional): The children of this component
color (string, optional): Sets the color of the NavbarSimple. Main options are primary, light and dark, default light. You can also choose one of the other contextual classes provided by Bootstrap (secondary, success, warning, danger, info, white) or any valid CSS color of your choice (e.g. a hex code, a decimal code or a CSS color name)
dark (boolean, optional): Applies the `navbar-dark` class to the NavbarSimple, causing text in the children of the Navbar to use light colors for contrast / visibility.
light (boolean, optional): Applies the `navbar-light` class to the NavbarSimple, causing text in the children of the Navbar to use dark colors for contrast / visibility.
sticky (string, optional): Stick the navbar to the top or the bottom of the viewport, options: top, bottom. With `sticky`, the navbar remains in the viewport when you scroll. By contrast, with `fixed`, the navbar will remain at the top or bottom of the page.
"""

navbar = dbc.NavbarSimple(
    brand="Quake Labs",
    brand_href="/",
    children=[
        dbc.NavItem(dcc.Link("Local History", href="/history", className="nav-link")),
        dbc.NavItem(
            dcc.Link("Earthquake Saftey Tips", href="/tips", className="nav-link")
        ),
        dbc.NavItem(dcc.Link("Get Notified", href="/signup", className="nav-link")),
        dbc.NavItem(dcc.Link("About The API", href="/aboutapi", className="nav-link")),
    ],
    sticky="top",
    color="dark",
    light=False,
    dark=True,
    style={"height": "15px"},
)

footer = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.P(
                [
                    html.Span("Quake Labs", className="mr-2"),
                    html.A(
                        html.I(className="fas fa-envelope-square mr-1"),
                        href="mailto:quakelabs.ds.lambda@gmail.com",
                    ),
                    html.A(
                        html.I(className="fab fa-github-square mr-1"),
                        href="https://github.com/quake-labs",
                    ),
                ],
                className="lead",
            )
        )
    )
)

# For more explanation, see:
# Plotly Dash User Guide, URL Routing and Multiple Apps
# https://dash.plot.ly/urls

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        dbc.Container(id="page-content", className="h-25"),
        html.Hr(),
        footer,
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname == "/":
        return map.layout
    elif pathname == "/history":
        return history.layout
    elif pathname == "/histogram":
        return histogram.layout
    elif pathname == "/aboutapi":
        return aboutapi.layout
    elif pathname == "/tips":
        return tips.layout
    elif re.search("/quakedetail/*", str(pathname)):
        return detail.layout
    elif pathname == "/search":
        return search.layout
    elif pathname == "/signup":
        return signup.layout
    else:
        return dcc.Markdown("## Page not found")


if __name__ == "__main__":
    app.run_server(debug=True)
