import React, { useState } from 'react';
import PortfolioVisualizer from './components/PortfolioVisualizer';
import DCATimingDetector from './components/DCATimingDetector';
import './App.css';

type PageType = 'portfolio' | 'dca';

function App() {
  const [currentPage, setCurrentPage] = useState<PageType>('portfolio');

  return (
    <div className="App">
      <nav className="app-nav">
        <div className="nav-content">
          <h1 className="app-title">Risk Assessment Suite</h1>
          <div className="nav-buttons">
            <button
              className={`nav-button ${currentPage === 'portfolio' ? 'active' : ''}`}
              onClick={() => setCurrentPage('portfolio')}
            >
              Portfolio Visualizer
            </button>
            <button
              className={`nav-button ${currentPage === 'dca' ? 'active' : ''}`}
              onClick={() => setCurrentPage('dca')}
            >
              DCA Timing Detector
            </button>
          </div>
        </div>
      </nav>

      <main className="app-main">
        {currentPage === 'portfolio' && <PortfolioVisualizer />}
        {currentPage === 'dca' && <DCATimingDetector />}
      </main>
    </div>
  );
}

export default App;

