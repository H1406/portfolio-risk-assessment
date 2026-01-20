from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
import os
from portfolio import calculate_portfolio_var
from data_loader import load_data

app = Flask(__name__)
CORS(app) 

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# File paths
VN30_FILE_PATH = os.path.join(PROJECT_ROOT, 'data/raw/historical_prices_E1VFVN30.csv')
XAUTUSD_FILE_PATH = os.path.join(PROJECT_ROOT, 'data/raw/historical_prices_XAUTUSD.csv')
BTCUSD_FILE_PATH = os.path.join(PROJECT_ROOT, 'data/raw/historical_prices_BTCUSD.csv')

# Load data at startup
vn30_data = load_data(VN30_FILE_PATH)
xautusd_raw = pd.read_csv(XAUTUSD_FILE_PATH)
btcusd_raw = pd.read_csv(BTCUSD_FILE_PATH)

# Standardize column names for VN30
vn30_data = vn30_data.rename(columns={'time': 'date'})

# Process XAUTUSD and BTCUSD (they have different format)
xautusd_data = xautusd_raw.rename(columns={'Price': 'date', 'Close': 'close'})
btcusd_data = btcusd_raw.rename(columns={'Price': 'date', 'Close': 'close'})


@app.route('/api/assets', methods=['GET'])
def get_assets():
    """Get list of available assets"""
    return jsonify({
        'assets': [
            {'id': 'vn30', 'name': 'VN30', 'description': 'Vietnam VN30 Index'},
            {'id': 'xautusd', 'name': 'Gold (XAU/USD)', 'description': 'Gold vs USD'},
            {'id': 'btcusd', 'name': 'Bitcoin (BTC/USD)', 'description': 'Bitcoin vs USD'}
        ]
    })

@app.route('/api/historical-prices', methods=['GET'])
def get_historical_prices():
    """Get historical price data for all assets"""
    # Align dates across all datasets
    vn30_prices = vn30_data[['date', 'close']].rename(columns={'close': 'vn30'})
    xautusd_prices = xautusd_data[['date', 'close']].rename(columns={'close': 'xautusd'})
    btcusd_prices = btcusd_data[['date', 'close']].rename(columns={'close': 'btcusd'})
    
    # Merge on date
    merged = vn30_prices.merge(xautusd_prices, on='date', how='inner')
    merged = merged.merge(btcusd_prices, on='date', how='inner')
    merged = merged.sort_values('date')
    
    return jsonify({
        'data': merged.to_dict(orient='records')
    })

@app.route('/api/portfolio/calculate', methods=['POST'])
def calculate_portfolio():
    """Calculate portfolio metrics based on weights"""
    data = request.json
    weights = data.get('weights', [0.33, 0.33, 0.34])  # Default equal weights
    confidence_level = data.get('confidence_level', 0.95)
    
    # Validate weights
    if len(weights) != 3:
        return jsonify({'error': 'Must provide exactly 3 weights'}), 400
    
    # Normalize weights
    weights = np.array(weights)
    weights = weights / np.sum(weights)
    
    # Align dates and create price dataframe
    vn30_prices = vn30_data[['date', 'close']].rename(columns={'close': 'vn30'})
    vn30_prices = vn30_prices.head(len(xautusd_data))
    vn30_prices['date'] = xautusd_data['date'].values
    xautusd_prices = xautusd_data[['date', 'close']].rename(columns={'close': 'xautusd'})
    btcusd_prices = btcusd_data[['date', 'close']].rename(columns={'close': 'btcusd'})
    
    merged = vn30_prices.merge(xautusd_prices, on='date', how='inner')
    merged = merged.merge(btcusd_prices, on='date', how='inner')
    merged = merged.sort_values('date')
    
    # Create prices dataframe
    prices_df = merged[['vn30', 'xautusd', 'btcusd']]
    dates = merged['date'].values
    
    # Calculate portfolio metrics
    result = calculate_portfolio_var(prices_df, weights, confidence_level)
    
    # Calculate portfolio value over time (normalized to 100)
    portfolio_value = (1 + result['cumulative_returns']) * 100
    
    # Prepare response
    response = {
        'var': float(result['var']),
        'mean_return': float(result['mean_return']),
        'volatility': float(result['volatility']),
        'cumulative_return': float(result['cumulative_returns'].iloc[-1]) if len(result['cumulative_returns']) > 0 else 0,
        'weights': weights.tolist(),
        'portfolio_values': [
            {'date': dates[i], 'value': float(portfolio_value.iloc[i])}
            for i in range(len(portfolio_value))
        ],
        'dates': dates.tolist()
    }
    
    return jsonify(response)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
