# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 22:24:59 2018

@author: N4th4lie

myconnutils.py is a utility module to connect to the database openff.
It defines the getConnection() function to returns a connection.

"""

import pymysql.cursors  

# Function return a connection.
def getConnection():
    connection = pymysql.connect(host='localhost',
                             user='nath',
                             password='NathGolf',
                             db='openff',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor,
                             local_infile=True)
    return connection