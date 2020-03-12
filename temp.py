#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 14:15:13 2020

@author: guilherme
"""

import pandas as pd
import numpy as np

md = pd.read_csv("stations_inventory.csv")

f = open('WEATHER_STATIONS.txt', 'r')
stations = f.readlines()
f.close()

stations = [s.replace('\n','') for s in stations]

quebecStations = md[md['Province'] == 'QUEBEC']
six2ntyStations = quebecStations[(quebecStations['DLY First Year'] > 1960) & (quebecStations['DLY Last Year'] < 1991)]

f = open('WEATHER_STATIONS_IDs.txt', 'r')
IDs = f.readlines()
f.close()

IDs = [int(ID) for ID in IDs]

hw_stations = md[md['Station ID'].isin(IDs)]

for ID in IDs:
    six2ntyStations.insert(0, column=str(ID), 
                           value = [np.nan for i in range(six2ntyStations.shape[0])])
    

for index1,row1 in six2ntyStations.iterrows():
    x1,y1 = row1['Latitude (Decimal Degrees)'], row1['Longitude (Decimal Degrees)']
    for index2, row2 in hw_stations.iterrows():
        x2,y2 = row2['Latitude (Decimal Degrees)'], row2['Longitude (Decimal Degrees)']
        
        dist = ((x1-x2)**2 + (y1-y2)**2)**(1/2)
        
        six2ntyStations.loc[six2ntyStations['Station ID'] == row1['Station ID'], 
                            str(row2['Station ID'])] = dist