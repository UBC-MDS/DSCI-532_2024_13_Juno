from dash import Dash, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
#from vega_datasets import data
import pandas as pd

df = pd.read_csv('data/raw/filtered_canada.csv')

# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    dcc.Graph(id='pie-chart'),
    dcc.Dropdown(id='year', options=df["REF_DATE"], value='2016'),
])

# Server side callbacks/reactivity
@callback(
    #Output('scatter', 'spec'),
    Output('pie-chart', 'figure'),
    Input('x-col', 'value')
    

)
# def create_chart(x_col):
#     return(
#         alt.Chart(data).mark_point().encode(
#             x=x_col,
#             y='Miles_per_Gallon',
#             tooltip='Origin'
#         ).interactive().to_dict()
#     )
def create_pie_chart(x_col):
    return {
        'data': [{
            'labels': df[x_col].value_counts().index.tolist(),
            'values': df[x_col].value_counts().values.tolist(),
            'type': 'pie'
        }],
        'layout': {
            'title': f'Pie Chart of {x_col}'
        }
    }

# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True)