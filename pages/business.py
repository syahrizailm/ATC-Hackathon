import dash
from dash import Dash, dcc, html
from dash.dash_table import DataTable
from dash.dependencies import Input, Output, State
import pandas as pd

from layout.set_condition import set_condition
from database import get_matching

dash.register_page(__name__, path='/business', title='Catalyst Business', image="logo.png")
app = dash.get_app()

layout = html.Div([
    set_condition,
    dcc.Loading(
        id="get-loading", 
        children = [
            html.Div(
                DataTable(
                    data = [], 
                    columns = [],
                    id = "result-table",
                    style_cell={
                        'textAlign': 'left',
                        "fontFamily": "sans-serif",
                    },
                    style_data={
                        'color': 'black',
                        'backgroundColor': 'white',
                        "padding": "10px"
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#FAFDFF',
                        }
                    ],
                    style_header={
                        'backgroundColor': '#FAFDFF',
                        'color': 'black',
                        'fontWeight': 'bold',
                        "padding": "10px"
                    }
                ),
                style = {
                    "width": "60%",
                    "overflow": "scroll",
                    "margin": "80px auto",
                    "marginBottom": "0px",
                    "display": "block"
                }
            ),
            dcc.ConfirmDialog(
                id='get-failed',
                message='Server Error',
            ),
        ],
        type = "default",
        fullscreen = True,
        style = {"opacity": "60%"}
    ),
    html.Div(
        id = "button-container",
        style = {"display": "none"},   
        children = [
            html.Button(
                id = 'send-connection',
                n_clicks = 0, 
                children = 'Send Job Invitation',
                style = {
                    "margin": "10px auto",
                    "borderColor": "#33AAFF",
                    "color": "#33AAFF",
                    "fontSize": "16px",
                    "width": "80%"
                },
            )
        ] 
    ),
    dcc.ConfirmDialog(
        id='connection-result',
        message='Connection sent!',
    ),
])

@app.callback(
    Output('result-table', 'data'),
    Output('result-table', 'columns'),
    Output('get-failed', 'displayed'),
    Output('get-failed', 'message'),
    Output('button-container', 'style'),
    Input("find-talent-button", "n_clicks"),
    State("set_skills", "value"),
    State("set_programming", "value"),
    State("set_framework", "value"),
)
def get_profile(n_clicks, skills, programming, framework):
    # Don't run if submit button is never clicked
    if (n_clicks == 0):
        return [], [], False, "Server Error", {"display": "none"}

    # Changing result to fit API
    condition_query = []

    # Check if none
    if skills:
        for cond in skills:
            # Adding to query
            condition_query.append(
                {"param": "skills", "value": cond}
            )
    if programming: 
        for cond in programming:
            condition_query.append(
                {"param": "programming", "value": cond}
            )
    if framework:
        for cond in framework:
            condition_query.append(
                {"param": "framework", "value": cond}
            )
    # If no input
    if not condition_query:
        return [], [], True, "Please input condition first", {"display": "none"}

    # Get from DB
    matched = get_matching(condition_query)
    if matched:

        # Changing into pandas dataframe
        profile_df = pd.DataFrame(list(matched))
        profile_df = profile_df.drop(columns="_id")

        # Reordering columns
        profile_df = profile_df.reindex(columns = [
            "matching_score",
            "name",
            "skills", "programming", "framework",
            "japanese", "english",
            "uni", "year"
        ])

        # Changing column name
        profile_df = profile_df.rename(columns={
            "year": "graduation year",
            "matching_score": "matching score"
        })

        # Changing float to percentage
        profile_df.loc[:, "matching score"] = profile_df["matching score"].map(
            '{0:.0%}'.format
        )

        data = profile_df.to_dict("records")
        columns = [{"name": i.title(), "id": i} for i in profile_df.columns]

        # Button style
        style = {
            "margin": "10px auto",
            "width": "60%",
            "display": "block"
        }

        return data, columns, False, "Server Error", style
    else:
        return [], [], True, "Server Error", {"display": "none"}

# Send invitation
@app.callback(
    Output('connection-result', 'displayed'),
    Output('connection-result', 'message'),
    Input('send-connection', 'n_clicks'),
    State('result-table', 'data'),
)
def get_profile(n_clicks, data):
    if (data == []):
        return False, ""
    
    # Show that invitation is success
    return True, f"Job Invitation to {len(data)} talent is sent!"