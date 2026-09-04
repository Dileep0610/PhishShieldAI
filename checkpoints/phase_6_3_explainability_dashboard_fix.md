# Phase 6.3: Explainability Dashboard UI (Fix / Verification)

**Result:** PASS

## Root Causes & Fixes
- **Missing UI (Old Dashboard):** The `ExplainabilityPanel` component was correctly imported and integrated, but the Vite development server retained a stale cached version of `ScanResult.jsx`. 
  *Fix:* Killed the Vite process, deleted the `node_modules/.vite` cache directory, and restarted the server.
- **Google Domain Age Null:** The Python backend correctly parsed WHOIS but `domain_age_days` evaluated to Python `None` (JSON `null`). The frontend `ScanResult.jsx` utilized strict equality `=== undefined` for its fallback check, which bypassed `null` and inappropriately rendered it to the UI.
  *Fix:* Updated the frontend check to `domainAge == null` (which safely catches both `null` and `undefined`) forcing it to render the literal string `Unavailable`.

## Verification Checklist
- Backend Modified: NONE
- Model Modified: NO
- npm lint: PASS
- npm build: PASS
- Phase 5 Regression: PASS
