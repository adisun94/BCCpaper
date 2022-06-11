from dash import  dcc, html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import bcct, valid


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Screening      |      ', href='/apps/bcct'),
        dcc.Link('Validation', href='/apps/valid'),
        ], className="row"),
    html.Div(id='page-content', children=[])
    ])


@app.callback(Output('page-content', 'children'),
        [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/bcct':
        return bcct.layout
    if pathname == '/apps/valid':
        return valid.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=True)
