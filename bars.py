import matplotlib.pyplot as plt
import numpy as np
import os

import get_dc_data

# Differential figure.

casedata = get_dc_data.retrieve()

f2 = plt.figure(figsize=(6,4))
plt.suptitle("COVID-19 Data Summary, District of Columbia ",
             fontweight="bold")
plt.title("github.com/reidac/covid19-curve-dc", style="oblique")
plt.xlabel("Days since March 8, 2020")
plt.ylabel("Increments")

inclen = len(casedata.positive)-1
# total_incs = [casedata.total[i+1]-casedata.total[i] for i in range(inclen)]
pos_incs = [casedata.positive[i+1]-casedata.positive[i] for i in range(inclen)]
recov_incs = [casedata.recovered[i+1]-casedata.recovered[i] for i in range(inclen)]

# plt.bar(casedata.x[:-1],total_incs,color='b',width=0.3)
plt.bar(casedata.x[:-1],pos_incs,color='r',width=0.4)
plt.bar(casedata.x[:-1]+0.4,recov_incs,color='g',width=0.4)

plt.legend(labels=['Positives','Recoveries'])

if "FIG_PATH" in os.environ:
    fig_path = os.environ['FIG_PATH']
else:
    fig_path = "."

plt.savefig("{0}/us_dc_bars.png".format(fig_path),dpi=300,bbox_inches="tight")
