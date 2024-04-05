from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd

df = pd.read_csv('data/filtered/pie_chart_data.csv')

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Components
title = [html.H1('carXplorer'), html.Br()]
global_widgets = [
    dbc.Label('Select x-column'),
    dcc.Dropdown(id='x-col', options=cars.columns, value='Horsepower'),
    html.Br(),
    dbc.Label('Filter on Origin'),
    dcc.Dropdown(id='origin-filter', options=cars['Origin'].unique(), value='USA'),
]
card_avg = dbc.Card(id='card-avg')
card_count = dbc.Card(id='card-count')
scatter_chart = dvc.Vega(
    id='scatter',
    spec={},
    signalsToObserve=['scatter_select'],
    style={'width': '100%'}
)

# Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(title)),
    dbc.Row([
        dbc.Col(global_widgets, md=4),
        dbc.Col(
            [
                dbc.Row([dbc.Col(card_avg), dbc.Col(card_count)]),
                dbc.Row(dbc.Col(scatter_chart))
            ],
            md=8
        )
    ])
])
