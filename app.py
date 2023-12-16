from dash import Dash, html, dash_table, dcc, callback, Output, Input, State, ctx
import dash_ag_grid as dag
import plotly.express as px
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN,AffinityPropagation
from sklearn.decomposition import PCA


# Incorporate data
full_dataset = pd.read_csv('data/full_dataset.csv')
columns = full_dataset.columns.tolist()

# Clean the data
def convertir_number(x):
    if isinstance(x,str) and 'µ' in x:
        return float(x.replace('µ','')) * 1e-6
    elif isinstance(x,str) and 'k' in x:
        return float(x.replace('k','')) * 1e3
    else:
        return float(x)

full_dataset.loc[:, full_dataset.columns.difference(['country', 'region'])] = full_dataset.loc[:, full_dataset.columns.difference(['country', 'region'])].applymap(convertir_number)

# Initialize the app
app = Dash(__name__)


app.layout = html.Div(
    [   
        html.H1("Étude de différentes métriques sur les pays"),
        dcc.Tabs(id="general_tabs", value="t1", children=[
            dcc.Tab(label="Présentation", value="t1", children=[
                html.Div(children="présentation (à faire)")
            ]),
            dcc.Tab(label="Analyse", value="t2", children=[
                html.Label('Sélectionnez les colonnes à afficher :'),
                dcc.Dropdown(
                id='column-dropdown',
                options=[{'label': col, 'value': col} for col in full_dataset.columns],
                multi=True,
                value=full_dataset.columns,
                ),
                html.Button('Mettre à jour', id='update-button', n_clicks=0), 
                html.Button('Réinitialiser', id='reset-button', n_clicks=0),
                dag.AgGrid(
                    id="test",
                    columnDefs=[{"field": i} for i in full_dataset.columns],
                    rowData=full_dataset.to_dict("records"),
                    columnSize="autoSize",
                    defaultColDef={"resizable": True, "sortable": True, "filter": True},
                    dashGridOptions={"pagination": False},
                    style={"height": 265}),
                html.Hr(),
                dcc.Tabs(id="which_plot", value="scatter", children=[
                    dcc.Tab(label="Nuage de point entre deux métriques",id="scatter", children=[
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.Label('Abscisses:'),
                                        dcc.Dropdown(
                                            id='plot_x',
                                            options=[{'label': col, 'value': col} for col in full_dataset.columns],
                                        ),
                                    ],
                                    style={'flex': '50%', 'padding': '5px'}
                                ),
                                html.Div(
                                    [
                                        html.Label('Ordonnées:'),
                                        dcc.Dropdown(
                                            id='plot_y',
                                            options=[{'label': col, 'value': col} for col in full_dataset.columns],
                                        ),
                                    ],
                                    style={'flex': '50%', 'padding': '5px'}
                                ),
                            ],
                            style={'display': 'flex'}
                        ),
                        dcc.Graph(id="scatterplot"),
                    ]),
                    dcc.Tab(label="Clustering et ACP",id="cluster",children=[
                        dcc.RadioItems(
                            id = "clusteringmethod",
                            options=['AffinityPropagation','DBSCAN'], # regler dbscan probleme, pas de cluster = -1 donc mettre couleur noir si possible
                            value='AffinityPropagation',
                            inline=True),
                        dcc.Graph(id="clusterplot"),  # regler problem, need country et region to clusteriser
                    ])
                ]),
            ])
        ]),

    ],
    style={"margin": 20},
)

@callback(
    Output('test', 'columnDefs'),
    Output('test', 'rowData'),
    Output('column-dropdown', 'value'),
    Input('update-button', 'n_clicks'),
    Input('reset-button', 'n_clicks'),
    State('column-dropdown', 'value')
)

def update_data(update_clicks, reset_clicks, selected_columns):
    changed_id = [p['prop_id'] for p in ctx.triggered][0]
    if 'reset-button' in changed_id and reset_clicks > 0:
        updated_column_defs = [{"field": i} for i in full_dataset.columns]
        updated_data = full_dataset.to_dict('records')
        dropdown_value = full_dataset.columns 
    else:
        updated_column_defs = [{"field": col} for col in selected_columns]
        updated_data = full_dataset[selected_columns].to_dict('records')
        dropdown_value = selected_columns
    return updated_column_defs, updated_data, dropdown_value

@callback(
    Output("scatterplot", "figure"),
    Input("plot_x", "value"),
    Input("plot_y", "value")
)
def scatter(plot_x, plot_y):
    if plot_x and plot_y: 
        fig = px.scatter(
            full_dataset,
            x=plot_x,
            y=plot_y,
            color='region', 
            hover_data=[col for col in full_dataset.columns if col not in (plot_x, plot_y)]
        )
        return fig
    else:
        return {}


@callback(
    Output("clusterplot", "figure"),
    Input("clusteringmethod","value"),
    Input("test","rowData")
)
def cluster_and_represent(cmethod, data):
    data = pd.DataFrame.from_dict(data).dropna()
    scaler = StandardScaler()
    data_scaler = scaler.fit_transform(data.drop(["country","region"], axis=1))
    clusterer = DBSCAN() if cmethod=="DBSCAN" else AffinityPropagation()
    clustering = clusterer.fit(data_scaler)
    pca = PCA(n_components=2)
    data_pca = pca.fit_transform(data_scaler)
    fig = px.scatter(data_pca,
    color=clustering.labels_,
    hover_data=[data["country"],data["region"]]
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True)
