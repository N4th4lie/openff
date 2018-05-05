README.md

Auteur 	 : N4th4lie

Création : 15/04/2018

Dernière version : 05/05/2018

------------------------------------------------------
Recherche d'aliments dans la base Open Food Facts (FR)
------------------------------------------------------

Principe : 
l'application interagit avec la base Open Food Facts FR 
pour en récupérer des aliments, les comparer et pour,
considérant un aliment donné, en proposer un substitut plus sain.

Fonctionnalités :

l'utilisateur est sur le terminal Python.
Ce dernier lui propose le menu suivant :
 1. Choisir un aliment de départ et obtenir un aliment de substitution.
 2. Consulter l'historique i.e. retrouver les substitutions enregistrées.

Contenu :
 - présentation README.md
 - categories.csv (un jeu de catégories Open Food Facts sélectionnées)
 - répertoire data_categ (les produits en format json, téléchargés par catégorie)
 - fichiers csv extraits des json de data_categ :
   products.csv, cat_prod.csv
 - code création de la base de données :
   urlrequest_categories.py, read_products.py, load_data_in_openff.py
 - code du programme :
   openff.py, classes.py, constants.py, myconnutils.py
 - requirements.txt (déploiement de l'application)

To install and execute this program, you need to follow these steps:
1. git clone https://github.com/n4th4lie/openff.git && cd openff
2. python3 openff.py on macos/linux or py -3 openff.py on windows

If the dependencies are not installed, a virtual environment is automatically
created with the needed requirements installed inside.
