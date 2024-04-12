from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd
import plotly.graph_objs as go
import geopandas as gpd


# Map data loaded
canadian_provinces = gpd.read_file('data/filtered/map_chart_data.geojson')

# Plotting the map of Canada and the 
map_chart = alt.Chart(canadian_provinces, width= 800, height=600).mark_geoshape(stroke='white').project(
    'transverseMercator',
    rotate=[90, 0, 0]
).encode(
    tooltip=['name','prop_women'],
    color=alt.Color('prop_women', 
                    scale=alt.Scale(domain=[0, 1], 
                                    scheme='viridis'), 
                    title='Proportion of Women')
)

labels = alt.Chart(canadian_provinces).mark_text().encode(
    longitude='longitude:Q',
    latitude='latitude:Q',
    text='postal',
    size=alt.value(15),
    opacity=alt.value(1),
)

combined_chart = (map_chart+labels).properties(
    title = "Overall Proportion Across Provinces",
).configure_legend(
    orient='bottom'
)


# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


# Layout
app.layout = dbc.Container([
    dbc.Row([dvc.Vega(id="altair-chart",opt = {"rendered":"svg", "actions":False},spec=combined_chart.to_dict())])
])

# Run the app/dashboard
if __name__ == '__main__':
    app.run(port=8051, debug=True)