# -*- coding: utf-8 -*-
# Based on https://stackoverflow.com/questions/24633664/confidence-interval-for-exponential-curve-fit/37080916#37080916

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from kapteyn import kmpfit
from time import strptime
from datetime import date
from scipy.stats import t

"""
Logistic Curve, via SymPy

y    = c/(exp((b - x)/a) + 1)
dyda = c*(b - x)*exp((b - x)/a)/(a**2*(exp((b - x)/a) + 1)**2)
dydb = -c*exp((b - x)/a)/(a*(exp((b - x)/a) + 1)**2)
dydc =  1/(exp((b - x)/a) + 1)
"""


def model(p, x):
    a, b, c = p
    return c / (np.exp((b - x) / a) + 1)


fig = plt.figure(figsize=(6, 4))
plt.suptitle("COVID-19 Cases: Montgomery County, MD")
plt.title("github.com/tkphd/covid19-curve-your-county")
plt.xlabel("# Days")
plt.ylabel("# Diagnosed Cases")

# Data

df = pd.read_csv("us_md_montgomery.csv")

y = np.array(df["diagnosed"])
start = strptime(df["date"].iloc[0], "%Y-%m-%d").tm_yday
today = strptime(df["date"].iloc[-1], "%Y-%m-%d").tm_yday

x = np.zeros_like(y)
for i in range(len(x)):
    x[i] = strptime(df["date"].iloc[i], "%Y-%m-%d").tm_yday - start

plt.scatter(x, y, marker=".", s=10, color="k", zorder=10)

# Levenburg-Marquardt Least-Squares Fit

f = kmpfit.simplefit(model, [1, 1, 1], x, y)
a, b, c = f.params

print("cases ~ {0:.1f}/(1 + exp(({1:.1f} - t)/{2:.1f}))".format(c, b, a))

# Confidence Band: dfdp represents the partial derivatives of the model with respect to each parameter p (i.e., a, b, and c)

xhat = np.linspace(0, x[-1] + 7, 100)
dfdp = np.array([
    c * (b - xhat) * np.exp((b - xhat) / a) / (a** 2 * (np.exp((b - xhat) / a) + 1)** 2),
    -c * np.exp((b - xhat) / a) / (a * (np.exp((b - xhat) / a) + 1)** 2),
    1 / (np.exp((b - xhat) / a) + 1)
])
level = 0.95
yhat, upper, lower = f.confidence_band(xhat, dfdp, level, model)
ix = np.argsort(xhat)
plt.plot(xhat[ix], yhat[ix], c="red", lw=1, zorder=5)
plt.fill_between(
    xhat[ix], upper[ix], yhat[ix], edgecolor=None, facecolor="silver", zorder=1
)
plt.fill_between(
    xhat[ix], lower[ix], yhat[ix], edgecolor=None, facecolor="silver", zorder=1
)

# Plot Boundaries

plt.xlim([0, xhat[-1]])
plt.ylim([0, upper[-1]])

# Predictions

tomorrow = date.fromordinal(today + 1)
nextWeek = date.fromordinal(today + 7)

xhat = np.array([tomorrow.toordinal() - start, nextWeek.toordinal() - start])
dfdp = np.array([
    c * (b - xhat) * np.exp((b - xhat) / a) / (a ** 2 * (np.exp((b - xhat) / a) + 1) ** 2),
    -c * np.exp((b - xhat) / a) / (a * (np.exp((b - xhat) / a) + 1) ** 2),
    1 / (np.exp((b - xhat) / a) + 1)
])
yhat, upper, lower = f.confidence_band(xhat, dfdp, level, model)
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

plt.savefig("us_md_montgomery.png", dpi=400, bbox_inches="tight")