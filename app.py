from dash import Dash, html, dcc
import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, use_pages=True, external_stylesheets=external_stylesheets, title="Catalyst")

server = app.server

app.layout = html.Div([
	dash.page_container
])

if __name__ == '__main__':
	app.run_server(debug=True)