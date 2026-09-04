# Phase 6.1 Explainability Architecture Audit

**PASS / FAIL**: PASS

## Project State
* Phases 1–5 complete.
* Frozen model: XGBoost Classifier.
* Production feature count: 47 (25 URL, 16 HTML, 6 RT).
* Inference API and contract frozen.

## Frozen Model Information
* **Type**: `xgboost.sklearn.XGBClassifier`
* **Features**: 47
* **Classes**: [0, 1] (0 = Legitimate, 1 = Phishing)
* **predict_proba**: Available
* **Feature Importances**: Available

## Model Compatibility Findings
The current frozen model is fully compatible with native local feature contribution explanations (`pred_contribs=True` inside XGBoost) and global feature importances without requiring any retraining, dependency addition, or modifications.

## Explainability Approaches Evaluated

| Approach | Compatible? | Retraining? | New Dependencies? | Scope | Recommendation |
|---|---|---|---|---|---|
| A. Global Feature Importance | Yes | No | No | Global | Reject (Doesn't explain specific URLs) |
| B. XGBoost Native `pred_contribs` | Yes | No | No | Local | **Recommended** (Built-in, precise, fast) |
| C. SHAP TreeExplainer (`shap`) | Yes | No | Yes | Local | Reject (Unnecessary dependency overhead) |
| D. Permutation Importance | Yes | No | No | Global | Reject (Expensive, not local) |

## Recommended Approach
**XGBoost Native `pred_contribs` (Per-instance contribution)**. It hooks directly into the XGBoost C++ backend of the frozen model to extract Tree SHAP values without requiring the Python `shap` package, without retraining, and without altering predictions.

## 47-Feature Explanation Mapping
*See final report for the full mapping of all 47 features from technical to human-readable names.*

## RT Feature Handling
Four RT features are resolved via the lookup mapping. Two (PctExtResourceUrlsRT, ExtMetaScriptLinkRT) remain unresolved and often return NaN. The explanation system will explicitly format NaN as "unavailable/unknown" and will NOT treat them as 0, safe, or benign. They will be placed in an `unavailable_evidence` section.

## Proposed Explanation Data Model
The response will include a new `explainability` object containing:
* `model_explanation`: Top features driving the score (with raw value, contribution magnitude, and direction).
* `security_evidence`: Observed facts categorized by URL and HTML (e.g., "The URL contains an IP address").
* `threat_intelligence`: External service findings.
* `unavailable_evidence`: Features that could not be evaluated (e.g., specific RT checks).

## Model vs Security Evidence Separation
* **Model Explanation**: Quantifies the ML reasoning (e.g., "IpAddress feature contributed +1.2 to the phishing score").
* **Security Evidence**: States observable facts (e.g., "The URL uses an IP address").
This prevents hallucinations where the system falsely claims causal inference from a black-box model.

## Proposed API Architecture
**Extend existing `/predict` response.**
* Why: Features and external threat intel are already extracted and held in memory during `/predict`. Extending the schema avoids complex distributed caching or re-extraction, minimizing latency. It's fully backward compatible if clients ignore the new key.

## Proposed Frontend Architecture
The React UI will gain a new expandable "Explainability Dashboard" below the Risk Score. It will feature three distinct visual panels:
1. **Model Evidence**: Visual bar charts of top contributing features (Phishing vs Legitimate direction).
2. **Website Evidence**: Bullet points of factual observations.
3. **Threat Intelligence**: Summaries of VT/SSL/Whois.

## Performance Considerations
Native XGBoost `pred_contribs` for a single instance is extremely fast (<5ms) and purely CPU-bound. It will not bottleneck the existing `/predict` endpoint, which is currently dominated by I/O (VT, Whois, page fetch).

## Security Considerations
Raw feature values and names can be exposed because this is a client-facing security tool meant to educate. However, the exact model thresholds, decision tree splits, API keys, and internal extraction filesystem paths must NEVER be exposed.

## No-Code-Change Verification
Verified via file status inspection. No production backend or frontend code was altered.

## Known Limitations
* The exact UI charting library for the frontend is not yet decided.
* Local interpretation (SHAP values) assumes feature independence, which is an approximation in tree models.
