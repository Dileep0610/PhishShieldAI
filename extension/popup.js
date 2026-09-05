document.addEventListener('DOMContentLoaded', () => {
    // Buttons
    const scanButton = document.getElementById('scan-button');
    const scanAgainSuccess = document.getElementById('scan-again-success-button');
    const scanAgainError = document.getElementById('scan-again-error-button');
    
    // States
    const stateIdle = document.getElementById('state-idle');
    const stateLoading = document.getElementById('state-loading');
    const stateError = document.getElementById('state-error');
    const stateSuccess = document.getElementById('state-success');
    
    // UI Elements
    const urlDisplay = document.getElementById('current-url');
    const errorMessage = document.getElementById('error-message');
    const resultBadge = document.getElementById('result-badge');
    const riskScoreDisplay = document.getElementById('risk-score');
    const confidenceScoreDisplay = document.getElementById('confidence-score');
    
    // Security Signals
    const signalSsl = document.getElementById('signal-ssl');
    const signalRedirects = document.getElementById('signal-redirects');
    const signalVt = document.getElementById('signal-vt');
    const signalDomain = document.getElementById('signal-domain');
    
    // Forensics & Recs
    const findingsList = document.getElementById('findings-list');
    const recommendationArea = document.getElementById('recommendation-area');
    
    const API_BASE_URL = 'http://127.0.0.1:8000';
    const REQUEST_TIMEOUT_MS = 15000;
    
    init();

    function init() {
        scanButton.addEventListener('click', handleScanClick);
        scanAgainSuccess.addEventListener('click', () => setUIState('IDLE'));
        scanAgainError.addEventListener('click', () => setUIState('IDLE'));
    }

    function validateURL(urlStr) {
        if (!urlStr || urlStr.trim() === '') {
            return { valid: false, error: 'Empty URL. Cannot scan this page.' };
        }
        
        try {
            const parsedUrl = new URL(urlStr);
            if (parsedUrl.protocol === 'http:' || parsedUrl.protocol === 'https:') {
                return { valid: true, url: urlStr };
            } else {
                return { valid: false, error: 'This page cannot be scanned. Please open a normal HTTP or HTTPS webpage.' };
            }
        } catch (e) {
            return { valid: false, error: 'Invalid URL format.' };
        }
    }

    function displayError(msg) {
        setUIState('ERROR');
        errorMessage.textContent = msg;
    }

    async function handleScanClick() {
        setUIState('LOADING');
        
        if (!chrome || !chrome.tabs || !chrome.tabs.query) {
            displayError("Chrome extension API is not available.");
            return;
        }

        try {
            chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
                if (chrome.runtime.lastError) {
                    displayError('Error querying active tab: ' + chrome.runtime.lastError.message);
                    return;
                }
                
                if (!tabs || tabs.length === 0) {
                    displayError('No active tab found.');
                    return;
                }

                const activeTab = tabs[0];
                const activeUrl = activeTab.url;
                const validationResult = validateURL(activeUrl);

                if (!validationResult.valid) {
                    displayError(validationResult.error);
                } else {
                    await scanUrl(validationResult.url);
                }
            });
        } catch (err) {
            displayError('An unexpected error occurred: ' + err.message);
        }
    }
    
    async function scanUrl(url) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);
        
        try {
            const response = await fetch(`${API_BASE_URL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url }),
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                let errMsg = 'Unexpected response from PhishShield backend.';
                if (response.status === 400 || response.status === 422) {
                    errMsg = 'Invalid URL request.';
                } else if (response.status >= 500) {
                    errMsg = 'PhishShield backend is unavailable.';
                }
                throw new Error(errMsg);
            }
            
            const data = await response.json();
            renderSuccessState(url, data);
            
        } catch (error) {
            clearTimeout(timeoutId);
            if (error.name === 'AbortError') {
                displayError('Scan timed out. Please try again.');
            } else if (error.message === 'Failed to fetch') {
                displayError('PhishShield backend is unavailable or CORS blocked the request.');
            } else {
                displayError(error.message);
            }
        }
    }

    function renderSuccessState(url, data) {
        // Scanned URL
        urlDisplay.textContent = url;
        
        // Primary Verdict
        const prediction = data.prediction;
        resultBadge.textContent = prediction || "UNKNOWN";
        if (prediction === "Phishing") {
            resultBadge.className = "badge phishing";
        } else if (prediction === "Legitimate") {
            resultBadge.className = "badge safe";
            resultBadge.textContent = "SAFE";
        } else {
            resultBadge.className = "badge";
        }
        
        // Risk Score
        if (data.risk_score !== undefined && data.risk_score !== null) {
            riskScoreDisplay.textContent = data.risk_score;
        } else {
            riskScoreDisplay.textContent = 'Unavailable';
        }
        
        // Confidence
        if (data.confidence !== undefined && data.confidence !== null) {
            confidenceScoreDisplay.textContent = `${data.confidence.toFixed(1)}%`;
        } else {
            confidenceScoreDisplay.textContent = 'Unavailable';
        }

        // Security Signals
        // SSL
        if (data.ssl) {
            signalSsl.textContent = data.ssl.ssl_valid ? 'Valid' : 'Invalid';
        } else {
            signalSsl.textContent = 'Unavailable';
        }
        
        // Redirects
        if (data.redirect && data.redirect.redirect_count !== undefined) {
            signalRedirects.textContent = data.redirect.redirect_count.toString();
        } else {
            signalRedirects.textContent = 'Unavailable';
        }
        
        // VirusTotal
        if (data.virustotal && data.virustotal.malicious !== undefined) {
            signalVt.textContent = `${data.virustotal.malicious} Malicious`;
        } else {
            signalVt.textContent = 'Unavailable';
        }
        
        // Domain Age
        if (data.whois && data.whois.domain_age_days !== undefined && data.whois.domain_age_days !== null) {
            signalDomain.textContent = `${data.whois.domain_age_days} days`;
        } else {
            signalDomain.textContent = 'Unavailable';
        }

        // Forensic Findings
        findingsList.textContent = ''; // safe clear before appending
        const findings = data.forensic_report && data.forensic_report.findings ? data.forensic_report.findings : [];
        
        if (findings.length === 0) {
            const li = document.createElement('li');
            li.className = 'no-findings';
            li.textContent = 'No forensic findings detected.';
            findingsList.appendChild(li);
        } else {
            const validSeverities = ['INFO', 'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'];
            findings.forEach(finding => {
                const li = document.createElement('li');
                li.className = 'finding-item';
                
                const header = document.createElement('div');
                header.className = 'finding-header';
                
                const sevBadge = document.createElement('span');
                const safeSeverity = validSeverities.includes(finding.severity) ? finding.severity : 'INFO';
                sevBadge.className = `finding-severity sev-${safeSeverity}`;
                sevBadge.textContent = safeSeverity;
                
                const titleStr = document.createElement('span');
                titleStr.className = 'finding-title';
                titleStr.textContent = finding.title || 'Finding';
                
                header.appendChild(sevBadge);
                header.appendChild(titleStr);
                
                const desc = document.createElement('div');
                desc.className = 'finding-desc';
                desc.textContent = finding.description || '';
                
                li.appendChild(header);
                li.appendChild(desc);
                
                findingsList.appendChild(li);
            });
        }
        
        // Recommendation
        recommendationArea.textContent = data.recommendation || 'Recommendation unavailable';
        
        setUIState('SUCCESS');
    }

    function setUIState(state) {
        stateIdle.classList.add('hidden');
        stateLoading.classList.add('hidden');
        stateError.classList.add('hidden');
        stateSuccess.classList.add('hidden');

        switch (state) {
            case 'IDLE':
                stateIdle.classList.remove('hidden');
                break;
            case 'LOADING':
                stateLoading.classList.remove('hidden');
                break;
            case 'SUCCESS':
                stateSuccess.classList.remove('hidden');
                break;
            case 'ERROR':
                stateError.classList.remove('hidden');
                break;
        }
    }
});
