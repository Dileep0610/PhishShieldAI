# Phase 8.4: Predict API Integration

## Overview
This phase integrates the existing Phase 8.3 browser extension foundation with the backend `POST /predict` API. The extension captures the active tab URL and sends it securely to the backend for analysis, receiving the JSON response.

## Integration Details
- **API Base URL:** `http://127.0.0.1:8000`
- **Endpoint:** `/predict` (POST)
- **Request Body:** `{"url": "captured_url"}`
- **Timeout:** 15 seconds (implemented via `AbortController`)
- **Error Handling:** Catches 400/422 as invalid requests, 500+ as backend unavailable, and handles network/timeout issues with clear UI messages.

## Security & Architecture Rules Followed
- **No Secrets:** No API keys are embedded in the extension.
- **No ML in Extension:** All prediction, forensics, and ML execution remain strictly in the backend.
- **Duplicate Protection:** The Scan button is disabled while the `fetch` is active.
- **XSS Protection:** Backend response fields are injected using `.textContent` instead of `.innerHTML`.
- **Backend Unchanged:** The backend logic and routes were NOT modified.

## CORS Audit
Currently, the backend configuration (`ALLOWED_ORIGINS` in `config/settings.py`) restricts access to `http://localhost:3000` and similar web origins. The extension runs under a `chrome-extension://<id>` origin. Therefore, the extension will encounter a CORS Block on actual execution until the backend is updated. **CORS was NOT modified in this phase.**
