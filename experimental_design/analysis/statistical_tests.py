"""A module for storing general statistical test functions"""

import scipy.stats as st

def _distribution_gettter(distribution, *args, **kwargs):
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


def upper_CI(distribution, alpha, *args, **kwargs):
    dist_obj = _distribution_gettter(distribution, *args, **kwargs)
    return dist_obj.isf(1-alpha)


def lower_CI(distribution, alpha, *args, **kwargs):
    pass


def central_CI(distribution, alpha, *args, **kwargs):
    pass


def upper_prob():
    pass


def lower_prob():
    pass


def central_prob():
    pass










