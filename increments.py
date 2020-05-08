import matplotlib.pyplot as plt
import numpy as np
import os

import get_dc_data

# Differential figure.

casedata = get_dc_data.retrieve()

f2 = plt.figure(figsize=(6,4))
plt.suptitle("COVID-19 Case Increments, District of Columbia ",
             fontweight="bold")
plt.title("github.com/reidac/covid19-curve-dc", style="oblique")
plt.xlabel("Case count")
plt.ylabel("Case increment")

dx = casedata.positive[:-1]
dy = np.array([casedata.positive[i+1]-casedata.positive[i]
               for i in range(len(dx))])

plt.scatter(dx,dy,marker="o",s=10,color="k",zorder=10)

if "FIG_PATH" in os.environ:
    fig_path = os.environ['FIG_PATH']
else:
    fig_path = "."

plt.savefig("{0}/us_dc_diff.png".format(fig_path),dpi=300,bbox_inches="tight")
