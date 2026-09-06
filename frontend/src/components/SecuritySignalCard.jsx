export default function SecuritySignalCard({ title, value, status = 'neutral', children }) {
  // status: 'safe', 'danger', 'neutral', 'unavailable'
  const getStatusClass = () => {
    switch(status) {
      case 'safe': return 'signal-safe';
      case 'danger': return 'signal-danger';
      case 'unavailable': return 'signal-unavailable';
      default: return 'signal-neutral';
    }
  };

  return (
    <div className={`signal-card ${getStatusClass()}`}>
      <div className="signal-title">{title}</div>
      <div className="signal-value">{value}</div>
      {children && (
        <details className="signal-details">
          <summary>Details</summary>
          <div className="signal-details-content">
            {children}
          </div>
        </details>
      )}
    </div>
  );
}
