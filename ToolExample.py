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

method       = 'daily'
dataPath     = "../data_set/EnviromentCanada/QuebecStations/"+method+"/"

#It opens the metadata and selects the Ids from the Province of Quebec.
metaData = pd.read_csv("stations_inventory.csv")
quebecStations = metaData[metaData["Province"] == "QUEBEC"]
IDs = quebecStations["Station ID"].unique()

#It downloads data from 06/2018 to 08/2018 of the Quebec Stations
#ecl.downloadData(IDs = IDs, start = (2018, 6), end = (2018,8), method = 'daily', path='/home/guilherme/Documents/GIT REPOSITORIES/data_set/EnviromentCanada/QuebecStations/daily/')

dataSet = dict()

#It gets the name of each file downloaded previously
stationFiles = os.listdir(dataPath)

#It opens them
for file in stationFiles:
    data = pd.read_csv(dataPath+file)
    data = data.dropna(axis = 0, how = 'all')
    dataSet[file.replace('.csv','')] = data

#It computes how many relevant data are missing on the dataset
countmaxTemp = countminTemp = 0
missingData = pd.DataFrame([], columns = ['Station ID', 'Station Name', 'Has Max Temp', 'Has Min Temp', 'lat', 'lng'])
missingData['Station ID']   = (quebecStations['Station ID'].values).astype('str')
missingData['Station Name'] = quebecStations['Name'].values
missingData['lat']          = np.asarray(quebecStations['Latitude (Decimal Degrees)'].values)
missingData['lng']          = np.asarray(quebecStations['Longitude (Decimal Degrees)'].values)
for key in dataSet:
    data = dataSet[key]
    
    nomaxTmp = data['Max Temp (°C)'].isna().all()
    nominTmp = data['Min Temp (°C)'].isna().all()
    countmaxTemp += int(nomaxTmp)
    countminTemp += int(nominTmp)
    missingData.loc[missingData['Station ID'] == key,'Has Max Temp'] = not nomaxTmp
    missingData.loc[missingData['Station ID'] == key,'Has Min Temp'] = not nominTmp

dataLength = len(dataSet)
print('Missing Data in %d stations:' %dataLength)
print('Max Air Temperature:     %.2f'  %(100*countmaxTemp/dataLength) + '%')
print('Min Air Temperature:     %.2f'  %(100*countminTemp/dataLength) + '%')
