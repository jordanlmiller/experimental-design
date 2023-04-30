"""A module for storing general statistical test functions"""

import scipy.stats as st
import numpy as np

def _distribution_gettter(distribution: str, *args, **kwargs):
    """return instance of scipy.stats.rv_continuous corresponding to keyword"""
    if distribution == "normal":
        dist_obj = st.norm(*args, **kwargs)
    elif distribution == "t":
        dist_obj = st.t(*args, **kwargs)
    elif distribution == "chi-squared":
        dist_obj = st.chi2(*args, **kwargs)
    elif distribution == "f":
        dist_obj = st.f(*args, **kwargs)
    elif distribution == "ncf":
        dist_obj = st.ncf(*args, **kwargs)
    else:
        raise Exception("Distribution '{d}', is not understood".format(d=distribution))
    return dist_obj


def upper_CI(distribution: str, alpha: float, *args, **kwargs):
    dist_obj = _distribution_gettter(distribution, *args, **kwargs)
    return dist_obj.isf(alpha)


def lower_CI(distribution: str, alpha: float, *args, **kwargs):
    dist_obj = _distribution_gettter(distribution, *args, **kwargs)
    return dist_obj.ppf(alpha)


def central_CI(distribution: str, alpha: float, *args, **kwargs):
    dist_obj = _distribution_gettter(distribution, *args, **kwargs)
    return [dist_obj.ppf(alpha/2), dist_obj.isf(alpha/2)]


def upper_prob(distribution: str, x: float, *args, **kwargs):
    dist_obj = _distribution_gettter(distribution, *args, **kwargs)
    return dist_obj.sf(x)


def lower_prob(distribution: str, x: float, *args, **kwargs):
    dist_obj = _distribution_gettter(distribution, *args, **kwargs)
    return dist_obj.cdf(x)


def central_prob(distribution: str, x1: float, x2: float, *args, **kwargs):
    """return probability associated  with region between x2 and x1"""
    dist_obj = _distribution_gettter(distribution, *args, **kwargs)
    return np.abs(dist_obj.cdf(x2) - dist_obj.cdf(x1))


def one_sample_mean_diff(sample_mean: float, pop_mean: float, pop_var: float, n: int, *args, **kwargs):
    z_value = np.abs((sample_mean - pop_mean) / (pop_var / np.sqrt(n)))
    return 2*upper_prob("normal", z_value)













