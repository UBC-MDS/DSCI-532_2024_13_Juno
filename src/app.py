from dash import Dash, dcc, callback, Output, Input, html
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd
import plotly.graph_objs as go

# Filter the data for a pie chart by province and year
df = pd.read_csv("data/raw/filtered_canada.csv")

# new_df = df[(df['Type of corporation'] == 'Total all corporations') & 
#             (df['Industry'] == 'Total all industries') & 
#             (df["Size of enterprise"] == "Total all sizes") &
#             (df["Unit of measure"] == "Number") &
#             (df["Executive"] == "All officers\xa0") &
#             (df["GEO"] != "Canada, total") &
#             (df["GEO"] != "Unclassified province or territory")
# ].copy()

new_df = df[(df['Type of corporation'] == 'Total all corporations') & 
            (df['Industry'] == 'Total all industries') & 
            (df["Size of enterprise"] == "Total all sizes") &
            (df["Unit of measure"] == "Number") &
            (df["Executive"] == "All officers\xa0") &
            (df["GEO"] != "Unclassified province or territory")
].copy()
new_df = new_df.loc[:, ["REF_DATE", "Gender", "GEO", "VALUE"]]
new_df.head()

new_df.to_csv('data/filtered/province_data.csv', index=False)
new_df["GEO"].unique()
df = pd.read_csv('data/filtered/province_data.csv')
#############





# Initiatlize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server


card_data = pd.read_csv('data/filtered/cards_data.csv')
# Components

title = [html.H1('Juno: Gender Equality in Executive Positions Across Canada'), html.Br()]
province_columns = card_data['GEO'].unique()#.remove('Unclassified province or territory')
province_columns = province_columns[province_columns!='Unclassified province or territory']
industry_columns = card_data['Industry'].unique()
time_columns = card_data['REF_DATE'].unique()
global_widgets = [
    dbc.Label('Filter on Province'),
    dcc.Dropdown(id='province-filter', options=province_columns, value='Canada, total'),
    html.Br(),
    dbc.Label('Filter on Year'),
    dcc.Dropdown(id='year-filter', options=time_columns, value= 2016)  # Might want to consider a multi-filter option for year
]
card_women = dbc.Card(id='card-women')
card_men = dbc.Card(id='card-men')



industry = dcc.Dropdown(id='industry-filter', options=industry_columns, value='Total all industries'),

# Layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(title)),
    dbc.Row([
        dbc.Col(global_widgets, md=4),
        dbc.Col(
            [
                dbc.Row([dbc.Col(card_women), dbc.Col(card_men), dbc.Col(industry) ])

            ],
            md= "8"
        ),
    dbc.Row(dvc.Vega(id='line-chart')),
    dbc.Row(dcc.Graph(id='bar-chart')),
    dbc.Row(dcc.Graph(id='bar2-chart'))
    ])
])

# Server side callbacks/reactivity
@callback(
    Output('card-women', 'children'),
    Output('card-men', 'children'),
    Input('province-filter', 'value'),
    Input('industry-filter', 'value'),
    Input('year-filter', 'value'),
)
def calculate_proportion(province_filter, industry_filter, year_filter):
    # There is no need to drop na for card_data because there are no NAs in this filtered dataset, but this is the code to check
    # For this and drop NA if needed in the future
    # print(f'Card_df shape: {card_data.shape}')
    # print(f"NA values in card df: {card_data['VALUE'].isna().sum()}")
    # card_data.dropna(subset=['VALUE'], inplace=True)

    # Implementing filtering based on widgets
    # Bug with filtering everything at once - will filter step wise until I find a solution
    geo_filtered_data = card_data[card_data['GEO'] == province_filter]
    industry_filtered_data = geo_filtered_data[geo_filtered_data['Industry'] == industry_filter]
    filtered_data = industry_filtered_data[industry_filtered_data['REF_DATE'] == year_filter]  # Final filter

    women_card_df = filtered_data.query('Gender == "Women"')
    men_card_df = filtered_data.query('Gender == "Men"')
    # print(f"NA values in women df: {women_card_df.isna()}")
    # print(f"NA values in men df: {men_card_df.isna()}")
    total_people = filtered_data['VALUE'].sum()
    total_women = women_card_df['VALUE'].sum()
    total_men = men_card_df['VALUE'].sum()
    prop_women = (total_women / total_people) * 100
    prop_men = (total_men / total_people) * 100

    card_women_content = [
        dbc.CardHeader('Overall Proportion of Women in this Subset (%)'),
        dbc.CardBody(f'{round(prop_women, 2)} %')
    ]
    card_men_content = [
        dbc.CardHeader('Overall Proportion of Men in this Subset (%)'),
        dbc.CardBody(f'{round(prop_men, 2)} %')
    ]
    return card_women_content, card_men_content



# Server side callbacks/reactivity
@app.callback(
    Output('bar2-chart', 'figure'),
    [Input('year-filter', 'value'),
     Input('province-filter', 'value')]
)
def update_chart(year, province):
    df = pd.read_csv('data/filtered/bar_chart2_data.csv')
    # Filter the DataFrame based on selected year and province
    filtered_df = df[(df["REF_DATE"] == year) & (df["GEO"] == province)]

    # Group the filtered DataFrame by 'Type of corporation' and 'Gender' and count occurrences
    grouped_df = filtered_df.groupby(['Industry', 'Gender'])['VALUE'].sum().unstack(fill_value=0)
    
    # Create clustered bar chart with data labels
    data = []
    if 'Men' in grouped_df.columns:
        data.append(go.Bar(x=grouped_df.index, y=grouped_df['Men'], name='Men', text=grouped_df['Men'], textposition='inside'))
    if 'Women' in grouped_df.columns:
        data.append(go.Bar(x=grouped_df.index, y=grouped_df['Women'], name='Women', text=grouped_df['Women'], textposition='inside'))

    layout = go.Layout(barmode='group', title='Distribution by Industry and Gender', xaxis=dict(title='Industry'), yaxis=dict(title='Count'))

    return {'data': data, 'layout': layout}


# Server side callbacks/reactivity
@callback(
    Output('line-chart', 'spec'),
    Input('province-filter', 'value'),
)
def create_chart(prov):
    filtered_df = df[(df["GEO"] == prov)]

    chart = alt.Chart(filtered_df).mark_line().encode(
        x = alt.X('REF_DATE:O', axis=alt.Axis(title='Year')),
        y = alt.Y('VALUE:Q', axis=alt.Axis(title='Number of People')),
        color = 'Gender:N',
        tooltip = ['Gender:N', 'VALUE:Q']
    ).properties(
        title='Number of Men and Women in Executive Positions in {} Over the Years'.format(prov),
        width=1200,
        height=200
    ).configure_axis(
    labelAngle=0
    )
    return chart.to_dict()


@app.callback(
    Output('bar-chart', 'figure'),
    [Input('year-filter', 'value'),
     Input('province-filter', 'value')]
)
def update_chart(year, province):
    df = pd.read_csv('data/filtered/bar_chart_data.csv')
    # Filter the DataFrame based on selected year and province
    filtered_df = df[(df["REF_DATE"] == year) & (df["GEO"] == province)]

    # Group the filtered DataFrame by 'Type of corporation' and 'Gender' and count occurrences
    grouped_df = filtered_df.groupby(['Type of corporation', 'Gender'])['VALUE'].sum().unstack(fill_value=0)
    
    # Create clustered bar chart with data labels
    data = []
    if 'Men' in grouped_df.columns:
        data.append(go.Bar(x=grouped_df.index, y=grouped_df['Men'], name='Men', text=grouped_df['Men'], textposition='inside'))
    if 'Women' in grouped_df.columns:
        data.append(go.Bar(x=grouped_df.index, y=grouped_df['Women'], name='Women', text=grouped_df['Women'], textposition='inside'))

    layout = go.Layout(barmode='group', title='Distribution by Type of corporation and Gender', xaxis=dict(title='Type of corporation'), yaxis=dict(title='Count'))

    return {'data': data, 'layout': layout}



# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port = 8052)
