from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os

from layout.candidate_info import detailed_info
from layout.portfolio import input_field


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

# Check local or prod
is_prod = os.environ.get('IS_HEROKU', None)

# Get Password
if is_prod:
    PASS = os.environ.get('MONGO_PASS')
else:
    load_dotenv()
    PASS = os.environ["MONGO_PASS"]

# Provide the mongodb atlas url to connect python to mongodb using pymongo
CONNECTION_STRING = f"mongodb+srv://syahrizailm:{PASS}@cluster0.xvzk5.mongodb.net/?retryWrites=true&w=majority"

# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
client = MongoClient(CONNECTION_STRING)
db = client['portfolio_list']

server = app.server

profiles = pd.read_csv("profile.csv")

app.layout = html.Div([
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
    input_field
])

@app.callback(
    Output('success', 'displayed'),
    Output('failed', 'displayed'),
    Input("submit-button-state", "n_clicks"),
    State("input_Email", "value"),
    State("input_Name", "value"),
    State("input_University", "value"),
    State("input_Graduate Year", "value"),
    State("input_programming", "value"),
    State("input_framework", "value"),
    State("input_japanese", "value"),
    State("input_english", "value"),
)
def upload_profile(n_clicks, email, name, uni, year, programming, framework, japanese, english):
    if (n_clicks == 0):
        return False, False

    data = {
        "email": email,
        "name": name,
        "uni": uni,
        "year": year,
        "programming": programming,
        "framework": framework,
        "japanese": japanese,
        "english": english
    }
    try:
        portfolio_collection = db["portfolio_collection"]
        portfolio_collection.insert_one(data)
        return True, False
    except:
        return False, True

if __name__ == '__main__':
    app.run_server(debug=True)
