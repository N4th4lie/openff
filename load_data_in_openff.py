# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 19:52:04 2018

@author: N4th4lie

load_data_in_openff.py

>> Categories : 32 rows in set
>> Products : 1470 rows in set
>> Cat_Prod : 1504 rows in set

"""

import pymysql.cursors

# Connect to the database.
connection = pymysql.connect(host='localhost',
                             user='nath',
                             password='NathGolf',
                             db='openff',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             local_infile=True)

print ("connect successful!!")

try:
    with connection.cursor() as cursor:
        
        files = {"Categories":"(id,category,en_categ,url) ", \
                 "Products":"(id, score, url, label, gen_label, quantity, \
                             packaging, brand, link, store) ",
                 "Cat_Prod":"(category, product, score) "}
        
        path ="'C:/Users/user/Documents/OPENCLASSROOMS/DA Python/Projet05/bdd/"
        sql_end = """ FIELDS TERMINATED BY ';' ENCLOSED BY '\"' 
                        LINES TERMINATED BY '\r\n' """
        
        for key,val in files.items():
            print("Chargement de la table : " + key)
            # SQL
            
            sql="LOAD DATA LOCAL INFILE " +path +key + ".csv' INTO TABLE " + \
                  key + sql_end + val
            #sql = "DELETE FROM "+ key
            # Execute query.
            cursor.execute(sql)
            print ("cursor.description: ", cursor.description)
            print()
            
            # Rectify Import Error in line 1, value 0 instead of 1 :
            if key == "Categories":
                print("Correction id du 1er enregistrement de Categories")
                sql2 = "UPDATE Categories SET id = 1 WHERE id = 0 " 
                rowCount = cursor.execute(sql2)
                print ("Updated! ", rowCount, " rows")
                print()      

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()
            
finally:
    # Close connection.
    connection.close()




