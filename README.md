# PhishShield AI — AI-Powered Phishing Detection and Security Analysis

## 1. Project Description
**AI-powered phishing detection and security analysis for URLs, emails, and QR codes.**

PhishShield AI is an advanced, multi-layered cybersecurity platform designed to analyze suspicious digital content and identify potential phishing threats with high accuracy and interpretability. It integrates machine learning with deterministic threat intelligence and forensic analysis to provide actionable insights. *(Note: Email scanning is currently in development/planned and not yet active in the main pipeline).*

## 2. Key Features
- **URL Phishing Detection & Scanning Dashboard:** Input and scan any URL.
- **QR Code Scanning and Analysis:** Scan QR codes via camera or image upload, safely decoded and validated.
- **Machine-Learning-Based URL Classification**
- **Risk Scoring**
- **Threat Intelligence Analysis**
- **VirusTotal Integration**
- **SSL Certificate Validation**
- **WHOIS/Domain Information**
- **Redirect Analysis**
- **Deterministic Forensic Findings**
- **Explainable AI / Model Explainability**
- **Security Analysis Dashboard**
- **Browser Extension:** Scan current pages directly from the browser (Manifest V3).
- **Light/Dark Mode**
- **Responsive Frontend**

## 3. System Workflow
User Input -> URL / QR / other supported input -> Feature Extraction & Analysis -> ML Prediction -> Threat Intelligence -> Risk Aggregation -> Forensic Findings / Explainability -> Security Result

## 4. Machine Learning
The pipeline extracts features via local parsing and live network requests to build a feature vector for phishing URL classification.
- **Feature-based URL analysis:** The current trained URL model uses **47 features**.
- **XGBoost Primary Model:** A frozen XGBoost model (`xgboost_frozen.pkl`) is used as the authoritative production model.
- **Random Forest:** Evaluated as part of the model suite for high-accuracy predictions.

## 5. Security Intelligence
Incorporates external and live checks:
- **VirusTotal:** API-based malware detection.
- **SSL Validation:** Certificate validation.
- **WHOIS/Domain Intelligence:** Domain age and registration verification.
- **Redirect Tracking:** Chain tracking and protocol analysis.
- **Deterministic Forensic Analysis:** Extracts hard evidence to present categorical severity badges independently of ML.
- **Risk Aggregation:** Combines ML and deterministic factors into a unified risk score.

## 6. Explainable AI (XAI)
The dashboard provides a "Why this result?" section that visualizes the top factors contributing to a prediction, helping users understand the exact evidence pushing the model towards or away from a phishing prediction.

## 7. Browser Extension
A Manifest V3 Chrome Extension is provided for active-tab URL capture and result display directly in the browser.

## 8. QR Scanner
A built-in QR scanning workflow decodes QR payloads and analyzes them through the security pipeline when identified as valid HTTP/HTTPS URLs.

## 9. Technology Stack
**Frontend:**
- React / Vite
- Vanilla CSS / Semantic variables

**Backend:**
- Python
- FastAPI

**Machine Learning:**
- Scikit-learn
- XGBoost
- Pandas / NumPy

**Security Intelligence:**
- VirusTotal API
- WHOIS
- SSL Verification
- Redirect Analysis

## 10. Project Structure
```text
PhishShieldAI/
├── backend/            # FastAPI, Extractors, Services, Models
├── frontend/           # React, Vite, Dashboard UI
├── extension/          # Browser Extension
├── checkpoints/        # Development Phase Tracking
└── README.md
```

## 11. Installation / Running Locally

**Backend Setup**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app:app --reload
```

**Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

**Environment Variables**
- Backend: `.env` (Requires `VT_API_KEY`)
- Frontend: `.env.local` (`VITE_API_BASE_URL=http://localhost:8000`)

Ensure both backend and frontend servers are running concurrently.

## 12. Disclaimer
*PhishShield AI is intended for security analysis, research, and educational purposes. It should not be treated as an absolute guarantee that a website is safe. Always exercise caution and follow standard security practices.*
