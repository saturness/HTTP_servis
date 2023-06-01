import dash
from dash import dcc
from dash import html
from dash.dependencies import Input,Output,State
import pandas as pd 
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import dash_bootstrap_components as dbc
from dash import dash_table, Dash

pio.renderers.default ='browser'
df = pd.read_csv("D:\IT\ITGracheva\Anime.csv", delimiter=";")
fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df.Name, df.Type, df.Episodes, df.Genre],
               fill_color='lavender',
               align='left'))
    ])
tab1_content=[dbc.Row([html.Div([
    html.H4('Analysis of the types and ages of anime'),
    dcc.Graph(id="graph"),
    html.P("Names:"),
    dcc.Dropdown(id='names',
        options=['Type', 'Age'],
        value='Type', clearable=False
    )
])
    ])]
tab2_content=[
    dbc.Row([html.Div([
    html.H4('Graph about studies and their ranks and ratings'),
    dcc.Graph(id="graph1"),
    html.P("Values:"),
    dcc.Dropdown(id='values',
        options=['Rating', 'Ranking', 'Episodes'],
        value='Rating', clearable=False
    )
])
    ])
]
tab3_content=[dbc.Card(
    dbc.CardBody(
        dcc.Markdown('''
            [Data are sourced from Kaggle](https://www.kaggle.com/datasets/angadchau/anime-dataset) \n
            ## About:\n
            Anime\n
            is hand-drawn and computer-generated animation originating from Japan. \n
            Outside of Japan and in English, anime refers to Japanese animation, 
            and refers specifically to animation produced in Japan. However, in Japan and in Japanese,\n
            anime describes all animated works, regardless of style or origin.\n
            Animation produced outside of Japan with similar style to Japanese animation
            is commonly referred to as anime-influenced animation.
            ''')
        )
)]
tab4_content=[
    dbc.Row(
        [html.Div([
    html.H4('Table of anime'),dbc.Label('Click a cell in the table:'),
    dash_table.DataTable(df.to_dict('records'),[{"name": i, "id": i} for i in df.columns], id='tbl'),
    dbc.Alert(id='tbl_out')
    ])])]
tab5_content=[dbc.Row([
    html.H4('Sunburst anime selector'),
    dcc.Graph(id='sunburst'),
    dcc.Dropdown(id='nnames',
        options=['Name', 'Study'],
        value='Name', clearable=False
    )
])
]

app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])


app.layout = html.Div([
    #голова
dbc.Row([
    dbc.Col([html.H1('Information'),
    dbc.Card(
        dbc.CardBody([
        dcc.Markdown('''![ ](https://sinister.ly/uploads/avatars/avatar_60528.png?dateline=1479818344)'''),
        dcc.Markdown('''# Read about anime''')])),
    dbc.Tabs([
    dbc.Tab(tab3_content,label="Start"),
    dbc.Tab(
        tab1_content,label="Types"
    ),
    dbc.Tab(
        tab2_content,label="Study analisys"
    ),
    dbc.Tab(
        tab5_content,label="Selector"
    ),
    dbc.Tab(
        tab4_content,label="Data Info"
    )]
)
]) ]) ])

@app.callback(
    Output("graph", "figure"), 
    Input("names", "value"))
def generate_chart(names):
    fig = px.pie(df, values="Rating", names=names, hole=.3)
    return fig

@app.callback(
    Output("graph1", "figure"), 
    Input("values", "value"))
def generate_chart(values):
    fig1 = px.histogram(df, x="Study", y=values, barmode='group', text_auto='.2s')
    return fig1

@app.callback(
    Output('tbl_out', 'children'), 
    Input('tbl', 'active_cell'))
def update_graphs(active_cell):
    return str(active_cell) if active_cell else "Click the table"

@app.callback(
    Output("sunburst", "figure"),  
    Input("nnames", "value"))
def generate_chart(nnames):
    fig2 = px.sunburst(df, path=['Type', 'Episodes', 'Age', nnames], maxdepth = 2)
    return fig2

app.run_server(debug=True)
