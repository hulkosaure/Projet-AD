# Présentation
blabla dashboard projet analyse de données python pedro adrifeur blabla

# Installation des dépendances et mise en route
Toutes les libraires nécessaires au fonctionnement du dashboard sont répertoriées dans le fichier requirements.txt
Elles peuvent être installées automatiquement avec la commande :  
`pip install -r requirements.txt`

Le dashboard est lancé avec la ligne de commande `python app.py` ou `python3 app.py` et est accessible à l'adresse affichée dans la console (ex: http://127.0.0.1:8050/)

# Dataset  
Notre jeu de données est issu de la fusion de plusieurs jeux de données simples téléchargés sur Gapminder.  
Pour le choix des colonnes, nous avons chacun de notre côté sélectionné plusieurs jeux de données qui nous semblaient intéressants, puis nous avons mis nos choix en commun et procédé à un nettoyage des données. Certaines données n'étaient pas disponibles pour près de la moitié des pays (décès liés à des accidents de voiture), et certains pays ne présentaient que très peu de données par rapport au nombre total de métriques sélectionnées (Vatican, autres exemples de petites iles): dans les deux cas, nous avons fait le choix de supprimer les données.  
Les pays ont été attribués à différents régions selon la classification des groupes régionaux des Nations Unies.

L'ensemble des données utilisées est disponible dans le répertoire data.  
Détail de chaque métrique
