from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from parameters.portfolio import *

def generate_input_field(field_name, input_type):
    return html.Div(
        children = [ 
            html.H5(field_name),
            dcc.Input(
                id = f"input_{field_name}",
                type = input_type,
                placeholder = field_name,
                style = { 
                    "width": "80%",
                },
            )
        ]
    )


input_field = html.Div(
    style = {
        "margin": "60px auto",
        "width": "40%",
        "display": "block"
    },
    children = [ 
        html.H1("Your Portfolio"),

        html.H3(
            "Personal Information",
            style = {"marginTop": "40px"}
        ),
        html.Div([ 
            generate_input_field("Email", "email"),
            generate_input_field("Name", "text"),
            generate_input_field("University", "text"),
            generate_input_field("Graduate Year", "number"), 
        ]),

        html.H3(
            "Your Skills",
            style = {"marginTop": "40px"}
        ),
        html.Div([ 
            html.Div([
                html.H5("Skills"),
                dcc.Dropdown(
                    id = "input_skills",
                    options = skills,
                    multi = True,
                    placeholder = "Skills",
                )
            ]),
            html.Div([
                html.H5("Programming Language"),
                dcc.Dropdown(
                    id = "input_programming",
                    options = programming_language,
                    multi = True,
                    placeholder = "Programming Language",
                )
            ]),
            html.Div([
                html.H5("Framework"),
                dcc.Dropdown(
                    id = "input_framework",
                    options = framework,
                    multi = True,
                    placeholder = "Framework",
                )
            ]),
            html.Div([
                html.H5("Japanese Language Skill"),
                dcc.RadioItems(
                    id = "input_japanese",
                    options = ["N5", "N4", "N3", "N2", "N1"],
                    inline = True,
                    labelStyle = { "paddingRight": "10px" },
                )
            ]),
            html.Div([
                html.H5("English Language Skill"),
                dcc.RadioItems(
                    id = "input_english",
                    options = ["Beginner", "Intermediate", "Business", "Native"],
                    inline = True,
                    labelStyle = { "paddingRight": "10px" }
                )
            ]),
        ], style = { "width": "80%"}),

        html.Button(
            id = 'submit-button-state',
            n_clicks = 0, 
            children = 'Submit',
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