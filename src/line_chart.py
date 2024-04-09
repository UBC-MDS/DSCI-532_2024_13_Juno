from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd

df = pd.read_csv('data/filtered/province_data.csv')
card_data = pd.read_csv('data/filtered/cards_data.csv')
time_columns = card_data['REF_DATE'].unique()
province_columns = card_data['GEO'].unique()#.remove('Unclassified province or territory')

# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    dvc.Vega(id='line-chart', spec={}),
    html.P(html.Br()),
    dbc.Label('Filter on Province'),
    dcc.Dropdown(id='province-filter', options=province_columns, value='Canada, total'),
    html.Br(),
    dbc.Label('Filter on Year'),
    dcc.Dropdown(id='year-filter', options=time_columns, value= 2016)
])

# Server side callbacks/reactivity
@callback(
    Output('line-chart', 'spec'),
    [Input('province-filter', 'value'),
     Input('year-filter', 'value')]
)
def create_chart(prov, selected_year):
    filtered_df = df[(df["GEO"] == prov)]

    chart = alt.Chart(filtered_df).mark_line().encode(
        x=alt.X('REF_DATE:O', axis=alt.Axis(title='Year')),
        y=alt.Y('VALUE:Q', axis=alt.Axis(title='Number of People')),
        color='Gender:N',
        tooltip=['Gender:N', 'VALUE:Q']
    ).properties(
        title='Number of Men and Women in Executive Positions in {} Over the Years'.format(prov),
        width=1200,
        height=200
    )

    if selected_year is not None:
        rule = alt.Chart(pd.DataFrame({'selected_year': [selected_year]})).mark_rule(color='red').encode(
            x='selected_year:O'
        ).transform_filter(
            alt.FieldEqualPredicate(field='selected_year', equal=selected_year)
        )
        chart_with_marker = chart + rule
    else:
        chart_with_marker = chart

    return chart_with_marker.configure_axis(
        labelAngle=0
    ).to_dict()


# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True)