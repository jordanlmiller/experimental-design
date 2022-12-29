"""A module for analyzing the statistical power of a prospective experiment"""

import numpy as np
import scipy.stats as st

def test_power(alpha: float, delta: float, r: int, v: int, variance: float) -> float:
    """
    return the power of the f-test

    Parameters
    ----------
    alpha : float in the interval [0, 1]
        probablity of Type I error
    delta : float
        difference in means
    r : int
        number of observations at each treatment level
    v : int
        number of treatment levels
    variance: float
        variance of the observations

    Returns
    -------
    power : float
        the power of the test, 1 - beta


    """ 
    #degrees of freedom
    dfn = v - 1
    dfd = v * ( r - 1 )   
    #phi
    nc = (r * (delta**2) / (2 * variance))
    Falpha = st.f.isf(alpha, dfn, dfd)
    power = st.ncf.sf(Falpha, dfn, dfd, nc)
    return power


def num_observations(alpha: float, beta: float, delta: float, v: int, variance: float) -> int:
    """
    return the number of observations taken at each treatment level necessary
    to produce a test with a given power

    Parameters
    ----------
    alpha : float in the interval [0, 1]
        probablity of Type I error
    beta : float in the interval [0, 1]
        probability of Type II error
    delta : float
        difference in means
    v : int
        number of treatment levels
    variance: float
        variance of the observations

    Returns
    -------
    r : int
        number of required observations 


    """ 
    test_power = 0
    r = 2
    while test_power(alpha, delta, r, v, variance) < (1-beta):
        r += 1
    return r



