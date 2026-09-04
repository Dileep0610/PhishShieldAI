from pydantic import BaseModel
from typing import Optional, List, Any
from enum import Enum



class WHOISResponse(BaseModel):

    domain: Optional[str] = None
    registrar: Optional[str] = None
    creation_date: Optional[str] = None
    expiration_date: Optional[str] = None
    domain_age_days: Optional[int] = None


class SSLResponse(BaseModel):

    ssl_valid: bool

    issuer: Optional[str] = None

    common_name: Optional[str] = None

    expiry_date: Optional[str] = None

    days_until_expiry: Optional[int] = None


class RedirectResponse(BaseModel):

    redirected: bool

    redirect_count: int

    final_url: str | None = None

    redirect_chain: list[str]

    protocol_changed: bool

    domain_changed: bool

    uses_shortener: bool

class VirusTotalResponse(BaseModel):

    malicious: int

    suspicious: int

    harmless: int

    undetected: int
    
class Contributor(BaseModel):
    feature: str
    human_name: str
    category: str
    raw_value: Optional[float] = None
    contribution: float
    direction: str
    status: str

class ModelExplanation(BaseModel):
    top_positive_contributors: List[Contributor] = []
    top_negative_contributors: List[Contributor] = []

class SecurityEvidence(BaseModel):
    url_evidence: List[str] = []
    html_evidence: List[str] = []
    rt_evidence: List[str] = []

class ThreatIntelligence(BaseModel):
    virustotal: List[str] = []
    ssl: List[str] = []
    whois: List[str] = []
    redirect: List[str] = []

class UnavailableEvidence(BaseModel):
    feature: str
    raw_value: Optional[Any] = None
    status: str

class ExplainabilityModel(BaseModel):
    status: str
    reason: Optional[str] = None
    model_explanation: Optional[ModelExplanation] = None
    security_evidence: Optional[SecurityEvidence] = None
    threat_intelligence: Optional[ThreatIntelligence] = None
    unavailable_evidence: Optional[List[UnavailableEvidence]] = None

class ForensicCategory(str, Enum):
    URL = "URL"
    HTML = "HTML"
    SSL = "SSL"
    WHOIS = "WHOIS"
    REDIRECT = "REDIRECT"
    VIRUSTOTAL = "VIRUSTOTAL"

class ForensicSeverity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ForensicFinding(BaseModel):
    finding_id: str
    category: ForensicCategory
    severity: ForensicSeverity
    title: str
    description: str
    evidence: str
    source: str
    remediation: str

class ForensicReport(BaseModel):
    findings: List[ForensicFinding]

class PredictionResponse(BaseModel):

    url: str

    prediction: str

    confidence: float

    risk_score: float

    risk_level: str

    processing_time_ms: float

    recommendation: str

    whois: WHOISResponse

    ssl: SSLResponse

    redirect: RedirectResponse

    virustotal: VirusTotalResponse

    explainability: Optional[ExplainabilityModel] = None

    forensic_report: Optional[ForensicReport] = None
