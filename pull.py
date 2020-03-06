#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 02:02:42 2019

@author: guilherme
"""

import os, sys
import envcanlib as ecl

if len(sys.argv) < 7:
    quit('Missing Arguments.The arguments should be like the following\n'+
         '<STARTYEAR> <STARTMONTH> <ENDYEAR> <ENDMONTH> <PATH> <STATIONSLISTFILE> <METHOD(hourly or daily)>')
    
startYear  = int(sys.argv[1])
startMonth = int(sys.argv[2])
endYear    = int(sys.argv[3])
endMonth   = int(sys.argv[4])
method     = sys.argv[7]
dataPath   = sys.argv[5]+method+"/"
file       = sys.argv[6]


stationsListF = open(file, 'r')
IDs = stationsListF.readlines()
stationsListF.close()

IDs = [ID.replace('\n','') for ID in IDs]

for year in range(startYear, endYear+1):    
    try:
        os.makedirs(dataPath+str(year))
    except FileExistsError:
        pass
    
    ecl.downloadData(IDs = IDs, start = (year, startMonth), end = (year, endMonth), 
                     method = method, path=dataPath+str(year)+'/')