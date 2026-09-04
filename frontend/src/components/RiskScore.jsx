export default function RiskScore({ score, riskLevel }) {
  const isInvalid = score === null || score === undefined || isNaN(score);
  
  if (isInvalid) {
    return (
      <div className="risk-score-container" aria-label="Risk score unavailable">
        <div className="risk-score-header">
          <span className="risk-score-label">Risk Score</span>
          <span className="risk-score-value" style={{ color: 'var(--text-muted)' }}>Unavailable</span>
        </div>
      </div>
    );
  }

  const getScoreColor = (value) => {
    if (value <= 30) return 'var(--safe)';
    if (value <= 75) return 'var(--warning)';
    return 'var(--danger)';
  };

  const numericScore = Number(score);
  const color = getScoreColor(numericScore);
  const percentage = Math.min(100, Math.max(0, numericScore));
  const levelText = riskLevel || 'Unknown';

  return (
    <div className="risk-score-container" aria-label={`Risk score: ${numericScore} out of 100. Risk level: ${levelText}.`}>
      <div className="risk-score-header">
        <span className="risk-score-label">Risk Score</span>
        <span className="risk-score-value" style={{ color }}>{numericScore} / 100</span>
      </div>
      <div className="risk-meter-track" aria-hidden="true">
        <div 
          className="risk-meter-fill" 
          style={{ width: `${percentage}%`, backgroundColor: color }}
        ></div>
      </div>
    </div>
  );
}
