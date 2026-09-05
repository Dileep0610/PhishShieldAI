# Phase 9.3: QR Payload Validation & Filtering

## Overview
Successfully implemented strict payload validation for decoded QR codes within the frontend. The system safely validates and categorizes QR data into supported URLs or unsupported payloads.

## Validation Policy
- **URL Parsing**: Relies on the browser's native `URL()` parser for robust processing.
- **Maximum Length**: Hard limit of 2048 characters to prevent UI/DoS issues (`TOO_LONG`).
- **Protocols**: Strictly enforces `http:` and `https:`. All other schemes (e.g., `javascript:`, `data:`, `file:`, `chrome:`, `blob:`) are rejected as `UNSUPPORTED_SCHEME`.
- **Control Characters**: Rejects payloads containing any C0 control characters or DEL (`[\x00-\x1F\x7F]`) to prevent injection anomalies.
- **Whitespace**: Safely trims surrounding whitespace before validation, preserving the core URL.

## Security Controls
- **XSS Prevention**: Decoded strings are rendered exclusively as text nodes via React JSX. `innerHTML` and code execution primitives are strictly avoided.
- **Localhost / Private IP**: Identified using regex (`127.0.0.1`, `localhost`, `10.x.x.x`, `192.168.x.x`, `172.16.x.x`) and flagged with a `SECURITY_WARNING` rather than outright rejection, maintaining visibility into the payload.
- **UserInfo**: Preserved without modification (e.g. `https://user:pass@example.com`).
- **Execution & Networking**: ZERO external requests are made. No DNS resolution, no HTTP fetches, and absolutely no automatic navigation.

## Testing Results
- `javascript:alert(1)` ➔ `UNSUPPORTED_SCHEME`
- `data:text/html,...` ➔ `UNSUPPORTED_SCHEME`
- `https://www.google.com` ➔ `VALID_URL`
- `http://localhost:8000` ➔ `SECURITY_WARNING`
- Malformed text ➔ `INVALID_URL`

## Status
- **Lint & Build**: PASS (0 errors, 0 warnings).
- **Backend Integrity**: 100% untouched. No calls to `/predict` or any other API are made during this validation phase.
