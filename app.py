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
marks = {i: str(labels[i]) for i in range(0, len(labels), 2)}

# ---------- Create dashboard components ----------
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
title = dcc.Markdown(children = '# Military spending of European countries post Cold War')
subtitle = dcc.Markdown(children = 'Expressed as percentage of country GDP')
graph = dcc.Graph(figure={})
slider = dcc.Slider(0, 30, step = None, marks = marks, value = 30)

# ---------- Create dashboard layout ----------
app.layout = dbc.Container([title, subtitle, graph, slider])

# ---------- Create application callback ----------
@app.callback(
    Output(graph, 'figure'),
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
                        height=600,
                        color=marks[column_name],
                        color_continuous_scale='ylgnbu')
    return fig

# Run app
if __name__=='__main__':
    app.run_server(debug=True, port=8054)

