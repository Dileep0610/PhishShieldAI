# Phase 9.4: QR -> /predict API Integration

## Overview
Successfully integrated the validated QR scanner output with the existing backend `/predict` endpoint. The frontend acts as a thin client, passing the validated URL payload to the existing machine learning pipeline.

## API Integration Details
- **Endpoint**: Reused `POST /predict` using the existing `predictUrl(url)` utility function in `src/services/api.js`.
- **Request Format**: The exact request body format `{ "url": "<validated URL>" }` is preserved and utilized.
- **Validation Gate**: The `/predict` call is strictly gated behind the Phase 9.3 validation logic. It is only accessible if the validation state is `VALID_URL` (or `SECURITY_WARNING`). Unsupported payloads, overly long payloads, or malformed payloads cannot trigger the API call.

## Security Constraints Enforced
- **Zero Image Upload**: The QR image bytes (or Base64 data) are never sent to the backend, eliminating backend image attack surfaces.
- **Thin Client Enforcement**: The frontend performs zero machine learning, risk calculation, confidence scoring, or forensic severity evaluation. It strictly relies on the backend's `PredictionResponse`.
- **No Automatic Execution**: The decoded URL is not executed, fetched, or navigated to by the frontend browser.

## UI State Machine
The QR Scanner state seamlessly transitions with the App state:
`IDLE` ➔ `DECODING` (Camera/Upload) ➔ `DECODED` (QR payload parsed) ➔ `ANALYZING` (Calling `/predict`) ➔ `SUCCESS`/`ERROR` (Rendering `ScanResult` dashboard).

## Regression Testing
- **URL Scanner**: The existing URL scanner remains fully functional and its behavior is unchanged.
- **ScanResult**: The existing `ScanResult` UI component is 100% reused to display the phishing results for the QR URL, maintaining UI consistency.

## Status
- **Lint**: PASS
- **Build**: PASS
- **Backend Changes**: NONE
