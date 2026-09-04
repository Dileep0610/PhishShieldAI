from predictor import predict

sample = {
    "NumDots":1,
    "SubdomainLevel":0,
    "PathLevel":0,
    "UrlLength":18,
    "NumDash":0,
    "NumDashInHostname":0,
    "AtSymbol":0,
    "TildeSymbol":0,
    "NumUnderscore":0,
    "NumPercent":0,
    "NumQueryComponents":0,
    "NumAmpersand":0,
    "NumHash":0,
    "NumNumericChars":0,
    "NoHttps":0,
    "RandomString":0,
    "IpAddress":0,
    "DomainInSubdomains":0,
    "DomainInPaths":0,
    "HttpsInHostname":0,
    "HostnameLength":10,
    "PathLength":0,
    "QueryLength":0,
    "DoubleSlashInPath":0,
    "NumSensitiveWords":0
}

print(predict(sample))