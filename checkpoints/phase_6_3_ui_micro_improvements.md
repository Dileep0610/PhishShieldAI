# Phase 6.3: UI Micro Improvements

**Result:** PASS

## Improvement 1
Updated the "Unavailable Evidence" copy in `EvidenceSection.jsx` to read: "Some advanced website signals could not be reliably extracted from the live page. These signals were not guessed or replaced with synthetic values." Retained the dynamic loop for `unavailable_evidence`. Replaced the previous explicit "Unavailable from live page" per-item label with an em-dash `" — Unavailable"`.

## Improvement 2
Added a single explanatory paragraph in `ExplainabilityPanel.jsx` under the Model Factors section stating: "Positive factors increase phishing likelihood, while negative factors reduce phishing likelihood." without changing any model calculations or state flows.

## Validations
- Backend Modified: NONE
- Model Modified: NO
- Retraining Performed: NO
- npm lint: PASS
- npm build: PASS
- Regression: PASS across Google, Portfolio, ResumeIQ, and Raktha Setu URLs.
