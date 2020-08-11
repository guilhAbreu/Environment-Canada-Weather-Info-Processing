#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 14:15:13 2020

@author: guilherme
"""

def distanceCalculator(lat1, lon1, lat2, lon2):
    '''
    It computes the distance in kilometers between 2 given geometric coordinates.
    
    Formula Explanation: https://en.wikipedia.org/wiki/Haversine_formula
    '''
    
    import math
    
    R = 6378.137 # Radius of earth in KM
    dLat = lat2 * math.pi / 180.0 - lat1 * math.pi / 180.0
    dLon = lon2 * math.pi / 180.0 - lon1 * math.pi / 180.0
    a = math.sin(dLat/2) * math.sin(dLat/2) +\
        math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) *\
        math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

import pandas as pd
import numpy as np
import envcanlib

#get IDs of the stations of interest
IDs = ['51157', '53001']

#open and filter what stations have information on the period of interest
md = pd.read_csv("stations_inventory.csv")
quebecStations = md[md['Province'] == 'QUEBEC']
possStations = quebecStations[(quebecStations['HLY First Year'] <= 2010) & (quebecStations['HLY Last Year'] >= 2012)]

#get the information of the stations of interest
IDs = [int(ID) for ID in IDs]
hw_stations = md[md['Station ID'].isin(IDs)]

#create new one columns for each station of interest
for ID in IDs:
    possStations.insert(0, column=str(ID), 
                           value = [np.nan for i in range(possStations.shape[0])])

#compute the distance in coordinates for each station
for index1,row1 in possStations.iterrows():
    x1,y1 = row1['Latitude (Decimal Degrees)'], row1['Longitude (Decimal Degrees)']
    for index2, row2 in hw_stations.iterrows():
        x2,y2 = row2['Latitude (Decimal Degrees)'], row2['Longitude (Decimal Degrees)']
        
        dist = distanceCalculator(x1, y1, x2, y2)
        
        possStations.loc[(possStations['Station ID'] == row1['Station ID']), 
                            str(row2['Station ID'])] = dist

#create a dictionary to store the closest station to each station of interest
data = list()
for i in range(len(IDs)):
    temp = possStations.sort_values(by=[str(IDs[i])], ignore_index=True)
    data.append([str(IDs[i]), str(temp['Station ID'][1]), round(temp[str(IDs[i])][0], 2)])
    
new_table = pd.DataFrame(data = data, columns=['Station ID', 'Closest Station ID', 'Distance (Km)'])
new_table.to_csv('closest_stations_2010-2012.csv')

envcanlib.downloadData(IDs = [new_table.iloc[:,1].unique()[0]], start=(2010,6), end=(2012,8), continuous = False)

envcanlib.downloadData(IDs = [new_table.iloc[:,1].unique()[1]], start=(2010,6), end=(2014,8), continuous = False)
