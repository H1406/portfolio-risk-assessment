# Quick Start Guide

## First Time Setup

### 1. Set up the backend (Python)

```bash
# Make the setup script executable (if not already done)
chmod +x setup_backend.sh

# Run the setup script
./setup_backend.sh
```

This will create a virtual environment and install all Python dependencies.

## Running the Application

You need TWO terminal windows/tabs:

### Terminal 1: Backend Server

```bash
# Activate virtual environment
source venv/bin/activate

# Navigate to src and start the Flask server
cd src
python api.py
```

You should see:
```
* Running on http://127.0.0.1:5000
```

### Terminal 2: Frontend Server

```bash
# Navigate to frontend directory
cd frontend

# Start the React development server
npm start
```

The browser should automatically open to `http://localhost:3000`

## Using the App

1. **Adjust Asset Weights**: Use the sliders to change allocation between VN30, Gold, and Bitcoin
2. **View Metrics**: See your portfolio's:
   - Cumulative Return
   - Value at Risk (VaR) at 95% confidence
   - Mean Daily Return
   - Volatility
3. **Visualize Performance**: Watch the chart update showing portfolio value over time
4. **Update**: Click "Update Portfolio" or release the slider to recalculate

## Stopping the Servers

- Backend: Press `Ctrl+C` in Terminal 1
- Frontend: Press `Ctrl+C` in Terminal 2

## Troubleshooting

**Backend won't start:**
- Make sure you activated the virtual environment: `source venv/bin/activate`
- Check that port 5000 is not in use

**Frontend shows connection error:**
- Make sure the backend server is running on port 5000
- Check the browser console for detailed error messages

**Module not found errors:**
- Re-run the setup script: `./setup_backend.sh`
- For frontend: `cd frontend && npm install`
