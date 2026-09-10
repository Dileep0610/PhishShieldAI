import RiskScore from './RiskScore';
import ExplainabilityPanel from './ExplainabilityPanel';
import ForensicFindings from './ForensicFindings';
import SecuritySignalCard from './SecuritySignalCard';

export default function EmailScanResult({ status, result, error, onReset }) {
  if (status === 'IDLE') {
    return (
      <div className="result-card idle" aria-live="polite">
        <p>Enter an email above to analyze its phishing risk.</p>
      </div>
    );
  }

  if (status === 'SCANNING') {
    return (
      <div className="result-card scanning" aria-live="polite" aria-busy="true">
        <div className="loader" role="status" aria-label="Loading"></div>
        <p className="primary-msg">Analyzing Email...</p>
        <p className="subtext">Extracting security features and evaluating risk.</p>
      </div>
    );
  }

  if (status === 'ERROR') {
    return (
      <div className="result-card error-card" aria-live="assertive">
        <h3>Analysis Failed</h3>
        <p>{error}</p>
        <button onClick={onReset} className="reset-button">Scan Another Email</button>
      </div>
    );
  }

  if (status === 'SUCCESS' && result) {
    const report = result.security_report;
    const isPhishing = report ? report.verdict.prediction === 'Phishing' : result.prediction === 'Phishing';
    
    const riskLevel = report ? report.verdict.risk_level : result.overall_risk_level || result.risk_level;
    const primaryReason = report ? report.verdict.primary_reason : result.primary_reason;
    const recommendation = report ? report.verdict.recommendation : result.recommendation;
    const processingTime = report ? report.metadata.processing_time_ms : result.processing_time_ms;
    
    // ML Evidence
    const mlEvidence = report ? report.ml_evidence : { prediction: result.prediction, decision_score: result.decision_score };
    const decisionScore = mlEvidence ? mlEvidence.decision_score : result.decision_score;

    // Forensic Evidence
    const forensicEvidence = report ? report.forensic_evidence : {
      summary: result.forensic_summary,
      indicators: result.forensic_indicators
    };
    
    // URLs
    const urls = result.extracted_urls || [];
    const urlAnalysis = result.url_analysis || [];

    // Explainability
    const explainability = report ? report.explainability : result.explainability;

    return (
      <div className={`result-dashboard ${isPhishing ? 'dashboard-phishing' : 'dashboard-safe'}`} aria-live="assertive">
        
        {/* Header Section */}
        <div className="dashboard-header">
          <h2 className={isPhishing ? 'text-danger' : 'text-safe'}>
            {isPhishing ? 'PHISHING' : 'SAFE'}
          </h2>
          <div className="dashboard-risk-level">
            Risk Level: <strong>{riskLevel ? riskLevel.toUpperCase() : 'UNAVAILABLE'}</strong>
          </div>
          {/* Note: RiskScore currently takes a score (0-100), decision score is not a 0-100 score. 
              We pass riskLevel directly to RiskScore if score isn't relevant, or omit score if it's ML decision score. */}
          <RiskScore riskLevel={riskLevel} />
          
          {primaryReason && (
             <div className="mt-2 text-muted">
               <strong>Reason:</strong> {primaryReason}
             </div>
          )}
        </div>

        {/* ML Evidence */}
        <div className="dashboard-section">
          <h3>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
            ML Evidence
          </h3>
          <div className="domain-info-card" style={{ display: 'block' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
               <span className="domain-label">Prediction:</span>
               <span className={`domain-value ${mlEvidence?.prediction === 'Phishing' ? 'text-danger' : 'text-safe'}`}>{mlEvidence?.prediction || 'Unavailable'}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
               <span className="domain-label">Decision Score:</span>
               <span className="domain-value">{decisionScore != null ? decisionScore.toFixed(3) : 'Unavailable'}</span>
            </div>
          </div>
        </div>

        {/* Forensic Findings */}
        {forensicEvidence && (
           <ForensicFindings forensicReport={forensicEvidence} />
        )}

        {/* URL Evidence */}
        <div className="dashboard-section">
          <h3>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
            Extracted URLs
          </h3>
          {urls.length === 0 ? (
             <p className="text-muted" style={{ padding: '0 20px' }}>No URLs detected in this email.</p>
          ) : (
             <div className="signals-grid">
               {urls.map((url, idx) => {
                 const analysis = urlAnalysis.find(u => u.url === url) || {};
                 const urlPrediction = analysis.prediction || 'Unknown';
                 const urlRisk = analysis.risk_level || 'Unknown';
                 const isUrlDanger = urlPrediction === 'Phishing';
                 return (
                   <SecuritySignalCard 
                     key={idx}
                     title={`URL ${idx + 1}`}
                     value={urlRisk}
                     status={isUrlDanger ? 'danger' : (urlRisk === 'Unknown' ? 'unavailable' : 'safe')}
                   >
                     <div style={{ wordBreak: 'break-all', marginBottom: '8px', fontSize: '0.9rem' }}>{url}</div>
                     <div><strong>Prediction:</strong> <span className={isUrlDanger ? 'text-danger' : 'text-safe'}>{urlPrediction}</span></div>
                     {analysis.risk_score != null && <div><strong>Risk Score:</strong> {analysis.risk_score}</div>}
                   </SecuritySignalCard>
                 );
               })}
             </div>
          )}
        </div>

        {/* Explainability Panel */}
        {explainability && (
          <ExplainabilityPanel 
            explainability={explainability} 
            threatIntel={null} 
          />
        )}

        {/* Recommendation Section */}
        {recommendation && (
          <div className="dashboard-section recommendation-box">
            <h3>
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>
              Recommendation
            </h3>
            <p>{recommendation}</p>
          </div>
        )}

        {/* Footer */}
        <div className="dashboard-footer">
          <div className="text-muted mt-4" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.85rem' }}>
            <span style={{ marginRight: '5px' }}>⏱️</span>
            Analysis completed in {processingTime != null ? processingTime : '?'} ms
          </div>
          <button onClick={onReset} className="reset-button">Scan Another Email</button>
        </div>

      </div>
    );
  }

  return null;
}
