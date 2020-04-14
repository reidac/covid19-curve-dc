
# Methods to reach out to covidtracking.com and get a historical
# JSON blob, parse it, and return a "CaseData" object with arrays
# of case data and days-since-day-of-record numbers, plus some
# date-time metadata.

import requests,json
from datetime import date
import numpy as np
from time import strptime

URL="https://covidtracking.com/api/states/daily?state=DC"

# Container, so we can pass the offset to the day of record.
class CaseData:
    def __init__(self,size):
        self.x = np.zeros(size)
        self.y = np.zeros(size)
        self.start = 0 # Ordinal of the smallest date seen.
        self.today = 0 # Ordinal of the largest date seen.
    def normalize(self): # Convert x to day-of-record and sort by date.
        self.start = int(min(self.x))
        self.today = int(max(self.x))
        nx = np.subtract(self.x,self.start)
        idarr = np.argsort(nx)
        self.x = np.take_along_axis(nx,idarr,axis=0)
        self.y = np.take_along_axis(self.y,idarr,axis=0)
        

def retrieve():
    jsn = (requests.get(url=URL)).json()
    daylist = []
    caselist = []
    # Step 0: Make a list of case data, and exclude days with zero cases.
    for ji in jsn:
        dbj = strptime(str(ji['date']),'%Y%m%d')
        daynumber = date(dbj.tm_year,dbj.tm_mon, dbj.tm_mday).toordinal()
        casecount = int(ji['positive'])
        if casecount>0:
            daylist.append(daynumber)
            caselist.append(casecount)
    # Step 1: Make the CaseData object.
    cd = CaseData(len(caselist))
    for (idx,day,case) in zip(range(len(caselist)),daylist,caselist):
        cd.x[idx] = day
        cd.y[idx] = case
    cd.normalize()
    return cd
        

# Diagnostic.  Grab the data and just dump it to output.
if __name__=="__main__":
    cd = retrieve()
    print(cd.x)
    print(cd.y)
    print("Last date: ",date.fromordinal(cd.today))
