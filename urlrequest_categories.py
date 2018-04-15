# -*- coding: utf-8 -*-
"""
Created on Tue Apr 10 21:45:50 2018

@author: N4th4lie

urlrequest_categories.py

Download 32 files CATEGORIES RETENUES (44.234 produits)
from `file_url` and save it locally under `file_name`
"""

import requests
from datetime import datetime

src = "https://fr.openfoodfacts.org/"
variable = "cgi/search.pl?tagtype_0=categories&tag_contains_0=contains"
#value = "&tag_0=cocoa-and-hazelnuts-spreads"
size = "&page_size=500"
# page = "&page=1" : 
# not useful because there is less than 300 products in the selected categories
end_url = "&action=process&json=1"

print("début : " + str(datetime.now()))

"""
https://fr.openfoodfacts.org/categorie/ >> chaîne à partir du caractère 40.
012345678901234567890123456789012345678
	     10	       20	     30
"""
# Give a CSV file and return the categories List
with open("categories.csv", "r") as file_src:
    categ = []
    for num,line in enumerate(file_src,0):
        line2 = line.split(";")
        length = len(line2[3]) - 1
        categ.append(line2[3][39:length])
        print(categ[num])

for num,c in enumerate(categ,1):
        if num<10:
            page="0"+str(num)
        else:
            page=str(num)
        file_url = src+variable+"&tag_0="+ c + size + end_url
        file_name = "data_categ\categ" + page + ".json"
        print(file_name)
        r = requests.get(file_url, stream = True)
        with open(file_name, 'wb') as file_json:
            for chunk in r.iter_content(chunk_size=3072):
                # writing one chunk at a time to json file
                if chunk:
                    file_json.write(chunk)
                
print("fin : " + str(datetime.now()))

"""
début   : 2018-04-10 23:53:23.430038
fin     : 2018-04-10 23:57:22.560614
43+112+26+70+49+40+58+46+31+26+47+49+31+25+29+23+27+227+161+114
+32+59+58+38+41+23+47+30+51+41+149+16
= 1819 produits (dont certains sans score nutritionnel)
"""