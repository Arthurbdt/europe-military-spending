'''
Simple first app where the data from 2022 is displayed on a map
'''

from dash import Dash, dcc, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

# ---------- Prepare data for dashboard ----------
data = pd.read_csv('europe_spending.csv')
# slider data
labels = data.columns.values[2:]
fig2 = px.line(data_frame = data, x = 'Country', y= '2021')
marks = {i: str(labels[i]) for i in range(0, len(labels), 2)}

# ---------- Create dashboard components ----------
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
title = dcc.Markdown(
    children = 
        '''  
        ### European military spending

        [Source: SIPRI Military Expenditure Database](https://www.sipri.org/databases/milex)
        '''
        )
subtitle = dcc.Markdown(children = 'Post Cold War, expressed as percentage of country GDP')
map_europe = dcc.Graph(figure={})
slider = dcc.Slider(min = 0, max = 30, step = None, marks = marks, 
    value = 30, vertical = True, verticalHeight = 600)
line_chart = dcc.Graph(figure = fig2)

# ---------- Create dashboard layout ----------
'''
format for layout
dbc.Container()
dbc.Row()
dbc.Col()
'''
app.layout = dbc.Container([
    dbc.Row([  
        dbc.Col([title], width = 5)
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
        dbc.Col([line_chart])
    ])
])

# ---------- Create application callback ----------
@app.callback(
    Output(map_europe, 'figure'),
    Input(slider, 'value')
)
def update_graph(column_name):
    # viridis
    # plasma
    # pubu
    fig = px.choropleth(data_frame = data,
                        locations = 'Country',
                        locationmode = "country names",
                        scope = "europe",
                        height =600,
                        width = 1100,
                        color = marks[column_name],
                        color_continuous_scale='ylgnbu')
    fig.update_layout(margin=dict(t=10, b=0, l=0, r=0))
    return fig

# Run app
if __name__=='__main__':
    app.run_server(debug=True, port=8054)

