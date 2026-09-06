import { useState, useEffect } from 'react';
import Header from './components/Header';
import UrlScanner from './components/UrlScanner';
import QRScanner from './components/QRScanner';
import ScanResult from './components/ScanResult';
import { predictUrl } from './services/api';
import './index.css';

function App() {
  const [scanStatus, setScanStatus] = useState('IDLE');
  const [scanResult, setScanResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  const [activeTab, setActiveTab] = useState('URL');

  const [theme, setTheme] = useState(() => {
    const saved = localStorage.getItem('theme');
    if (saved) return saved;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };

  const handleScan = async (url) => {
    setScanStatus('SCANNING');
    setErrorMessage('');
    setScanResult(null);

    try {
      const data = await predictUrl(url);
      setScanResult(data);
      setScanStatus('SUCCESS');
    } catch (err) {
      setErrorMessage(err.message);
      setScanStatus('ERROR');
    }
  };

  const handleReset = () => {
    setScanStatus('IDLE');
    setScanResult(null);
    setErrorMessage('');
  };

  const switchTab = (tab) => {
    if (scanStatus === 'SCANNING') return;
    setActiveTab(tab);
    handleReset();
  };

  return (
    <div className="app-layout">
      <Header theme={theme} toggleTheme={toggleTheme} />
      <main className="container main-content">
        <div className="scanner-tabs">
          <button 
            className={`tab-btn ${activeTab === 'URL' ? 'active' : ''}`}
            onClick={() => switchTab('URL')}
            disabled={scanStatus === 'SCANNING'}
            aria-selected={activeTab === 'URL'}
          >
            URL Scanner
          </button>
          <button 
            className={`tab-btn ${activeTab === 'QR' ? 'active' : ''}`}
            onClick={() => switchTab('QR')}
            disabled={scanStatus === 'SCANNING'}
            aria-selected={activeTab === 'QR'}
          >
            QR Scanner
          </button>
        </div>

        {activeTab === 'URL' && (
          <>
            <UrlScanner onScan={handleScan} isScanning={scanStatus === 'SCANNING'} />
            <ScanResult 
              status={scanStatus} 
              result={scanResult} 
              error={errorMessage} 
              onReset={handleReset} 
            />
          </>
        )}

        {activeTab === 'QR' && (
          <>
            <QRScanner 
              onScan={handleScan} 
              isScanning={scanStatus === 'SCANNING'} 
              onResetExt={handleReset}
            />
            {scanStatus !== 'IDLE' && (
                <ScanResult 
                  status={scanStatus} 
                  result={scanResult} 
                  error={errorMessage} 
                  onReset={handleReset} 
                />
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default App;
