import pandas as pd
from returns import calculate_log_returns, calculate_simple_returns
from risk_metrics import calculate_var
from data_loader import load_data
import numpy as np


VN30_FILE_PATH = './data/raw/historical_prices_E1VFVN30.csv'
xautusd_FILE_PATH = './data/raw/historical_prices_XAUTUSD.csv'
btcusd_FILE_PATH = './data/raw/historical_prices_BTCUSD.csv'

def calculate_correlation(prices_A, prices_B) -> float:
    """
    Calculate the correlation coefficient between two assets' prices.
    Parameters:
    prices_A (pd.Series): Price series of asset A.
    prices_B (pd.Series): Price series of asset B.
    Returns:
    float: Correlation coefficient between asset A and asset B.
    """
    return prices_A.corr(prices_B)

def calculate_portfolio_var(prices, weights: np.ndarray, confidence_level: float = 0.95):
    """
    Calculate the Value at Risk (VaR) for a portfolio of assets.
    
    Parameters:
    prices (dict or pd.DataFrame): Dictionary of asset prices or DataFrame with asset price columns.
                                   If dict, keys are asset names and values are pd.Series of prices.
    weights (np.ndarray): Array of portfolio weights for each asset (should sum to 1).
    confidence_level (float): Confidence level for VaR calculation (default is 0.95).
    
    Returns:
    dict: Dictionary containing portfolio VaR, returns, and statistics.
    """
    # Normalize weights to ensure they sum to 1
    weights = np.array(weights) / np.sum(weights)
    
    # Convert prices to DataFrame if it's a dictionary
    if isinstance(prices, dict):
        prices_df = pd.DataFrame(prices)
    else:
        prices_df = prices
    
    # Validate that we have at least 2 price points per asset
    if len(prices_df) < 2:
        raise ValueError(f"Insufficient price data: need at least 2 price points per asset, but got {len(prices_df)}. "
                        f"Ensure all assets have overlapping date ranges.")
    
    # Calculate returns for each asset
    returns_df = prices_df.pct_change().dropna()
    
    # Validate that we have returns data
    if len(returns_df) == 0:
        raise ValueError("No returns could be calculated. This may happen if: "
                        f"1) Assets have no overlapping dates (merged data is empty), "
                        f"2) Data contains only one price point per asset, or "
                        f"3) Data is malformed. Current price data shape: {prices_df.shape}")
    
    # Calculate portfolio returns as weighted sum of individual returns
    portfolio_returns = (returns_df * weights).sum(axis=1)
    
    # Calculate portfolio VaR
    portfolio_var = calculate_var(np.array(portfolio_returns), confidence_level)
    
    # Calculate additional portfolio statistics
    portfolio_mean_return = portfolio_returns.mean()
    portfolio_std = portfolio_returns.std()
    portfolio_cumulative_return = (1 + portfolio_returns).cumprod() - 1
    
    return {
        'var': portfolio_var,
        'returns': portfolio_returns,
        'mean_return': portfolio_mean_return,
        'volatility': portfolio_std,
        'cumulative_returns': portfolio_cumulative_return,
        'weights': weights
    }

def main():
    # Load VN30 historical price data
    vn30_data = load_data(VN30_FILE_PATH)
    xautusd_data = load_data(xautusd_FILE_PATH)
    btcusd_data = load_data(btcusd_FILE_PATH)
    # Calculate log returns and simple returns
    log_returns_vn30 = calculate_log_returns(vn30_data['close'])
    log_returns_xautusd = calculate_log_returns(xautusd_data['Close'])
    log_returns_btcusd = calculate_log_returns(btcusd_data['Close'])
    # Calculate VaR for log returns and simple returns
    var_log_vn30 = calculate_var(np.array(log_returns_vn30), confidence_level=0.95)
    var_log_xautusd = calculate_var(np.array(log_returns_xautusd), confidence_level=0.95)
    var_log_btcusd = calculate_var(np.array(log_returns_btcusd), confidence_level=0.95)

    print(f"Value at Risk (VaR) at 95% confidence level for Log Returns: {var_log_vn30:.4f}")
    print(f"Value at Risk (VaR) at 95% confidence level for XAUT-USD Log Returns: {var_log_xautusd:.4f}")
    print(f"Value at Risk (VaR) at 95% confidence level for BTC-USD Log Returns: {var_log_btcusd:.4f}")

if __name__ == "__main__":
    main()