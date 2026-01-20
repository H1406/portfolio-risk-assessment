# Portfolio Risk Assessment

A full-stack web application for portfolio risk analysis and visualization. Calculate Value at Risk (VaR) and visualize portfolio performance with interactive asset weight adjustments.

## Features

- 📊 **Interactive Visualization**: Real-time portfolio value charts using Recharts
- 🎚️ **Weight Adjustment Sliders**: Easily adjust asset allocation with auto-normalization
- 📈 **Risk Metrics**: Calculate VaR, volatility, and returns
- 🔄 **Real-time Updates**: Instant portfolio recalculation
- 💼 **Multi-Asset Support**: VN30, Gold (XAU/USD), and Bitcoin (BTC/USD)

## Technology Stack

### Backend
- Python 3.8+
- Flask (REST API)
- Pandas (Data processing)
- NumPy (Numerical calculations)

### Frontend
- React 18 with TypeScript
- Recharts (Data visualization)
- Axios (API communication)
- CSS3 (Responsive design)

## Quick Start

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

### 1. Setup Backend

```bash
./setup_backend.sh
```

### 2. Run Backend (Terminal 1)

```bash
source venv/bin/activate
cd src
python api.py
```

### 3. Run Frontend (Terminal 2)

```bash
cd frontend
npm start
```

Open `http://localhost:3000` in your browser.

## Documentation

- [Quick Start Guide](QUICKSTART.md) - Get up and running quickly
- [Setup Guide](SETUP.md) - Detailed setup and usage instructions

## Project Structure

```
portfolio-risk-assessment/
├── src/                    # Backend Python code
│   ├── api.py             # Flask REST API
│   ├── portfolio.py       # Portfolio calculations
│   ├── risk_metrics.py    # VaR and CVaR
│   └── ...
├── frontend/              # React frontend
│   └── src/
│       └── components/
│           └── PortfolioVisualizer.tsx
├── data/raw/              # Historical price data
└── requirements.txt       # Python dependencies
```

## API Endpoints

- `GET /api/assets` - List available assets
- `GET /api/historical-prices` - Get historical price data
- `POST /api/portfolio/calculate` - Calculate portfolio metrics
- `GET /api/health` - Health check

## License

See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.