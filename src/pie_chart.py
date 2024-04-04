from dash import Dash, dcc, callback, Output, Input, html
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
    dvc.Vega(id='pie-chart', spec={}),
    html.P(html.Br()),
    html.Label('Select a Year'),
    dcc.Dropdown(id='year', options=[{'label': year, 'value': year} for year in df["REF_DATE"].unique()], value='2016'),
    html.Label('Select an Industry'),
    dcc.Dropdown(id='industry', options=[{'label': industry, 'value': industry} for industry in df["Industry"].unique()], value='Finance')
])

# Server side callbacks/reactivity
@callback(
    Output('pie-chart', 'spec'),
    Input('year', 'value'),
    Input('industry', 'value')
)

# def filter_data(df, year, industry):
#     # return df[(df["Industry"] == industry) & (df["REF_DATE"] == year)]
#     filtered_rows = []
#     for index, row in df.iterrows():
#         if row["Industry"] == industry and row["REF_DATE"] == year:
#             filtered_rows.append(row)
#     return pd.DataFrame(filtered_rows)

def create_chart(year, industry):
    
    #filtered_df = filter_data(df, year, industry)

    chart = alt.Chart(df).mark_arc().encode(
        theta="VALUE",
        color="Gender"
    )

    return chart.to_dict()


# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True)