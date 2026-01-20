import numpy as np

def calculate_var(returns: np.ndarray, confidence_level: float = 0.95) -> float:
    """
    Calculate the Value at Risk (VaR) at a specified confidence level using the historical method.

    Parameters:
    returns (np.ndarray): Array of asset returns.
    confidence_level (float): Confidence level for VaR calculation (default is 0.95).

    Returns:
    float: The VaR value.
    """
    if not 0 < confidence_level < 1:
        raise ValueError("Confidence level must be between 0 and 1.")
    
    if len(returns) == 0:
        raise ValueError("Returns array is empty. Ensure sufficient price data is available for all assets.")
    
    if len(returns) < 2:
        raise ValueError(f"Insufficient data: need at least 2 return observations, but got {len(returns)}.")
    
    sorted_returns = np.sort(returns)
    index = int((1 - confidence_level) * len(sorted_returns))
    # Ensure index doesn't exceed array bounds
    index = min(index, len(sorted_returns) - 1)
    var = -sorted_returns[index]
    
    return var

def calculate_cvar(returns: np.ndarray, confidence_level: float = 0.95) -> float:
    """
    Calculate the Conditional Value at Risk (CVaR) at a specified confidence level.

    Parameters:
    returns (np.ndarray): Array of asset returns.
    confidence_level (float): Confidence level for CVaR calculation (default is 0.95).

    Returns:
    float: The CVaR value.
    """
    if not 0 < confidence_level < 1:
        raise ValueError("Confidence level must be between 0 and 1.")
    
    if len(returns) == 0:
        raise ValueError("Returns array is empty. Ensure sufficient price data is available for all assets.")
    
    var = calculate_var(returns, confidence_level)
    tail_returns = returns[returns <= -var]
    if len(tail_returns) == 0:
        cvar = var  # If no returns are worse than VaR, use VaR as fallback
    else:
        cvar = -np.mean(tail_returns)
    
    return cvar
