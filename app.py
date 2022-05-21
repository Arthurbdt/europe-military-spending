'''
Simple first app where the data from 2022 is displayed on a map
'''

from dash import Dash, dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# ---------- Prepare data for dashboard ----------
data = pd.read_csv('clean_data.csv')

# slider data
labels = data['Year'].unique()
marks = {i: str(labels[i]) for i in range(0, len(labels), 2)}

# dropdown options
dpdn_options = [{'label': 'Percentage of GDP', 'value': 'percent_gdp'},
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
subtitle = dcc.Markdown(children = 'Post Cold War, expressed as percentage of country GDP')
map_europe = dcc.Graph(figure={})
slider = dcc.Slider(min = 0, max = 30, step = None, marks = marks, 
    value = 30, vertical = True, verticalHeight = 550)
bar_chart = dcc.Graph(figure = {})
dropdown = dcc.Dropdown(id = 'my-dpdn', multi = False, value = 'percent_gdp',
    options = dpdn_options)

# ---------- Create dashboard layout ----------
app.layout = dbc.Container([
    dbc.Row([  
        dbc.Col([title], width = 5)
    ], justify = 'left'),

    dbc.Row([  
        dbc.Col([dropdown], width = 3)
    ], justify = 'left'),

    dbc.Row([
        dbc.Col([''], width = 3)
    ], justify = 'left'),

    # graph and slider row
    dbc.Row([
        dbc.Col([slider], width = 1),
        dbc.Col([map_europe], width = 11)
    ], justify = 'center'),
    dbc.Row([
        dbc.Col([bar_chart])
    ])
])

# ---------- Create application callback ----------
@app.callback(
    Output(map_europe, 'figure'),
    Output(bar_chart, 'figure'),
    Input(slider, 'value')
)
def update_graphs(column_name):
    # update europe map
    fig1 = px.choropleth(data_frame = data,
                        locations = 'Country',
                        locationmode = "country names",
                        scope = "europe",
                        height =550,
                        width = 1100,
                        color = marks[column_name],
                        color_continuous_scale='ylgnbu')
    fig1.update_layout(margin=dict(t=10, b=0, l=0, r=0))

    # update bar chart
    fig2 = px.bar(data_frame = data, 
                x = 'Country', 
                y= marks[column_name],
                height = 550)
    fig2.update_layout(xaxis={'categoryorder':'total descending'})

    return fig1, fig2

# Run app
if __name__=='__main__':
    app.run_server(debug=True, port=8054)

