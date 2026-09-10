import re
from typing import Dict, Any, List
from schemas.response_models import EmailForensicSummary, EmailForensicFinding

class EmailForensicService:
    def __init__(self):
        # A. Urgency / Pressure
        self.urgency_pattern = re.compile(
            r'\b(urgent|immediately|act now|action required|within \d+ hours|final warning|verify now|immediate verification)\b',
            re.IGNORECASE
        )
        
        # B. Credential / Account Request
        self.credential_pattern = re.compile(
            r'\b(verify your account|confirm your password|enter your credentials|provide your otp|confirm your login|login credentials|account verification|verify your bank account)\b',
            re.IGNORECASE
        )
        
        # C. Financial / Payment Request
        self.financial_pattern = re.compile(
            r'\b(payment required|send money|transfer funds|bank account|credit card|debit card|invoice payment|refund claim|payment verification|required payment)\b',
            re.IGNORECASE
        )
        
        # D. Reward / Prize / Free Money Language
        self.reward_pattern = re.compile(
            r'\b(you won|winner|cash prize|lottery|claim your reward|free money|congratulations|selected for a prize)\b',
            re.IGNORECASE
        )
        
        # E. Suspicious Call-to-Action Language
        self.cta_pattern = re.compile(
            r'\b(click here|click the link|verify now|confirm now|login here|open the link|download now|update your information)\b',
            re.IGNORECASE
        )
        
        # F. Threat / Consequence Language
        self.threat_pattern = re.compile(
            r'\b(account suspended|account terminated|legal action|penalty|service disabled|access revoked|security breach|failure to verify|account suspension|account will be suspended)\b',
            re.IGNORECASE
        )

        # G. Capitalization pattern - conservative check for known suspicious all-caps terms
        self.caps_pattern = re.compile(
            r'\b(URGENT|ACTION REQUIRED|VERIFY NOW|FINAL WARNING)\b'
        )

    def analyze(self, subject: str, body: str) -> Dict[str, Any]:
        subject = subject or ""
        body = body or ""
        
        indicators: List[EmailForensicFinding] = []
        
        self._check_pattern(subject, body, self.urgency_pattern, "urgency_language", "medium", "Urgent or time-pressure language was detected.", indicators)
        self._check_pattern(subject, body, self.credential_pattern, "credential_request", "high", "The email appears to request account or credential information.", indicators)
        self._check_pattern(subject, body, self.financial_pattern, "financial_request", "high", "The email contains a financial or payment request.", indicators)
        self._check_pattern(subject, body, self.reward_pattern, "reward_prize", "medium", "The email contains reward, prize, or lottery language.", indicators)
        self._check_pattern(subject, body, self.cta_pattern, "call_to_action", "low", "A strong call-to-action requesting the user to click or verify was detected.", indicators)
        self._check_pattern(subject, body, self.threat_pattern, "threat_consequence", "medium", "Threatening or consequence-based language was detected.", indicators)
        self._check_pattern(subject, body, self.caps_pattern, "suspicious_capitalization", "low", "Suspicious use of excessive capitalization was detected.", indicators)

        summary = EmailForensicSummary(
            indicator_count=len(indicators),
            high_severity_count=sum(1 for i in indicators if i.severity == "high"),
            medium_severity_count=sum(1 for i in indicators if i.severity == "medium"),
            low_severity_count=sum(1 for i in indicators if i.severity == "low")
        )
        
        return {
            "forensic_summary": summary,
            "indicators": indicators
        }
        
    def _check_pattern(self, subject: str, body: str, pattern: re.Pattern, indicator_name: str, severity: str, description: str, indicators: List[EmailForensicFinding]):
        locs = []
        if pattern.search(subject):
            locs.append("subject")
        if pattern.search(body):
            locs.append("body")
            
        if locs:
            indicators.append(EmailForensicFinding(
                indicator=indicator_name,
                detected=True,
                severity=severity,
                locations=locs,
                description=description
            ))
