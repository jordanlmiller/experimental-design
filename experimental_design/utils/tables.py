"""Module for storing classes representing different data tables"""

from pandas import DataFrame
from IPython.display import display

class Anova_Table(DataFrame):
    """A Template for Anova Tables
    
    Parameters
    ----------
    sov : list
        list containing sources of variation
    dof : list
        list containing degrees of freedom for each source of variation
    ms : list
        list containing mean squares
    fvalue : list
        list containing the F-values
    pvalue : list
        list containing the p-values of each source of variation
    """

    def __init__(self, sov: list, dof: list, ms: list, fvalue: list, pvalue: list):
        data = {
            "Source of Variation" : sov,
            "Degrees of Freedom" : dof,
            "Mean Square" : ms,
            "F-Value" : fvalue,
            "P-Value" : pvalue,
        }
        n = len(sov)
        super().__init__(self, data, [""]*n)

class DOM_Table(DataFrame):
    """A Template for Difference of Means Tables
    
    Parameters
    ----------
    """

    def __init__(self):
        super().__init__(self)



sov = ["Treatment", "Error", "Total"]
dof = [3, 13, 15]
ms = [123, 432, 421]
fvalue = [234, 523, 51]
pvalue = [123, 123, ""]

print("test")
#print(Anova_Table(sov, dof, ms, fvalue, pvalue))
