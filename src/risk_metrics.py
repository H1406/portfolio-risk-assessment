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
    
    sorted_returns = np.sort(returns)
    index = int((1 - confidence_level) * len(sorted_returns))
    var = -sorted_returns[index]
    
    return var