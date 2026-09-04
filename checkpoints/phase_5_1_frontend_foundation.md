# PhishShield AI — Phase 5.1 Frontend Foundation

## Summary
Phase 5.1 established the initial frontend application for PhishShield AI using React, Vite, and JavaScript. The frontend was built entirely from scratch inside `D:\PhishShieldAI\frontend`, creating a modular and extensible component architecture to support subsequent dashboard expansions.

## Architectural Decisions
1. **Framework:** Used `React` + `Vite` for a lightweight and lightning-fast developer experience. Kept dependencies minimal.
2. **Styling:** Selected Vanilla CSS over Tailwind CSS to satisfy the requirement of not polluting the dependency tree with unnecessary packages if they weren't already configured. The vanilla styles establish a dark, professional cybersecurity appearance.
3. **API Integration:** Implemented `src/services/api.js` to perform safe `POST /predict` calls against `VITE_API_BASE_URL`.
4. **URL Preservation:** The `UrlScanner` component passes the exact, unmodified user input URL directly to the backend API, deferring authoritative validation to the established backend rules.
5. **Security:** No API keys are exposed. Handled connection and frontend validation errors gracefully without leaking stack traces.

## Backend Integrity
The existing FastAPI backend application (`D:\PhishShieldAI\backend`) and its ML logic remain 100% frozen and untouched.
