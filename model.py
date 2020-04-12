
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


def fitchecker(func):
    def _fitchecker(self,*args,**kwargs):
        if (self.fitted):
            return func(self,*args,**kwargs)
        else:
            raise ModelError(str(self.__class__))
    return _fitchecker
            
class Model:
    def __init__(self,d):
        self.fitted = False
        self.params = [1]*d
        self.deltas = [0]*d
        self.sglist = []

    def fit(self,xdata,ydata):
        popt,pcov = curve_fit(self.model, xdata, ydata,
                              p0=self.params,sigma=None,method="lm",
                              jac=self.jacobian)
        self.params = popt
        self.deltas = np.sqrt(np.diag(pcov))
        self.fitted = True

    @fitchecker
    def evaluate(self,t):
        return self.model(t,*self.params)
        
    def _evaluate_all_deltas(self,t):
        # Returns a list of all the hypercube corner points.
        # Because of the trickery, this function can only take scalar
        # arguments for t.

        # Generator for the possible sign combinations.
        def _allsigns(n):
            signset = [-1,1]
            if (n==1):
                for s in signset:
                    yield [s]
            else:
                for s in signset:
                    for tail in _allsigns(n-1):
                        yield [s]+tail
        
        res = []
        for sg in _allsigns(len(self.deltas)):
            params = [ p+s*d for (p,s,d) in zip(self.params,sg,self.deltas) ]
            res.append(self.model(t,*params))
        return res

    @fitchecker
    def evaluate_h(self,t):
        if type(t) is np.ndarray:  # AAAAAAARGH!
            return np.array( [max(self._evaluate_all_deltas(ti)) for
                                      ti in t] )
        else:
            return max(self._evaluate_all_deltas(t))

    @fitchecker
    def evaluate_l(self,t):
        if type(t) is np.ndarray: # See above.
            return np.array( [min(self._evaluate_all_deltas(ti)) for
                              ti in t])
        else:
            return min(self._evaluate_all_deltas(t))

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
# without parameter arguments, and _l and _h vectors should bracket
# the evaluation vector.  Evaluate should work with both scalar
# and np.ndarray-type arguments.

if __name__=="__main__":
    xvs = np.array([0.0, 1.0, 2.0, 3.0,4.0])
    yvs = np.array([1.0, 1.1, 1.2, 1.3,1.4])

    m1 = Exponential()
    try:
        m1.evaluate(0.0)
    except ModelError as m:
        print(m)

    m1.fit(xvs,yvs)
    print (m1.evaluate(4.0))
    print (m1.evaluate_h(4.0))
    print (m1.evaluate_l(4.0))

    print (m1.evaluate_l(xvs))
    print (m1.evaluate(xvs))
    print (m1.evaluate_h(xvs))
    
    m2 = Logistic()
    try:
        m2.evaluate(0.0)
    except ModelError as m:
        print(m)
        
    m2.fit(xvs,yvs)
    print (m2.evaluate(4.0))
    print (m2.evaluate_h(4.0))
    print (m2.evaluate_l(4.0))

    print (m2.evaluate_l(xvs))
    print (m2.evaluate(xvs))
    print (m2.evaluate_h(xvs))
    
