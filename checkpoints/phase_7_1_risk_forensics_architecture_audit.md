# Phase 7.1 Risk Intelligence & Forensic Layer Architecture Audit

## Status: PASS

### Current Architecture
The `PredictionService` orchestrates feature extraction, XGBoost inference, and concurrent external API calls (VT, SSL, WHOIS, Redirect). The `RiskEngine` calculates a 0-100 score heavily influenced by the ML prediction. The `ExplainabilityService` maps feature contributions and threat intel into basic descriptive strings.

### Gaps Identified
- Threat Intel and Security Evidence are output as flat arrays of strings without severity, categorization, or structured IDs.
- Logic is duplicated: `risk_engine.py` assigns numerical penalties to Threat Intel, while `explainability_service.py` independently parses the same Threat Intel to generate strings.
- There is no structured "Forensic" view that separates ML probabilities from deterministic security facts.

### Proposed Architecture
A new `ForensicEngine` that consumes the feature vector and Threat Intel to output a `List[ForensicFinding]`. This will preserve the ML prediction intact while providing structured `INFO`, `LOW`, `MEDIUM`, `HIGH`, and `CRITICAL` severity facts to the analyst.

### ML vs Forensic Separation
The ML model provides a statistical decision based on 47 features. The Forensic Layer provides deterministic context based on specific observations. A `CRITICAL` forensic finding (e.g., an Invalid SSL) will not override a `Legitimate` ML prediction. The conflict will be explicitly preserved and reported.
