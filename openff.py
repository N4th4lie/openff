# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 21:23:43 2018
@author: N4th4lie

openff.py is the main program:
    
    - Home menu >> launch part 1 or part 2, or quit
                   by creating instances of Menu
                    (methods : display() and make_choice())
                    
    - part 1 :  1. load food categories from openff database
                2. display the list of categories (create an instance of Menu)
                3. a category is selected >> create an instance of Category
                    (methods : list_products() and substitute())
                    
    - part 2 :  1. load results recorded from openff database
                2. display all results (create an instance of Menu)
                2. a result is selected >> create an instance of Result
                    (method : display())
"""

from constants import *
from classes import *
import myconnutils


end = False

while not end:
    # Display main menu
    print("--------------------------------------------")
    print("MENU PRINCIPAL :")
    home_menu = Menu(HOME_LIST)
    home_menu.display()
    choice = home_menu.make_choice()
    print("--------------------------------------------")

    if choice == "1":
        # Part 1 : choose a category, then a product and obtain a substitute
        
        # load categories
        connection = myconnutils.getConnection()
        try:
            with connection.cursor() as cursor:
                # Read categories from openff database:
                sql = """SELECT id AS num, category AS label FROM Categories
                         ORDER BY id"""
                cursor.execute(sql)
                categ_list = []
                for row in cursor:
                    categ_list.append(row)
        finally:
            # Close connection.
            connection.close()

        # Display categories
        print("LISTE DES CATEGORIES")
        print("--------------------------------------------")
        print("Choisissez une catégorie d'aliments parmi les suivantes :")
        categ_menu = Menu(categ_list)
        categ_menu.display()
        # Select a category
        print("\nVeuillez saisir le code de la catégorie souhaitée.")
        categ_choice = int(categ_menu.make_choice())
        my_categ = Category(categ_list[categ_choice - 1])
        
        # Choose a substitute for a selected product in the category    
        my_categ.substitute()
               
    if choice == "2":
        # Part 2 : display recorded results1
        
        # load results
        connection = myconnutils.getConnection()
        try:
            with connection.cursor() as cursor:
                # Read results from openff database:
                sql = """SELECT R.id, R.category, C.category AS categ_lab,
                R.initial, P.score AS init_score, P.label AS init_lab, 
                P.brand AS init_brand, substitute, res_date 
                FROM Results AS R 
                INNER JOIN Categories AS C ON C.id = R.category
                INNER JOIN Products AS P ON P.id = R.initial 
                ORDER BY id """
                cursor.execute(sql)
                res_list = []
                for row in cursor:
                    res_list.append(row)
        finally:
            # Close connection.
            connection.close()
        
        # Display results
        print("LISTE DES REMPLACEMENTS ENREGISTRES")
        print("--------------------------------------------")
        print("NUMERO -- (CATEGORIE) -- SCORE -- PRODUIT INITIAL")
        res_list2 = []
        for res in res_list:
            menu_fields = {}
            menu_fields["num"]=res["id"]
            menu_fields["label"]=("(%s %s) score %s - %s / %s"
                       %(res["category"],res["categ_lab"],
                         res["init_score"].upper(),
                         res["init_lab"],res["init_brand"]))
            res_list2.append(menu_fields)
        res_menu = Menu(res_list2)
        res_menu.display()
        # Select a result to consult
        print("\nVeuillez saisir le numéro du remplacement à consulter.")
        res_choice = int(res_menu.make_choice())
        # id is AUTO-INCREMENT and results are not supposed to be deleted 
        # (in the other hand:
        #  add a while research on res_list[ind]["id"]==choice)
        my_result = Result(res_list[res_choice - 1])
        
        # Display the result selected    
        my_result.display()
            
    if choice == "3":
        # Quit
        print("Au revoir")
        end = True
