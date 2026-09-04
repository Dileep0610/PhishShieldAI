import React from 'react';

export default function EvidenceSection({ title, evidenceList, isUnavailable = false }) {
  if (!evidenceList || evidenceList.length === 0) {
    return null;
  }

  return (
    <div className={`evidence-section ${isUnavailable ? 'evidence-unavailable' : ''}`}>
      <h4 className="evidence-title">{title}</h4>
      
      {isUnavailable && (
        <p className="text-muted mb-2">Some advanced website signals could not be reliably extracted from the live page. These signals were not guessed or replaced with synthetic values.</p>
      )}

      <ul className="evidence-list">
        {evidenceList.map((item, idx) => {
          if (typeof item === 'string') {
            return <li key={idx} className="evidence-item">{item}</li>;
          }
          
          if (isUnavailable && item.feature) {
            return (
              <li key={idx} className="evidence-item unavailable-item">
                <span className="evidence-feature">• {item.feature}</span>
                <span className="evidence-status text-muted">— Unavailable</span>
              </li>
            );
          }
          
          return null;
        })}
      </ul>
    </div>
  );
}
