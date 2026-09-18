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
    
    url_pattern = re.compile(
        r'(?:https?://[^\s<>\"\'{}|\\^\[\]`]+)|'
        r'(?:\b(?:www\.)?[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}(?::\d{1,5})?(?:/[^\s<>\"\'{}|\\^\[\]`]*)?)', 
        re.IGNORECASE
    )
    
    matches = url_pattern.finditer(text)
    
    unique_urls = []
    seen = set()
    
    for match in matches:
        url = match.group(0)
        start = match.start()
        end = match.end()
        
        # Skip if it's part of an email address domain (e.g. @example.com)
        if start > 0 and text[start-1] == '@':
            continue
            
        # Skip if it's the local part of an email address (e.g. john.doe@)
        if end < len(text) and text[end] == '@':
            continue
            
        # Skip if it's immediately preceded by a dot or word char (partial string match)
        if start > 0 and re.match(r'[a-zA-Z0-9.-]', text[start-1]):
            continue
            
        # Strip trailing punctuation commonly added at the end of sentences
        url = url.rstrip(".,;!?:")
        
        if url not in seen:
            seen.add(url)
            unique_urls.append(url)
            
    return unique_urls
