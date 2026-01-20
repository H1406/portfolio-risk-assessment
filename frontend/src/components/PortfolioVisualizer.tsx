import React, { useState, useEffect } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import axios from 'axios';
import './PortfolioVisualizer.css';

interface PortfolioData {
  var: number;
  mean_return: number;
  volatility: number;
  cumulative_return: number;
  weights: number[];
  portfolio_values: Array<{ date: string; value: number }>;
}

const PortfolioVisualizer: React.FC = () => {
  const [weights, setWeights] = useState<number[]>([33.33, 33.33, 33.34]);
  const [portfolioData, setPortfolioData] = useState<PortfolioData | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const assetNames = ['VN30', 'Gold (XAU/USD)', 'Bitcoin (BTC/USD)'];
  const assetColors = ['#3b82f6', '#fbbf24', '#f97316'];

  useEffect(() => {
    fetchPortfolioData();
  }, []);

  const fetchPortfolioData = async () => {
    setLoading(true);
    setError(null);

    try {
      const normalizedWeights = normalizeWeights(weights);
      const response = await axios.post('http://127.0.0.1:5000/api/portfolio/calculate', {
        weights: normalizedWeights.map(w => w / 100),
        confidence_level: 0.95,
      });

      setPortfolioData(response.data);
    } catch (err) {
      setError('Failed to fetch portfolio data. Make sure the backend server is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const normalizeWeights = (weights: number[]): number[] => {
    const total = weights.reduce((sum, w) => sum + w, 0);
    return weights.map(w => (w / total) * 100);
  };

  const handleWeightChange = (index: number, value: number) => {
    const newWeights = [...weights];
    newWeights[index] = Math.max(0, Math.min(100, value));
    setWeights(newWeights);
  };

  const handleSliderRelease = () => {
    fetchPortfolioData();
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
  };

  const chartData = portfolioData?.portfolio_values.map((item, index) => ({
    date: formatDate(item.date),
    value: item.value,
    // Only show label every N points for readability
    displayDate: index % Math.floor(portfolioData.portfolio_values.length / 10) === 0 
      ? formatDate(item.date) 
      : '',
  })) || [];

  const normalizedWeights = normalizeWeights(weights);

  return (
    <div className="portfolio-visualizer">
      <header className="header">
        <h1>Portfolio Risk Assessment</h1>
        <p>Visualize your portfolio performance and adjust asset weights</p>
      </header>

      <div className="content">
        <div className="controls-section">
          <h2>Asset Allocation</h2>
          <p className="subtitle">Adjust weights for each asset (auto-normalized to 100%)</p>
          
          <div className="sliders">
            {assetNames.map((name, index) => (
              <div key={index} className="slider-container">
                <div className="slider-header">
                  <label htmlFor={`slider-${index}`}>
                    <span className="asset-dot" style={{ backgroundColor: assetColors[index] }}></span>
                    {name}
                  </label>
                  <span className="weight-value">
                    {normalizedWeights[index].toFixed(2)}%
                  </span>
                </div>
                <input
                  id={`slider-${index}`}
                  type="range"
                  min="0"
                  max="100"
                  step="0.1"
                  value={weights[index]}
                  onChange={(e) => handleWeightChange(index, parseFloat(e.target.value))}
                  onMouseUp={handleSliderRelease}
                  onTouchEnd={handleSliderRelease}
                  className="slider"
                  style={{
                    background: `linear-gradient(to right, ${assetColors[index]} 0%, ${assetColors[index]} ${normalizedWeights[index]}%, #ddd ${normalizedWeights[index]}%, #ddd 100%)`
                  }}
                />
              </div>
            ))}
          </div>

          <button 
            onClick={fetchPortfolioData} 
            className="update-button"
            disabled={loading}
          >
            {loading ? 'Updating...' : 'Update Portfolio'}
          </button>
        </div>

        <div className="visualization-section">
          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          {loading && !portfolioData && (
            <div className="loading">Loading portfolio data...</div>
          )}

          {portfolioData && (
            <>
              <div className="metrics-grid">
                <div className="metric-card">
                  <h3>Cumulative Return</h3>
                  <p className={portfolioData.cumulative_return >= 0 ? 'positive' : 'negative'}>
                    {(portfolioData.cumulative_return * 100).toFixed(2)}%
                  </p>
                </div>
                <div className="metric-card">
                  <h3>Value at Risk (95%)</h3>
                  <p className="negative">
                    {(portfolioData.var * 100).toFixed(2)}%
                  </p>
                </div>
                <div className="metric-card">
                  <h3>Mean Daily Return</h3>
                  <p className={portfolioData.mean_return >= 0 ? 'positive' : 'negative'}>
                    {(portfolioData.mean_return * 100).toFixed(4)}%
                  </p>
                </div>
                <div className="metric-card">
                  <h3>Volatility (Std Dev)</h3>
                  <p>
                    {(portfolioData.volatility * 100).toFixed(2)}%
                  </p>
                </div>
              </div>

              <div className="chart-container">
                <h2>Portfolio Value Over Time</h2>
                <p className="chart-subtitle">Starting value: $100</p>
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="displayDate" 
                      tick={{ fontSize: 12 }}
                    />
                    <YAxis 
                      label={{ value: 'Portfolio Value ($)', angle: -90, position: 'insideLeft' }}
                      tick={{ fontSize: 12 }}
                    />
                    <Tooltip 
                      formatter={(value) => [`$${Number(value).toFixed(2)}`, 'Value']}
                      labelFormatter={(label) => `Date: ${label}`}
                    />
                    <Legend />
                    <Line 
                      type="monotone" 
                      dataKey="value" 
                      stroke="#3b82f6" 
                      strokeWidth={2}
                      dot={false}
                      name="Portfolio Value"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default PortfolioVisualizer;
