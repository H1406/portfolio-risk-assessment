# Portfolio Risk Assessment - Setup Guide

This application allows you to visualize portfolio performance and adjust asset weights with interactive sliders.

## Architecture

- **Backend**: Flask API (Python) - Calculates portfolio metrics and serves data
- **Frontend**: React (TypeScript) - Interactive visualization with Recharts
- **Assets**: VN30, Gold (XAU/USD), Bitcoin (BTC/USD)

## Prerequisites

- Python 3.8+
- Node.js 14+ and npm
- Git

## Installation

### 1. Backend Setup

Install Python dependencies:

```bash
pip install -r requirements.txt
```

### 2. Frontend Setup

The frontend is already installed. If you need to reinstall dependencies:

```bash
cd frontend
npm install
cd ..
```

## Running the Application

You need to run both the backend and frontend servers simultaneously.

### Terminal 1: Start the Backend Server

```bash
# From the project root directory
cd src
python api.py
```

The backend API will start on `http://localhost:5000`

### Terminal 2: Start the Frontend Development Server

```bash
# From the project root directory
cd frontend
npm start
```

The frontend will start on `http://localhost:3000` and automatically open in your browser.

## Using the Application

1. Once both servers are running, open `http://localhost:3000` in your browser
2. You'll see:
   - **Asset Allocation Sliders**: Adjust the weight of each asset (VN30, Gold, Bitcoin)
   - **Portfolio Metrics**: View Cumulative Return, Value at Risk (95%), Mean Daily Return, and Volatility
   - **Portfolio Value Chart**: Visualize portfolio performance over time

3. Adjust the sliders to change asset weights:
   - Weights are automatically normalized to sum to 100%
   - The chart updates when you release the slider or click "Update Portfolio"

## API Endpoints

- `GET /api/assets` - Get list of available assets
- `GET /api/historical-prices` - Get historical price data
- `POST /api/portfolio/calculate` - Calculate portfolio metrics given weights
- `GET /api/health` - Health check

## Features

- **Real-time Portfolio Calculation**: Adjust weights and see updated metrics
- **Risk Metrics**: Value at Risk (VaR), volatility, and returns
- **Interactive Visualization**: Line chart showing portfolio value over time
- **Auto-normalization**: Weights automatically normalize to 100%
- **Responsive Design**: Works on desktop and mobile devices

## Troubleshooting

### Backend Issues

- **Error loading data**: Make sure the CSV files exist in `data/raw/`
- **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`
- **Port 5000 in use**: Change the port in `src/api.py` line 110

### Frontend Issues

- **Cannot connect to backend**: Ensure the backend server is running on port 5000
- **npm errors**: Try deleting `node_modules` and running `npm install` again
- **Port 3000 in use**: The app will prompt to use a different port

## Project Structure

```
portfolio-risk-assessment/
├── src/
│   ├── api.py              # Flask API server
│   ├── portfolio.py        # Portfolio calculations
│   ├── risk_metrics.py     # VaR and CVaR calculations
│   ├── returns.py          # Return calculations
│   └── data_loader.py      # Data loading utilities
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── PortfolioVisualizer.tsx    # Main component
│   │   │   └── PortfolioVisualizer.css    # Styles
│   │   ├── App.tsx         # React app entry
│   │   └── index.tsx       # React DOM entry
│   └── package.json        # Frontend dependencies
├── data/raw/               # Historical price data
└── requirements.txt        # Python dependencies
```

## Technologies Used

- **Backend**: Flask, Flask-CORS, Pandas, NumPy
- **Frontend**: React, TypeScript, Recharts, Axios
- **Visualization**: Recharts (React charting library)
