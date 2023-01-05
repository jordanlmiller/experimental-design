"""Module containing functions related to the Anova class and its methods"""

import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as plt


class Anova:
    """Class for performing Single Anova"""

    def __init__(self, df: pd.DataFrame, x: str, y: str):
        """
        Perform ANOVA on a dataset in the form of a pandas dataframe where each column represents\n
        a different factor.
        
        Parameters
        ----------
        df : pandas.DataFrame
            pandas DataFrame containing experimental data
        x : string
            name of the column representing the dependent variable
        y : string
            name of the column representing the dependent variable
            

            
        """
        self.x = x
        self.y = y
        self.xdata = df[self.x]
        self.ydata = df[self.y]

        """check that the inputs are the correct type for anova"""
        #check that the input, df, is a pandas DataFrame
        if not isinstance(df, pd.DataFrame):
            raise TypeError("The input, df, must be a pandas DataFrame. Given input is {}".format(type(self.df))) 
        #check that the input, x, is a string
        if not isinstance(self.x, str):
            raise TypeError("The input, x, must be a string. Given input is {}".format(type(self.x)))
        #check that the input, y, is a string
        if not isinstance(self.y, str):
            raise TypeError("The input, y, must be a string. Given input is {}".format(type(self.y)))
        #check that the inputs x and y correspond to columns of the DataFrame, df
        if not self.x in df.columns:
            raise LookupError("{} is not a column in the given DataFrame".format(self.x))
        if not self.y in df.columns:
            raise LookupError("{} is not a column in the given DataFrame".format(self.y))

        #calculate average over all observations
        self.n = len(df)
        self.grand_total = np.sum(df[self.y])
        self.grand_average = self.grand_total / self.n
        
        #Total
        self.sstot = np.sum(df[self.y]**2) - (self.n * self.grand_average**2)
        self.total_dof = self.n - 1
        
        #Treatment
        self.treatment_lvls = np.unique(df[self.x])
        self.v = self.treatment_lvls.shape[0]
        self.r = np.zeros(self.v)
        self.treatment_dof = self.v - 1
        self.treatment_lvl_avg = np.zeros(self.v)
        self.treatment_lvl_std = np.zeros(self.v)
        for i, treatment_lvl in enumerate(self.treatment_lvls):
            self.r[i] = np.sum(df[self.x] == treatment_lvl)
            self.treatment_lvl_avg[i] = np.mean(df[self.y][df[self.x] == treatment_lvl])
            self.treatment_lvl_std[i] = np.std(df[self.y][df[self.x] == treatment_lvl])
        #least squares treatment fitting parameters
        self.tau = self.treatment_lvl_avg - self.grand_average
        #Sum of squares for treatments
        self.ssT = np.dot(self.r, self.treatment_lvl_avg**2) - (self.n * self.grand_average**2)
        self.msT = self.ssT / self.treatment_dof
        self.r_squared = self.ssT / self.sstot
            
        #Error
        self.ssE = np.sum(df[self.y]**2) - np.dot(self.treatment_lvl_avg**2, self.r)
        self.error_dof = self.total_dof - self.treatment_dof
        self.msE = self.ssE / self.error_dof
                
        #generate ANOVA table        
        anova_dict = {
            "Source of Variation" : [self.x, "Error", "Total"],
            "Degrees of Freedom" : [self.treatment_dof, self.error_dof, self.total_dof],
            "Sum of Squares" : [self.ssT, self.ssE, self.sstot],
            "Mean Square" : [self.msT, self.msE, ""],
            "Ratio" : [self.msT / self.msE, "", ""],
            "p-Value" : [st.f.sf(self.msT / self.msE, self.treatment_dof, self.error_dof), st.chi2.sf(self.msE, self.error_dof), ""]
        }
        self.anova_table = pd.DataFrame(anova_dict)


    def contrast_pvalue(self, contrast: np.array, bound="two-sided",  equal_variance=True) -> float:
        """return the p-value associated with an arbitrary contrast"""
        #estimate of the standard deviation
        if equal_variance:
            std_estimate = np.sqrt(self.msE * np.sum(np.divide(contrast**2, self.r)))
        else:
            std_estimate = np.sqrt(np.dot(self.treatment_lvl_std , np.divide(contrast**2, self.r)))
        mean_estimate = np.dot(contrast, self.treatment_lvl_avg)

        if bound == "upper":
            return st.t.sf((mean_estimate) / (std_estimate), self.error_dof, scale=std_estimate)
        elif bound == "lower":
            return st.t.cdf((mean_estimate) / (std_estimate), self.error_dof, scale=std_estimate)
        elif bound == "two-sided":
            return st.f.sf((mean_estimate)**2 / (std_estimate**2), 1, self.error_dof)
        else:
            raise Exception("The bound must be 'upper', 'lower', or 'two-sided'. The given bound was {}.".format(bound))


    def contrast_confidence_bound(self, contrast: np.array, confidence: float, bound="two-sided",  equal_variance=True) -> tuple:
        """return the confidence interval for an arbitrary contrast"""
        if not (confidence >= 0. and confidence <= 1.):
            raise Exception("Confidence must be a float between 0 and 1. The given confidence was {}.".format(confidence))

        #estimate of the standard deviation
        if equal_variance:
            std_estimate = np.sqrt(self.msE * np.sum(np.divide(contrast**2, self.r)))
        else:
            std_estimate = np.sqrt(np.dot(self.treatment_lvl_std , np.divide(contrast**2, self.r)))
        mean_estimate = np.dot(contrast, self.treatment_lvl_avg)

        if bound == "upper":
            return mean_estimate + st.t.isf(1-confidence, self.error_dof, scale=std_estimate)
        elif bound == "lower":
            return mean_estimate - st.t.isf(1-confidence, self.error_dof, scale=std_estimate)
        elif bound == "two-sided":
            return st.t.interval(confidence, self.error_dof, loc=mean_estimate, scale=std_estimate)
        else:
            raise Exception("The bound must be 'upper', 'lower', or 'two-sided'. The given bound was {}.".format(bound))


    def scheffe(alpha: float):
        pass

    def tukey():
        pass

    def dunnett():
        pass

    def scatter(self, confidence=0.95):
        """generate a scatter plot of the data"""
        fig = plt.figure(figsize=(6,6), dpi=300, tight_layout=True)

        #check if the independent variable is categorical        

        #plot all data points
        plt.scatter(self.xdata, self.ydata)
        for i, avg in enumerate(self.treatment_lvl_avg):
            yerror = st.t.isf((1-confidence)/2, self.error_dof) * np.sqrt(self.msE / self.r[i])
            plt.errorbar(self.treatment_lvls[i], avg, yerr=yerror, color='y')
        
        #format plot
        plt.xticks(ticks=self.treatment_lvls, labels=self.treatment_lvls)#, minor=False)
        plt.xlabel(self.x)
        plt.ylabel(self.y)

        plt.savefig("test.png")

