import { useState, useEffect } from 'react';

const TypewriterText = ({ text }) => {
  const [displayedText, setDisplayedText] = useState('');
  
  useEffect(() => {
    let i = 0;
    setDisplayedText('');
    const timer = setInterval(() => {
      if (i < text.length) {
        setDisplayedText(text.slice(0, i + 1));
        i++;
      } else {
        clearInterval(timer);
      }
    }, 35); // Fast, smooth typing speed
    return () => clearInterval(timer);
  }, [text]);

  return (
    <span>
      {displayedText}
      <span className="cursor-blink">|</span>
    </span>
  );
};

export default function Header({ theme, toggleTheme }) {
  return (
    <header className="header">
      <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ flex: 1 }}></div>
        <div style={{ textAlign: 'center' }}>
          <h1 className="header-title">PHISHSHIELD AI</h1>
          <p><TypewriterText text="AI-powered phishing detection and security analysis for URLs, emails, and QR codes." /></p>
        </div>
        <div style={{ flex: 1, display: 'flex', justifyContent: 'flex-end' }}>
          <button 
            onClick={toggleTheme} 
            className="theme-toggle-btn"
            title={theme === 'light' ? 'Switch to Dark Mode' : 'Switch to Light Mode'}
            aria-label="Toggle Theme"
          >
            {theme === 'light' ? (
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
            )}
          </button>
        </div>
      </div>
    </header>
  );
}
