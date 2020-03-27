#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 02:02:42 2019

@author: Guilherme de Brito Abreu
@email: debritoabreu@gmail.com

Description: It downloads weather information from the Environment Canada website. 
         
<STARTYEAR> <STARTMONTH> <ENDYEAR> <ENDMONTH> is the period of the interest passed as numbers. 
<FORMAT> specify the format of the data. The options are 'default', which means one file per station,
and 'oneFile', which means one file for all stations.

Change CONTFLAG to False if it is intended to download just a slice of month of each year passed.

Contact me in case of any bug being reported.
"""

METADATAFILE = 'stations_inventory.csv'

import os
import envcanlib as ecl
import pandas as pd
from datetime import date

FIRSTYEAR  = 1840
LASTYEAR   = date.today().year
FIRSTMONTH = 1
LASTMONTH  = date.today().month
CONTFLAG   = True


if __name__ == '__main__':
    
    # download stations inventory
    os.system("wget --no-check-certificate 'https://docs.google.com/uc?export=download&id=1egfzGgzUb0RFu_EE5AYFZtsyXPfZ11y2' -O " + METADATAFILE)
    
    inventF = open(METADATAFILE, 'r')
    rows = inventF.readlines()
    inventF.close()
    rows = rows[3:] #erase comments
    rows = [r.replace('\n','').replace('"','').split(',') for r in rows] #remove ",\n and make a list as matrix
    
    # adapt data considering that there are station names that contain commas
    for r in rows:
        if len(r) > len(rows[0]):
            r.pop(1)
    
    # create a dataframe
    md = pd.DataFrame(rows[1:], columns=rows[0])
    
    startYear  = FIRSTYEAR
    endYear    = LASTYEAR
    startMonth = FIRSTMONTH
    endMonth   = LASTMONTH
    conFlag    = CONTFLAG
    
    IDs = md['Station ID'].unique()
    
    for method in ['daily','hourly']:
        ecl.downloadData(IDs = IDs, start = (startYear, startMonth), end = (endYear, endMonth), 
                         method = method,dataFormat = 'oneFile', continuous = conFlag, metaData=md)