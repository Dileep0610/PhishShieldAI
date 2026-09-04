import re
from urllib.parse import urlparse

def extract_url_features(url):

    parsed = urlparse(url)

    hostname = parsed.netloc
    path = parsed.path
    query = parsed.query

    features = {}

    features["NumDots"] = url.count(".")
    features["SubdomainLevel"] = hostname.count(".")-1 if hostname.count(".")>0 else 0
    features["PathLevel"] = path.count("/")
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
    features["NoHttps"] = 0 if parsed.scheme=="https" else 1
    features["RandomString"] = 0
    features["IpAddress"] = 1 if re.match(r"^\d+\.\d+\.\d+\.\d+$",hostname) else 0
    features["DomainInSubdomains"] = 0
    features["DomainInPaths"] = 0
    features["HttpsInHostname"] = 1 if "https" in hostname else 0
    features["HostnameLength"] = len(hostname)
    features["PathLength"] = len(path)
    features["QueryLength"] = len(query)
    features["DoubleSlashInPath"] = 1 if "//" in path else 0
    features["NumSensitiveWords"] = sum(
        word in url.lower()
        for word in [
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
    )

    return features