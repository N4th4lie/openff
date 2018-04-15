# -*- coding: utf-8 -*-

"""
Created on Wed Apr 11 21:15:15 2018
@author: N4th4lie

read_products.py

Lire les 1819 produits des 32 catégories sélectionnées
soit 32 pages JSON d'Openfoodfacts FR, les categXX.json,
dans Projet05\DATA\DATA_CATEG.

Remarque :
--------    
En chargeant les produits catégorie par catégorie, on peut se retrouver
avec le même produit dans plusieurs catégories. Par exemple :
le produit "3596710359431" est dans les catégories "10" et "13"
(pizzerias au jambon et pizzerias ovales).

>> Créer un dictionnaire product_res (sans doublon),
c'est ce dictionnaire qui au final sera écrit dans products.csv

1) Créer products_res = { key=code produit: value=dictionnaire des champs }
   Ouvrie en écriture le fichier cat_prod.csv
   Boucler sur les json:
     1.1. Stocker les données du fichier JSON dans un dictionnaire python.
     1.2. Filtrer les produits du dictionaire précédent :
    - sur ceux qui ont un score nutritionnel et les copier avec les variables 
      intéressantes (descriptif_json_OFF.txt) dans un CSV pour la furure BDD
    - ajouter la condition suivante pour la catégorie du NUTELLA
      ("cocoa-and-hazelnuts-spreads" in "categories_tags") :
          score nutritionnel dans ('a','b','e') 
          et pour les E "pot" in packaging"
     1.3. Si filtre ok, ajouter le produit au dictionnaire products_res.
2) Copier le dictionnaire products_res dans products.csv
   
Résultat : on part des 1819 produits dans les json par catégorie (32) 
  >> products.csv : 1470 produits (sans doublon) avec score nutritionnel 
              et filtre spécifique pour les produits de type Nutella.
  >> cat_prod.csv : les 1504 produits avec score nutritionnel par catégorie
                    (avec doublons sur code produit)
              
STRUCTURE DE LA TABLE products :   
    "id (code)","score (nutrition_grades)","url","label (product_name_fr)","gen_label (generic_name_fr)",
    "quantity","packaging","brand (brands)","link","store (stores_tags)"
STRUCTURE DE LA TABLE cat_prod : 
    "category (code)","product (code)","score (nutrition_grades)"
"""

import json

# Give a Json file and return a Dictionnary
def read_values_from_json(file_src):
    f = open(file_src, "rb")
    page_dict = json.load(f)
    f.close()
    return page_dict

products_res = {}
# dictionnaire des produits :   key = code du produit, 
#                               value = dictionnaire décrivant le produit

with open('cat_prod.csv', 'w', encoding="utf8") as xfile:
    for p in range(1, 33):
        if p<10:
            page="0"+str(p)
        else:
            page=str(p)
        filename = "data_categ\categ" + page + ".json"
        print(filename)
        data_dict = {}
        # read a Json file
        data_dict = read_values_from_json(filename)
        ##################
        prod_list = data_dict["products"]
        # prod_list is a list of products. Products are dictionnaries
        keys_tuple = ("code","nutrition_grades","url","product_name_fr",
            "generic_name_fr","quantity","packaging","brands","link",
            "stores_tags")
        """
        je sors "ingredients_text" car présence de \r  \n
        également "nutrition_grade_fr", "nutrition_grades" à peine mieux.
        Autres champs inutiles : "categories_tags","countries",
        "purchase_places_tags"
        """
        for product in prod_list:
            # filter on nutrition_grades or nutrition_grade_fr available
            selected = False
            product.setdefault("nutrition_grades","")
            product.setdefault("categories_tags","")
            nutri_score = ("a","b","c","d","e")
            score = product["nutrition_grades"]
            selected = score in nutri_score
            if selected and "en:cocoa-and-hazelnuts-spreads" \
                in product["categories_tags"]:
                nutri_score2 = ("a","b","e")
                selected = score in nutri_score2 
                if selected and score=="e":
                    selected = "pot" in product["packaging"]
            # the product has been filtered  
            if selected:
                the_prod = product["code"]
                # copy (category, product,score) in cat_prod.csv
                xfile.write("\"" + page + "\";\"" + str(the_prod) + "\";\"" 
                        + score + "\"\n")
                if not (the_prod in products_res):
                    # add the new product to products_res
                    d_temp = {}
                    for key in keys_tuple:
                        product.setdefault(key,"")
                        d_temp[key] = product[key]
                    products_res[the_prod]=d_temp.copy()

# Give the products_res Dictionnary and return the products CSV file
with open('products9.csv', 'w', encoding="utf8") as file:
    keys_res = ("code","nutrition_grades","url",
    "product_name_fr","generic_name_fr","quantity","packaging","brands","link",
    "stores_tags")
    for prod in products_res:
        newrow = []
        for k in keys_res:
            value = products_res[prod][k]
            if isinstance(value,list):
                value = ", ".join(value)
            newrow.append(str(value))
        file.write("\"" + "\";\"".join(newrow) + "\"\n")
        