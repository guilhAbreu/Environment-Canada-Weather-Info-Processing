#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 02:02:42 2019

@author: guilherme
"""

import os
import pandas as pd
import envcanlib as ecl


#It opens the metadata and selects the Ids from the Province of Quebec.
metaData = pd.read_csv("stations_inventory.csv")
quebecStations = metaData[metaData["Province"] == "QUEBEC"]
IDs = quebecStations["Station ID"].unique()

#It downloads data
ecl.downloadData(IDs = [5205], yearRange = [2018], monthRange = [2], method = 'daily')

dataSet = dict()
dataPath = "../data_set/EnviromentCanada/QuebecStations/"

#It gets the name of each file downloaded previously
pipe = os.popen("ls -N " + dataPath)
stationFiles = pipe.readlines()
stationFiles = [file.replace('\n','') for file in stationFiles]

#It opens them
for file in stationFiles:
    data = pd.read_csv(dataPath+file)
    data = data.dropna(axis = 0, how = 'all')
    dataSet[file.replace('.csv','')] = data

#It computes how many relevant data are missing on the dataset
countTemp = countRH = countDP   = 0
for key in dataSet:
    data = dataSet[key]
    countTemp += int(data['Temp (°C)'].isna().all())
    countRH   += int(data['Rel Hum (%)'].isna().all())
    countDP   += int(data['Dew Point Temp (°C)'].isna().all())
    
print('Missing Data:\nTemp: %d of %d\nRH:   %d of %d\nDP:   %d of %d' %(countTemp,len(dataSet),
                                                                        countRH,len(dataSet),
                                                                        countDP,len(dataSet)))