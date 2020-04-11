# -*- coding: utf-8 -*-
# Based on https://stackoverflow.com/questions/24633664/confidence-interval-for-exponential-curve-fit/37080916#37080916

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from time import strptime
from datetime import date
from scipy.optimize import curve_fit
from scipy.stats import describe, t
import os

def model(t,a,b,c):
    return c / (np.exp((b - t)/a) + 1)
    
def jacobian(t,a,b,c):
    return np.array([c*(b - t)*np.exp((b - t)/a)/(a**2*(np.exp((b - t)/a) + 1)**2),
                     -c*np.exp((b - t)/a)/(a*(np.exp((b - t)/a) + 1)**2),
                     1/(np.exp((b - t)/a) + 1)]).T

start_n = 10


# Data

import get_dc_data
casedata = get_dc_data.retrieve()

# The new improved CaseData object promises us data
# sorted in order of increasing x.
x = casedata.x
y = casedata.y

# Do an initial fit to the whole data set to get the bounds.
popt,pcov = curve_fit(model, x, y, p0=[1,1,1],sigma=None, method="lm",
                      jac=jacobian)
perr = np.sqrt(np.diag(pcov))
coef = describe(pcov)

bhat = np.linspace(0, casedata.today-casedata.start+7, 100)

upper = model(bhat, popt[0]+perr[0], popt[1]+perr[1], popt[2]+perr[2])

global_xlim = [0, bhat[-1]]
global_ylim = [0, upper[-1]]


# For each day from start_n to the end, draw the figure.
for panel in range(start_n,len(x)):

    fig = plt.figure(figsize=(6, 4))
    plt.suptitle("COVID-19 Cases: District of Columbia", fontweight="bold")
    plt.title("github.com/reidac/covid19-curve-dc", style="oblique")
    plt.xlabel("Day of Record")
    plt.ylabel("# Diagnosed Cases")

    plt.scatter(x[:panel], y[:panel], marker=".", s=10, color="k", zorder=10)

    # Levenburg-Marquardt Least-Squares Fit
    
    popt,pcov = curve_fit(model, x[:panel], y[:panel], p0=[1,1,1],
                          sigma=None, method="lm", jac=jacobian)

    perr = np.sqrt(np.diag(pcov))
    coef = describe(pcov)

    a, b, c = popt

    # Use casedata, not the trailing item in the list, which for us
    # is not the largest abscissa!
    xhat = np.linspace(0, casedata.today-casedata.start+7, 100)
    yhat = model(xhat,a,b,c)

    upr_a = a+perr[0]
    upr_b = b+perr[1]
    upr_c = c+perr[2]
    
    lwr_a = a-perr[0]
    lwr_b = b-perr[1]
    lwr_c = c-perr[2]
    
    upper = model(xhat, upr_a, upr_b, upr_c)
    lower = model(xhat, lwr_a, lwr_b, lwr_c)

    ix = np.argsort(xhat)
    plt.plot(xhat[ix], yhat[ix], c="red", lw=1, zorder=5)
    plt.fill_between(
        xhat[ix], upper[ix], yhat[ix], edgecolor=None,
        facecolor="silver", zorder=1
    )
    plt.fill_between(
        xhat[ix], lower[ix], yhat[ix], edgecolor=None,
        facecolor="silver", zorder=1
    )

    # Plot Boundaries

    plt.xlim(global_xlim)
    plt.ylim(global_ylim)

    if "FIG_PATH" in os.environ:
        fig_path = os.environ['FIG_PATH']
    else:
        fig_path = "."

        plt.savefig("{0}/us_dc_logpanel_{1:02d}.png".format(fig_path,panel),
                    dpi=150, bbox_inches="tight")
    plt.close()

# Then you can maybe generate an animated gif or something.
# convert -delay 20 -loop 0 <pattern> <name>.gif
