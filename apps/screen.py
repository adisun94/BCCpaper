from dash import Dash, dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from glob import glob
import numpy as np
import pandas as pd
import pathlib
from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath('../data').resolve()

df=pd.read_csv(DATA_PATH.joinpath('../data/1184alloys.txt'),sep=' ')
df=np.round(df,3)
df.insert(0,'id',list(range(1184)))
bcc=np.loadtxt(DATA_PATH.joinpath('../data/BCCscreen.txt'))
bcc=bcc.astype(int)
df.rename(columns={'surf':'surf (J/m\u00b2)','gsf':'usf (J/m\u00b2)'},inplace=True)


layout = html.Div([
    dcc.Markdown('''
        #### 1184 quaternary alloy compositions screened using the hierarchical model; original publication accessible here. This project was sponsored by NSF. All phase diagrams calculated using the [TCHEA4](https://thermocalc.com/products/databases/high-entropy-alloys/) database using the [TC-Python API](https://thermocalc.com/products/software-development-kits/tc-python/)'''),
    html.Br(),
    dash_table.DataTable(
        id='table-screening',
        columns=[
            {'name':iname,'id':iname,'selectable':True}
            for iname in df.columns
        ],
        data=df.to_dict('records'),
        export_format='csv',
        editable=False,
        filter_action='native',
        sort_action='native',
        sort_mode='single',
        row_selectable=False,
        page_action='native',
        page_current=0,
        page_size=10,
        style_cell={
            'minWidth':25, 'maxWidth':25, 'width':25,'fontSize':13
        },
        style_header_conditional=[
            {"if": {"column_id": "id"}, "color": "blue",'fontWeight': 'bold'},
            {"if": {"column_id": "Ti"}, "color": "red",'fontWeight': 'bold'},
            {"if": {"column_id": "Zr"}, "color": "red",'fontWeight': 'bold'},
            {"if": {"column_id": "Hf"}, "color": "red",'fontWeight': 'bold'},
            {"if": {"column_id": "V"}, "color": "red",'fontWeight': 'bold'},
            {"if": {"column_id": "Nb"}, "color": "red",'fontWeight': 'bold'},
            {"if": {"column_id": "Ta"}, "color": "red",'fontWeight': 'bold'},
            {"if": {"column_id": "Mo"}, "color": "red",'fontWeight': 'bold'},
            {"if": {"column_id": "W"}, "color": "red",'fontWeight': 'bold'},
            {"if": {"column_id": "Re"}, "color": "red",'fontWeight': 'bold'},
            {"if": {"column_id": "Ru"}, "color": "red",'fontWeight': 'bold'},
            {"if": {"column_id": "Al"}, "color": "red",'fontWeight': 'bold'},
            {"if": {"column_id": "Cr"}, "color": "red",'fontWeight': 'bold'},
            {"if": {"column_id": "Si"}, "color": "red",'fontWeight': 'bold'},
            {"if": {"column_id": 'surf (J/m\u00b2)'}, "color": "green",'fontWeight': 'bold'},
            {"if": {"column_id": 'usf (J/m\u00b2)'}, "color": "green",'fontWeight': 'bold'},
            {"if": {"column_id": "D"}, "color": "green",'fontWeight': 'bold'},
            ],
        style_data={'color': 'black','backgroundColor': 'white'},
        style_data_conditional=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(245, 245, 245)',}],
        ),
    html.Div([
        "Enter alloy id between 0 and 1183 and press 'Enter': ",
        dcc.Input(id='alloyID', value=123, type='number',placeholder="Alloy ID", debounce=True,min=0, max=1183, step=1)
        ]),
    html.Br(),
    html.Div(id='composition'),
    html.Br(),
    html.Div(id='prediction'),
    dcc.Graph(id='PD', figure={})
    ])

@app.callback(
    Output(component_id='composition',component_property='children'),
    Output(component_id='prediction', component_property='children'),
    Output(component_id='PD', component_property='figure'),
    Input(component_id='alloyID', component_property='value')
    )

def update_output(input_id):

    mass={22:'Ti',40:'Zr',72:'Hf',23:'V',41:'Nb',73:'Ta',42:'Mo',74:'W',75:'Re',44:'Ru',13:'Al',24:'Cr',14:'Si'}
    temp=[]
    print(input_id)
    p=bcc[input_id]
    print(p)
    
    a=[]
    with open(DATA_PATH.joinpath('../data/1184/'+str(p)+'.txt')) as f:
        for line in f:
            a.append(line.split())

    elems=''
    for i in range(4):
        elems=elems+mass[int(a[0][i])]+'('
        elems=elems+str(round(float(a[1][i])*72))+')-'
    print(elems)

    phasefracs={}
    for l in range(2,len(a),3):
        phasefracs[a[l][0]]=[]
    for l in range(2,len(a),3):
        phasefracs[a[l][0]].append(np.column_stack((np.array(a[l+1]).astype(float),np.array(a[l+2]).astype(float))))

    trace=[]
    fig=make_subplots()
    for n in phasefracs:
        x,y=phasefracs[n][0][:,0]-273,phasefracs[n][0][:,1]
        fig.add_trace(go.Scatter(x=x,y=y,name=n))

    fig.update_xaxes(title='Temperature (C)')
    fig.update_yaxes(title='Mass fraction')
    fig.update_layout(height=600, width=600)
    fig.update_layout({'paper_bgcolor': 'rgb(255,255,240)'})

    o1='The alloy composition in mole percent is: '+elems
    o2='Strength parameter (usf) = '+str(float(df.iloc[[input_id]]['usf (J/m\u00b2)']))+' J/m\u00b2, Ductility parameter (D) = '+str(float(df.iloc[[input_id]]['D']))
    return o1,o2,fig

