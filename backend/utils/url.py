import urllib.parse

def normalize_url(url: str) -> str:
    """
    Normalizes a URL string.
    1. Strips whitespace.
    2. Prepends https:// if no scheme is provided.
    3. Validates scheme and netloc.
    """
    url_str = str(url).strip()
    if not url_str:
        raise ValueError("Invalid URL")
    
    lower_url = url_str.lower()
    if not (lower_url.startswith("http://") or lower_url.startswith("https://")):
        url_str = "https://" + url_str
        
    parsed = urllib.parse.urlparse(url_str)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("Invalid URL scheme or format")
        
    return url_str
