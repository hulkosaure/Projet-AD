from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_ag_grid as dag
import plotly.express as px
import pandas as pd

# Incorporate data
full_dataset = pd.read_csv('full_dataset.csv')
columns = full_dataset.columns.tolist()
print(full_dataset)

# Initialize the app
app = Dash(__name__)


app.layout = html.Div(
    [   
        html.Div(children='Quoi la fure'),
        html.Hr(),
        html.Label('test'),
        dcc.Dropdown(columns,
                    multi=True),
        dcc.Textarea(id="col1"),
        dcc.Textarea(id="col2"),
        dag.AgGrid(
            id="test",
            columnDefs=[{"field": i} for i in full_dataset.columns],
            rowData=full_dataset.to_dict("records"),
            columnSize="autoSize",
            defaultColDef={"resizable": True, "sortable": True, "filter": True},
            dashGridOptions={"pagination": True}        ),
            dcc.Graph(id="scatterplot"),
    ],
    style={"margin": 20},
)


@callback(
    Output("scatterplot","figure"),
    Input("col1","value"),
    Input("col2","value")
)
def scatter(col1,col2):
    print(col1, col2)
    current_data = full_dataset[["country","region",col1,col2]]
    print(current_data)
    fig = px.scatter(current_data,
    x=col1,
    y=col2,
    color="region",
    hover_data=["country"]
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True)
