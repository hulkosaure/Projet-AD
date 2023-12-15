from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_ag_grid as dag
import plotly.express as px
import pandas as pd


# Incorporate data
full_dataset = pd.read_csv('full_dataset.csv')
full_dataset = full_dataset.loc[:, ~full_dataset.columns.str.contains('^Unnamed')]
columns = full_dataset.columns.tolist()


# Initialize the app
app = Dash(__name__)

app.layout = html.Div(
    [   
        html.Div(children='Quoi le feur'),
        html.Hr(),
        html.Label('test'),
        dcc.Dropdown(columns,
                    multi=True),
        dag.AgGrid(
            id="test",
            columnDefs=[{"field": i} for i in full_dataset.columns],
            rowData=full_dataset.to_dict("records"),
            columnSize="autoSize",
            defaultColDef={"resizable": True, "sortable": True, "filter": True},
            dashGridOptions={"pagination": True}        )
        # dcc.Markdown(
        #     "Auto Page Size example.  Enter grid height in px", style={"marginTop": 100}
        # ),
        # dcc.Input(id="input-height", type="number", min=150, max=1000, value=400),
        # dag.AgGrid(
        #     id="grid-height",
        #     columnDefs=columnDefs,
        #     rowData=df.to_dict("records"),
        #     columnSize="sizeToFit",
        #     defaultColDef={"resizable": True, "sortable": True, "filter": True},
        #     dashGridOptions={"pagination": True, "paginationAutoPageSize": True},
        # ),
    ],
    style={"margin": 20},
)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)



@callback(Output("grid-height", "style"), Input("input-height", "value"))
def update_height(h):
    h = "400px" if h is None else h
    return {"height": h, "width": "100%"}


if __name__ == "__main__":
    app.run(debug=False)
