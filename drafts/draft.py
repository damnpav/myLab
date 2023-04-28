# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 03:40:24 2019

@author: hcani
"""

import mysql.connector
import pandas as pd

pathToPass = r"C:\Users\hcani\Documents\MySQL Settings\sql_key.txt"
password = open(pathToPass).readlines()[0]

cnx = mysql.connector.connect(user = 'root', password = password, host = '127.0.0.1', database = 'stocks')
cursor = cnx.cursor()

query = ("SELECT * FROM ibexdata WHERE id = 0")
#cursor.execute(query)
# data = cursor.fetchall()
# print(data)

df = pd.read_sql('SELECT * FROM ibexdata', con = cnx)
print(df)

cnx.close()