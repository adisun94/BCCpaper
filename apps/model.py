from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from glob import glob
import numpy as np
import pandas as pd
import pathlib
from app import app
from dash import callback_context

fig=go.Figure()
n_steps=5

layout = html.Div([
        dcc.Markdown('''
                    #### Hierarchical screening workflow; original publication accessible here. This project was sponsored by NSF.'''),
        html.Div([html.Button("Step {}".format(i), id=str(i)) for i in range(1,n_steps+1)] + [html.Div(id="step")]),
        dcc.Graph(id='pyramid', figure={})
        ])

@app.callback(
        Output(component_id='pyramid', component_property='figure'),
        Output("step", "children"), [Input(str(i), "n_clicks") for i in range(1,n_steps+1)]
        )
def func(*args):
    trigger = callback_context.triggered[0] 
    step_id=trigger['prop_id'].split('.')[0]
    sel=1
    for j in range(1,6):
        if step_id==str(j):
            sel=j
    step_detail=['','Screening using random forest regression model (built using DFT data) <br> step size = 1/72 <br> max amount of any element = 60 mole%',
        'Screening likely BCC compositions <br> 3.0 < D <3.5, 0.6 < usf < 0.8',
        'Screening using <br> CALPHAD phase diagrams <br> amount of BCC > 99.99% at 800 C <br> Al + Cr + Si = 10-20%',
        'Oxide phases <br> using CALPHAD',
        'DFT <br> validation']

    trace=[]
    fig=make_subplots()
    fig.add_trace(go.Scatter(x=[0,1,9,10,0],y=[0,2,2,0,0],fill='toself'))
    fig.add_trace(go.Scatter(x=[1,2,8,9,1],y=[2,4,4,2,2],fill='toself'))
    fig.add_trace(go.Scatter(x=[2,3,7,8,2],y=[4,6,6,4,4],fill='toself'))
    fig.add_trace(go.Scatter(x=[3,4,6,7,3],y=[6,8,8,6,6],fill='toself'))
    fig.add_trace(go.Scatter(x=[4,5,6,4],y=[8,10,8,8],fill='toself'))
    fig.update_layout(height=525, width=600)
    fig.add_annotation(x=5, y=2*sel-1, text=step_detail[sel],showarrow=False)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout({'paper_bgcolor': 'rgb(255,255,240)', 'plot_bgcolor': 'rgb(255,255,240)'})
    fig.update_layout(showlegend=False)
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))

    selection="Screening step {}".format(step_id)

    return fig, selection

