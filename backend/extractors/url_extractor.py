import re
from urllib.parse import urlparse

class FeatureExtractor:

    def __init__(self):
        pass

    def extract_url_features(self, url):

        parsed = urlparse(url)

        hostname = parsed.netloc
        path = parsed.path
        query = parsed.query

        features = {}

        features["NumDots"] = url.count(".")
        features["SubdomainLevel"] = max(hostname.count(".") - 1, 0)
        stripped_path = path.rstrip("/")
        features["PathLevel"] = stripped_path.count("/") if stripped_path else 0
        features["UrlLength"] = len(url)
        features["NumDash"] = url.count("-")
        features["NumDashInHostname"] = hostname.count("-")
        features["AtSymbol"] = url.count("@")
        features["TildeSymbol"] = url.count("~")
        features["NumUnderscore"] = url.count("_")
        features["NumPercent"] = url.count("%")
        features["NumQueryComponents"] = len(query.split("&")) if query else 0
        features["NumAmpersand"] = url.count("&")
        features["NumHash"] = url.count("#")
        features["NumNumericChars"] = sum(c.isdigit() for c in url)
        features["NoHttps"] = 0 if parsed.scheme == "https" else 1
        features["RandomString"] = 0
        features["IpAddress"] = 1 if re.match(r"^\d+\.\d+\.\d+\.\d+$", hostname) else 0
        features["DomainInSubdomains"] = 0
        features["DomainInPaths"] = 0
        features["HostnameLength"] = len(hostname)
        features["PathLength"] = len(path)
        features["QueryLength"] = len(query)
        features["DoubleSlashInPath"] = 1 if "//" in path else 0

        sensitive_words = [
            "login",
            "signin",
            "verify",
            "bank",
            "secure",
            "account",
            "update",
            "paypal",
            "password"
        ]

        features["NumSensitiveWords"] = sum(
            word in url.lower()
            for word in sensitive_words
        )
        
        # EmbeddedBrandName Implementation
        brand_names = [
            "paypal", "apple", "microsoft", "google", "facebook", 
            "amazon", "netflix", "bank", "whatsapp", "instagram"
        ]
        
        hostname_path_lower = hostname.lower() + path.lower()
        features["EmbeddedBrandName"] = 1 if any(brand in hostname_path_lower for brand in brand_names) else 0

        return features