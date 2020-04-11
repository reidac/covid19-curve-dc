# Extrapolated COVID-19 Infections

Ported from @psteinb's excellent chart for [Dresden, Germany](https://github.com/psteinb/covid19-curve-your-city)

Then ported again from @tkphd's chart for 
[Montgomery County, Maryland](https://github.com/tkphd/covid19-curve-your-county)

## District of Columbia, USA

![DC](us_dc_exp.png)

Data source: https://covidtracking.com/api/states/daily?state=DC

The fitting process used in this analysis gives a covariance matrix for
the model parameters, and from this matrix, it's possible to derive 
one-sigma bounds on the parameters, assuming that the uncertainty on
all of the input data points are the same. 

The gray bands are the plus-one-sigma (upper) and minus-one-sigma (lower)
deviations from the least-squares fit.

A second figure is also available, showing the daily case increment as
a function of the total number of reported cases.  A feature of 
exponential growth is that the rate of growth of the system is 
proportional to the size of the system.  This figure visually
tests that hypothesis, and illustrates the large amount of noise
in the data.
![deltaDC](us_dc_diff.png)

## Reproduce This!

1. Install [Python](https://www.anaconda.com/distribution/)
2. Install dependencies

   ```bash
   $ conda install matplotlib numpy pandas scipy
   ```

3. Run the `exponential.py` script.

   ``` 
   $ python exponential.py
   ```

  For this version, the script will make a GET query to the Covid tracking site and pull
  down the relevant data and parse the JSON. 

   Gaps in the data are OK, just provide what you have. You will want to edit the script to set the
   proper place-name and URL in the title.

4. Share your findings to help others assess the spread of SARS-CoV-2, and to gauge the
   effectiveness of our collective response.
