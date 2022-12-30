"""A module containing functions which generate contrasts"""

import numpy as np

def linear_trend_contrast(r: np.ndarray, x: np.ndarray) -> np.ndarray:
    """
    Generate the contrasts necessary to determine a linear trend

    Parameters
    ----------
    r : array_like, int
        number of observations at each treatment level
    x : array_like, float
        the treatment levels


    Returns
    -------
    c : array_like, float
        contrast coefficients  

    """
    level_averages = np.dot(r, x) / r.shape[0]
    c = r * (x - level_averages)
    return c


def polynomial_trend_contrast(r: np.ndarray, x: np.ndarray, n: int) -> np.ndarray:
    """
    Generate the constrasts necessary to determine a polynomial trend of order n

    Parameters
    ----------
    r : array_like, int
        number of observations at each treatment level
    x : array_like, float
        treatment levels
    n : int
        order of the polynomial


    Returns
    -------
    c : array_like, float
        contrast coefficients  

    """
    pass


def group_difference(a: list, b: list):
    """
    Contrast for comparing the means of two groups
    
    Parameters
    ----------
    a : list
        first list of treatment levels
    b : list
        second list of treatment levels


    Returns
    -------
    c : array_like, float
        contrast coefficients

    """
    pass