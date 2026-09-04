import { useState } from 'react';
import Header from './components/Header';
import UrlScanner from './components/UrlScanner';
import ScanResult from './components/ScanResult';
import { predictUrl } from './services/api';
import './index.css';

function App() {
  const [scanStatus, setScanStatus] = useState('IDLE');
  const [scanResult, setScanResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');

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

  return (
    <div className="app-layout">
      <Header />
      <main className="container main-content">
        <UrlScanner onScan={handleScan} isScanning={scanStatus === 'SCANNING'} />
        <ScanResult 
          status={scanStatus} 
          result={scanResult} 
          error={errorMessage} 
          onReset={handleReset} 
        />
      </main>
    </div>
  );
}

export default App;
