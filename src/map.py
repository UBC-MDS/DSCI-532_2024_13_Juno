from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd
import plotly.graph_objs as go
import geopandas as gpd


# Map data loaded
df = pd.read_csv('C:/Users/karan/MDS/Block_6/DSCI-532/DSCI-532_2024_13_appname/data/raw/filtered_canada_num.csv')


new_df = df[(df['Type of corporation'] == 'Total all corporations') & 
            (df['Industry'] == 'Total all industries') & 
            (df["Size of enterprise"] == "Total all sizes") &
            (df["Executive"] == "All officers\xa0") &
            (df["GEO"] != "Canada, total")
].copy()

new_df_sum = pd.DataFrame(new_df.groupby(['GEO','Gender'])['VALUE'].sum().unstack())
new_df_sum['prop_women'] = new_df_sum['Women']/(new_df_sum['Women']+new_df_sum['Men'])
new_df_sum = new_df_sum.fillna(0)

url = 'https://naciscdn.org/naturalearth/50m/cultural/ne_50m_admin_1_states_provinces.zip'
world_regions = gpd.read_file(url)

canadian_provinces = world_regions.query("iso_a2 == 'CA'")[['wikipedia', 'name', 'region', 'postal', 'latitude', 'longitude', 'geometry']]

canadian_provinces = canadian_provinces.merge(new_df_sum, left_on = 'name', right_on = 'GEO')

# canadian_provinces = canadian_provinces[['name','postal','latitude','longitude','geometry','Men','Women','prop_women']]
canadian_provinces.prop_women = canadian_provinces.prop_women.round(2)
canadian_provinces

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