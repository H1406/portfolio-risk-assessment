import pandas as pd
from returns import calculate_log_returns, calculate_simple_returns
from risk_metrics import calculate_var
from data_loader import load_data
import numpy as np

VN30_FILE_PATH = 'data/raw/historical_prices_E1VFVN30.csv'
xautusd_FILE_PATH = 'data/raw/historical_prices_XAUTUSD.csv'
btcusd_FILE_PATH = 'data/raw/historical_prices_BTCUSD.csv'

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