import React from 'react';

export default function ContributionList({ contributors }) {
  if (!contributors || contributors.length === 0) {
    return <p className="text-muted">No model factors available.</p>;
  }

  // Find max contribution for scaling visually (but never normalize the actual value displayed)
  const maxContrib = Math.max(...contributors.map(c => Math.abs(c.contribution)));

  return (
    <div className="contribution-list">
      {contributors.map((contrib, idx) => {
        const isPositive = contrib.direction === 'phishing';
        const percentWidth = maxContrib === 0 ? 0 : (Math.abs(contrib.contribution) / maxContrib) * 100;
        
        return (
          <div key={`${contrib.feature}-${idx}`} className="contribution-row">
            <div className="contribution-info">
              <span className="contribution-feature" title={contrib.feature}>
                {contrib.human_name || contrib.feature}
              </span>
              <span className={`contribution-value ${isPositive ? 'text-danger' : 'text-safe'}`}>
                {contrib.contribution > 0 ? '+' : ''}{contrib.contribution.toFixed(4)}
              </span>
            </div>
            
            <div className="contribution-direction-label text-muted">
              {isPositive ? 'Increases phishing likelihood' : 'Decreases phishing likelihood'}
            </div>
            
            <div className="contribution-bar-container">
              <div 
                className={`contribution-bar ${isPositive ? 'bar-phishing' : 'bar-safe'}`} 
                style={{ width: `${percentWidth}%` }}
                aria-hidden="true"
              ></div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
