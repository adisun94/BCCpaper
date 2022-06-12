from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from glob import glob
import numpy as np
import pandas as pd
import pathlib
from app import app
from PIL import Image

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../data').resolve()

df=pd.read_excel(DATA_PATH.joinpath('../data/validation.xlsx'))
df.insert(0,'id',list(range(10)))

layout = html.Div([
    dcc.Markdown('''
                #### 10 quaternary alloy compositions validated using DFT and CALPHAD; original publication accessible here. This project was sponsored by NSF. All phase diagrams calculated using the [TCHEA4](https://thermocalc.com/products/databases/high-entropy-alloys/) and [SSUB6](https://thermocalc.com/products/databases/general-alloys-and-pure-substances/) databases.'''),
    dash_table.DataTable(
        id='table-validation',
        columns=[
            {'name':i,'id':i,'selectable':True}
            for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=False,
        filter_action='none',
        #sort_action='native',
        #sort_mode='single',
        row_selectable='single',
        page_action='native',
        page_current=0,
        page_size=10,
        style_cell={
            'minWidth':175, 'maxWidth':175, 'width':175,'fontSize':13
        },
        fill_width=False,
        style_header_conditional=[
            {"if": {"column_id": "id"}, "color": "blue",'fontWeight': 'bold'},
            {"if": {"column_id": "composition"}, "color": "red",'fontWeight': 'bold'},
            {"if": {"column_id": "surf_DFT"}, "color": "green",'fontWeight': 'bold'},
            {"if": {"column_id": "surf_model"}, "color": "green",'fontWeight': 'bold'},
            {"if": {"column_id": "usf_DFT"}, "color": "green",'fontWeight': 'bold'},
            {"if": {"column_id": "usf_model"}, "color": "green",'fontWeight': 'bold'},
            {"if": {"column_id": "D_DFT"}, "color": "green",'fontWeight': 'bold'},
            {"if": {"column_id": "D_model"}, "color": "green",'fontWeight': 'bold'}],
        style_data={'color': 'black','backgroundColor': 'white'},
        style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(245, 245, 245)',}],
        ),
    html.Br(),
    html.Div(id='composition2'),
    dcc.Graph(id='PD2', figure={})
    ])

@app.callback(
    Output(component_id='composition2',component_property='children'),
    Output(component_id='PD2', component_property='figure'),
    Input(component_id='table-validation',component_property='derived_virtual_selected_rows')
    )

def update_image(slctd_row_indices):
    o1='Oxide phase diagram for alloy '+str(slctd_row_indices)

    img = np.array(Image.open(DATA_PATH.joinpath('../data/PD1.jpg')))
    fig = px.imshow(img, color_continuous_scale="gray")
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(showticklabels=False)
    fig.update_layout({'paper_bgcolor': 'rgb(255,255,240)'})


    return o1, fig

