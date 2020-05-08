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
plt.xlabel("Days from onset")
# plt.ylabel("Cases")

plt.bar(casedata.x,casedata.total,bottom=casedata.positive,color='b')
plt.bar(casedata.x,casedata.positive,bottom=casedata.recovered,color='r')
plt.bar(casedata.x,casedata.recovered,color='g')

plt.legend(labels=['Tests','Positives','Recoveries'])

if "FIG_PATH" in os.environ:
    fig_path = os.environ['FIG_PATH']
else:
    fig_path = "."

plt.savefig("{0}/us_dc_bars.png".format(fig_path),dpi=300,bbox_inches="tight")
