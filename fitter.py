# -*- coding: utf-8 -*-
# Based on https://stackoverflow.com/questions/24633664/confidence-interval-for-exponential-curve-fit/37080916#37080916

import matplotlib.pyplot as plt
import numpy as np
from datetime import date
from scipy.stats import describe
import os

def figurize(mdl,sfx):
    # Arguments are a model object and a suffix for the filename.
    fig = plt.figure(figsize=(6, 4))
    plt.suptitle("COVID-19 Cases: District of Columbia", fontweight="bold")
    plt.title("github.com/reidac/covid19-curve-dc", style="oblique")
    plt.xlabel("Day of Record")
    plt.ylabel("# Diagnosed Cases")

    # Data

    import get_dc_data
    casedata = get_dc_data.retrieve()

    # The new improved CaseData object promises us data
    # sorted in order of increasing x.
    x = casedata.x
    y = casedata.y
    
    plt.scatter(x, y, marker=".", s=10, color="k", zorder=10)

    # Levenburg-Marquardt Least-Squares Fit

    mdl.fit(x,y)

    # print("cases ~ {0:.2g} * (1 + {1:.2g})^t".format(a, b))

    # Confidence Band: dfdp represents the partial derivatives of
    # the model with respect to each parameter p (i.e., a and b)

    # Use casedata, not the trailing item in the list, which for us
    # is not the largest abscissa!
    xhat = np.linspace(0, casedata.today-casedata.start+7, 100)
    yhat = mdl.evaluate(xhat)

    upper = mdl.evaluate_h(xhat)
    lower = mdl.evaluate_l(xhat)

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

    plt.xlim([0, xhat[-1]])
    plt.ylim([0, upper[-1]])

    # Predictions

    tomorrow = date.fromordinal(casedata.today + 1)
    nextWeek = date.fromordinal(casedata.today + 7)

    # print(tomorrow.toordinal()-casedata.start)
    # print(nextWeek.toordinal()-casedata.start)
    xhat = np.array([tomorrow.toordinal() - casedata.start,
                     nextWeek.toordinal() - casedata.start])

    yhat = mdl.evaluate(xhat)
    upper = mdl.evaluate_h(xhat)
    lower = mdl.evaluate_l(xhat)

    dx = 0.25

    plt.text(
        dx,
        yhat[0],
        "{0}/{1}: ({2:.0f} < {3:.0f} < {4:.0f})".format(
            tomorrow.month, tomorrow.day, lower[0], yhat[0], upper[0]
        ),
        va="center",
        zorder=5,
        bbox=dict(boxstyle="round", ec="black", fc="white", linewidth=dx),
    )
    plt.text(
        dx,
        yhat[1],
        "{0}/{1}: ({2:.0f} < {3:.0f} < {4:.0f})".format(
            nextWeek.month, nextWeek.day, lower[1], yhat[1], upper[1]
        ),
        va="center",
        zorder=5,
        bbox=dict(boxstyle="round", ec="black", fc="white", linewidth=dx),
    )

    hw = (upper[1] - lower[1]) / 50
    hl = xhat[1] / 100

    plt.arrow(
        dx,
        yhat[0],
        xhat[0] - dx - 0.0625,
        0,
        fc="black",
        ec="black",
        head_width=hw,
        head_length=hl,
        overhang=dx,
        length_includes_head=True,
        linewidth=0.5,
        zorder=2,
    )
    plt.arrow(
        dx,
        yhat[1],
        xhat[1] - dx - 0.0625,
        0,
        fc="black",
        ec="black",
        head_width=hw,
        head_length=hl,
        overhang=dx,
        length_includes_head=True,
        linewidth=0.5,
        zorder=2,
    )

    # Save figure
    
    if "FIG_PATH" in os.environ:
        fig_path = os.environ['FIG_PATH']
    else:
        fig_path = "."

        plt.savefig("{0}/us_dc_{1}.png".format(fig_path,sfx), dpi=300,
                    bbox_inches="tight")

if __name__=="__main__":

    import model
    m = model.Exponential()
    figurize(m,"exp")
    
