#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 02:02:42 2019

@author: guilherme
"""

import os
import pandas as pd
import envcanlib as ecl
import numpy as np

def countData(dataFrame, dictionary, column, dataQuantity):
    '''
    Description: It calculate the pecentage of data available  
    '''
    dataSet = dictionary.copy()
    newdf = dataFrame.copy()
    pct = list()
    for station in dataSet:
        data = dataSet[station]
        pct.append(round(100*data[column].count()/dataQuantity,2))
    
    newdf["Data Available "+column] = pct
    return newdf

method       = 'daily'
dataPath     = "../data_set/EnviromentCanada/QuebecStations/"+method+"/"

#It opens the metadata and selects the Ids from the Province of Quebec.
metaData = pd.read_csv("stations_inventory.csv")
quebecStations = metaData[(metaData["Province"] == "QUEBEC") & (metaData["DLY Last Year"] >= 2019)]

IDs = quebecStations['Station ID'].unique()

#It downloads data from 06/2018 to 08/2018 of the Quebec Stations
ecl.downloadData(IDs = IDs, start = (2019, 6), end = (2019,8), method = method, 
                 path='/home/guilherme/Documents/GIT REPOSITORIES/data_set/EnviromentCanada/QuebecStations/'+method+'/2019 - Jun2Aug/')

dataSet = dict()

#It gets the name of each file downloaded previously
stationFiles = quebecStations['Station ID'].unique().astype('str')

#It opens them
for file in stationFiles:
    data = pd.read_csv(dataPath+'Heatwave/'+file+'.csv')
    data = data.dropna(axis = 0, how = 'all')
    dataSet[file] = data

from datetime import date
delta = date(2018, 8, 31) - date(2018, 6, 1)
quebecStations = countData(quebecStations, dataSet, 'Max Temp (°C)', (delta.days + 1))
