# -*- coding: utf-8 -*-

# Driver for the logistic version of the fitting process.

import model
import fitter

m = model.Logistic()
# The guess is the solution from April 13.  Fixes some
# numerical stability issues in the model related to
# bad initial guesses.
fitter.figurize(m,"log",guess=[5.03091769,30.44230917,2632.41090794] )

