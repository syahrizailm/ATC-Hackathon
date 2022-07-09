from dash import html

detailed_info = html.Div(
    children = [
        html.Div(
            children = [
                html.H5("Chirstine Jones"),
                html.P("80% match"),
            ]
        ),
        html.Div(
            children = [
                html.Div("University of Tokyo")
            ]
        )
    ]
)
