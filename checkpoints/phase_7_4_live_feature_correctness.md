# Phase 7.4 Live Feature Correctness Audit

## Objective
Investigate whether `NoHttps` was incorrectly extracted as `1` for `https://www.google.com` due to an explainability contribution of +0.8584, and audit `RelativeFormAction`.

## Investigation Findings
1. **NoHttps**: Extracted the exact live feature vector for `https://www.google.com`. The value for `NoHttps` at index 14 is `0.0`. The extraction logic (`0 if parsed.scheme == 'https' else 1`) functions perfectly. The positive explainability contribution (+0.8584) occurs natively within the frozen XGBoost model where `NoHttps=0` happened to push the model towards phishing in this specific branch. **Conclusion**: Not a bug in extraction. No changes required to `NoHttps`.
2. **RelativeFormAction**: Extracted as `1.0` correctly because Google's search form uses `action="/search"`. The logic matches the dataset semantics. We modified the wording in `ForensicEngine` to clarify that this is a deterministic observation rather than an inherently malicious finding.

## Files Modified
- `backend/services/forensic_engine.py` (Updated wording for RelativeFormAction)

## Integrity
- XGBoost Model: Unchanged
- Feature Contract: Unchanged
- RT Mappings: Unchanged
