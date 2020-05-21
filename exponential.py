# -*- coding: utf-8 -*-

# Driver for the exponential version of the fitting process.

import model
import fitter

m = model.Exponential()
# "Guess" is approximately the May 20 result.
fitter.figurize(m,"exp",guess=[440,0.04])
