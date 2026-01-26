import React, { useState, useEffect, useCallback } from 'react';
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
import './DCATimingDetector.css';

interface PriceData {
  date: string;
  price: number;
  signal?: number;
}

interface DCASignal {
  signal: 'BUY' | 'HOLD' | 'SELL';
  confidence: number;
  reasoning: string;
  current_price: number;
  sma_20: number;
  sma_50: number;
  rsi: number;
}

const DCATimingDetector: React.FC = () => {
  const [selectedAsset, setSelectedAsset] = useState<'btcusd' | 'xautusd' | 'vn30'>('btcusd');
  const [priceData, setPriceData] = useState<PriceData[]>([]);
  const [dcaSignal, setDCASignal] = useState<DCASignal | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [signalLoading, setSignalLoading] = useState<boolean>(false);

  const assets = [
    { id: 'btcusd' as const, name: 'Bitcoin (BTC/USD)', color: '#f97316' },
    { id: 'xautusd' as const, name: 'Gold (XAU/USD)', color: '#fbbf24' },
    { id: 'vn30' as const, name: 'VN30', color: '#3b82f6' },
  ];

  const fetchPriceData = useCallback(async () => {
    setLoading(true);
    setError(null);
    setDCASignal(null);

    try {
      const response = await axios.get(`http://127.0.0.1:5000/api/asset-prices/${selectedAsset}`);
      setPriceData(response.data.data);
    } catch (err) {
      setError('Failed to fetch price data. Make sure the backend server is running.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [selectedAsset]);

  useEffect(() => {
    fetchPriceData();
  }, [fetchPriceData]);

  const fetchDCASignal = async () => {
    setSignalLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/dca-timing', {
        asset: selectedAsset,
      });
      setDCASignal(response.data);
    } catch (err) {
      setError('Failed to fetch DCA signal. Make sure the backend server is running.');
      console.error(err);
    } finally {
      setSignalLoading(false);
    }
  };

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  const chartData = priceData.map((item, index) => ({
    date: formatDate(item.date),
    price: item.price,
    // Show every 20th data point
    displayDate: index % 20 === 0 ? formatDate(item.date) : '',
  }));

  const currentAsset = assets.find(a => a.id === selectedAsset);
  const signalColor = dcaSignal?.signal === 'BUY' ? '#10b981' : dcaSignal?.signal === 'SELL' ? '#ef4444' : '#6b7280';

  return (
    <div className="dca-timing-detector">
      <header className="header">
        <h1>DCA Timing Detector</h1>
        <p>Analyze optimal Dollar-Cost Averaging entry points using technical indicators</p>
      </header>

      <div className="content">
        <div className="controls-section">
          <h2>Select Asset</h2>
          <div className="asset-buttons">
            {assets.map(asset => (
              <button
                key={asset.id}
                className={`asset-button ${selectedAsset === asset.id ? 'active' : ''}`}
                onClick={() => setSelectedAsset(asset.id)}
                style={{
                  borderColor: asset.color,
                  backgroundColor: selectedAsset === asset.id ? asset.color : 'transparent',
                }}
              >
                {asset.name}
              </button>
            ))}
          </div>

          <button
            className="detect-button"
            onClick={fetchDCASignal}
            disabled={loading || signalLoading}
            style={{ backgroundColor: currentAsset?.color }}
          >
            {signalLoading ? 'Analyzing...' : 'Get DCA Signal'}
          </button>

          {error && <div className="error-message">{error}</div>}
        </div>

        {dcaSignal && (
          <div className="signal-section">
            <div className="signal-card" style={{ borderLeftColor: signalColor }}>
              <div className="signal-header">
                <h3>DCA Signal</h3>
                <div className="signal-badge" style={{ backgroundColor: signalColor }}>
                  {dcaSignal.signal}
                </div>
              </div>
              <div className="signal-details">
                <div className="detail-row">
                  <span className="label">Current Price:</span>
                  <span className="value">${dcaSignal.current_price.toFixed(2)}</span>
                </div>
                <div className="detail-row">
                  <span className="label">20-Day SMA:</span>
                  <span className="value">${dcaSignal.sma_20.toFixed(2)}</span>
                </div>
                <div className="detail-row">
                  <span className="label">50-Day SMA:</span>
                  <span className="value">${dcaSignal.sma_50.toFixed(2)}</span>
                </div>
                <div className="detail-row">
                  <span className="label">RSI (14):</span>
                  <span className="value">{dcaSignal.rsi.toFixed(2)}</span>
                </div>
                <div className="detail-row">
                  <span className="label">Confidence:</span>
                  <span className="value">{(dcaSignal.confidence * 100).toFixed(0)}%</span>
                </div>
                <div className="detail-row full-width">
                  <span className="label">Reasoning:</span>
                  <span className="reasoning">{dcaSignal.reasoning}</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {priceData.length > 0 && (
          <div className="chart-section">
            <h2>Price Chart - {currentAsset?.name}</h2>
            <ResponsiveContainer width="100%" height={400}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis
                  dataKey="displayDate"
                  stroke="#6b7280"
                  tick={{ fontSize: 12 }}
                />
                <YAxis stroke="#6b7280" tick={{ fontSize: 12 }} />
                <Tooltip
                  formatter={(value: number | undefined) => value !== undefined ? `$${value.toFixed(2)}` : '$0.00'}
                  labelFormatter={(label) => `Date: ${label}`}
                  contentStyle={{
                    backgroundColor: '#1f2937',
                    border: `2px solid ${currentAsset?.color}`,
                    borderRadius: '8px',
                    color: '#fff',
                  }}
                />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="price"
                  stroke={currentAsset?.color}
                  dot={false}
                  strokeWidth={2}
                  name="Price"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        {loading && <div className="loading-message">Loading price data...</div>}
      </div>
    </div>
  );
};

export default DCATimingDetector;
