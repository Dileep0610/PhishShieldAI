import re
from typing import List

def extract_urls(subject: str, body: str) -> List[str]:
    """
    Extracts HTTP and HTTPS URLs from the subject and body of an email.
    Deduplicates URLs, preserves order, and strips trailing punctuation.
    Ignores unsupported schemes (mailto:, ftp:, etc.).
    """
    subject_str = str(subject) if subject is not None else ""
    body_str = str(body) if body is not None else ""
    text = f"{subject_str} {body_str}"
    
    # Match http:// or https:// followed by valid URL characters (excluding common HTML/punctuation wrappers)
    url_pattern = re.compile(r'https?://[^\s<>\"\'{}|\\^\[\]`]+', re.IGNORECASE)
    
    matches = url_pattern.findall(text)
    
    unique_urls = []
    seen = set()
    
    for match in matches:
        # Strip trailing punctuation commonly added at the end of sentences
        url = match.rstrip(".,;!?:")
        
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)
            
    return unique_urls
