import dash
from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from pymongo import MongoClient
from dotenv import load_dotenv
import os

from layout.portfolio import input_field
from database import get_matching

dash.register_page(__name__, path='/business')
app = dash.get_app()

# Check local or prod
is_prod = os.environ.get('IS_HEROKU', None)

# Provide the mongodb atlas url to connect python to mongodb using pymongo
if is_prod:
    CONNECTION_STRING = os.environ.get('MONGO_CONNECTION')
else:
    load_dotenv()
    CONNECTION_STRING = os.environ["MONGO_CONNECTION"]

# Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
client = MongoClient(CONNECTION_STRING)
db = client['portfolio_list']
collection = db["portfolio_collection"]

# Query
matched = get_matching([
        {"param": "framework", "value": "TensorFlow"},
        {"param": "programming", "value": "Python"}
    ])
for i in matched:
    print(i["email"], i["matching_score"])

layout = html.Div(
    "Test"
)