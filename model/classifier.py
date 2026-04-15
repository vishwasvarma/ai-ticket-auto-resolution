# classifier.py
import re
from typing import Tuple

# ── Keyword rules (fire BEFORE the ML model) ──────────────────────────────
KEYWORD_RULES = {
    "Account": [
        r"\bpassword\b", r"\bpasswd\b", r"\blogin\b", r"\bsign.?in\b",
        r"\baccount\b", r"\bauthenti", r"\baccess.?denied\b",
        r"\blocked.?out\b", r"\breset\b", r"\bcredential",
        r"\bpermission\b", r"\bunauthori",
    ],
    "Printer": [
        r"\bprint", r"\bscanner\b", r"\bscanning\b", r"\btoner\b",
        r"\bcartridge\b", r"\bjam\b", r"\bspooler\b", r"\bink\b",
    ],
    "Network": [
        r"\binternet\b", r"\bwifi\b", r"\bwi-fi\b", r"\bnetwork\b",
        r"\bconnect", r"\bvpn\b", r"\bdns\b", r"\bip.?address\b",
        r"\blatency\b", r"\bbandwidth\b", r"\bfirewall\b",
    ],
    "Software": [
        r"\binstall", r"\bcrash", r"\bfreezing\b", r"\bfreeze\b",
        r"\bnot.?respond", r"\buninstall", r"\bupdate\b", r"\bpatch\b",
        r"\bbsod\b", r"\bblue.?screen\b", r"\bapplication\b",
        r"\bsoftware\b", r"\bapp\b",
    ],
    "Hardware": [
        r"\bkeyboard\b", r"\bmouse\b", r"\bmonitor\b", r"\bscreen\b",
        r"\blaptop\b", r"\bdesktop\b", r"\bbattery\b", r"\bcharger\b",
        r"\boverheating\b", r"\bhardware\b", r"\bram\b", r"\bssd\b",
        r"\bhard.?drive\b",
    ],
    "Database": [
        r"\bdatabase\b", r"\bsql\b", r"\bquery\b", r"\btable\b",
        r"\bdb\b", r"\bmongo", r"\bpostgres", r"\bmysql\b",
        r"\bbackup\b", r"\brestore\b", r"\bcorrupt",
    ],
    "Email": [
        r"\bemail\b", r"\boutlook\b", r"\bsmtp\b", r"\bimap\b",
        r"\bsent.?box\b", r"\binbox\b", r"\bspam\b", r"\battachment\b",
    ],
}

MIN_WORD_COUNT = 2          # Fix 2: was checking char length, now word count
CONFIDENCE_BANDS = {
    "manual_review":    (0.00, 0.35),
    "low_confidence":   (0.35, 0.55),
    "auto_with_review": (0.55, 0.75),
    "auto_resolve":     (0.75, 1.00),
}


def is_query_too_short(text: str) -> bool:
    """Fix 2: reject only if fewer than 2 words, not fewer than 3 chars."""
    return len(text.strip().split()) < MIN_WORD_COUNT


def keyword_classify(text: str) -> Tuple[str | None, float]:
    """
    Fix 3: Rule-based classifier that runs before the ML model.
    Returns (category, confidence) or (None, 0) if no rule matches.
    Multiple matches → category with most keyword hits wins.
    """
    text_lower = text.lower()
    scores: dict[str, int] = {}
    for category, patterns in KEYWORD_RULES.items():
        hits = sum(1 for p in patterns if re.search(p, text_lower))
        if hits > 0:
            scores[category] = hits
    if not scores:
        return None, 0.0
    best = max(scores, key=scores.get)
    # Confidence scales with number of hits: 1 hit → 0.70, 2+ hits → 0.85
    confidence = 0.70 if scores[best] == 1 else 0.85
    return best, confidence


def get_confidence_band(score: float) -> str:
    for band, (low, high) in CONFIDENCE_BANDS.items():
        if low <= score < high:
            return band
    return "auto_resolve"


def classify_ticket(text: str, ml_model, vectorizer) -> dict:
    """
    Full classification pipeline:
    1. Short query guard
    2. Keyword pre-classifier
    3. ML model fallback
    4. Confidence banding
    """
    if is_query_too_short(text):
        return {
            "category": "Unknown",
            "confidence": 0.0,
            "band": "manual_review",
            "source": "short_query",
            "message": "Please describe your issue in more detail.",
        }

    # Fix 3: try keyword rules first
    category, confidence = keyword_classify(text)
    source = "keyword"

    if category is None:
        # Fall back to ML model
        vec = vectorizer.transform([text])
        proba = ml_model.predict_proba(vec)[0]
        confidence = float(max(proba))
        category = ml_model.classes_[proba.argmax()]
        source = "ml_model"

    band = get_confidence_band(confidence)

    return {
        "category": category,
        "confidence": round(confidence, 3),
        "band": band,
        "source": source,
    }