from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd


# Incorporate data
full_dataset = pd.read_csv('full_dataset.csv')



# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data, Graph, and Controls'),
    html.Hr(),
    dash_table.DataTable(data=full_dataset.to_dict("records"), page_size=300),
])

# Add controls to build the interaction
# @callback(
#     Output(component_id='controls-and-graph', component_property='figure'),
#     Input(component_id='controls-and-radio-item', component_property='value')
# )
# def update_graph(col_chosen):
#     fig = px.histogram(songs, x='year', y=col_chosen, histfunc='avg')
#     return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)