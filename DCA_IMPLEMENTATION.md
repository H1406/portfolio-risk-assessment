# DCA Timing Detector Implementation Summary

## Overview

Added a new DCA (Dollar-Cost Averaging) timing detector feature that allows users to analyze optimal entry points for investing in three assets: Bitcoin (BTC/USD), Gold (XAU/USD), and Vietnam VN30 Index.

## Changes Made

### Backend (Python)

#### 1. **New File: `src/dca_detector.py`**

- Implements technical analysis algorithms for DCA signal detection
- Key functions:
  - `calculate_sma()` - Calculates Simple Moving Average
  - `calculate_rsi()` - Calculates Relative Strength Index (14-period)
  - `detect_dca_signal()` - Main function that analyzes an asset and returns BUY/HOLD/SELL signal
  - `get_asset_prices()` - Extracts price data for specific assets

- **Signal Logic:**
  - **BUY Signal**: Triggered when RSI < 30 (oversold) or price is significantly below moving averages
  - **SELL Signal**: Triggered when RSI > 70 (overbought)
  - **HOLD Signal**: Neutral conditions
  - Returns confidence level (0.2 - 0.95) and detailed reasoning
  - Considers 20-day SMA, 50-day SMA, RSI, and trend analysis

#### 2. **Updated: `src/api.py`**

- Added import for `dca_detector` module
- New API endpoints:

  **GET `/api/asset-prices/<asset_id>`**
  - Returns historical price data for a single asset
  - Supported assets: `btcusd`, `xautusd`, `vn30`
  - Response: Array of {date, price} objects

  **POST `/api/dca-timing`**
  - Main endpoint for DCA signal detection
  - Request body: `{ "asset": "btcusd|xautusd|vn30" }`
  - Response:
    ```json
    {
      "signal": "BUY|HOLD|SELL",
      "confidence": 0.0-1.0,
      "reasoning": "Detailed explanation",
      "current_price": float,
      "sma_20": float,
      "sma_50": float,
      "rsi": float
    }
    ```

### Frontend (React/TypeScript)

#### 1. **New File: `frontend/src/components/DCATimingDetector.tsx`**

- Complete React component for DCA timing analysis
- Features:
  - Asset selector buttons for BTC, XAU, and VN30
  - Interactive price chart using Recharts
  - "Get DCA Signal" button to fetch analysis
  - Signal display card showing:
    - BUY/HOLD/SELL signal with color coding
    - Confidence percentage
    - Current price
    - 20-day and 50-day SMAs
    - RSI value
    - Detailed reasoning for the signal
- Responsive design with smooth animations

#### 2. **New File: `frontend/src/components/DCATimingDetector.css`**

- Styling for DCA timing detector component
- Features:
  - Modern gradient background
  - Color-coded signals (Green=BUY, Red=SELL, Gray=HOLD)
  - Responsive grid layout
  - Animation effects for smooth transitions
  - Mobile-friendly design

#### 3. **Updated: `frontend/src/App.tsx`**

- Added navigation system between two pages
- State management for current page (portfolio | dca)
- Navigation bar with toggle buttons
- Conditional rendering of components

#### 4. **Updated: `frontend/src/App.css`**

- Added navigation bar styling
- Gradient header (purple to violet)
- Navigation button styles with active state
- Responsive layout for mobile devices

## How to Use

### 1. Start the Backend Server

```bash
cd /Users/phanhieu/portfolio-risk-assessment
source venv/bin/activate
python src/api.py
```

The server will run on `http://127.0.0.1:5000`

### 2. Start the Frontend Development Server

```bash
cd /Users/phanhieu/portfolio-risk-assessment/frontend
npm start
```

The frontend will run on `http://localhost:3000`

### 3. Access the DCA Timing Detector

- Click on "DCA Timing Detector" in the navigation bar
- Select an asset (BTC, XAU, or VN30)
- Click "Get DCA Signal" to analyze the asset
- View the technical indicators and buy/sell recommendation

## Technical Indicators Used

1. **RSI (Relative Strength Index)**
   - 14-period RSI
   - Oversold: < 30 (potential BUY)
   - Overbought: > 70 (potential SELL)
   - Neutral: 30-70

2. **SMA (Simple Moving Average)**
   - 20-day SMA: Short-term trend
   - 50-day SMA: Medium-term trend
   - Price-to-SMA comparison for entry points

3. **Trend Analysis**
   - 20-day SMA > 50-day SMA = Bullish
   - 20-day SMA < 50-day SMA = Bearish

4. **Volatility Check**
   - Reduces confidence in high volatility environments

## Signal Confidence Levels

The confidence level (0.2 - 0.95) indicates the strength of the signal:

- **0.2-0.4**: Low confidence, use with caution
- **0.4-0.6**: Moderate confidence
- **0.6-0.8**: Good confidence
- **0.8+**: High confidence

## Features

✅ Asset switching between 3 assets
✅ Real-time price visualization
✅ Technical indicator analysis
✅ Buy/Hold/Sell signals
✅ Confidence scoring
✅ Detailed reasoning for each signal
✅ Responsive mobile design
✅ Error handling and validation
✅ Historical price data integration

## Testing

To test the endpoints manually:

```bash
# Get prices for Bitcoin
curl http://127.0.0.1:5000/api/asset-prices/btcusd

# Get DCA signal for Bitcoin
curl -X POST http://127.0.0.1:5000/api/dca-timing \
  -H "Content-Type: application/json" \
  -d '{"asset": "btcusd"}'

# Get DCA signal for Gold
curl -X POST http://127.0.0.1:5000/api/dca-timing \
  -H "Content-Type: application/json" \
  -d '{"asset": "xautusd"}'
```

## Files Modified/Created

- ✅ Created: `src/dca_detector.py`
- ✅ Created: `frontend/src/components/DCATimingDetector.tsx`
- ✅ Created: `frontend/src/components/DCATimingDetector.css`
- ✅ Updated: `src/api.py` (added 2 new endpoints)
- ✅ Updated: `frontend/src/App.tsx` (added navigation)
- ✅ Updated: `frontend/src/App.css` (added nav styling)
