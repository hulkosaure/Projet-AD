à faire (écrire la meme chose que l'onglet présentation je pense)
# Installation des dépendances
Toutes les libraires nécessaire au fonctionnement du dashboard sont répertoriées dans le fichier requirements.txt
Elles peuvent être installées automatiquement avec la commande :  
`pip install-r requirements.txt`

# Dataset

Notre jeu de données est issu de la fusion de plusieurs jeux de données simples téléchargés sur Gapminder. Pour le choix des colonnes, nous avons chacun de notre côté sélectionné plusieurs jeux de données qui nous semblaient intéressants, puis nous avons mis nos choix en commun et procédé à un nettoyage des données. Certaines données n'étaient pas disponibles pour près de la moitié des pays (décès liés à des accidents de voiture), et certains pays ne présentaient que très peu de données par rapport au nombre total de métriques sélectionnées (Vatican, autres exemples de petites iles): dans les deux cas, nous avons fait le choix de supprimer les données.
Les pays ont été attribués à différents régions selon la classification des groupes régionaux des Nations Unies.

L'ensemble des données utilisées est disponible dans le répertoire data.
Détail de chaque métrique
