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
f = open('WEATHER_STATIONS.txt', 'r')
stations = f.readlines()
f.close()
stations = [s.replace('\n','') for s in stations]

#open and filter what stations have information on the period of interest
md = pd.read_csv("stations_inventory.csv")
quebecStations = md[md['Province'] == 'QUEBEC']
six2ntyStations = quebecStations[(quebecStations['DLY First Year'] <= 1981) & (quebecStations['DLY Last Year'] >= 2010)]

f = open('WEATHER_STATIONS_IDs.txt', 'r')
IDs = f.readlines()
f.close()

#get the information of the stations of interest
IDs = [int(ID) for ID in IDs]
hw_stations = md[md['Station ID'].isin(IDs)]

#create new one columns for each station of interest
for ID in IDs:
    six2ntyStations.insert(0, column=str(ID), 
                           value = [np.nan for i in range(six2ntyStations.shape[0])])

#compute the distance in coordinates for each station
for index1,row1 in six2ntyStations.iterrows():
    x1,y1 = row1['Latitude (Decimal Degrees)'], row1['Longitude (Decimal Degrees)']
    for index2, row2 in hw_stations.iterrows():
        x2,y2 = row2['Latitude (Decimal Degrees)'], row2['Longitude (Decimal Degrees)']
        
        dist = distanceCalculator(x1, y1, x2, y2)
        
        six2ntyStations.loc[(six2ntyStations['Station ID'] == row1['Station ID']), 
                            str(row2['Station ID'])] = dist

#create a dictionary to store the closest station to each station of interest
data = list()
for i in range(len(IDs)):
    temp = six2ntyStations.sort_values(by=[str(IDs[i])], ignore_index=True)
    data.append([str(IDs[i]), str(temp['Station ID'][0]), round(temp[str(IDs[i])][0], 2)])
    
new_table = pd.DataFrame(data = data, columns=['Station ID', 'Closest Station ID', 'Distance (Km)'])
new_table.to_csv('closest_stations_81-2010.csv')

envcanlib.downloadData(IDs = new_table['Closest Station ID'].unique(), start=(1981,1), end=(2010,12), method='daily',
                       path='/home/guilherme/Documents/GIT - REPOSITORIES/dataset/EnvironmentCanada/Quebec/climateNormals/1981-2010/')
