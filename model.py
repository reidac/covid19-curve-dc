
from scipy.optimize import curve_fit
from scipy.stats import describe
import numpy as np


# Stateful model objects that know when they've been
# fitted, and whose API is agnostic about the number
# of parameters.
class ModelError(Exception):
    def __init__(self, clstr):
        self.clstr = clstr
    def __str__(self):
        return "ModelError: Attempt to evaluate {0} before fitting.".format(self.clstr)
    
class Model:
    def __init__(self,d):
        self.fitted = False
        self.params = [1]*d
        self.deltas = [0]*d
    def fit(self,xdata,ydata):
        popt,pcov = curve_fit(self.model, xdata, ydata,
                              p0=self.params,sigma=None,method="lm",
                              jac=self.jacobian)
        self.params = popt
        self.deltas = np.sqrt(np.diag(pcov))
        self.fitted = True
    def evaluate(self,t):
        if (self.fitted):
            return self.model(t,*self.params)
        else:
            raise ModelError(str(self.__class__))
    def evaluate_h(self,t):
        if (self.fitted):
            h_params = [x+d for (x,d) in zip(self.params,self.deltas)]
            return self.model(t,*h_params)
        else:
            raise ModelError(str(self.__class__))
    def evaluate_l(self,t):
        if (self.fitted):
            l_params = [x-d for (x,d) in zip(self.params,self.deltas)]
            return self.model(t,*l_params)
        else:raise ModelError(str(self.__class__))
                            

class Exponential(Model):
    def __init__(self):
        Model.__init__(self,2)
    def model(self,t,*p):
        return p[0]*(1+p[1])**t
    def jacobian(self,t,*p):
        return np.array([(1+p[1])**t,(p[0]*t*(1+p[1])**t)/(1+p[1])]).T


class Logistic(Model):
    def __init__(self):
        Model.__init__(self,3)
    def model(self,t,*p):
        return p[2] / (np.exp((p[1] - t)/p[0]) + 1)
    def jacobian(self,t,*p):
        return np.array([p[2]*(p[1] - t)*
                         np.exp((p[1] - t)/p[0])/
                         (p[0]**2*(np.exp((p[1] - t)/p[0]) + 1)**2),
                         -p[2]*np.exp((p[1] - t)/p[0])/
                         (p[0]*(np.exp((p[1] - t)/p[0]) + 1)**2),
                         1/(np.exp((p[1] - t)/p[0]) + 1)]).T

# When run stand-alone, do some testing.  The exceptions
# should name the child class, the evaluations should work
# without parameter arguments, and the last call should
# return a vector of evaluations with the fitted parameters.
if __name__=="__main__":
    x = np.array([0.0, 1.0, 2.0, 3.0,4.0])
    y = np.array([1.0, 1.1, 1.2, 1.3,1.4])

    m1 = Exponential()
    try:
        m1.evaluate(0.0)
    except ModelError as m:
        print(m)

    m1.fit(x,y)
    print (m1.evaluate(4.0))
    print (m1.evaluate_h(4.0))
    print (m1.evaluate_l(4.0))
    
    m2 = Logistic()
    try:
        m2.evaluate(0.0)
    except ModelError as m:
        print(m)

    m2.fit(x,y)
    print (m2.evaluate(4.0))
    print (m2.evaluate_h(4.0))
    print (m2.evaluate_l(4.0))

    print (m2.evaluate(x))
    
