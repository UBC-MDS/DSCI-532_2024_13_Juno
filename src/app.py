from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd

# Filter the data for a pie chart by province and year
df = pd.read_csv("data/raw/filtered_canada.csv")

new_df = df[(df['Type of corporation'] == 'Total all corporations') & 
            (df['Industry'] == 'Total all industries') & 
            (df["Size of enterprise"] == "Total all sizes") &
            (df["Unit of measure"] == "Number") &
            (df["Executive"] == "All officers\xa0") &
            (df["GEO"] != "Canada, total") &
            (df["GEO"] != "Unclassified province or territory")
].copy()
new_df = new_df.loc[:, ["REF_DATE", "Gender", "GEO", "VALUE"]]
new_df.head()

new_df.to_csv('data/filtered/province_data.csv', index=False)
new_df["GEO"].unique()
df = pd.read_csv('data/filtered/province_data.csv')


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    dvc.Vega(id='pie-chart', spec={}),
    html.P(html.Br()),
    html.Label('Select a Year'),
    dcc.Dropdown(id='year', options=df["REF_DATE"].unique().tolist(), value = 2016),
    html.Label('Select a Province'),
    dcc.Dropdown(id='prov', options = df["GEO"].unique().tolist(), value ='British Columbia')
])

# Server side callbacks/reactivity
@callback(
    Output('pie-chart', 'spec'),
    Input('year', 'value'),
    Input('prov', 'value'),
)

def create_chart(year, prov):

    # Issue is with industry and year datatype - not recognised by pandas, so it returns empty df (filtered_df)
    filtered_df = df[(df["GEO"] == prov) & (df["REF_DATE"] == year)]

    
    chart = alt.Chart(filtered_df).mark_arc().encode(
        theta="VALUE",
        color="Gender", 
        tooltip=['Gender:N', 'VALUE:Q']).properties(
        title="Number of Women vs Men in Executive Positions"
)


    return chart.to_dict()


# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')