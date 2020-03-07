#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 02:02:42 2019

@author: Guilherme de Brito Abreu
@email: debritoabreu@gmail.com

Description: It downloads weather information from the Environment Canada website. 
It is possible to download daily or hourly information in a slice of time passed as an argument.
The Time Series passed can be continuous ou not continuous.

The arguments should be like the following:
    
         <STARTYEAR> <STARTMONTH> <ENDYEAR> <ENDMONTH> <PATH>
         <StationsListFile> <METHOD> <FORMAT> <ContinuousTimeSeriesFlag>
         
where <STARTYEAR> <STARTMONTH> <ENDYEAR> <ENDMONTH> is the period of the interest passed as numbers,
<PATH> is the path on the machine which the files will be stored. <StationsListFile> is the name of
file containing each Station ID per row to be downloaded. <METHOD> can be 'hourly' or 'daily' which 
means what type of information will be downloaded. <FORMAT> speciefy the format of the data. The 
options are 'default', which means one file per station,  and 'oneFile', which means one file for 
all stations. <ContinuousTimeSeriesFlag> indicates whether the period of time passed is continuous 
or not.
"""

import os, sys
import envcanlib as ecl

if __name__ == '__main__':
    if len(sys.argv) < 9:
        quit('Missing Arguments.The arguments should be like the following\n'+
             '<STARTYEAR> <ENDYEAR> <STARTMONTH> <ENDMONTH> <METHOD>'+
             '<PATH> <StationsListFile> <FORMAT> <ContinuousTimeSeriesFlag>')
        
    startYear  = int(sys.argv[1])
    startMonth = int(sys.argv[2])
    endYear    = int(sys.argv[3])
    endMonth   = int(sys.argv[4])
    method     = sys.argv[5]
    dataPath   = sys.argv[6]+method+"/"
    file       = sys.argv[7]
    dataFormat = sys.argv[8]
    conFlag    = True if sys.argv[9] == 'True' else False
    
    stationsListF = open(file, 'r')
    IDs = stationsListF.readlines()
    stationsListF.close()
    
    IDs = [ID.replace('\n','') for ID in IDs]
    
    try:
        os.makedirs(dataPath)
    except FileExistsError:
        pass
    
    ecl.downloadData(IDs = IDs, start = (startYear, startMonth), end = (endYear, endMonth), method = method, 
                     path=dataPath, dataFormat = dataFormat, continuous = conFlag)