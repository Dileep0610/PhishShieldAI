# Phase 8.1 Browser Extension Architecture Audit

## Overview
This document serves as the architectural blueprint for the PhishShield AI Chrome Browser Extension.

## Current Architecture
- Backend: FastAPI
- Frontend: React + Vite
- Existing API: POST `/predict` accepts a JSON `{ "url": "..." }` and returns a highly detailed JSON response containing risk level, confidence, explainability, and forensics.

## Recommended Extension Architecture
- **Manifest Version:** V3
- **Components:** Popup only. No service worker or content scripts needed.
- **Permissions:** `activeTab` only. This provides temporary access to the currently active tab when the user clicks the extension, satisfying the minimum privilege requirement.

## Strategy
- **URL Capture:** Use `chrome.tabs.query({active: true, currentWindow: true})` inside the popup script when opened.
- **Backend Communication:** The popup will issue a `fetch()` POST request directly to the backend's `/predict` endpoint.
- **CORS Requirements:** The backend `ALLOWED_ORIGINS` currently limits access to localhost web ports. It must be updated to include the extension's origin (`chrome-extension://...`) or allow all origins if dynamic. (NO BACKEND CHANGES MADE YET).

## Security Risks & Strategy
- **Secrets:** No API keys or backend secrets will be bundled into the extension.
- **CSP:** A strict Content Security Policy avoiding `unsafe-eval` and `unsafe-inline`.
- **Navigation:** The extension will not navigate the user, only report on the URL.

## UX & Error Handling
- **Duplicate Scans:** Disable the "Scan" button while a request is in flight.
- **Error Handling:** Gracefully handle network timeouts and HTTP errors with user-friendly messages (no tracebacks).
- **Popup Hierarchy:** Display Safe/Phishing status, Risk, Confidence, URL, and critical forensics. A link to the main dashboard can be provided for full details.

## Implementation Plan
- **Files to create:** `manifest.json`, `popup.html`, `popup.js`, `popup.css`, icons.
- **Files NOT to modify:** `xgboost_frozen.pkl`, `feature_names.pkl`, model logic, forensic logic.
- **New Endpoint:** NO.

**NOTE: No implementation occurred during this audit. No models were modified. No retraining occurred.**
