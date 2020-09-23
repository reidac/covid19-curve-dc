# Methods to reach out to covidtracking.com and get a historical
# JSON blob, parse it, and return a "CaseData" object with arrays
# of case data and days-since-day-of-record numbers, plus some
# date-time metadata.

import requests,json
from datetime import date
import numpy as np
from time import strptime
import math

URL="https://api.covidtracking.com/api/v1/states/dc/daily.json"

# Container, so we can pass the offset to the day of record.
class CaseData:
    def __init__(self,size):
        self.x = np.zeros(size)
        self.positive = np.zeros(size)
        self.total = np.zeros(size)
        self.recovered = np.zeros(size)
        self.deaths = np.zeros(size)
        self.start = 0 # Ordinal of the smallest date seen.
        self.today = 0 # Ordinal of the largest date seen.
    def normalize(self): # Convert x to day-of-record and sort by date.
        self.start = int(min(self.x))
        self.today = int(max(self.x))
        nx = np.subtract(self.x,self.start)
        idarr = np.argsort(nx)
        self.x = np.take(nx,idarr,axis=0)
        self.positive = np.take(self.positive,idarr,axis=0)
        self.total = np.take(self.total,idarr,axis=0)
        self.recovered = np.take(self.recovered,idarr,axis=0)
        self.deaths = np.take(self.deaths,idarr,axis=0)

def retrieve():
    jsn = (requests.get(url=URL)).json()
    daylist = []
    poslist = []
    testlist = []
    recovlist = []
    deathlist = []
    # Step 0: Make a list of case data, and exclude days with zero cases.
    for ji in jsn:
        dbj = strptime(str(ji['date']),'%Y%m%d')
        daynumber = date(dbj.tm_year,dbj.tm_mon, dbj.tm_mday).toordinal()
        # print(ji['positive'])
        # Positive data is also sometimes missing.
        try:
            poscount = int(ji['positive'])
        except TypeError:
            poscount = 0
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
        try:
            deathdatum = ji['death']
        except KeyError:
            deathcount = 0
        else:
            try:
                deathcount = int(deathdatum)
            except TypeError:
                deathcount = 0
        if poscount>0:
            daylist.append(daynumber)
            poslist.append(poscount)
            testlist.append(testcount)
            recovlist.append(recovcount)
            deathlist.append(deathcount)
    # Step 1: Make the CaseData object.
    cd = CaseData(len(poslist))
    for (idx,day,pos,test,recov,dth) in zip(range(len(poslist)),daylist,
                                             poslist,testlist,
                                             recovlist,deathlist):
        cd.x[idx] = day
        cd.positive[idx] = pos
        cd.total[idx] = test
        cd.recovered[idx] = recov
        cd.deaths[idx] = dth
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
    print("Dead:")
    print(cd.deaths)
    #
    print("First date: ",date.fromordinal(cd.start))
    print("Last date: ",date.fromordinal(cd.today))

    tday = date.fromordinal(cd.today)
    mday = int(tday.strftime("%d"))
    
    # Ordinal number trick from:
    # https://stackoverflow.com/questions/9647202/ordinal-numbers-replacement
    mdayth = "%d%s" % (mday,"tsnrhtdd"[(math.floor(mday/10)%10!=1)*(mday%10<4)*mday%10::4])

    # daystring = f'{tday.strftime("%A")}, {tday.strftime("%B")} {mdayth}, {tday.strftime("%Y")}'
    daystring = "%s, %s %s, %s" % (tday.strftime("%A"), tday.strftime("%B"), mdayth, tday.strftime("%Y"))
    # print(f'As of {daystring}, DC has reported {int(cd.positive[-1]):,} cases, with {int(cd.recovered[-1]):,} recoveries and {int(cd.deaths[-1]):,} deaths. Today\'s case increment is {int(cd.positive[-1]-cd.positive[-2])}.')
    # print( "As of %s, DC has reported %s cases, with %s recoveries and %d deaths. Today\'s case increment is %d." % (daystring, '{:,d}'.format(int(cd.positive[-1])), '{:,d}'.format(int(cd.recovered[-1])), int(cd.deaths[-1]), int(cd.positive[-1]-cd.positive[-2])) )
    print( 'As of {}, DC has reported {:,d} cases, with  {:,d} recoveries and {:d} deaths. Today\'s case increment is {:d}.'.format(daystring, int(cd.positive[-1]), int(cd.recovered[-1]), int(cd.deaths[-1]), int(cd.positive[-1]-cd.positive[-2])) )

