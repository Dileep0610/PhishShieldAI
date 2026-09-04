import { useState } from 'react';

export default function UrlScanner({ onScan, isScanning }) {
  const [inputUrl, setInputUrl] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputUrl.trim()) {
      setError('Please enter a URL to scan.');
      return;
    }
    setError('');
    onScan(inputUrl);
  };

  return (
    <div className="url-scanner">
      <form onSubmit={handleSubmit} className="scanner-form">
        <label htmlFor="url-input" className="sr-only">Enter suspicious URL</label>
        <input
          id="url-input"
          type="text"
          placeholder="https://example.com"
          value={inputUrl}
          onChange={(e) => setInputUrl(e.target.value)}
          disabled={isScanning}
          className="scanner-input"
        />
        <button type="submit" disabled={isScanning} className="scanner-button">
          {isScanning ? 'Scanning...' : 'Scan URL'}
        </button>
      </form>
      {error && <p className="error-text">{error}</p>}
    </div>
  );
}
