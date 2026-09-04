import time
import math
from typing import Dict, Any, List

from services.logger import logger

class ExplainabilityService:
    def __init__(self):
        # Authoritative mapping based on Phase 6.1 Audit
        self.feature_metadata = {
            "NumDots": {"human_name": "Number of dots in URL", "category": "URL"},
            "SubdomainLevel": {"human_name": "Number of subdomains", "category": "URL"},
            "PathLevel": {"human_name": "Depth of the URL path", "category": "URL"},
            "UrlLength": {"human_name": "Total length of the URL", "category": "URL"},
            "NumDash": {"human_name": "Number of dashes in URL", "category": "URL"},
            "NumDashInHostname": {"human_name": "Number of dashes in hostname", "category": "URL"},
            "AtSymbol": {"human_name": "Presence of '@' symbol", "category": "URL"},
            "TildeSymbol": {"human_name": "Presence of '~' symbol", "category": "URL"},
            "NumUnderscore": {"human_name": "Number of underscores in URL", "category": "URL"},
            "NumPercent": {"human_name": "Number of percent encodings", "category": "URL"},
            "NumQueryComponents": {"human_name": "Number of query parameters", "category": "URL"},
            "NumAmpersand": {"human_name": "Number of ampersands in URL", "category": "URL"},
            "NumHash": {"human_name": "Number of hash symbols in URL", "category": "URL"},
            "NumNumericChars": {"human_name": "Number of numeric characters in URL", "category": "URL"},
            "NoHttps": {"human_name": "Use of unencrypted HTTP", "category": "URL"},
            "RandomString": {"human_name": "Suspicious random string in URL", "category": "URL"},
            "IpAddress": {"human_name": "Use of IP address instead of domain name", "category": "URL"},
            "DomainInSubdomains": {"human_name": "TLD or domain name appearing in subdomains", "category": "URL"},
            "DomainInPaths": {"human_name": "Domain name appearing in the URL path", "category": "URL"},
            "HostnameLength": {"human_name": "Length of the hostname", "category": "URL"},
            "PathLength": {"human_name": "Length of the URL path", "category": "URL"},
            "QueryLength": {"human_name": "Length of the query string", "category": "URL"},
            "DoubleSlashInPath": {"human_name": "Extraneous double slashes in path", "category": "URL"},
            "NumSensitiveWords": {"human_name": "Number of sensitive/phishing keywords", "category": "URL"},
            "EmbeddedBrandName": {"human_name": "Brand names embedded in subdomains or paths", "category": "URL"},
            "PctExtHyperlinks": {"human_name": "Percentage of external hyperlinks", "category": "HTML"},
            "PctExtResourceUrls": {"human_name": "Percentage of external resource URLs", "category": "HTML"},
            "ExtFavicon": {"human_name": "Favicon loaded from external domain", "category": "HTML"},
            "InsecureForms": {"human_name": "Forms submitting over unencrypted HTTP", "category": "HTML"},
            "RelativeFormAction": {"human_name": "Form action uses a relative URL", "category": "HTML"},
            "ExtFormAction": {"human_name": "Form action submits to external domain", "category": "HTML"},
            "AbnormalFormAction": {"human_name": "Form action is empty or about:blank", "category": "HTML"},
            "PctNullSelfRedirectHyperlinks": {"human_name": "Percentage of empty or self-redirecting links", "category": "HTML"},
            "FrequentDomainNameMismatch": {"human_name": "High mismatch rate in domain names", "category": "HTML"},
            "FakeLinkInStatusBar": {"human_name": "Fake links displayed in status bar", "category": "HTML"},
            "RightClickDisabled": {"human_name": "Right-click functionality disabled", "category": "HTML"},
            "PopUpWindow": {"human_name": "Use of pop-up windows", "category": "HTML"},
            "SubmitInfoToEmail": {"human_name": "Form submits directly to an email address", "category": "HTML"},
            "IframeOrFrame": {"human_name": "Use of hidden or suspicious iframes", "category": "HTML"},
            "MissingTitle": {"human_name": "Web page is missing a title tag", "category": "HTML"},
            "ImagesOnlyInForm": {"human_name": "Form contains only images and no text", "category": "HTML"},
            "SubdomainLevelRT": {"human_name": "Real-time verified subdomain depth", "category": "RT"},
            "UrlLengthRT": {"human_name": "Real-time verified URL length", "category": "RT"},
            "PctExtResourceUrlsRT": {"human_name": "Real-time percentage of external resources", "category": "RT"},
            "AbnormalExtFormActionR": {"human_name": "Real-time abnormal or external form action", "category": "RT"},
            "ExtMetaScriptLinkRT": {"human_name": "Real-time external meta, script, or link tags", "category": "RT"},
            "PctExtNullSelfRedirectHyperlinksRT": {"human_name": "Real-time null/self-redirecting links", "category": "RT"}
        }

    def generate_explanation(
        self,
        model: Any,
        feature_names: List[str],
        feature_vector: Any,
        existing_whois_info: Dict[str, Any],
        existing_ssl_info: Dict[str, Any],
        existing_redirect_info: Dict[str, Any],
        existing_virustotal_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generates explanation using native XGBoost pred_contribs without any network requests.
        """
        start_time = time.perf_counter()
        
        try:
            # 1. Validation
            if len(feature_names) != 47:
                raise ValueError(f"Feature contract violation: expected 47, got {len(feature_names)}")

            import xgboost as xgb
            booster = model.get_booster()
            
            # Booster.predict requires DMatrix
            dmatrix = xgb.DMatrix(feature_vector, feature_names=feature_names)
            contributions = booster.predict(dmatrix, pred_contribs=True)[0]
            
            if len(contributions) != 48:
                raise ValueError(f"Contribution shape violation: expected 48, got {len(contributions)}")

            # 3. Align and Map Contributions
            contributors = []
            url_evidence = []
            html_evidence = []
            rt_evidence = []
            unavailable_evidence = []
            
            vector_values = feature_vector.iloc[0].to_dict() if hasattr(feature_vector, "iloc") else {feature_names[i]: float(feature_vector[0][i]) for i in range(47)}

            for i, feat_name in enumerate(feature_names):
                raw_val = vector_values.get(feat_name, float('nan'))
                contrib_val = float(contributions[i])
                
                # Handle NaN handling properly
                is_nan = math.isnan(raw_val)
                
                if is_nan:
                    unavailable_evidence.append({
                        "feature": feat_name,
                        "raw_value": None,
                        "status": "unavailable"
                    })
                    if feat_name in ["PctExtResourceUrlsRT", "ExtMetaScriptLinkRT"]:
                        if feat_name == "PctExtResourceUrlsRT":
                            rt_evidence.append("Real-time external resource percentage could not be verified.")
                        else:
                            rt_evidence.append("Real-time external meta/script/link percentage could not be verified.")
                    continue
                
                direction = "neutral"
                if contrib_val > 0:
                    direction = "phishing"
                elif contrib_val < 0:
                    direction = "legitimate"
                    
                meta = self.feature_metadata.get(feat_name, {})
                human_name = meta.get("human_name", feat_name)
                category = meta.get("category", "Unknown")
                
                contributors.append({
                    "feature": feat_name,
                    "human_name": human_name,
                    "category": category,
                    "raw_value": float(raw_val) if isinstance(raw_val, float) else raw_val,
                    "contribution": contrib_val,
                    "absolute_contribution": abs(contrib_val),
                    "direction": direction,
                    "status": "available"
                })
                
                # Security Evidence generation (deterministic based on non-NaN value)
                if category == "URL":
                    if feat_name == "IpAddress" and raw_val == 1:
                        url_evidence.append("The URL uses an IP address instead of a conventional domain.")
                    elif feat_name == "NoHttps" and raw_val == 1:
                        url_evidence.append("The URL uses an unencrypted HTTP protocol.")
                elif category == "HTML":
                    if feat_name == "InsecureForms" and raw_val == 1:
                        html_evidence.append("The page contains a form using an insecure HTTP action.")
                    elif feat_name == "ExtFormAction" and raw_val == 1:
                        html_evidence.append("The page contains a form submitting to an external domain.")
                    elif feat_name == "AbnormalFormAction" and raw_val == 1:
                        html_evidence.append("The page contains an abnormal form action.")
                    elif feat_name == "MissingTitle" and raw_val == 1:
                        html_evidence.append("The webpage is missing a title element.")
                    elif feat_name == "RightClickDisabled" and raw_val == 1:
                        html_evidence.append("Right-click functionality is disabled on the webpage.")
                    elif feat_name == "PopUpWindow" and raw_val == 1:
                        html_evidence.append("The webpage uses popup windows.")
                    elif feat_name == "IframeOrFrame" and raw_val == 1:
                        html_evidence.append("The webpage contains iframe/frame elements.")
                    elif feat_name == "SubmitInfoToEmail" and raw_val == 1:
                        html_evidence.append("The page contains a form that submits information to an email address.")

            # Top contributors
            pos_contributors = [c for c in contributors if c["direction"] == "phishing"]
            neg_contributors = [c for c in contributors if c["direction"] == "legitimate"]
            
            pos_contributors.sort(key=lambda x: x["absolute_contribution"], reverse=True)
            neg_contributors.sort(key=lambda x: x["absolute_contribution"], reverse=True)
            
            # Clean up keys for final output
            for c in pos_contributors + neg_contributors:
                c.pop("absolute_contribution", None)

            # 4. Threat Intel Evidence
            virustotal_evidence = []
            ssl_evidence = []
            whois_evidence = []
            redirect_evidence = []
            
            vt_malicious = existing_virustotal_info.get("malicious", 0)
            vt_suspicious = existing_virustotal_info.get("suspicious", 0)
            vt_error = existing_virustotal_info.get("error")
            if not vt_error and (vt_malicious > 0 or vt_suspicious > 0):
                virustotal_evidence.append(f"VirusTotal reported {vt_malicious} malicious detections.")
                
            ssl_valid = existing_ssl_info.get("ssl_valid")
            ssl_error = existing_ssl_info.get("error")
            if ssl_valid is False and ssl_error:
                ssl_evidence.append("The SSL certificate was reported as invalid.")
            
            domain_age = existing_whois_info.get("domain_age_days")
            if domain_age is not None:
                whois_evidence.append(f"The domain age is {domain_age} days.")
                
            redirect_count = existing_redirect_info.get("redirect_count")
            if redirect_count is not None and redirect_count > 0:
                redirect_evidence.append(f"The scan observed {redirect_count} redirects.")

            generation_time = round((time.perf_counter() - start_time) * 1000, 2)
            logger.info(f"Explainability Engine : {generation_time} ms")

            return {
                "status": "available",
                "model_explanation": {
                    "top_positive_contributors": pos_contributors[:5],
                    "top_negative_contributors": neg_contributors[:5]
                },
                "security_evidence": {
                    "url_evidence": url_evidence,
                    "html_evidence": html_evidence,
                    "rt_evidence": rt_evidence
                },
                "threat_intelligence": {
                    "virustotal": virustotal_evidence,
                    "ssl": ssl_evidence,
                    "whois": whois_evidence,
                    "redirect": redirect_evidence
                },
                "unavailable_evidence": unavailable_evidence
            }

        except Exception as e:
            logger.error(f"Explainability service failed safely: {e}")
            return {
                "status": "unavailable",
                "reason": "Explainability could not be generated."
            }
