import RiskScore from './RiskScore';
import SecuritySignalCard from './SecuritySignalCard';
import ExplainabilityPanel from './ExplainabilityPanel';
import ForensicFindings from './ForensicFindings';


export default function ScanResult({ status, result, error, onReset }) {
  if (status === 'IDLE') {
    return (
      <div className="result-card idle" aria-live="polite">
        <p>Enter a URL above to analyze its phishing risk.</p>
      </div>
    );
  }

  if (status === 'SCANNING') {
    return (
      <div className="result-card scanning" aria-live="polite" aria-busy="true">
        <div className="loader" role="status" aria-label="Loading"></div>
        <p className="primary-msg">Analyzing URL...</p>
        <p className="subtext">Extracting security features and evaluating risk.</p>
      </div>
    );
  }

  if (status === 'ERROR') {
    return (
      <div className="result-card error-card" aria-live="assertive">
        <h3>Analysis Failed</h3>
        <p>{error}</p>
        <button onClick={onReset} className="reset-button">Scan Another URL</button>
      </div>
    );
  }

  if (status === 'SUCCESS' && result) {
    const isPhishing = result.prediction === 'Phishing';
    
    // Parse Signals
    const sslStatus = !result.ssl ? 'unavailable' : result.ssl.ssl_valid ? 'safe' : 'danger';
    const sslValue = !result.ssl ? 'Unavailable' : result.ssl.ssl_valid ? 'Valid' : 'Invalid';

    const vtMalicious = result.virustotal?.malicious;
    const vtStatus = vtMalicious === undefined ? 'unavailable' : vtMalicious > 0 ? 'danger' : 'safe';
    const vtValue = vtMalicious === undefined ? 'Unavailable' : vtMalicious === 0 ? 'Clean' : `${vtMalicious} Flag(s)`;

    const redirectCount = result.redirect?.redirect_count;
    const redirectStatus = redirectCount === undefined ? 'unavailable' : redirectCount > 1 ? 'danger' : 'neutral';
    const redirectValue = redirectCount === undefined ? 'Unavailable' : redirectCount;

    const domainAge = result.whois?.domain_age_days;
    const domainStatus = domainAge == null ? 'unavailable' : domainAge < 30 ? 'danger' : 'safe';
    const domainValue = domainAge == null ? 'Unavailable' : `${domainAge} days`;

    const confidenceText = result.confidence != null && !isNaN(result.confidence) 
      ? `${result.confidence}%` 
      : 'Unavailable';

    return (
      <div className={`result-dashboard ${isPhishing ? 'dashboard-phishing' : 'dashboard-safe'}`} aria-live="assertive">
        
        {/* Header Section */}
        <div className="dashboard-header">
          <h2 className={isPhishing ? 'text-danger' : 'text-safe'}>
            {isPhishing ? 'PHISHING' : 'SAFE'}
          </h2>
          <div className="dashboard-risk-level">
            Risk Level: <strong>{result.risk_level ? result.risk_level.toUpperCase() : 'UNAVAILABLE'}</strong>
          </div>
          <RiskScore score={result.risk_score} riskLevel={result.risk_level} />
          <div className="dashboard-confidence mt-4">
            Confidence: {confidenceText}
          </div>
        </div>

        {/* URL Section */}
        <div className="dashboard-section url-section">
          <h3>Scanned URL</h3>
          <div className="url-display break-all">{result.url}</div>
        </div>

        {/* Security Signals */}
        <div className="dashboard-section">
          <h3>Security Signals</h3>
          <div className="signals-grid">
            <SecuritySignalCard title="SSL" value={sslValue} status={sslStatus} />
            <SecuritySignalCard title="Redirects" value={redirectValue} status={redirectStatus} />
            <SecuritySignalCard title="VirusTotal" value={vtValue} status={vtStatus} />
          </div>
        </div>

        {/* Domain Info */}
        <div className="dashboard-section">
          <h3>Domain Information</h3>
          <div className="domain-info-card">
            <span className="domain-label">Domain age:</span>
            <span className={`domain-value ${domainStatus === 'danger' ? 'text-danger' : ''}`}>{domainValue}</span>
          </div>
        </div>

        {/* Forensic Findings */}
        <ForensicFindings forensicReport={result.forensic_report} />

        {/* Explainability Panel */}
        <ExplainabilityPanel 
          explainability={result.explainability} 
          threatIntel={{
            virustotal: result.virustotal,
            ssl: result.ssl,
            whois: result.whois,
            redirect: result.redirect
          }} 
        />

        {/* Recommendation Section */}
        <div className="dashboard-section recommendation-box">
          <h3>Recommendation</h3>
          <p>{result.recommendation}</p>
        </div>

        {/* Footer */}
        <div className="dashboard-footer">
          <div className="footer-details">
            Analysis completed in {result.processing_time_ms} ms
          </div>
          <button onClick={onReset} className="reset-button">Scan Another URL</button>
        </div>

      </div>
    );
  }

  return null;
}
