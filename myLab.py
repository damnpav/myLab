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

def builtGraph:


# spList = indComp(sp500base)
# djList = indComp(dj)
# nasdaqList = indComp(nasdaq)

# rtsList = indComp(rts)
# showStructure(rtsList, 0.01)


# showStructure(spList, 1.4)
# showStructure(djList, 1.4)
#showStructure(nasdaqList, 1.4)

copyDates = []
for i in range(len(dates)):
    if i % delimiter != 0:
        copyDates.append('')
    else:
        copyDates.append(dates[i])