import { useState } from 'react';

export default function EmailScanner({ onScan, isScanning }) {
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!body.trim()) {
      setError('Please enter the email body to scan.');
      return;
    }
    
    if (subject.length > 1000) {
      setError('Subject must be less than 1000 characters.');
      return;
    }

    if (body.length > 100000) {
      setError('Body must be less than 100000 characters.');
      return;
    }

    setError('');
    onScan(subject, body);
  };

  return (
    <div className="url-scanner">
      <form onSubmit={handleSubmit} className="scanner-form" style={{ flexDirection: 'column', gap: '15px' }}>
        
        <div style={{ width: '100%' }}>
          <label htmlFor="email-subject-input" style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', textAlign: 'left', color: 'var(--text-color)' }}>Subject (Optional)</label>
          <input
            id="email-subject-input"
            type="text"
            placeholder="Enter email subject..."
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            disabled={isScanning}
            className="scanner-input"
            style={{ width: '100%' }}
          />
        </div>

        <div style={{ width: '100%' }}>
          <label htmlFor="email-body-input" style={{ display: 'block', marginBottom: '5px', fontWeight: 'bold', textAlign: 'left', color: 'var(--text-color)' }}>Email Body (Required)</label>
          <textarea
            id="email-body-input"
            placeholder="Paste email content here..."
            value={body}
            onChange={(e) => setBody(e.target.value)}
            disabled={isScanning}
            className="scanner-input"
            style={{ width: '100%', minHeight: '150px', resize: 'vertical', padding: '12px', fontFamily: 'inherit' }}
          />
        </div>

        <button type="submit" disabled={isScanning} className="scanner-button" style={{ alignSelf: 'flex-start' }}>
          {isScanning ? 'Analyzing Email...' : 'Analyze Email'}
        </button>
      </form>
      {error && <p className="error-text">{error}</p>}
    </div>
  );
}
