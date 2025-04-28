import re

def detect_slang(text: str) -> str:
    """Simple placeholder: identify slang or technical terms in text"""
    # Customize with real patterns
    slang_patterns = re.compile(r"\b(LOL|BTW|FYI)\b", re.IGNORECASE)
    matches = slang_patterns.findall(text)
    return ", ".join(set(matches)) if matches else ""