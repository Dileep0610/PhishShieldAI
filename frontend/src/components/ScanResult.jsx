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
            Confidence: <strong>{confidenceText}</strong>
          </div>
        </div>

        {/* URL Section */}
        <div className="dashboard-section url-section">
          <h3>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
            Scanned URL
          </h3>
          <div className="url-display break-all">{result.url}</div>
        </div>

        {/* Security Signals */}
        <div className="dashboard-section">
          <h3>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
            Security Signals
          </h3>
          <div className="signals-grid">
            <SecuritySignalCard title="SSL" value={sslValue} status={sslStatus}>
              {result.ssl ? (
                <>
                  <div><strong>Issuer:</strong> {result.ssl.issuer || 'Unknown'}</div>
                  <div><strong>Expires:</strong> {result.ssl.expiry_date || 'Unknown'}</div>
                  {result.ssl.days_until_expiry != null && (
                    <div>{result.ssl.days_until_expiry} days remaining</div>
                  )}
                </>
              ) : (
                <div>SSL information unavailable</div>
              )}
            </SecuritySignalCard>
            <SecuritySignalCard title="Redirects" value={redirectValue} status={redirectStatus}>
              {result.redirect ? (
                <>
                  <div><strong>Final URL:</strong><br/><span style={{wordBreak: 'break-all'}}>{result.redirect.final_url || 'Unknown'}</span></div>
                  <div><strong>Domain changed:</strong> {result.redirect.domain_changed ? 'Yes' : 'No'}</div>
                  <div><strong>Protocol changed:</strong> {result.redirect.protocol_changed ? 'Yes' : 'No'}</div>
                  <div><strong>URL shortener:</strong> {result.redirect.uses_shortener ? 'Yes' : 'No'}</div>
                </>
              ) : (
                <div>Redirect information unavailable</div>
              )}
            </SecuritySignalCard>
            <SecuritySignalCard title="VirusTotal" value={vtValue} status={vtStatus}>
              {result.virustotal ? (
                <>
                  <div><strong>Malicious:</strong> {result.virustotal.malicious}</div>
                  <div><strong>Suspicious:</strong> {result.virustotal.suspicious}</div>
                  <div><strong>Harmless:</strong> {result.virustotal.harmless}</div>
                  <div><strong>Undetected:</strong> {result.virustotal.undetected}</div>
                </>
              ) : (
                <div>VirusTotal information unavailable</div>
              )}
            </SecuritySignalCard>
          </div>
        </div>

        {/* Domain Info */}
        <div className="dashboard-section">
          <h3>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
            Domain Information
          </h3>
          <div className="domain-info-card" style={{ display: 'block' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span className="domain-label">Domain age:</span>
              <span className={`domain-value ${domainStatus === 'danger' ? 'text-danger' : ''}`}>{domainValue}</span>
            </div>
            {result.whois && result.whois.domain_age_days != null && (
              <details className="signal-details" style={{ marginTop: '10px' }}>
                <summary>Details</summary>
                <div className="signal-details-content">
                  <div><strong>Registrar:</strong> {result.whois.registrar || 'Unknown'}</div>
                  <div><strong>Created:</strong> {result.whois.creation_date || 'Unknown'}</div>
                  <div><strong>Expires:</strong> {result.whois.expiration_date || 'Unknown'}</div>
                </div>
              </details>
            )}
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
          <h3>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
            Recommendation
          </h3>
          <p>{result.recommendation}</p>
        </div>

        {/* Footer */}
        <div className="dashboard-footer">
          <div className="text-muted mt-4" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.85rem' }}>
            <span style={{ marginRight: '5px' }}>⏱️</span>
            Analysis completed in {result.processing_time_ms} ms
          </div>
          <button onClick={onReset} className="reset-button">Scan Another URL</button>
        </div>

      </div>
    );
  }

  return null;
}
