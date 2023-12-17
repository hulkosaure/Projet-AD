from dash import Dash, html, dash_table, dcc, callback, Output, Input, State, ctx
import dash_ag_grid as dag
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
import matplotlib as plt
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN,AffinityPropagation
from sklearn.decomposition import PCA


# Incorporate data
full_dataset = pd.read_csv('data/full_dataset.csv')
columns = full_dataset.columns.tolist()
numeric_columns = columns.copy()
numeric_columns.remove("country")
numeric_columns.remove("region")

# Clean the data
def convertir_number(x):
    if isinstance(x,str) and 'µ' in x:
        return float(x.replace('µ','')) * 1e-6
    elif isinstance(x,str) and 'k' in x:
        return float(x.replace('k','')) * 1e3
    else:
        return float(x)

full_dataset.loc[:, full_dataset.columns.difference(['country', 'region'])] = full_dataset.loc[:, full_dataset.columns.difference(['country', 'region'])].applymap(convertir_number)
# retrait manuel d'une valeur aberrante
full_dataset.loc[full_dataset['country'] == 'Georgia', 'consumption_emission_cap_2022'] = np.nan
with open('README.md', 'r', encoding='utf-8') as file:
    readme = file.read()

# Initialize the app
app = Dash(__name__)


app.layout = html.Div(
    [   
        html.H1("Étude de différentes métriques sur les pays"),
        dcc.Tabs(id="general_tabs", value="t1", children=[
            dcc.Tab(label="Présentation", value="t1", children=[
                dcc.Markdown(children=readme)
            ]),
            dcc.Tab(label="Analyse", value="t2", children=[
                html.Label('Sélectionnez les colonnes à afficher :'),
                dcc.Dropdown(
                    id='column-dropdown',
                    options=[{'label': col, 'value': col} for col in numeric_columns],
                    multi=True,
                    value=numeric_columns,
                ),
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
                                            value = "revenu_moyen_menage_2022",
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
                                            value = "child_mortality_0_5_year_olds_dying_per_1000_born_2022",
                                            options=[{'label': col, 'value': col} for col in full_dataset.columns],
                                        ),
                                    ],
                                    style={'flex': '50%', 'padding': '5px'}
                                ),
                            ],
                            style={'display': 'flex'}
                        ),
                        html.Label(id='selected_columns_label'),
                        dcc.Graph(id="scatterplot"),
                    ]),
                    dcc.Tab(label="Clustering et ACP",id="cluster",children=[
                        html.Label('Selectionner les colonnes voulus pour le clustering puis l\'ACP :'),
                        dcc.Dropdown(
                            id='analysed_data',
                            options=[{'label': col, 'value': col} for col in numeric_columns],
                            multi=True,
                            value=numeric_columns
                            ),
                        html.Label('Méthode de clustering :'),
                        dcc.RadioItems(
                            id = "clusteringmethod",
                            options=['AffinityPropagation','DBSCAN'], # regler dbscan probleme, pas de cluster = -1 donc mettre couleur noir si possible
                            value='AffinityPropagation',
                            inline=True),
                        html.Div(id="dbscan_parameters", children=[
                            daq.NumericInput(id="esp",
                                value = 0.5,
                                size = 60,
                                min = 0,
                                max = 50,
                                label = "Distance maximum entre deux points pour être considéré comme voisin (float)"),
                            daq.NumericInput(id="min_samples",
                                value = 5,
                                size = 60,
                                min = 1,
                                max = 50,
                                label = "Nombre minumum de point par cluster (int)")
                        ]),
                        dcc.Graph(id="clusterplot"),
                        dcc.Graph(id="clusterplot3d"),
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
    Input('reset-button', 'n_clicks'),
    Input('column-dropdown', 'value')
)

def update_data(reset_clicks, selected_columns):
    
    # Ajout des colonnes 'country' et 'region' en premier dans la sélection
    selected_columns = list(set(selected_columns + ['country', 'region']))
    
    changed_id = [p['prop_id'] for p in ctx.triggered][0]
    if 'reset-button' in changed_id and reset_clicks > 0:
        updated_column_defs = [{"field": i} for i in full_dataset.columns]
        updated_data = full_dataset.to_dict('records')
        dropdown_value = full_dataset.columns 
    else:
        updated_column_defs = [{"field": col} for col in selected_columns]
        updated_data = full_dataset[selected_columns].to_dict('records')
        dropdown_value = selected_columns
    
    updated_column_defs.sort(key=lambda x: 1 if x['field'] in ['country', 'region'] else 0, reverse=True)
    
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


# Function to convert group numbers to RGBA colors (with alpha=0.3 for -1)
def group_to_rgba(group):
    maxgroup = group.max()
    mingroup = group.min()
    lengroup = maxgroup-mingroup
    normalize_group = group.apply(lambda x : ((x-mingroup)/lengroup))
    color_group = normalize_group.apply(plt.cm.get_cmap("viridis"))
    to_opacify= (group == -1)
    color_group.loc[to_opacify] = color_group.loc[to_opacify].apply(lambda x: (x[0], x[1], x[2], 0.3))
    return color_group

@callback(
    Output('selected_columns_label', 'children'),
    Input("plot_x", "value"),
    Input("plot_y", "value")
)


def title(plot_x, plot_y):
    dico = {
        "country" : "Pays",
        "region" : "Région",
        "co2_emissions_tonnes_per_person_2018" : "Émissions de carbone",
        "consumption_emission_cap_2022" : "Émissions liées à la consommation par habitant",
        "corruption_perception_index_cpi_2017" : "Indice de perception de la corruption",
        "energy_production_per_person_2009" : "Région",
        "energy_use_per_person_2014" : "Utilisation d'énergie par habitant",
        "forest_coverage_percent_2019" : "Surface occupée par des forêts",
        "gini_inegalite_de_repartition_2018" : "Inégalités de répartitions",
        "hdi_human_development_index_2021" : "Indice de développement humain",
        "menace_changement_climatique_2021" : "Changement climatique évalué comme une menace",
        "percentage_women_in_national_parliaments_2021" : "Région",
        "personal_computers_per_100_people_2005" : "Nombre d'ordinateurs personnels pour 100 personnes",
        "revenu_moyen_menage_2022" : "Revenu moyen des ménages",
        "sex_ratio_all_age_groups_2022" : "Nombre d'hommes pour 100 femmes",
        "sustainable_developement_index_2019" : "Indice de développement durable",
        "child_mortality_0_5_year_olds_dying_per_1000_born_2022" : "Mortalité infantile pour 1000 naissances",    

    }
    selected_columns = f"{dico[plot_y]} en fonction de {dico[plot_x]}"
    return selected_columns


@callback(
    Output("clusterplot", "figure"),
    Output("clusterplot3d","figure"),
    Input("clusteringmethod","value"),
    Input("esp","value"),
    Input("min_samples","value"),
    Input("analysed_data", "value")
)
def cluster_and_represent(cmethod, esp, min_samples, selected_columns):

    # Select wanted data
    selected_columns_extended = list(set(selected_columns + ['country', 'region']))
    data_selected = full_dataset[selected_columns_extended].dropna()

    # Get country and region vector for hover data later
    country = data_selected["country"]
    region = data_selected["region"]

    # Get only numerical data
    data_selected = data_selected[selected_columns]

    # Normalize
    scaler = StandardScaler()
    data_scaler = scaler.fit_transform(data_selected)

    # Clustering
    clusterer = DBSCAN(eps = esp, min_samples = min_samples) if cmethod=="DBSCAN" else AffinityPropagation()
    clustering = clusterer.fit(data_scaler)

    transparency = [0.15 if label == -1 else 1 for label in clustering.labels_]

    # PCA
    pca = PCA(n_components=2)
    pca3d = PCA(n_components=3)
    data_pca = pca.fit_transform(data_scaler)
    data_pca_3d = pca3d.fit_transform(data_scaler)

    data_pca= pd.DataFrame(data_pca, columns=["PC1","PC2"])
    data_pca['cluster_labels'] = clustering.labels_
    data_pca["transparency"] = transparency

    data_pca_3d= pd.DataFrame(data_pca_3d, columns=["PC1","PC2","PC3"])
    data_pca_3d['cluster_labels'] = clustering.labels_
    data_pca_3d["color"] = group_to_rgba(data_pca_3d["cluster_labels"])

    # Plots
    fig = go.Figure(data=go.Scatter(x=data_pca["PC1"], y=data_pca["PC2"],
        mode="markers",
        marker=dict(color=data_pca["cluster_labels"],
                    opacity=data_pca["transparency"]),
        text=country,
        hovertemplate="<b>%{text}</b><br><br>" +
                    "Cluster: %{marker.color}<br>" +
                    "<extra></extra>",
    ))
    z1, z2, z3 = np.random.random((3, len(clustering.labels_), 1))
    fig3d = go.Figure(data=[go.Scatter3d(x=data_pca_3d["PC1"], y=data_pca_3d["PC2"], z=data_pca_3d["PC3"],
        mode="markers",
        marker=dict(color=data_pca_3d["color"]),
        text=country,
        customdata=clustering.labels_,
        hovertemplate="<b>%{text}</b><br><br>" +
                    "Cluster: %{customdata}<br>" +
                    "<extra></extra>",
    )])
    fig.update_layout(showlegend=False,
        xaxis_title="Première composante",
        yaxis_title="Seconde composante",
        title="Visualisation des axes de l'ACP à 2 dimensions (variance expliquée : "+str(pca.explained_variance_ratio_.sum()*100)+")")
    fig3d.update_layout(showlegend=False,
        scene = dict(
                    xaxis_title='Première composante',
                    yaxis_title='Deuxième composante',
                    zaxis_title='Troisième composante'),
        title="Visualisation des axes de l'ACP à 3 dimensions (variance expliquée : "+str(pca3d.explained_variance_ratio_.sum()*100)+")")
    return fig, fig3d


@callback(
    Output("dbscan_parameters","style"),
    Input("clusteringmethod","value")
)
def display_dbscan_param(clusteringmethod):
    """
    Afficher le choix des paramètres pour DBSCAN si DBSCAN est la méthode choisit.
    """
    if clusteringmethod == "DBSCAN":
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@callback(
    Output("min_samples","value"),
    Input("min_samples","value")
)
def check_int_value(val):
    """
    Vérifie si la valeur mise pour min_samples (DBSCAN) est entière.
        S'il est possible de la convertir, la convertit, sinon remet la valeur par défaut (5)
    """
    try:
        int_value = int(val)
        return int_value
    except ValueError:
        return 5  # si la valeur mise n'est pas un entier, alors la valeur par défaut 5 est mise


if __name__ == "__main__":
    app.run(debug=True)
