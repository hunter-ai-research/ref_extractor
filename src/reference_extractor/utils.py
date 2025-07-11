import re


def is_reference(text: str) -> bool:
    """
    Determines if a text string is likely an academic reference/bibliography entry.

    Args:
        text (str): The text string to analyze

    Returns:
        bool: True if the text appears to be a reference, False otherwise
    """
    text = text.strip()
    if not text:
        return False

    # Strong indicators (high confidence)
    strong_patterns = [
        r'^\[\d+\]\s',  # Starts with [number]
        r'^\d+\.\s',  # Starts with number followed by period
        r'doi:\s*10\.\d+',  # DOI pattern
        r'https?://doi\.org',  # DOI URL
        r'pp\.\s*\d+[-–]\d+',  # Page range with pp.
        r'vol\.\s*\d+.*no\.\s*\d+',  # Volume and number pattern
        r'\d+\(\d+\):\d+[-–]\d+',  # Journal vol(issue):pages pattern
    ]

    # Check for strong patterns first
    for pattern in strong_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True

    # Medium indicators (need multiple to be confident)
    medium_indicators = 0

    # Author name patterns
    author_patterns = [
        r'[A-Z][a-z]+,\s*[A-Z]\.(?:\s*[A-Z]\.)*',  # Last, F. M.
        r'[A-Z][a-z]+,\s*[A-Z][a-z]+',  # Last, First
        r'[A-Z]\.(?:\s*[A-Z]\.)*\s+[A-Z][a-z]+',  # F. M. Last
    ]

    for pattern in author_patterns:
        if re.search(pattern, text):
            medium_indicators += 1
            break

    # Year patterns
    year_patterns = [
        r'\(\d{4}\)',  # (2023)
        r'\b\d{4}\b',  # 2023 (standalone)
    ]

    for pattern in year_patterns:
        if re.search(pattern, text):
            medium_indicators += 1
            break

    # Publication venue indicators
    venue_patterns = [
        r'\bProceedings\s+of\b',
        r'\bIn:\s*\w+',
        r'\bJournal\s+of\b',
        r'\bIEEE\b',
        r'\bACM\b',
        r'\bSpringer\b',
        r'\bElsevier\b',
        r'\bConference\s+on\b',
        r'\bInternational\s+Conference\b',
    ]

    for pattern in venue_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            medium_indicators += 1
            break

    # Technical formatting indicators
    tech_patterns = [
        r'\bISBN\b',
        r'\bISSN\b',
        r'\barXiv:\d+',
        r'\bvol\.\s*\d+',
        r'\bno\.\s*\d+',
        r'\bpp\.\s*\d+',
        r'\bchapter\s+\d+',
        r'\bedition\b',
    ]

    for pattern in tech_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            medium_indicators += 1
            break

    # Publisher/location patterns
    pub_patterns = [
        r'[A-Z][a-z]+\s+Press\b',
        r'[A-Z][a-z]+,\s+[A-Z]{2,}',  # City, STATE/COUNTRY
        r'University\s+of\s+\w+',
    ]

    for pattern in pub_patterns:
        if re.search(pattern, text):
            medium_indicators += 1
            break

    # Check for quotation marks around titles
    if re.search(r'"[^"]{10,}"', text):
        medium_indicators += 1

    # Require at least 2 medium indicators for a positive match
    return medium_indicators >= 2
