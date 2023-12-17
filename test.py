from dash import Dash, html, dash_table, dcc, callback, Output, Input, State, ctx
import dash_ag_grid as dag
import dash_daq as daq
import plotly.express as px
import plotly.graph_objects as go
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

selected_columns = ["energy_use_per_person_2014","sex_ratio_all_age_groups_2022","gini_inegalite_de_repartition_2018"]

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
clusterer = AffinityPropagation()
clustering = clusterer.fit(data_scaler)

# PCA
pca = PCA(n_components=2)

data_pca = pca.fit_transform(data_scaler)

data_pca= pd.DataFrame(data_pca, columns=["PC1","PC2"])
data_pca['cluster_labels'] = clustering.labels_

fig = go.Figure(data=go.Scatter(x=data_pca["PC1"], y=data_pca["PC2"],
    mode="markers",
    marker=dict(color=data_pca["cluster_labels"]),
    text=country,
    hovertemplate="<b>%{text}</b><br><br>" +
                  "Cluster: %{marker.color}<br>" +
                  "<extra></extra>",
    customdata=[region]
#    hover_data=[country,region],
))

# df = px.data.tips()
# fig = px.scatter(data_pca, x="PC1", y="PC2", mode="markers",
#     markers=dict(color=data_pca["cluster_labels"]))
#                 #  title="Total Bill by Sex, Colored by Time")

# PCA 3D

pca3d = PCA(n_components=3)

data_pca_3d = pca3d.fit_transform(data_scaler)

data_pca_3d= pd.DataFrame(data_pca, columns=["PC1","PC2","PC3"])
data_pca_3d['cluster_labels'] = clustering.labels_


t = np.linspace(0, 10, 50)
x, y, z = np.cos(t), np.sin(t), t

fig = go.Figure(data=[go.Scatter3d(x=data_pca_3d["PC1"], y=data_pca_3d["PC2"], z=data_pca_3d["PC3"],
                                   mode='markers')])

fig.layout.update(showlegend=True)
fig.show()

fig.layout.update(showlegend=False)
fig.show()
