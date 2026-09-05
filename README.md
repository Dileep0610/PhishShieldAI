# PhishShield AI

Digital phishing detection and explainable security intelligence platform.

## 1. Project Overview
PhishShield AI is an advanced, multi-layered platform designed to detect and explain phishing URLs with high accuracy and interpretability. It integrates machine learning with deterministic threat intelligence and forensic analysis to provide actionable insights.

## 2. Problem Statement
Phishing attacks are becoming increasingly sophisticated. Traditional blocklists are reactive, and pure machine learning models often operate as "black boxes" that fail to explain *why* a URL is considered malicious. PhishShield AI bridges this gap.

## 3. Objectives
- Proactively detect phishing URLs using a robust machine learning pipeline.
- Provide clear, interpretable explainability for ML predictions.
- Supplement ML predictions with deterministic forensic findings and threat intelligence.

## 4. Key Features
- **URL Scanning Dashboard:** Input and scan any URL.
- **QR Scanner:** Scan QR codes via camera or image upload, safely validated strictly as text payloads before scanning.
- **Browser Extension:** Scan current pages independently directly from the browser (Manifest V3).
- **Explainable AI (XAI):** Native XGBoost contribution mapping to explain prediction factors.
- **Threat Intelligence Integration:** Live VirusTotal, SSL, WHOIS, and redirect chain analysis.
- **Deterministic Forensic Engine:** Evaluates security signals independently of the ML model.
- **Responsive UI:** Modern React frontend with intuitive data visualization.

## 5. System Architecture
- **Frontend:** React (Vite)
- **Backend:** Python (FastAPI)
- **Model:** XGBoost
- **Extension:** Chrome Extension (Manifest V3)

## 6. Machine-Learning Pipeline
The pipeline normalizes the input URL, extracts features via local parsing and live network requests (HTML scraping), and builds a feature vector.

## 7. 47-Feature Dataset/Model Contract
The model expects an exact 47-feature vector covering URL structure, HTML properties, and real-time (RT) verified characteristics.

## 8. XGBoost Primary Model
A frozen XGBoost model (`xgboost_frozen.pkl`) is used as the authoritative production model, relying on the 47-feature contract.

## 9. Model Performance
Held-out evaluation results on the dataset:

* Logistic Regression: Accuracy 95.13% | Precision 94.48% | Recall 95.87% | F1 95.17% | ROC-AUC 98.68%
* Random Forest: Accuracy 98.67% | Precision 98.28% | Recall 99.07% | F1 98.67% | ROC-AUC 99.95%
* **XGBoost (Primary Production Model): Accuracy 98.80% | Precision 98.16% | Recall 99.47% | F1 98.81% | ROC-AUC 99.95%**
* MLP: Accuracy 96.80% | Precision 96.31% | Recall 97.33% | F1 96.82% | ROC-AUC 99.32%
* ResMLP: Accuracy 96.33% | Precision 95.78% | Recall 96.93% | F1 96.36% | ROC-AUC 99.32%

## 10. Explainable AI
The dashboard provides a "Why this result?" section that visualizes the top factors pushing the model towards or away from a phishing prediction.

## 11. Threat Intelligence
Incorporates external and live checks:
- **VirusTotal:** API-based malware detection.
- **SSL:** Certificate validation.
- **WHOIS:** Domain age and registration verification.
- **Redirects:** Chain tracking and protocol analysis.

## 12. Deterministic Forensic Findings
A dedicated Forensic Engine extracts and assesses hard evidence (e.g., HTTP usage, relative forms, missing titles) to present categorical severity badges, irrespective of ML probabilities.

## 13. Unavailable Evidence Handling
Gracefully handles missing or unreachable features (e.g., timeout when fetching HTML) by safely replacing them and tagging them as "unavailable" in the explainability dashboard, preventing crashes while preserving model integrity.

## 14. Technology Stack
- **Frontend:** React, Vite, CSS
- **Backend:** Python, FastAPI, XGBoost, BeautifulSoup, requests
- **Extension:** HTML, CSS, Vanilla JS

## 15. Backend Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app:app --reload
```

## 16. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 17. Extension Setup
Load the `extension/` directory as an unpacked extension in Chrome via `chrome://extensions`.

## 18. Environment Variables
- Backend: `.env` (See `.env.example` for `VT_API_KEY`)
- Frontend: `.env.local` (`VITE_API_BASE_URL=http://localhost:8000`)

## 19. Running Locally
Ensure both backend and frontend servers are running concurrently.

## 20. API Overview
- `POST /predict`: Main endpoint accepting a URL string, returning ML predictions, explainability metrics, and deterministic forensic findings.

## 21. Project Structure
```
PhishShieldAI/
├── backend/            # FastAPI, Extractors, Services, Models
├── frontend/           # React, Vite, Dashboard UI
├── extension/          # Browser Extension
├── checkpoints/        # Development Phase Tracking
└── README.md
```

## 22. Security Considerations
API keys and environment secrets must be stored securely and excluded from source control. Forms and internal components use secure communication practices where available. QR scanning executes strictly as a local parsing action without remote fetching.

## 23. Current Development Status
Risk Intelligence, Forensic Layer, Browser Extension, and QR Scanning are fully implemented. 

## 24. Future Modules (Planned/Upcoming)
- Email scanning
- Authentication
- Scan history/analytics
- Production deployment
