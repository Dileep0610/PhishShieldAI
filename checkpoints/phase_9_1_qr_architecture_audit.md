# Phase 9.1: QR Code Phishing Detection - Architecture Audit

## 1. Recommended Architecture
**Hybrid Approach**: QR code decoding is performed entirely on the client-side (Frontend), and the resulting decoded URL is passed to the existing backend prediction pipeline.
- **Why**: Enhances privacy (images never leave the user's device), eliminates backend attack surfaces related to image parsing (decompression bombs, malformed files), reduces server load, and allows 100% reuse of the existing `/predict` endpoint.

## 2. QR Decoding Requirements
- **Technology**: A JavaScript library such as `html5-qrcode` or `jsQR`.
- **Reasoning**: Browser-native `BarcodeDetector` API lacks comprehensive cross-browser support.
- **Capabilities**: Support for both camera scanning and file uploads (PNG, JPG, WEBP).
- **Location**: Installed in the React frontend via npm.

## 3. Payload Handling & URL Validation
- **Policy**: Only payloads strictly validated as `http://` or `https://` URLs will be forwarded to the backend.
- **Validation**:
  - Reject `javascript:`, `data:`, `file:`, `chrome:`, `about:`, `blob:`.
  - Do NOT silently convert arbitrary text to URLs.
  - Non-URL payloads (vCard, Wi-Fi, plain text) must trigger an "Unsupported Payload" state and halt the analysis flow.
  - The decoded content must be treated strictly as DATA, not executed.

## 4. API & Result Flow
- **Reuse**: The existing `POST /predict` endpoint will be reused without modification. The decoded URL maps directly to the existing `URLRequest` schema.
- **No New Endpoint**: No QR-specific endpoint is required.
- **CORS**: No changes needed.
- **Result Display**: The existing `PredictionResponse` contract and `ScanResult` UI component will be reused to display Risk Score, Confidence, Forensics, etc.

## 5. Security Analysis
- **Image Security**: Handled natively by the browser. Malicious images cannot exploit backend image processing libraries because they are never uploaded.
- **Camera Security**: Requires HTTPS. The camera stream MUST be explicitly stopped immediately after a successful decode or component unmount to prevent background spying.
- **SSRF**: Passing QR URLs to the backend poses the exact same SSRF risk as manual URL entry. The backend must ensure protections against resolving `localhost` or internal IPs.
- **XSS**: Decoded payloads must be rendered using React's safe DOM insertion (which escapes by default). Direct DOM manipulation (`innerHTML`) must be strictly avoided. Clickable links must validate the `href`.
- **Duplicate Requests**: A state lock (`isScanning`) must be implemented to prevent rapid-fire camera decodes from spamming the backend API.

## 6. Frontend Architecture
- **Recommendation**: A tabbed interface in the main dashboard: `URL Scanner | QR Scanner`.
- **States**: `IDLE` -> `DECODING` -> `DECODED` -> `ANALYZING` -> `SUCCESS` / `ERROR` / `UNSUPPORTED PAYLOAD`.

## 7. Test Plan
- **QR Inputs**: Valid QR, corrupted image, unsupported formats.
- **Payloads**: HTTP/HTTPS URLs, plain text, malformed URLs, `javascript:` injections.
- **Security**: Rapid rescanning (debounce test), stopping camera stream, SSRF attempts via QR.
- **Integration**: Ensure the existing `ScanResult` renders the `/predict` response accurately.

## 8. Regression Status
- **Model**: FROZEN (No changes).
- **Features**: 47 FEATURES (No changes).
- **Backend Services**: UNCHANGED.
- **Extension**: UNCHANGED.
- **URL Scanner**: UNCHANGED.
