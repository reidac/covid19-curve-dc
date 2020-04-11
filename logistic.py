# -*- coding: utf-8 -*-

# Driver for the logistic version of the fitting process.

import model
import fitter

m = model.Logistic()
fitter.figurize(m,"log")
