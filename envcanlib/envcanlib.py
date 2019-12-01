#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 23:35:15 2019

@author: guilherme
"""

def downloadData(IDs, yearRange, monthRange, method = 'h', path = './'):
    '''
    Description: It downloads weather information from the Environment Canada website. 
    It is possible to download daily or hourly information in a slice of time passed as an argument.
    
    Input: IDs:  list of the target stations IDs.
    
           yearRange: Years range passed as a list.
           
           monthRange: Months range passed as a list.
           
           method: 'h' for hourly information (deafault) or 'd' for daily information.
           
           path: Path on the machine to save the data downloaded.
    '''
    
    import pandas as pd
    import urllib as url
    
    if method == 'h':
        method  = "&timeframe=1&submit=Download+Data"
    elif method == 'd':
        method  = "&timeframe=2&submit=Download+Data"
    else:
        print('method = ' + method + 'is not valid.')
        print('avalible methods are "h" or "d".')
    
    for ID in IDs:
        data = pd.DataFrame([])
        for intYr in yearRange:
            for intMnt in monthRange:
                #build the query
                strQry = 'http://climate.weather.gc.ca/climate_data/bulk_data_e.html?format=csv&stationID=' + str(ID) + "&Year=" + str(intYr) +'&Month=' + str(intMnt) + method 
                #print strQry
                print ('Querying station ' + str(ID) + ' for year ' + str(intYr) + ' and month ' + str(intMnt))
                try:
                    response = url.request.urlopen(strQry)
                    rawData = response.readlines()
                    response.close()
                    rawData = [row.decode('utf8').replace('"','').replace('\n','') for row in rawData]
                   
                    columns = rawData[0].split(',')
                    d = [line.split(',') for line in rawData[1:]]
                    
                    for i in range(len(d)):
                        if len(d[i]) > len(columns):
                            d[i][len(columns)-1] = "".join(d[i][len(columns)-1:])
                            d[i] = d[i][:len(columns)]
                            
                        if len(d[i]) < len(columns):
                            while len(d[i]) < len(columns):
                                d[i].append('')
                            
                    newData = pd.DataFrame(d, columns=columns)
                    data = data.append(newData, ignore_index=True, sort=False)
                except Exception:
                    print ('Failure getting data for '  + str(ID) + ' for year ' + str(intYr))
        
        data.to_csv(path+str(ID)+".csv", index=False, line_terminator="")