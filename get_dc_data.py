
# Methods to reach out to covidtracking.com and get a historical
# JSON blob, parse it, and return a "CaseData" object with arrays
# of case data and days-since-day-of-record numbers, plus some
# date-time metadata.

import requests,json
from datetime import date
import numpy as np
from time import strptime

URL="https://covidtracking.com/api/v1/states/DC/daily.json"

# Container, so we can pass the offset to the day of record.
class CaseData:
    def __init__(self,size):
        self.x = np.zeros(size)
        self.positive = np.zeros(size)
        self.total = np.zeros(size)
        self.recovered = np.zeros(size)
        self.start = 0 # Ordinal of the smallest date seen.
        self.today = 0 # Ordinal of the largest date seen.
    def normalize(self): # Convert x to day-of-record and sort by date.
        self.start = int(min(self.x))
        self.today = int(max(self.x))
        nx = np.subtract(self.x,self.start)
        idarr = np.argsort(nx)
        self.x = np.take_along_axis(nx,idarr,axis=0)
        self.positive = np.take_along_axis(self.positive,idarr,axis=0)
        self.total = np.take_along_axis(self.total,idarr,axis=0)
        self.recovered = np.take_along_axis(self.recovered,idarr,axis=0)
        

def retrieve():
    jsn = (requests.get(url=URL)).json()
    daylist = []
    poslist = []
    testlist = []
    recovlist = []
    # Step 0: Make a list of case data, and exclude days with zero cases.
    for ji in jsn:
        # print(str(ji['date']) )
        dbj = strptime(str(ji['date']),'%Y%m%d')
        daynumber = date(dbj.tm_year,dbj.tm_mon, dbj.tm_mday).toordinal()
        # print(ji['positive'])
        poscount = int(ji['positive'])
        testcount = int(ji['totalTestResults'])
        # Recovery data is somtimes 'null', and sometimes missing.
        try:
            recovdatum = ji['recovered']
        except KeyError:
            recovcount = 0
        else:
            try:
                recovcount = int(recovdatum)
            except TypeError:
                recovcount = 0
        if poscount>0:
            daylist.append(daynumber)
            poslist.append(poscount)
            testlist.append(testcount)
            recovlist.append(recovcount)
    # Step 1: Make the CaseData object.
    cd = CaseData(len(poslist))
    for (idx,day,pos,test,recov) in zip(range(len(poslist)),daylist,
                                        poslist,testlist,recovlist):
        cd.x[idx] = day
        cd.positive[idx] = pos
        cd.total[idx] = test
        cd.recovered[idx] = recov
    cd.normalize()
    return cd
        

# Diagnostic.  Grab the data and just dump it to output.
if __name__=="__main__":
    cd = retrieve()
    print(cd.x)
    print("Total tests:")
    print(cd.total)
    #
    print("Positive cases:")
    print(cd.positive)
    #
    print("Recovered:")
    print(cd.recovered)
    #
    print("First date: ",date.fromordinal(cd.start))
    print("Last date: ",date.fromordinal(cd.today))
