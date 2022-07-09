from dash import Dash, dcc, html, Input, Output
import pandas as pd
import os

from layout.candidate_info import detailed_info
from layout.portfolio import input_field


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

profiles = pd.read_csv("profile.csv")

app.layout = html.Div([
    input_field
])

if __name__ == '__main__':
    app.run_server(debug=True)
