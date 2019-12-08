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

#It downloads data from 06/2018 to 08/2018 of the Quebec Stations
ecl.downloadData(IDs = IDs, start = (2018, 6), end = (2018,8), method = 'daily', path='/home/guilherme/Documents/GIT REPOSITORIES/data_set/EnviromentCanada/QuebecStations/daily/')
