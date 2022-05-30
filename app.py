'''
Simple first app where the data from 2022 is displayed on a map
'''

from dash import Dash, dcc, Output, Input
import dash_bootstrap_components as dbc
from matplotlib.pyplot import figimage
import plotly.express as px
import pandas as pd

# ---------- Prepare data for dashboard ----------
data = pd.read_csv('clean_data.csv')

# slider data
labels = data['Year'].unique()
marks = {i: str(labels[i]) for i in range(0, len(labels), 2)}

# create measures options for dropdown menu
dropdown_options = [{'label': 'Percentage of GDP', 'value': 'percent_gdp'},
                    {'label': 'US dollars per capita', 'value': 'usd_per_capita'},
                    {'label': 'US dollars', 'value': 'usd'}]

# ---------- Create dashboard components ----------
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
title = dcc.Markdown(
    children = 
        '''  
        # European military spending

        [Source: SIPRI Military Expenditure Database](https://www.sipri.org/databases/milex)

        Here will be the explanation of all possible dropdown options:
        - *Percentage of GDP*: lorem ipsum et spiritus sancta
        - *US dollars per capita*: nove sed non-nova
        - *US dollars: constant dollar*: insert definition
        '''
        )

# generate empty figures
map_europe = dcc.Graph(figure={})
time_series = dcc.Graph(figure = {})

# generate slider and dropdown menu
year_slider = dcc.Slider(min = 0, max = 30, step = None, 
                    marks = marks, value = 30, 
                    vertical = True, verticalHeight = 550)
measure_dropdown = dcc.Dropdown(id = 'my-dpdn', multi = False, 
                                value = 'percent_gdp', options = dropdown_options)

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
    Output(map_europe, 'figure'),
    Input(year_slider, 'value')
)
def update_map(period):
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
                        color = 'Pct_gdp',
                        color_continuous_scale='ylgnbu')
    fig.update_layout(margin=dict(t=10, b=0, l=0, r=0))
    return fig

@app.callback(
    Output(time_series, 'figure'),
    Input(map_europe, 'clickData')
)
def update_ts(input):
    # calculate something
    area = input['points'][0]['location']
    sample = data[data['Country']==area]

    # update chart
    fig = px.line(data_frame = sample, 
                x = 'Year', 
                y = 'Pct_gdp',
                color = 'Country',
                height = 550)

    # return graph
    return fig

# Run app
if __name__=='__main__':
    app.run_server(debug=True, port=8054)

