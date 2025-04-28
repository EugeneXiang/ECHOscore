import hashlib

def stable_score(system: str, text: str, dimension: str) -> float:
    """Generate a stable 1.0–5.0 (step 0.1) score from MD5 hash"""
    key = f"{text}_{system}_{dimension}"
    h = hashlib.md5(key.encode()).hexdigest()
    v = int(h, 16) % 41  # 0–40
    return round(v / 10 + 1, 1)
