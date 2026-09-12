<div align="center">

# PhishShield AI
**Intelligent Phishing Detection & Security Analysis Platform**

[![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-150458?style=for-the-badge&logo=xgboost&logoColor=white)](https://xgboost.ai/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Chrome Extension](https://img.shields.io/badge/Chrome_Extension-4285F4?style=for-the-badge&logo=google-chrome&logoColor=white)](https://developer.chrome.com/docs/extensions/mv3/)

</div>

## 📖 1. Project Introduction

PhishShield AI is an intelligent security-analysis platform designed for high-accuracy phishing detection. By combining advanced Machine Learning models, deterministic threat intelligence, and security forensics, the system delivers highly accurate and explainable results.

It supports:
- URL phishing detection
- Email phishing detection
- QR-based analysis
- Threat intelligence (VirusTotal, WHOIS, SSL)
- Security forensics (Hidden iframes, redirects, etc.)
- Explainable security results
- Browser-based URL scanning

---

## ✨ 2. Key Features

- 🤖 **AI/ML-based URL phishing detection**
- 📧 **Email phishing detection**
- 🔗 **URL extraction from emails**
- 🧠 **Combined email + URL risk intelligence**
- ⚠️ **Deterministic risk scoring**
- 🔍 **Email forensic analysis**
- 💡 **Explainable "Why This Result?" analysis**
- 🛡️ **Unified Security Report**
- 🌐 **WHOIS intelligence**
- 🔐 **SSL/TLS analysis**
- 🔄 **Redirect analysis**
- 🦠 **VirusTotal threat intelligence**
- 📱 **QR scanner**
- 🧩 **URL browser extension**
- 🖥️ **Responsive web dashboard**

---

## 🏗️ 3. System Architecture

```mermaid
flowchart TD
    User([User])

    subgraph UserInterfaces [User Interfaces]
        WebDash[Web Dashboard]
        QRScan[QR Scanner]
        BrowserExt[URL Browser Extension]
    end

    subgraph Backend [FastAPI Backend]
        API[FastAPI Gateway]
    end

    subgraph AnalysisEngine [Analysis & Intelligence]
        URLAnalysis[URL Analysis]
        EmailAnalysis[Email Analysis]
        URLExtract[URL Extraction]
        Risk[Risk Engine]
        Forensics[Forensic Analysis]
        Explain[Explainability]
        
        Models[ML Models]
        WHOIS[WHOIS]
        SSL[SSL/TLS]
        Redirects[Redirect Analysis]
        VT[VirusTotal]
    end
    
    subgraph Report [Security Report]
        Verdict[Final Security Verdict: Prediction, Risk Level, Score, Evidence, Recommendations]
    end

    User --> WebDash
    User --> QRScan
    User --> BrowserExt

    WebDash --> API
    QRScan --> API
    BrowserExt --> API

    API --> URLAnalysis
    API --> EmailAnalysis
    
    EmailAnalysis --> URLExtract
    URLExtract --> URLAnalysis
    
    URLAnalysis --> Models
    EmailAnalysis --> Models
    
    URLAnalysis --> WHOIS
    URLAnalysis --> SSL
    URLAnalysis --> Redirects
    URLAnalysis --> VT
    URLAnalysis --> Forensics
    EmailAnalysis --> Forensics
    
    Models --> Risk
    WHOIS --> Risk
    SSL --> Risk
    Redirects --> Risk
    VT --> Risk
    Forensics --> Risk
    
    Models --> Explain
    
    Risk --> Verdict
    Explain --> Verdict
```

---

## 🤖 4. URL Detection

The URL phishing detection pipeline relies on extracting **47 distinct features** from target URLs, including lexical, structural, and network-level properties.

- **XGBoost Classifier**: The primary ML engine uses an XGBoost-based prediction model (`xgboost_frozen.pkl`).
- **Random Forest Comparison**: Evaluated alongside XGBoost, an optimized Random Forest model demonstrated comparable high performance.
- The pipeline provides an ML prediction, a confidence score, a deterministic risk score, threat intelligence signals, and aggregates these into a final security verdict.

---

## 📧 5. Email Detection

The platform provides a comprehensive pipeline for scanning email content:
- **Email Input** -> **TF-IDF Vectorization** -> **Linear SVM** -> **Email Prediction**.
- **Linear SVM** serves as the production email model.
- (A **BiLSTM** model was evaluated as an experimental deep-learning model).
- Automatically performs **URL Extraction** on email bodies and passes them through the URL Analysis pipeline.
- Performs **Forensic Analysis** on email properties.
- Integrates **Explainability** and **Risk Aggregation** to generate a unified security report.

---

## 🔍 6. Security Intelligence

PhishShield AI enhances ML predictions with deterministic security intelligence:
- **WHOIS**: Analyzes domain age and registration anomalies.
- **SSL Certificate Validation**: Checks for missing, invalid, or suspicious TLS/SSL certificates.
- **Redirect Tracking**: Detects suspicious redirection chains and obfuscation tactics.
- **VirusTotal**: API integration to check against known malware and phishing engines.
- **Deterministic Risk Scoring**: Applies rigid penalty rules based on intelligence to adjust the final score.
- **Forensic Indicators**: Identifies hidden iframes, scripts, and embedded threats.
- **Explainability**: Clarifies exactly how these signals contribute to the final security analysis.

---

## ⚠️ 7. Risk Levels

The system combines available security signals (ML, Forensics, Intelligence) and maps them into clear risk levels:
- 🟢 **Very Safe**
- 🔵 **Safe**
- 🟡 **Suspicious**
- 🟠 **High Risk**
- 🔴 **Very High Risk**

*Note: The ML prediction is an isolated component; the final Risk Level is a unified result of all evidence combined by the Risk Engine.*

---

## 🛡️ 8. Unified Security Report

The final output is a structured `SecurityReport` encompassing these major evidence categories:
- **ML Evidence**: Confidence scores, probabilities, and raw predictions.
- **Forensic Evidence**: Hard indicators (e.g., hidden elements, zero-day domains).
- **URL Evidence**: Direct lexical and structural details from the URL.
- **Threat Intelligence**: Data from VirusTotal, WHOIS, and SSL validation.
- **Explainability**: Factors directly influencing the ML model's decision.
- **Verdict & Metadata**: The aggregated risk level, recommendations, and processing details.

---

## 🧩 9. Browser Extension

The PhishShield **URL Browser Extension** provides seamless protection in the browser:
- Built with **Chrome Manifest V3**.
- Automatically performs **active-tab URL capture**.
- Sends the URL securely to the local PhishShield backend for analysis.
- Displays a clean popup with the **prediction**, **confidence**, **risk score**, **risk level**, **recommendation**, and **threat/security signals**.
- Features safe handling of unsupported browser URLs (e.g., `chrome://`).

---

## 📂 10. Project Structure

```text
PhishShieldAI/
├── backend/
│   ├── api/
│   ├── config/
│   ├── debug/
│   ├── extractors/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── tests/
│   └── utils/
├── checkpoints/
├── datasets/
├── extension/
├── frontend/
├── logs/
├── notebooks/
└── README.md
```

---

## 🔌 11. API Endpoints

- `POST /predict`
  - *Purpose*: Analyzes a target URL and returns a unified `SecurityReport`.
- `POST /api/analyze-email`
  - *Purpose*: Analyzes raw email text, extracts URLs, and returns a combined `SecurityReport`.
- `GET /health`
  - *Purpose*: Validates the operational status of the FastAPI backend.

---

## 📊 12. ML Performance

**URL Models:**
| Model | Accuracy |
| :--- | :--- |
| Decision Tree | 96.50% |
| XGBoost | 98.50% |
| Random Forest | 98.60% |
| Optimized Random Forest | 98.65% |

**Email Models:**
| Model | Accuracy |
| :--- | :--- |
| Multinomial Naive Bayes | 98.28% |
| Logistic Regression | 99.53% |
| BiLSTM *(Experimental)* | 99.65% |
| **Linear SVM** *(Production)* | **99.76%** |

---

## 🚀 13. Setup & Usage

**1. Clone Repository:**
```bash
git clone https://github.com/Dileep0610/PhishShieldAI.git
cd PhishShieldAI
```

**2. Backend Setup:**
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app:app --reload
```

**3. Frontend Setup:**
```bash
cd ../frontend
npm install
npm run dev
```

**4. Browser Extension:**
- Open Chrome and navigate to `chrome://extensions/`
- Enable "Developer mode" (top right)
- Click "Load unpacked" and select the `extension/` directory.

**Usage:**
- **Scan a URL:** Enter the URL in the main Web Dashboard input.
- **Analyze an Email:** Switch to the Email Analysis tab and paste the email text.
- **Use QR Scanner:** Click the QR scanner tab to decode a QR image.

---

## ⚠️ 14. Limitations

- Threat intelligence features (like VirusTotal) depend on external API availability and usage limits.
- The WHOIS intelligence module may occasionally be blocked by registrars limiting automated queries.

---

## 🔮 15. Future Scope

- **Email Browser Extension**: Integration of email scanning capabilities directly into email client interfaces.
- Broader email-provider integration.
- Improved threat-intelligence coverage.
- Production deployment.
- Additional security intelligence sources.

---

## 👨‍💻 16. Author

**Kothakota Dileep Kumar**
- 🔗 LinkedIn: [https://www.linkedin.com/in/dileep0610/](https://www.linkedin.com/in/dileep0610/)
- 🌐 Portfolio: [https://dileepkumar-flax.vercel.app/](https://dileepkumar-flax.vercel.app/)
- 🐙 GitHub: [https://github.com/Dileep0610](https://github.com/Dileep0610)

---

*Disclaimer: PhishShield AI is intended for security analysis, research, and educational purposes. It should not be treated as an absolute guarantee that a website or email is safe or malicious. Always exercise caution and follow standard security practices.*
