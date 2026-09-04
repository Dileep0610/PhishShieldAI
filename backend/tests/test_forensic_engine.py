import pytest
import numpy as np
import pandas as pd
from services.forensic_engine import ForensicEngine
from schemas.response_models import ForensicCategory, ForensicSeverity, ForensicReport

@pytest.fixture
def engine():
    return ForensicEngine()

def create_base_features():
    # Helper to create an empty 47-feature array based on the ordered names
    names = [
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
    # Initialize all to 0.0
    return {n: 0.0 for n in names}

def get_report(engine, features, whois=None, ssl=None, redirect=None, virustotal=None):
    if whois is None: whois = {}
    if ssl is None: ssl = {}
    if redirect is None: redirect = {}
    if virustotal is None: virustotal = {}
    
    # Pack as dataframe matching production structure
    df = pd.DataFrame([features])
    return engine.generate_findings(df, whois, ssl, redirect, virustotal)


def test_1_nohttps(engine):
    feats = create_base_features()
    feats["NoHttps"] = 1.0
    rep = get_report(engine, feats)
    assert len(rep.findings) == 1
    assert rep.findings[0].finding_id == "URL_NO_HTTPS"
    assert rep.findings[0].severity == ForensicSeverity.MEDIUM

def test_2_ipaddress(engine):
    feats = create_base_features()
    feats["IpAddress"] = 1.0
    rep = get_report(engine, feats)
    assert len(rep.findings) == 1
    assert rep.findings[0].finding_id == "URL_IP_ADDRESS"
    assert rep.findings[0].severity == ForensicSeverity.MEDIUM

def test_3_both_url_findings(engine):
    feats = create_base_features()
    feats["NoHttps"] = 1.0
    feats["IpAddress"] = 1.0
    rep = get_report(engine, feats)
    assert len(rep.findings) == 2
    ids = [f.finding_id for f in rep.findings]
    assert "URL_NO_HTTPS" in ids
    assert "URL_IP_ADDRESS" in ids

def test_4_insecure_forms(engine):
    feats = create_base_features()
    feats["InsecureForms"] = 1.0
    rep = get_report(engine, feats)
    assert rep.findings[0].finding_id == "HTML_INSECURE_FORMS"

def test_5_ext_form_action(engine):
    feats = create_base_features()
    feats["ExtFormAction"] = 1.0
    rep = get_report(engine, feats)
    assert rep.findings[0].finding_id == "HTML_EXTERNAL_FORM_ACTION"
    assert rep.findings[0].severity == ForensicSeverity.HIGH

def test_6_relative_form_action(engine):
    feats = create_base_features()
    feats["RelativeFormAction"] = 1.0
    rep = get_report(engine, feats)
    assert rep.findings[0].finding_id == "HTML_RELATIVE_FORM_ACTION"
    assert rep.findings[0].severity == ForensicSeverity.LOW

def test_7_abnormal_form_action(engine):
    feats = create_base_features()
    feats["AbnormalFormAction"] = 1.0
    rep = get_report(engine, feats)
    assert rep.findings[0].finding_id == "HTML_ABNORMAL_FORM_ACTION"
    assert rep.findings[0].severity == ForensicSeverity.HIGH

def test_8_missing_title(engine):
    feats = create_base_features()
    feats["MissingTitle"] = 1.0
    rep = get_report(engine, feats)
    assert rep.findings[0].finding_id == "HTML_MISSING_TITLE"

def test_9_right_click_disabled(engine):
    feats = create_base_features()
    feats["RightClickDisabled"] = 1.0
    rep = get_report(engine, feats)
    assert rep.findings[0].finding_id == "HTML_RIGHT_CLICK_DISABLED"

def test_10_popup_window(engine):
    feats = create_base_features()
    feats["PopUpWindow"] = 1.0
    rep = get_report(engine, feats)
    assert rep.findings[0].finding_id == "HTML_POPUP_WINDOW"

def test_11_submit_email(engine):
    feats = create_base_features()
    feats["SubmitInfoToEmail"] = 1.0
    rep = get_report(engine, feats)
    assert rep.findings[0].finding_id == "HTML_SUBMIT_INFO_EMAIL"

def test_12_iframe(engine):
    feats = create_base_features()
    feats["IframeOrFrame"] = 1.0
    rep = get_report(engine, feats)
    assert rep.findings[0].finding_id == "HTML_IFRAME"

def test_13_invalid_ssl(engine):
    rep = get_report(engine, create_base_features(), ssl={"ssl_valid": False, "error": "certificate expired"})
    assert len(rep.findings) == 1
    assert rep.findings[0].finding_id == "SSL_INVALID"

def test_14_ssl_valid_no_finding(engine):
    rep = get_report(engine, create_base_features(), ssl={"ssl_valid": True, "error": None})
    assert len(rep.findings) == 0

def test_15_vt_malicious_3(engine):
    rep = get_report(engine, create_base_features(), virustotal={"malicious": 3})
    assert len(rep.findings) == 1
    assert rep.findings[0].severity == ForensicSeverity.CRITICAL

def test_16_vt_malicious_1(engine):
    rep = get_report(engine, create_base_features(), virustotal={"malicious": 1})
    assert len(rep.findings) == 1
    assert rep.findings[0].severity == ForensicSeverity.HIGH

def test_17_vt_malicious_0(engine):
    rep = get_report(engine, create_base_features(), virustotal={"malicious": 0})
    assert len(rep.findings) == 0

def test_18_redirect_count_1(engine):
    rep = get_report(engine, create_base_features(), redirect={"redirect_count": 1})
    assert len(rep.findings) == 1
    assert rep.findings[0].severity == ForensicSeverity.INFO

def test_19_redirect_count_multi(engine):
    rep = get_report(engine, create_base_features(), redirect={"redirect_count": 3})
    assert len(rep.findings) == 1
    assert rep.findings[0].severity == ForensicSeverity.LOW

def test_20_domain_changed(engine):
    rep = get_report(engine, create_base_features(), redirect={"domain_changed": True})
    assert len(rep.findings) == 1
    assert rep.findings[0].finding_id == "REDIRECT_DOMAIN_CHANGED"

def test_21_protocol_changed(engine):
    rep = get_report(engine, create_base_features(), redirect={"protocol_changed": True})
    assert len(rep.findings) == 1
    assert rep.findings[0].finding_id == "REDIRECT_PROTOCOL_CHANGED"

def test_22_uses_shortener(engine):
    rep = get_report(engine, create_base_features(), redirect={"uses_shortener": True})
    assert len(rep.findings) == 1
    assert rep.findings[0].finding_id == "REDIRECT_SHORTENER"

def test_23_whois_established(engine):
    rep = get_report(engine, create_base_features(), whois={"domain_age_days": 400})
    assert len(rep.findings) == 1
    assert rep.findings[0].severity == ForensicSeverity.INFO

def test_24_whois_recent(engine):
    rep = get_report(engine, create_base_features(), whois={"domain_age_days": 10})
    assert len(rep.findings) == 1
    assert rep.findings[0].severity == ForensicSeverity.MEDIUM

def test_25_whois_unavailable(engine):
    rep = get_report(engine, create_base_features(), whois={"domain_age_days": None})
    assert len(rep.findings) == 0
    rep = get_report(engine, create_base_features(), whois={"domain_age_days": np.nan})
    assert len(rep.findings) == 0

def test_nan_feature_values(engine):
    feats = create_base_features()
    feats["MissingTitle"] = np.nan
    rep = get_report(engine, feats)
    assert len(rep.findings) == 0

def test_deterministic_ordering(engine):
    feats = create_base_features()
    feats["NoHttps"] = 1.0
    feats["MissingTitle"] = 1.0
    rep = get_report(engine, feats, virustotal={"malicious": 1}, ssl={"ssl_valid": False, "error": "cert"})
    ids = [f.finding_id for f in rep.findings]
    assert ids == ["URL_NO_HTTPS", "HTML_MISSING_TITLE", "SSL_INVALID", "VT_MALICIOUS_DETECTION"]

def test_safe_error_handling(engine):
    # Pass garbage feature_vector that fails parsing
    rep = engine.generate_findings("not_a_vector", {}, {}, {}, {})
    assert len(rep.findings) == 0
    assert isinstance(rep, ForensicReport)
