import pandas as pd
from data_loader import load_data
import numpy as np
import os

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VN30_FILE_PATH = os.path.join(PROJECT_ROOT, 'data/raw/historical_prices_E1VFVN30.csv')
XAUTUSD_FILE_PATH = os.path.join(PROJECT_ROOT, 'data/raw/historical_prices_XAUTUSD.csv')
BTCUSD_FILE_PATH = os.path.join(PROJECT_ROOT, 'data/raw/historical_prices_BTCUSD.csv')

vn_30_prices = load_data(VN30_FILE_PATH)
xautusd_prices = load_data(XAUTUSD_FILE_PATH)
btcusd_prices = load_data(BTCUSD_FILE_PATH)

vn_30_date = pd.to_datetime(vn_30_prices['time'])
xautusd_date = pd.to_datetime(xautusd_prices['Price'])

print(vn_30_date[vn_30_date.isin(xautusd_date)])