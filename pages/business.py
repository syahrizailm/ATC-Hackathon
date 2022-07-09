import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State

from layout.set_condition import set_condition
from database import get_matching

dash.register_page(__name__, path='/business')
app = dash.get_app()

layout = html.Div([
    dcc.Loading(
        id="get-loading", 
        children = [
            dcc.ConfirmDialog(
                id='get-success',
                message='Profile found',
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
    set_condition
])

@app.callback(
    Output('get-success', 'displayed'),
    Output('get-failed', 'displayed'),
    Input("find-talent-button", "n_clicks"),
    State("set_skills", "value"),
    State("set_programming", "value"),
    State("set_framework", "value"),
)
def get_profile(n_clicks, skills, programming, framework):
    # Don't run if submit button is never clicked
    if (n_clicks == 0):
        return False, False

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

    # Get from DB
    matched = get_matching(condition_query)
    if matched:
        # Show Success/Failed
        for i in matched:
            print(i["email"], i["matching_score"])
        return True, False
    else:
        return False, True