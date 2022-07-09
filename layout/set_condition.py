from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from layout.portfolio_parameters import *

set_condition = html.Div(
    style = {
        "margin": "60px auto",
        "width": "40%",
        "display": "block"
    },
    children = [ 
        html.H1("Talent Database"),

        html.H3(
            "Set your condition",
            style = {"marginTop": "40px"}
        ),

        html.Div([ 
            html.Div([
                html.H5("Skills"),
                dcc.Dropdown(
                    id = "set_skills",
                    options = skills,
                    multi = True,
                    placeholder = "Skills",
                )
            ]),
            html.Div([
                html.H5("Programming Language"),
                dcc.Dropdown(
                    id = "set_programming",
                    options = programming_language,
                    multi = True,
                    placeholder = "Programming Language",
                )
            ]),
            html.Div([
                html.H5("Framework"),
                dcc.Dropdown(
                    id = "set_framework",
                    options = framework,
                    multi = True,
                    placeholder = "Framework",
                )
            ]),
        ], style = { "width": "80%"}),

        html.Button(
            id = 'find-talent-button',
            n_clicks = 0, 
            children = 'Find Talent',
            style = {
                "marginTop": "40px",
                "borderColor": "#33AAFF",
                "color": "#33AAFF",
                "width": "80%",
                "fontSize": "16px"
            }
        )
    ]
)