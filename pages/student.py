import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State

from layout.portfolio import input_field
from database import insert

dash.register_page(__name__, path='/')
app = dash.get_app()

# Main app Layout
layout = html.Div([
    # Success/Failed Modal
    dcc.Loading(
        id="ls-loading", 
        children = [
            dcc.ConfirmDialog(
                id='success',
                message='Portfolio has been updated',
            ),
            dcc.ConfirmDialog(
                id='failed',
                message='Server Error',
            ),
        ],
        type = "default",
        fullscreen = True,
        style = {"opacity": "60%"}
    ),

    # Input Portfolio
    input_field
])

# Function to submit
@app.callback(
    Output('success', 'displayed'),
    Output('failed', 'displayed'),
    Input("submit-button-state", "n_clicks"),
    State("input_Email", "value"),
    State("input_Name", "value"),
    State("input_University", "value"),
    State("input_Graduate Year", "value"),
    State("input_skills", "value"),
    State("input_programming", "value"),
    State("input_framework", "value"),
    State("input_japanese", "value"),
    State("input_english", "value"),
)
def upload_profile(n_clicks, email, name, uni, year, skills, programming, framework, japanese, english):
    # Don't run if submit button is never clicked
    if (n_clicks == 0):
        return False, False

    data = {
        "email": email,
        "name": name,
        "uni": uni,
        "year": year,
        "skills": skills,
        "programming": programming,
        "framework": framework,
        "japanese": japanese,
        "english": english
    }

    # Insert to DB
    if insert(data): 
        # Show Success/Failed
        return True, False
    else:
        return False, True
