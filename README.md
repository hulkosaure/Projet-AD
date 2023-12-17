# Présentation
Ce dashboard a été conçu dans le cadre d'un projet pour l'UE Analyse de Données du master 2 de bioinformatique à l'université Claude Bernard Lyon 1.
Il permet de visualiser le jeu de données sous la forme d'un tableau, et de nuages de points. Une recherche de clusters peut être effectuées sur une sélection de données choisies par l'utilisateur, et les résultats peuvent être observés à l'aide d'une analyse en composantes principales.  


# Installation des dépendances et mise en route
Toutes les libraires nécessaires au fonctionnement du dashboard sont répertoriées dans le fichier requirements.txt.  
Elles peuvent être installées automatiquement avec la commande :  
`pip install -r requirements.txt`

Le dashboard est lancé avec la ligne de commande `python app.py` ou `python3 app.py` et est accessible à l'adresse affichée dans la console (ex: http://127.0.0.1:8050/).

# Explication du dashboard

L'onglet `Analyse` permet de visualiser les données. L'utilisateur peut choisir les colonnes à afficher ou les masquer dans le cadre situé au dessus du tableau de données.  
L'onglet `Nuage de points entre deux métriques`, situé en dessous du tableau de données permet de choisir librement deux colonnes du tableau pour créer un nuage de points. Les points sont colorés en fonction de la région du pays selon les groupes régionaux des Nations Unies.  
L'onglet `Clustering et ACP` permet à l'utilisateur de sélectionner plusieurs colonnes de son choix et d'appliquer une méthode de clustering entre `AffinityPropagation` et `DBSCAN`, en choisissant les paramètres pour `DBSCAN`. Une ACP est ensuite effectuée sur les résultats pour permettre une visualisation dans l'espace des clusters détectés.  

# Dataset  
Notre jeu de données est issu de la fusion de plusieurs jeux de données simples téléchargés sur Gapminder.
Pour le choix des colonnes, nous avons chacun de notre côté sélectionné plusieurs jeux de données qui nous semblaient intéressants, puis nous avons mis nos choix en commun et procédé à un nettoyage des données. Certaines données n'étaient pas disponibles pour près de la moitié des pays (décès liés à des accidents de voiture), et certains pays ne présentaient que très peu de données par rapport au nombre total de métriques sélectionnées (Vatican, autres exemples de petites iles): dans les deux cas, nous avons fait le choix de supprimer les données.  
Les pays ont été attribués à différents régions selon la classification des groupes régionaux des Nations Unies.

L'ensemble des données utilisées est disponible dans le répertoire data.  
Détail de chaque métrique :   
**Country** : Nom du pays.  
**Region** : Groupe d'appartenance dans la classification des groupes régionaux des Nations Unies.  
**personal_computers_per_100_people** : Nombre d'ordinateurs par personne (2005).  
**consumption_emission_cap** : Les émissions de consommation pour un pays divisées par sa population en tonnes de CO2 par habitant.  
**menace_changement_climatique** : Part de la population qui considèrent le changement climatique comme véritablement dangereux.  
**child_mortality_0_5_year_olds_dying_per_1000_born** : Mortalité infantile pour 1000 naissances (2022).  
**forest_coverage_percent** : Part du territoire national occupée par des forêts.  
**corruption_perception_index_cpi** : Indice de perception de la corruption  dans le secteur public (Transparency International).  
**energy_production_per_person**: Productions des différentes formes d'énergie primaire et d'électricité primaire converties en tonnes équivalent pétrole.  
**energy_use_per_person** : Utilisation d'énergie par habitant dans un pays.  
**hdi_human_development_index** : Indice de développement humain du pays.  
**percentage_women_in_national_parliaments** : Pourcentage de sièges occupés par des femmes au parlement national.  
**sex_ratio_all_age_groups** : Nomnbre d'hommes pour 100 femmes, en prenant en compte toutes les tranches d'âge d'une population.  
**gini_inegalite_de_repartition** : Indice de Gini, quantifie ici les inégalités de répartition des richesses. Il s'échelonne de 0 (égalité parfaite) à 1 (inégalités extrêmes).   
**sustainable_developement_index** : Indice de développement durable. Il présente l'efficacité mesurée d'un pays à promouvoir le développement humain de manière écologique. Il est calculé comme le rapport entre l'indice de développement humain et l'impact écologique (écart à la consommation personnelle théorique en fonction de la production annuelle de ressources de la planète).   
**co2_emissions_tonnes_per_person** : Émissions de carbone dues à la combustion d'énergies fossiles.  
**revenu_moyen_menage** : Revenu moyen d'un ménage (2022).  

La compilation des données brutes de Gapminder et une partie du preprocessing est disponible dans le jupyter notebook [`./make_full_dataset.ipynb`](./make_full_dataset.ipynb).













