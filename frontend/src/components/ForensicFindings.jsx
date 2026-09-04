import React from 'react';

export default function ForensicFindings({ forensicReport }) {
  const findings = forensicReport?.findings;

  // Empty State
  if (!findings || !Array.isArray(findings) || findings.length === 0) {
    return (
      <div className="dashboard-section forensic-findings">
        <h3>FORENSIC FINDINGS</h3>
        <p className="forensic-disclaimer">
          These findings are deterministic observations from the scanned URL, page content, and available security intelligence. They do not replace the machine-learning prediction.
        </p>
        <div className="forensic-empty-state">
          No deterministic forensic findings were returned from the available evidence.
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-section forensic-findings">
      <h3>FORENSIC FINDINGS</h3>
      <p className="forensic-disclaimer">
        These findings are deterministic observations from the scanned URL, page content, and available security intelligence. They do not replace the machine-learning prediction.
      </p>

      <div className="forensic-cards-container">
        {findings.map((finding, idx) => {
          // Safety fallbacks
          if (!finding) return null;
          
          const severity = finding.severity || 'UNKNOWN';
          const category = finding.category || 'UNKNOWN';
          const title = finding.title || 'Untitled finding';
          const description = finding.description || 'Unavailable';
          const evidence = finding.evidence || 'Unavailable';
          const source = finding.source || 'Unavailable';
          const remediation = finding.remediation || 'Unavailable';

          return (
            <div key={finding.finding_id || idx} className="forensic-card">
              <div className="forensic-card-header">
                <span className={`forensic-severity severity-${severity.toLowerCase()}`}>
                  {severity}
                </span>
                <span className="forensic-category-dot">·</span>
                <span className="forensic-category">{category}</span>
              </div>
              
              <h4 className="forensic-title">{title}</h4>
              <p className="forensic-description">{description}</p>
              
              <details className="forensic-details">
                <summary>Evidence and details</summary>
                <div className="forensic-details-content">
                  <div className="detail-row">
                    <strong>Evidence</strong>
                    <div className="detail-value">{evidence}</div>
                  </div>
                  <div className="detail-row">
                    <strong>Source</strong>
                    <div className="detail-value">{source}</div>
                  </div>
                  <div className="detail-row">
                    <strong>Recommended action</strong>
                    <div className="detail-value">{remediation}</div>
                  </div>
                </div>
              </details>
            </div>
          );
        })}
      </div>
    </div>
  );
}
