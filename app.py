'''
Author: @Arthurbdt
Web-app visualizing european militray spending since the end of the Cold War.
App built with Dash, data from SIPRI
'''

from dash import Dash, dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# ---------- Prepare data for dashboard ----------
data = pd.read_csv('.\datasets\clean_data.csv')

# slider data
labels_year = data['Year'].unique()
marks = {i: str(labels_year[i]) for i in range(0, len(labels_year), 2)}

# create measures options for dropdown menu
dropdown_options = [{'label': 'Percentage of GDP', 'value': 'Percent_gdp'},
                    {'label': 'Constant US dollars', 'value': 'constant_usd'},
                    {'label': 'US dollars per capita', 'value': 'usd_per_capita'}]

# ---------- Create dashboard components ----------
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
title = dcc.Markdown(
    children = 
        '''  
        # European military spending

        [Source: SIPRI Military Expenditure Database](https://www.sipri.org/databases/milex)

        This web application visualizes the military spending of European countries since the end of the Cold War through
        three variables:
        - **Percentage of GDP:** percentage of gross domestic product allocated to military spending
        - **US dollars:** military expenditure (in $Bn) expressed in constant dollars of 2020
        - **US dollars per capita:** current dollars per country inhabitant allocated to military spending 

        Select the measure of interest in the dropdown menu to update all figures. You can visualize the evolution
        of military spending over time by changing dates on the slider. Clicking on a country will filter out all
        other countries on the time series chart.

        You can select one or multiple countries on the time series chart using the legend on the left hand side.
        '''
        )

# generate empty figures
map_europe = dcc.Graph(figure={})
time_series = dcc.Graph(figure = {})

# generate slider, dropdown
year_slider = dcc.Slider(min = 0, max = 30, step = None, 
                    marks = marks, value = 30, 
                    vertical = True, verticalHeight = 580)
measure_dropdown = dcc.Dropdown(id = 'my-dpdn', multi = False, clearable = False, 
                                value = 'Percent_gdp', options = dropdown_options)

# ---------- Create dashboard layout ----------
app.layout = dbc.Container([
    dbc.Row([  
        dbc.Col([title], width = 10)
    ], justify = 'left'),

    dbc.Row([  
        dbc.Col([measure_dropdown], width = 3)
    ], justify = 'left'),   
    # graph and slider row
    dbc.Row([
        dbc.Col([year_slider], width = 1),
        dbc.Col([map_europe], width = 11)
    ], justify = 'left', align = 'center'),
    # radio items and time series
    dbc.Row([
        dbc.Col([time_series], width = 12)
    ], align = 'center')
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
                        height = 580,
                        width = 1100,
                        color = measure,
                        color_continuous_scale='ylgnbu')
    fig.update_layout(margin=dict(t=10, b=0, l=0, r=0))
    fig.update_geos(fitbounds="locations")
    return fig

@app.callback(
    Output(time_series, 'figure'),      # update time series chart
    Input(map_europe, 'clickData'),     # country selected on map
    Input(measure_dropdown, 'value')   # measure selected on dropdown menu
)
def update_ts(click, measure):
    if click:
        # restrict dataset to selected country
        area = click['points'][0]['location']
        sample = data[data['Country']==area]
    else:
        # plot all countries
        sample = data
    # update chart
    fig = px.line(data_frame = sample, x = 'Year', y = measure, 
                 color = 'Country', height = 500, template = 'simple_white')
    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)
    # add NATO guidelines for percentage of gdp
    if measure == 'Percent_gdp':
        fig.add_shape(type = 'line', line_color = 'red', line_width = 3,
            y0 = 2.0, y1 = 2.0, x0 = '1991', x1 = '2021', yref = 'y')
    # return graph
    return fig

# Run app
if __name__=='__main__':
    app.run_server(debug=True, port=8054)


