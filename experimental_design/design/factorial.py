"""Template for designing multi-factorial experiments"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def factorial_table(treatments):
    """
    Parameters
    ----------

    treatments: dict
        dictionary of treatment names and treatment levels

    Returns
    -------

    experiment_table: pandas.DataFrame
        experiment template dataframe

    """
    experiment_dict = {}
    v = []
    for factor in treatments.keys():
        if not isinstance(treatments[factor], list):
            treatments[factor] = list(treatments[factor])
        v.append(len(treatments[factor]))

    n = list_product(v)

    for i, factor in zip(range(len(v)), treatments.keys()):
        factor_treatments = []
        for level in treatments[factor]:
            factor_treatments += [level]*(n // (list_product(v[:i]) * v[i]))
        experiment_dict[factor] = factor_treatments*(n // (list_product(v[i+1:]) * v[i]))

    experiment_dict["Run_Order"] = np.random.permutation(n)
    return pd.DataFrame(experiment_dict)



def list_product(l):
    product = 1
    for element in l:
        product *= element
    return product

        
        
