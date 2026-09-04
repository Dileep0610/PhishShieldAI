import React, { useState } from 'react';
import ContributionList from './ContributionList';
import EvidenceSection from './EvidenceSection';

export default function ExplainabilityPanel({ explainability, threatIntel }) {
  const [isExpanded, setIsExpanded] = useState(false);

  if (!explainability) {
    return (
      <div className="dashboard-section explainability-section">
        <h3>WHY THIS RESULT?</h3>
        <p className="text-muted">Explainability information is unavailable for this scan.</p>
      </div>
    );
  }

  if (explainability.status === 'unavailable') {
    return (
      <div className="dashboard-section explainability-section">
        <h3>WHY THIS RESULT?</h3>
        <p className="text-muted">{explainability.reason || "Explainability could not be generated for this scan."}</p>
      </div>
    );
  }

  const togglePanel = () => setIsExpanded(!isExpanded);

  // Combine top positive and negative contributors
  const modelExplanation = explainability.model_explanation || {};
  const topPositive = modelExplanation.top_positive_contributors || [];
  const topNegative = modelExplanation.top_negative_contributors || [];
  const contributors = [...topPositive, ...topNegative];

  const securityEvidence = explainability.security_evidence || {};

  return (
    <div className="dashboard-section explainability-section">
      <h3>WHY THIS RESULT?</h3>
      <p className="text-muted subtitle">Evidence used by the phishing detection model</p>
      
      <button 
        className="explainability-toggle" 
        onClick={togglePanel} 
        aria-expanded={isExpanded}
        aria-label="Toggle explainability details"
      >
        <span className="toggle-text">
          {isExpanded ? 'Hide Details' : 'View the model factors and security evidence behind this prediction.'}
        </span>
        <span className={`toggle-icon ${isExpanded ? 'expanded' : ''}`}>▼</span>
      </button>

      {isExpanded && (
        <div className="explainability-content">
          
          {/* Model Explanation */}
          <div className="explainability-block">
            <h4 className="explainability-block-title">Model Factors</h4>
            <p className="text-muted mb-2">Features that contributed most strongly to this prediction.</p>
            <p className="text-muted mb-3">Positive factors increase phishing likelihood, while negative factors reduce phishing likelihood.</p>
            <ContributionList contributors={contributors} />
          </div>

          {/* URL Evidence */}
          {(securityEvidence.url_evidence?.length > 0) && (
            <div className="explainability-block">
              <EvidenceSection 
                title="URL Security Evidence" 
                evidenceList={securityEvidence.url_evidence} 
              />
            </div>
          )}

          {/* HTML Evidence */}
          {(securityEvidence.html_evidence?.length > 0) && (
            <div className="explainability-block">
              <EvidenceSection 
                title="Website Security Evidence" 
                evidenceList={securityEvidence.html_evidence} 
              />
            </div>
          )}

          {/* Unavailable Evidence */}
          {(explainability.unavailable_evidence?.length > 0) && (
            <div className="explainability-block">
              <EvidenceSection 
                title="Unavailable Evidence" 
                evidenceList={explainability.unavailable_evidence} 
                isUnavailable={true}
              />
            </div>
          )}
          
          {/* Threat Intelligence */}
          <div className="explainability-block threat-intel-block">
            <h4 className="explainability-block-title">Threat Intelligence</h4>
            <div className="threat-intel-grid">
              
              <div className="threat-intel-card">
                <span className="threat-intel-label">VirusTotal</span>
                <span className="threat-intel-value">
                  {threatIntel?.virustotal?.malicious !== undefined 
                    ? `Malicious detections: ${threatIntel.virustotal.malicious}` 
                    : 'Unavailable'}
                </span>
              </div>
              
              <div className="threat-intel-card">
                <span className="threat-intel-label">SSL</span>
                <span className="threat-intel-value">
                  {threatIntel?.ssl?.ssl_valid !== undefined 
                    ? `Valid: ${threatIntel.ssl.ssl_valid ? 'Yes' : 'No'}` 
                    : 'Unavailable'}
                </span>
              </div>
              
              <div className="threat-intel-card">
                <span className="threat-intel-label">WHOIS</span>
                <span className="threat-intel-value">
                  {threatIntel?.whois?.domain_age_days !== undefined && threatIntel.whois.domain_age_days !== null
                    ? `Domain age: ${threatIntel.whois.domain_age_days} days` 
                    : 'Unavailable'}
                </span>
              </div>

              <div className="threat-intel-card">
                <span className="threat-intel-label">Redirects</span>
                <span className="threat-intel-value">
                  {threatIntel?.redirect?.redirect_count !== undefined 
                    ? `Count: ${threatIntel.redirect.redirect_count}` 
                    : 'Unavailable'}
                </span>
              </div>

            </div>
          </div>

        </div>
      )}
    </div>
  );
}
