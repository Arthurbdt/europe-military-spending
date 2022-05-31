'''
Simple first app where the data from 2022 is displayed on a map
'''

from dash import Dash, dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# ---------- Prepare data for dashboard ----------
data = pd.read_csv('.\datasets\clean_data.csv')

# slider data
labels = data['Year'].unique()
marks = {i: str(labels[i]) for i in range(0, len(labels), 2)}

# create measures options for dropdown menu
dropdown_options = [{'label': 'Percentage of GDP', 'value': 'Percent_gdp'},
                    {'label': 'US dollars (2021)', 'value': '2021_usd'},
                    {'label': 'US dollars (2021) per capita', 'value': '2021_usd_per_capita'}]

# ---------- Create dashboard components ----------
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
title = dcc.Markdown(
    children = 
        '''  
        # European military spending

        [Source: SIPRI Military Expenditure Database](https://www.sipri.org/databases/milex)

        Here will be the explanation of all possible dropdown options:
        - *Percentage of GDP*: tbd
        - *US dollars (2021) per capita*: tbd
        - *US dollars (2021):*: tbd
        '''
        )

# generate empty figures
map_europe = dcc.Graph(figure={})
time_series = dcc.Graph(figure = {})

# generate slider and dropdown menu
year_slider = dcc.Slider(min = 0, max = 30, step = None, 
                    marks = marks, value = 30, 
                    vertical = True, verticalHeight = 550)
measure_dropdown = dcc.Dropdown(id = 'my-dpdn', multi = False, clearable = False, 
                                value = 'Percent_gdp', options = dropdown_options)

# ---------- Create dashboard layout ----------
app.layout = dbc.Container([
    dbc.Row([  
        dbc.Col([title], width = 5)
    ], justify = 'left'),

    dbc.Row([  
        dbc.Col([measure_dropdown], width = 3)
    ], justify = 'left'),

    dbc.Row([
        dbc.Col([''], width = 3)
    ], justify = 'left'),

    # graph and slider row
    dbc.Row([
        dbc.Col([year_slider], width = 1),
        dbc.Col([map_europe], width = 11)
    ], justify = 'center'),
    dbc.Row([
        dbc.Col([time_series])
    ])
])

# ---------- Create application callback ----------
@app.callback(
    Output(map_europe, 'figure'),       # update map of europe
    Input(year_slider, 'value'),        # year selected on slider
    Input(measure_dropdown, 'value')    # measure selected on dropdown menu
)
def update_map(period, measure):
    # select sample of data
    target_year = int(marks[period])
    sample = data[data['Year'] == target_year]

    # update color map
    fig = px.choropleth(data_frame = sample,
                        locations = 'Country',
                        locationmode = "country names",
                        scope = "europe",
                        height =550,
                        width = 1100,
                        color = measure,
                        color_continuous_scale='ylgnbu')
    fig.update_layout(margin=dict(t=10, b=0, l=0, r=0))
    return fig

@app.callback(
    Output(time_series, 'figure'),      # update time series chart
    Input(map_europe, 'clickData'),     # country selected on map
    Input(measure_dropdown, 'value')    # measure selected on dropdown menu  
)
def update_ts(click, measure):
    if click:
        # calculate something
        area = click['points'][0]['location']
        sample = data[data['Country']==area]
    else:
        sample = data
    # update chart
    fig = px.line(data_frame = sample, 
                x = 'Year', 
                y = measure,
                color = 'Country',
                height = 550)

    # return graph
    return fig

# Run app
if __name__=='__main__':
    app.run_server(debug=True, port=8054)

