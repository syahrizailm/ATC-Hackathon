import dash
from dash import Dash, dcc, html
from dash.dash_table import DataTable
from dash.dependencies import Input, Output, State
import pandas as pd

from layout.set_condition import set_condition
from database import get_matching

dash.register_page(__name__, path='/business')
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
                            'backgroundColor': '#ECF0F3',
                        }
                    ],
                    style_header={
                        'backgroundColor': '#ECF0F3',
                        'color': 'black',
                        'fontWeight': 'bold',
                        "padding": "10px"
                    }
                ),
                style = {
                    "width": "80%",
                    "overflow": "scroll",
                    "margin": "60px auto",
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
])

@app.callback(
    Output('result-table', 'data'),
    Output('result-table', 'columns'),
    Output('get-failed', 'displayed'),
    Output('get-failed', 'message'),
    Input("find-talent-button", "n_clicks"),
    State("set_skills", "value"),
    State("set_programming", "value"),
    State("set_framework", "value"),
)
def get_profile(n_clicks, skills, programming, framework):
    # Don't run if submit button is never clicked
    if (n_clicks == 0):
        return [], [], False, "Server Error"

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
        return [], [], True, "Please input condition first"

    # Get from DB
    matched = get_matching(condition_query)
    if matched:
        # Show Success/Failed
        profile_df = pd.DataFrame(list(matched))
        profile_df = profile_df.drop(columns="_id")
        data = profile_df.to_dict("records")
        columns = [{"name": i.title(), "id": i} for i in profile_df.columns]
        return data, columns, False, "Server Error"
    else:
        return [], [], True, "Server Error"