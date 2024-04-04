from dash import Dash, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
#from vega_datasets import data
import pandas as pd

df = pd.read_csv('data/filtered/pie_chart_data.csv')

# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    dvc.Vega(id='scatter', spec={}),
    dcc.Dropdown(id='year', options=df["REF_DATE"], value='2016'),
    dcc.Dropdown(id='industry', options=df["Industry"], value='Finance')
])

# Server side callbacks/reactivity
@callback(
    Output('scatter', 'spec'),
    Input('year', 'value'),
    Input('industry', 'value')
)

def create_chart(year, industry):

    chart_df = df[(df["Industry"] == industry) &
                     (df["REF_DATE"] == year)]
    return(
        alt.Chart(chart_df).mark_arc().encode(
            theta="VALUE",
            color="Gender"
        )
    )


# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True)