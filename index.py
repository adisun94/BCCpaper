from dash import  dcc, html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import model, screen, valid


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Workflow          |      ', href='/apps/model'),
        dcc.Link('Screening      |      ', href='/apps/screen'),
        dcc.Link('Validation', href='/apps/valid'),
        ], className="row"),
    html.Div(id='page-content', children=[])
    ])


@app.callback(Output('page-content', 'children'),
        [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/model':
        return model.layout
    if pathname == '/apps/screen':
        return screen.layout
    if pathname == '/apps/valid':
        return valid.layout
    else:
        return "Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=True)
