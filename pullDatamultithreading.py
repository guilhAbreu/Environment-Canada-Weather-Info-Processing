import envcanlib as ecl
import pandas as pd
import os
import numpy as np
import threading

class myThread (threading.Thread):
    def __init__(self, threadID, IDs, start, end, path, method):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.IDs = IDs
        self.strt = start
        self.end = end
        self.path = path
        self.method = method

    def run(self):
        print('Thread '+str(self.threadID)+' initiated..')
        ecl.downloadData(IDs = self.IDs,
                         start= self.strt, end=self.end,
                         method=self.method,
                         path=self.path
                        )
N_threads = 2*os.cpu_count()

threads = list()
metaData = pd.read_csv('stations_inventory.csv')
allQuebec = metaData[metaData['Province'] == 'QUEBEC']

ids_dnl = os.listdir('/home/guilherme/Documents/GIT - REPOSITORIES/dataset/EnvironmentCanada/Quebec/hourly/alltime/')
ids_dnl = [i.replace('.csv', '') for i in ids_dnl]
IDs = allQuebec['Station ID'].unique().astype(str)
hourlyIDs = np.setdiff1d(IDs, np.asarray(ids_dnl))

length = hourlyIDs.shape[0]

for i in range(N_threads):
    thread = myThread(i, hourlyIDs[i*length//N_threads:(i+1)*length//N_threads], (1980,1), (2019, 12),'/home/guilherme/Documents/GIT - REPOSITORIES/dataset/EnvironmentCanada/Quebec/hourly/alltime/', 'hourly')
    thread.start()
    threads.append(thread)

# Wait for all threads to complete
for t in threads:
    t.join()
print ("Exiting Main Thread")
