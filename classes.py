# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 19:13:38 2018
@author: N4th4lie

classes.py

    1. class Menu with methods:
        - display() : display the menu
        - make_choice : return the answer
        
    2. class Product:
        - useful for manage products
        - method display() is called  :
            * from class Category >> display the result of substitute()
            * from class Result >>  display the initial and substitute products
            from a result selected in part 2 (find a substitution recorded).

    3. class Category, methods:
        - list_products() : return all products in the category and the 
                            highest score among them.
        - substitute() :
            1.  create an instance of Menu with a sublist of all products :
                products of the category except those with highest score 
                >> display() it.
            2.  select a product with make_choice().
            3.  create an instance of Product and display the selected product.
            4.  create a sublist of all products : products of the category 
                with better score than the selected product.
            5.  from the previous sublist, 
                extract randomly a product as substitute.
            6.  create an instance of Product and display the substitute.
            7.  create an instance of Menu, display and make_choice :
                *********************************************************
                if user wants to save the result, add it in Results table
                of openff database.
                *********************************************************
            
    4. class Result: the method in Result displays the whole description 
            of a result. Attribut of Result is a row of Results table from 
            openff database, from which we only get id number of the initial
            and substitute products.
            So we have to load this couple of products from openff database
            to get more information about them (name, score, url,etc.)
"""

from random import randint
import time
# my utility module connexion
import myconnutils
from constants import *

class Menu:

    def __init__(self, list_options):
        self.list_options = list_options
        
    # Display the menu
    def display(self):
        for option in self.list_options:
            print("-" + str(option["num"]).rjust(2) + " : " + option["label"])
    
    # Return the answer
    def make_choice(self):
        list1 = []
        for option in self.list_options:
            list1.append(str(option["num"]))
        answer = input("Votre choix : ")    
        while not (answer in list1):
            print("Réponse non valide. Saisir le numéro de votre choix.")
            answer = input("Votre choix : ")
        return(answer)

class Product:

    def __init__(self, prod_dict):
        self.prod_dict = prod_dict
        self.id = prod_dict["id"]
        self.url = prod_dict["url"]
        self.score = prod_dict["score"]
        self.label = prod_dict["label"]
        self.gen_label = prod_dict["gen_label"]
        self.brand = prod_dict["brand"]
        self.link = prod_dict["link"]
        self.packaging = prod_dict["packaging"]
        self.quantity = prod_dict["quantity"]
        self.store = prod_dict["store"]

    # Describe the product
    def display(self):
        print("Lien OpenFoodFacts : " + self.url)
        print("Score nutritionnel : " + self.score.upper())
        print("Nom                : " + self.label)
        print("Description        : " + self.gen_label)
        print("Marque             : " + self.brand)
        print("Site de la marque  : " + self.link)
        print("Conditionnement    : " + self.packaging)
        print("Quantité           : " + self.quantity)
        print("Points de vente    : " + self.store)

class Category:

    def __init__(self, categ_dict):
        self.num = categ_dict["num"]
        self.label = categ_dict["label"]
        
    # Return products and the highest score in the category
    def list_products(self):
        connection = myconnutils.getConnection()
        try:
            with connection.cursor() as cursor:
                # Read all products from the category
                sql = """SELECT category, Cat_Prod.score AS score, id, url, 
                label, gen_label, quantity, packaging, brand, link, store 
                FROM Cat_Prod INNER JOIN Products
                ON Cat_Prod.product = Products.id 
                WHERE Cat_Prod.category = %s """
                cursor.execute(sql, (self.num))
                food = []           # all products with complete information
                high_score = "e"    # find the best score (nutrition_grades)
                for row in cursor:
                    food.append(row)
                    if row["score"] < high_score:
                        high_score = row["score"]
        finally:
            # Close connection
            connection.close()
        return(food, high_score)
        
    # Choose a substitute for a selected product in the category
    def substitute(self):
        # Return all products and the highest score in the category 
        (my_products, high_score) = self.list_products()
        
        end_categ = False
        while not end_categ:
            # Display the products except the highest score level
            print("---------------------------------------------------------")
            print("Aliments de la catégorie %s = %s" %(str(self.num),
                                                       self.label))
            n = 1
            prod_list = []
            for prod in my_products:
                if prod["score"] != high_score:
                    # Display the product
                    print("%s : score %s, %s / %s" %(str(n).rjust(2), 
                    prod["score"].upper(),prod["label"], prod["brand"]))
                    # Define prod_list for prod_menu
                    prod_list.append({"num":str(n), "prod1":prod})
                    n += 1
            print("---------------------------------------------------------")
            # Select a product    
            prod_menu = Menu(prod_list)
            my_prod_num = prod_menu.make_choice()
            my_prod_ind = int(my_prod_num) - 1
            my_prod = Product(prod_list[my_prod_ind]["prod1"])
            # Display the whole description of the selected product
            print("--------------------")
            print("Aliment sélectionné :")
            print("--------------------")
            my_prod.display()
            
            # Give a substitute (choose randomly among better score products)
            better_prod = []
            my_score = my_prod.score
            for prod in my_products:
                if prod["score"] < my_score:
                    better_prod.append(prod)
            my_substit = Product(better_prod[randint(0, len(better_prod) - 1)])
            # Display the whole description of the substitute
            print("--------------------------------")
            print("Produit de remplacement proposé :")
            print("--------------------------------")
            my_substit.display()
            print("--------------------------------")
        
            # Save this result ? Test another food from the category ? Quit ?
            # Display quit_prod menu
            print("MENU :")
            quit_prod = Menu(PROD_QUIT)
            quit_prod.display()
            qchoice = quit_prod.make_choice()
            if qchoice == "1":
                connection = myconnutils.getConnection()
                try:
                    with connection.cursor() as cursor:
                        # Create a new record in openff with the result to save
                        sql = """INSERT INTO Results (category, initial, 
                        substitute, res_date) VALUES (%s, %s, %s, %s)"""
                        cursor.execute(sql, (self.num, my_prod.id, 
                                 my_substit.id, 
                                 (time.strftime('%Y-%m-%d %H:%M:%S'))))
                        #"res_date":time.strftime("%d %b %Y %H:%M")
                        # time.strptime(str(time.localtime()), "%b %d %Y %H:%M")
                    connection.commit()
                finally:
                    # Close connection
                    connection.close()
                print("Le remplacement de produit a bien été sauvegardé")
                end_categ = True
            if qchoice == "3":
                # Back to home_menu
                end_categ = True
            # ELSE: Test another product from the same category
                
class Result:

    def __init__(self, res_dict):
        self.res_dict = res_dict
        self.id = res_dict["id"]
        self.category = res_dict["category"]
        self.categ_lab = res_dict["categ_lab"]
        self.initial = res_dict["initial"]
        self.substitute = res_dict["substitute"]
        self.res_date = res_dict["res_date"]

    # Describe the result
    def display(self):
        
        # General information
        print("\n---------------------------------------------------------")
        my_date = time.strptime(str(self.res_date), "%Y-%m-%d %H:%M:%S")
        print("Enregistrement n°%s du %s/%s/%s à %sh%s" %(str(self.id),
            str(my_date[2]).rjust(2,"0"),str(my_date[1]).rjust(2,"0"),
            str(my_date[0]),str(my_date[3]).rjust(2,"0"),
            str(my_date[4]).rjust(2,"0")))
        print("Aliments de la catégorie %s = %s" %(str(self.category),
                                                       self.categ_lab))
        print("---------------------------------------------------------\n")

        # Load the initial and substitute products
        connection = myconnutils.getConnection()
        try:
            with connection.cursor() as cursor:
                # Read the initial product
                sql = """SELECT id, url, score,
                label, gen_label, quantity, packaging, brand, link, store 
                FROM Products WHERE id = %s"""
                cursor.execute(sql, (self.initial))
                init_prod = Product(cursor.fetchone())
                # Read the substitute product
                sql = """SELECT id, url, score,
                label, gen_label, quantity, packaging, brand, link, store 
                FROM Products WHERE id = %s"""
                cursor.execute(sql, (self.substitute))
                subst_prod = Product(cursor.fetchone())
        finally:
            # Close connection
            connection.close()

        # Call display method of Product class (a product description)
        my_food = (init_prod, subst_prod)
        for i in range(0,2):
            if i==0:
                print("  ****  Aliment à remplacer  ****")
            else:
                print("  ****  Aliment de remplacement  ****")
            my_food[i].display()
            print()