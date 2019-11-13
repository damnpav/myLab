# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 15:12:45 2019

@author: dpavlin001
"""
# TODO make MySQL store for shares

sp500base = 'C:/Users/hcani/Documents/GitHub/myLab/sp500.xlsx' #путь к файлу с Сп500
dj = 'C:/Users/hcani/Documents/GitHub/myLab/dowJones.xlsx'
rts = 'C:/Users/hcani/Documents/GitHub/myLab/rts.xlsx'

import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests

def indComp(rout): # retrieve data from excel frames
    myDf = pd.read_excel(rout, "comp")
    compNames = myDf['Company'].tolist()
    compSymbols = myDf['Symbol']
    compWeights = myDf['Weight']
    finalList = [compNames, compSymbols, compWeights]
    return(finalList)

def showStructure(indexLists, porog): #show structure of index
    labels =indexLists[1]
    sizes = indexLists[2] #weights
    for i in range(len(labels)):
        if sizes[i] < porog: #treshold
            labels[i] = ""
    plt.pie(sizes, labels = labels)
    plt.axis('equal')
    plt.show()

def ibexUpdater(nameOfshare):
    ibexUrl = 'http://www.bolsamadrid.es/ing/aspx/Mercados/Precios.aspx?indice=ESI100000000' # page with market data
    doc = requests.get(ibexUrl) # query to page
    soup = BeautifulSoup(''.join(doc.text)) # push page to soup
    bsResult = soup.findAll(text = True) # retrieve all text from soup
    resultDict = {}
    for i in range(len(bsResult)):
        if str(bsResult[i]).find(nameOfshare) != -1:
            resultDict['nameOfshare'] = bsResult[i]
            resultDict['last'] = bsResult[i+1]
            resultDict['high'] = bsResult[i+3]
            resultDict['low'] = bsResult[i+4]
            resultDict['volume'] = bsResult[i+5]
    return resultDict

# spList = indComp(sp500base)
# djList = indComp(dj)
# nasdaqList = indComp(nasdaq)

# rtsList = indComp(rts)
# showStructure(rtsList, 0.01)


# showStructure(spList, 1.4)
# showStructure(djList, 1.4)
#showStructure(nasdaqList, 1.4)
