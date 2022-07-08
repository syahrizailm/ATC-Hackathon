from dash import Dash, dcc, html, Input, Output
import os


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H2('Hello ATC-Hackathon'),
])

if __name__ == '__main__':
    app.run_server(debug=True)
