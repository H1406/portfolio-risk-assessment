from vnstock import Vnstock
"""
stock data fetching from VCI(vnstock), especially for E1VFVN30
"""
stock = Vnstock().stock(symbol='E1VFVN30', source='VCI')
df_stock = stock.quote.history(start='2021-01-01', end='2025-01-01', interval='1W')
print(df_stock.head())
df_stock.to_csv('./data/raw/historical_prices_E1VFVN30.csv', index=False)
print("Saved into file 'historical_prices_E1VFVN30.csv'")


"""
historical gold prices(xautusd) from yfinance
"""
import yfinance as yf

gold_data = yf.download("XAUT-USD", start="2021-01-01", end="2025-01-01", interval="1wk")
print(gold_data.head())
gold_data.to_csv('./data/raw/historical_prices_XAUTUSD.csv')
print("Saved into file 'historical_prices_XAUTUSD.csv'")

"""
historical bitcoin prices from yfinance
"""

btc_data = yf.download("BTC-USD", start="2021-01-01", end="2025-01-01", interval="1wk")
print(btc_data.head())
btc_data.to_csv('./data/raw/historical_prices_BTCUSD.csv')
print("Saved into file 'historical_prices_BTCUSD.csv'")




