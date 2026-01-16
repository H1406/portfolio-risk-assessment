import pandas as pd
import numpy as np

def calculate_log_returns(prices):
    """
    Calculate the daily returns for each asset in the DataFrame.
    Assumes the first column is 'DATE' and subsequent columns are asset prices.

    Parameters:
    data (pd.DataFrame): DataFrame containing asset prices with a 'DATE' column.

    Returns:
    pd.DataFrame: DataFrame containing daily returns for each asset.
    """
    return (prices/prices.shift(1)).apply(np.log).dropna()

def calculate_simple_returns(prices):
    """
    Calculate the simple daily returns for each asset in the DataFrame.
    Assumes the first column is 'DATE' and subsequent columns are asset prices.

    Parameters:
    data (pd.DataFrame): DataFrame containing asset prices with a 'DATE' column.

    Returns:
    pd.DataFrame: DataFrame containing simple daily returns for each asset.
    """
    return prices.pct_change().dropna()
