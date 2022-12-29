"""A module for performing contingency analysis on an observational dataset"""

import numpy as np
import pandas as pd


def contingency_table(df, a, b):
    """
    Construct a contingency table from a pandas DataFrame for two variables
    
    Parameters
    ----------
    df : pandas.DataFrame
        pandas DataFrame containing experimental data
    a : string
        the name of the column in the DataFrame corresponding to the first variable of interest
    b : string
        the name of the column in the DataFrame corresponding to the second variable of interest    
    
    Returns
    -------
    contingency_table : pandas.DataFrame
        pandas DataFrame containing contingency table
        

        
    """
    a_levels = np.unique(df[a])
    b_levels = np.unique(df[b])

    #The columns will represents the a value while the rows will represent the b value
    contingency_table[""] = np.concatenate(b_levels, np.array(["Total"]))

    #add each column associated with each a value
    nrows = b_levels.shape[0]
    for i, a_lvl_value in enumerate(a_levels):
        column = np.zeros(nrows+1)
        for j, b_lvl_value in enumerate(b_levels):
            column[j] = np.sum((df[a]==a_lvl_value) * (df[b]==b_lvl_value))
        column[-1] = np.sum(column)
        contingency_table[a_lvl_value] = column
    
    #add a final totals column
    contingency_table["Total"] = [sum([contingency_table[a_lvl][b_lvl] for a_lvl in a_levels]) for b_lvl in b_levels]

    return pd.DataFrame(contingency_table)