import re

def extract_domain(url):
    """
    Extracts the domain from a given URL.
    """
    pattern = r'^(?:https?|chrome-extension)://([^/?#]+)'
    match = re.match(pattern, url)
    return match.group(1).lower() if match else None


def is_valid_url(url):
    """
    Validates the URL format, including chrome-extension URLs.
    """
    regex = re.compile(
        r'^(?:https?|chrome-extension)://'  # http://, https://, or chrome-extension://
        r'(?:\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None
