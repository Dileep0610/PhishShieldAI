import math
from typing import Dict, Any, List
from schemas.response_models import ForensicFinding, ForensicReport, ForensicCategory, ForensicSeverity
from services.logger import logger

class ForensicEngine:
    def __init__(self):
        # The exact 47 features from backend/models/feature_names.pkl
        self.feature_names = [
            'NumDots', 'SubdomainLevel', 'PathLevel', 'UrlLength', 'NumDash', 'NumDashInHostname', 
            'AtSymbol', 'TildeSymbol', 'NumUnderscore', 'NumPercent', 'NumQueryComponents', 
            'NumAmpersand', 'NumHash', 'NumNumericChars', 'NoHttps', 'RandomString', 'IpAddress', 
            'DomainInSubdomains', 'DomainInPaths', 'HostnameLength', 'PathLength', 'QueryLength', 
            'DoubleSlashInPath', 'NumSensitiveWords', 'EmbeddedBrandName', 'PctExtHyperlinks', 
            'PctExtResourceUrls', 'ExtFavicon', 'InsecureForms', 'RelativeFormAction', 'ExtFormAction', 
            'AbnormalFormAction', 'PctNullSelfRedirectHyperlinks', 'FrequentDomainNameMismatch', 
            'FakeLinkInStatusBar', 'RightClickDisabled', 'PopUpWindow', 'SubmitInfoToEmail', 
            'IframeOrFrame', 'MissingTitle', 'ImagesOnlyInForm', 'SubdomainLevelRT', 'UrlLengthRT', 
            'PctExtResourceUrlsRT', 'AbnormalExtFormActionR', 'ExtMetaScriptLinkRT', 
            'PctExtNullSelfRedirectHyperlinksRT'
        ]

    def _is_valid(self, val):
        if val is None: return False
        if isinstance(val, float) and math.isnan(val): return False
        return True

    def generate_findings(
        self,
        feature_vector,
        whois: Dict[str, Any],
        ssl: Dict[str, Any],
        redirect: Dict[str, Any],
        virustotal: Dict[str, Any]
    ) -> ForensicReport:
        findings: List[ForensicFinding] = []

        try:
            # Safely parse feature vector
            vector_values = {}
            if hasattr(feature_vector, "iloc"):
                vector_values = feature_vector.iloc[0].to_dict()
            elif hasattr(feature_vector, "__getitem__") and len(feature_vector) > 0 and len(feature_vector[0]) == len(self.feature_names):
                for i, name in enumerate(self.feature_names):
                    vector_values[name] = float(feature_vector[0][i])
            else:
                raise ValueError("Could not parse feature_vector securely.")

            # -------------------------------------------------------------
            # 1. URL Rules
            # -------------------------------------------------------------
            val_nohttps = vector_values.get("NoHttps")
            if self._is_valid(val_nohttps) and val_nohttps == 1:
                findings.append(ForensicFinding(
                    finding_id="URL_NO_HTTPS",
                    category=ForensicCategory.URL,
                    severity=ForensicSeverity.MEDIUM,
                    title="Unencrypted HTTP connection",
                    description="The URL uses HTTP instead of HTTPS. Data transmitted over an unencrypted connection may be exposed or modified.",
                    evidence="Observed dataset feature: NoHttps=1.",
                    source="Dataset URL feature: NoHttps",
                    remediation="Prefer HTTPS and avoid transmitting sensitive information over unencrypted connections."
                ))

            val_ip = vector_values.get("IpAddress")
            if self._is_valid(val_ip) and val_ip == 1:
                findings.append(ForensicFinding(
                    finding_id="URL_IP_ADDRESS",
                    category=ForensicCategory.URL,
                    severity=ForensicSeverity.MEDIUM,
                    title="IP address used as host",
                    description="The URL uses an IP address instead of a conventional domain name. This can make the destination harder to identify and may warrant additional scrutiny.",
                    evidence="Observed dataset feature: IpAddress=1.",
                    source="Dataset URL feature: IpAddress",
                    remediation="Verify the destination carefully before entering credentials or sensitive information."
                ))

            # -------------------------------------------------------------
            # 2. HTML Rules
            # -------------------------------------------------------------
            val_insecure_forms = vector_values.get("InsecureForms")
            if self._is_valid(val_insecure_forms) and val_insecure_forms == 1:
                findings.append(ForensicFinding(
                    finding_id="HTML_INSECURE_FORMS",
                    category=ForensicCategory.HTML,
                    severity=ForensicSeverity.MEDIUM,
                    title="Insecure form detected",
                    description="The page contains a form that submits data over an unencrypted HTTP connection.",
                    evidence="Observed dataset feature: InsecureForms=1.",
                    source="Dataset HTML feature: InsecureForms",
                    remediation="Ensure forms submit to an HTTPS endpoint to protect user data."
                ))
            
            val_ext_form_action = vector_values.get("ExtFormAction")
            if self._is_valid(val_ext_form_action) and val_ext_form_action == 1:
                findings.append(ForensicFinding(
                    finding_id="HTML_EXTERNAL_FORM_ACTION",
                    category=ForensicCategory.HTML,
                    severity=ForensicSeverity.HIGH,
                    title="External form submission",
                    description="The form submits information to a different external domain.",
                    evidence="Observed dataset feature: ExtFormAction=1.",
                    source="Dataset HTML feature: ExtFormAction",
                    remediation="Verify the external destination is trusted before submitting sensitive information."
                ))

            val_relative_form = vector_values.get("RelativeFormAction")
            if self._is_valid(val_relative_form) and val_relative_form == 1:
                findings.append(ForensicFinding(
                    finding_id="HTML_RELATIVE_FORM_ACTION",
                    category=ForensicCategory.HTML,
                    severity=ForensicSeverity.LOW,
                    title="Relative form action",
                    description="A relative or empty form destination was observed. This is not inherently malicious, but the submission behavior should be verified when handling sensitive information.",
                    evidence="Observed dataset feature: RelativeFormAction=1.",
                    source="Dataset HTML feature: RelativeFormAction",
                    remediation="Verify the form destination is correct."
                ))

            val_abnormal_form = vector_values.get("AbnormalFormAction")
            if self._is_valid(val_abnormal_form) and val_abnormal_form == 1:
                findings.append(ForensicFinding(
                    finding_id="HTML_ABNORMAL_FORM_ACTION",
                    category=ForensicCategory.HTML,
                    severity=ForensicSeverity.HIGH,
                    title="Abnormal form action",
                    description="Form action is empty, #, or javascript:void(0). Verify the form submission logic.",
                    evidence="Observed dataset feature: AbnormalFormAction=1.",
                    source="Dataset HTML feature: AbnormalFormAction",
                    remediation="Check if the page handles form submission via JavaScript instead of standard HTML, or if the form is a decoy."
                ))

            val_missing_title = vector_values.get("MissingTitle")
            if self._is_valid(val_missing_title) and val_missing_title == 1:
                findings.append(ForensicFinding(
                    finding_id="HTML_MISSING_TITLE",
                    category=ForensicCategory.HTML,
                    severity=ForensicSeverity.LOW,
                    title="Missing page title",
                    description="The scanned webpage does not contain a title element.",
                    evidence="Observed dataset feature: MissingTitle=1.",
                    source="Dataset HTML feature: MissingTitle",
                    remediation="Add a descriptive HTML title element."
                ))

            val_right_click = vector_values.get("RightClickDisabled")
            if self._is_valid(val_right_click) and val_right_click == 1:
                findings.append(ForensicFinding(
                    finding_id="HTML_RIGHT_CLICK_DISABLED",
                    category=ForensicCategory.HTML,
                    severity=ForensicSeverity.MEDIUM,
                    title="Right-click disabled",
                    description="The webpage restricts right-click functionality, which is sometimes used to hide source code.",
                    evidence="Observed dataset feature: RightClickDisabled=1.",
                    source="Dataset HTML feature: RightClickDisabled",
                    remediation="Avoid artificially disabling context menus unless specifically required by the application."
                ))

            val_popup = vector_values.get("PopUpWindow")
            if self._is_valid(val_popup) and val_popup == 1:
                findings.append(ForensicFinding(
                    finding_id="HTML_POPUP_WINDOW",
                    category=ForensicCategory.HTML,
                    severity=ForensicSeverity.LOW,
                    title="Pop-up window behavior detected",
                    description="The webpage attempts to open new windows, which can be intrusive.",
                    evidence="Observed dataset feature: PopUpWindow=1.",
                    source="Dataset HTML feature: PopUpWindow",
                    remediation="Minimize the use of pop-up windows to improve user experience."
                ))
            
            val_submit_email = vector_values.get("SubmitInfoToEmail")
            if self._is_valid(val_submit_email) and val_submit_email == 1:
                findings.append(ForensicFinding(
                    finding_id="HTML_SUBMIT_INFO_EMAIL",
                    category=ForensicCategory.HTML,
                    severity=ForensicSeverity.HIGH,
                    title="Form submits information to email",
                    description="The page contains a form configured to submit data directly to an email address via mailto.",
                    evidence="Observed dataset feature: SubmitInfoToEmail=1.",
                    source="Dataset HTML feature: SubmitInfoToEmail",
                    remediation="Ensure form data is submitted to a secure backend endpoint rather than directly to an email client."
                ))

            val_iframe = vector_values.get("IframeOrFrame")
            if self._is_valid(val_iframe) and val_iframe == 1:
                findings.append(ForensicFinding(
                    finding_id="HTML_IFRAME",
                    category=ForensicCategory.HTML,
                    severity=ForensicSeverity.LOW,
                    title="Iframe or frame detected",
                    description="The page embeds other web content via iframes or frames.",
                    evidence="Observed dataset feature: IframeOrFrame=1.",
                    source="Dataset HTML feature: IframeOrFrame",
                    remediation="Ensure embedded content comes from trusted sources."
                ))

            # -------------------------------------------------------------
            # 3. SSL Rules
            # -------------------------------------------------------------
            ssl_valid = ssl.get("ssl_valid")
            ssl_error = ssl.get("error", "Unknown SSL error")
            if ssl_valid is False and ssl_error and "HTTP URL" not in ssl_error:
                findings.append(ForensicFinding(
                    finding_id="SSL_INVALID",
                    category=ForensicCategory.SSL,
                    severity=ForensicSeverity.HIGH,
                    title="SSL certificate validation failed",
                    description="SSL certificate validation failed for the scanned destination.",
                    evidence=f"Observed SSL failure: {ssl_error}",
                    source="SSL service",
                    remediation="Verify the certificate and avoid entering sensitive information until the connection can be trusted."
                ))

            # -------------------------------------------------------------
            # 4. VirusTotal Rules
            # -------------------------------------------------------------
            vt_malicious = virustotal.get("malicious")
            if self._is_valid(vt_malicious) and not virustotal.get("error"):
                vt_malicious = int(vt_malicious)
                if vt_malicious >= 3:
                    findings.append(ForensicFinding(
                        finding_id="VT_MALICIOUS_MULTIPLE",
                        category=ForensicCategory.VIRUSTOTAL,
                        severity=ForensicSeverity.CRITICAL,
                        title="Multiple malicious detections",
                        description=f"VirusTotal engines reported this URL as malicious.",
                        evidence=f"Observed {vt_malicious} malicious detections.",
                        source="VirusTotal service",
                        remediation="Do not interact with this website. It has been widely flagged as malicious."
                    ))
                elif vt_malicious >= 1:
                    findings.append(ForensicFinding(
                        finding_id="VT_MALICIOUS_DETECTION",
                        category=ForensicCategory.VIRUSTOTAL,
                        severity=ForensicSeverity.HIGH,
                        title="Malicious detections reported",
                        description=f"At least one VirusTotal engine reported this URL as malicious.",
                        evidence=f"Observed {vt_malicious} malicious detections.",
                        source="VirusTotal service",
                        remediation="Exercise extreme caution. This website has been flagged by security vendors."
                    ))

            # -------------------------------------------------------------
            # 5. Redirect Rules
            # -------------------------------------------------------------
            redirect_count = redirect.get("redirect_count")
            if self._is_valid(redirect_count):
                redirect_count = int(redirect_count)
                if redirect_count == 1:
                    findings.append(ForensicFinding(
                        finding_id="REDIRECT_SINGLE",
                        category=ForensicCategory.REDIRECT,
                        severity=ForensicSeverity.INFO,
                        title="Single redirect observed",
                        description="The URL redirected once before reaching its final destination.",
                        evidence="Observed redirect_count=1.",
                        source="Redirect service",
                        remediation="Ensure the final destination matches your expectations."
                    ))
                elif redirect_count > 1:
                    findings.append(ForensicFinding(
                        finding_id="REDIRECT_MULTIPLE",
                        category=ForensicCategory.REDIRECT,
                        severity=ForensicSeverity.LOW,
                        title="Multiple redirects observed",
                        description="The URL redirected multiple times before reaching its final destination.",
                        evidence=f"Observed redirect_count={redirect_count}.",
                        source="Redirect service",
                        remediation="Verify the final destination domain carefully."
                    ))
            
            domain_changed = redirect.get("domain_changed")
            if self._is_valid(domain_changed) and domain_changed:
                findings.append(ForensicFinding(
                    finding_id="REDIRECT_DOMAIN_CHANGED",
                    category=ForensicCategory.REDIRECT,
                    severity=ForensicSeverity.MEDIUM,
                    title="Redirect changed destination domain",
                    description="The redirect chain resulted in a different domain than originally requested.",
                    evidence="Observed domain_changed=True.",
                    source="Redirect service",
                    remediation="Verify that the final domain is trusted."
                ))

            protocol_changed = redirect.get("protocol_changed")
            if self._is_valid(protocol_changed) and protocol_changed:
                findings.append(ForensicFinding(
                    finding_id="REDIRECT_PROTOCOL_CHANGED",
                    category=ForensicCategory.REDIRECT,
                    severity=ForensicSeverity.MEDIUM,
                    title="Redirect changed protocol",
                    description="The redirect chain altered the connection protocol (e.g., HTTP to HTTPS, or vice-versa).",
                    evidence="Observed protocol_changed=True.",
                    source="Redirect service",
                    remediation="Ensure the final connection is secure."
                ))
            
            uses_shortener = redirect.get("uses_shortener")
            if self._is_valid(uses_shortener) and uses_shortener:
                findings.append(ForensicFinding(
                    finding_id="REDIRECT_SHORTENER",
                    category=ForensicCategory.REDIRECT,
                    severity=ForensicSeverity.MEDIUM,
                    title="URL shortener detected",
                    description="The original URL belongs to a known URL shortening service, obscuring the final destination.",
                    evidence="Observed uses_shortener=True.",
                    source="Redirect service",
                    remediation="Always verify the final expanded URL before interacting with the site."
                ))

            # -------------------------------------------------------------
            # 6. WHOIS Rules
            # -------------------------------------------------------------
            domain_age = whois.get("domain_age_days")
            if self._is_valid(domain_age):
                domain_age = int(domain_age)
                if domain_age >= 365:
                    findings.append(ForensicFinding(
                        finding_id="WHOIS_ESTABLISHED",
                        category=ForensicCategory.WHOIS,
                        severity=ForensicSeverity.INFO,
                        title="Established domain",
                        description="WHOIS indicates that the domain has been registered for at least one year.",
                        evidence=f"Observed domain age of {domain_age} days.",
                        source="WHOIS service",
                        remediation="Continue to apply standard security practices."
                    ))
                elif domain_age < 30:
                    findings.append(ForensicFinding(
                        finding_id="WHOIS_RECENT",
                        category=ForensicCategory.WHOIS,
                        severity=ForensicSeverity.MEDIUM,
                        title="Recently registered domain",
                        description="The domain was registered less than 30 days ago. Newly registered domains may warrant additional scrutiny but are not inherently malicious.",
                        evidence=f"Observed domain age of {domain_age} days.",
                        source="WHOIS service",
                        remediation="Verify the domain independently before entering credentials or sensitive information."
                    ))
            
        except Exception as e:
            logger.error(f"Forensic engine encountered a safe error: {e}")
            return ForensicReport(findings=[])

        return ForensicReport(findings=findings)
