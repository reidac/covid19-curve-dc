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
plt.ylabel("Cases")

plt.bar(casedata.x,casedata.positive,color='y',width=1.0)
plt.bar(casedata.x,casedata.recovered,
        bottom=casedata.positive-casedata.recovered,color='g',width=1.0)
plt.bar(casedata.x,casedata.deaths,color='r',width=1.0)

plt.legend(labels=['Positives','Recovered positives','Deaths'])

if "FIG_PATH" in os.environ:
    fig_path = os.environ['FIG_PATH']
else:
    fig_path = "."

plt.savefig("{0}/us_dc_cases.png".format(fig_path),dpi=300,bbox_inches="tight")
