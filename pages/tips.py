import dash_html_components as html
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML as rawHtml
from .safety import safe_html

safety = rawHtml(safe_html)

layout = html.Div(safety, style={'margin-top': 40})
