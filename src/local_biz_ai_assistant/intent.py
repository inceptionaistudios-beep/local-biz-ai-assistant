"""Small deterministic intent and language detector for local mode."""

import re

from local_biz_ai_assistant.models import FAQ, BusinessProfile, Intent, Language

HINGLISH_WORDS = {
    "aap",
    "aapki",
    "hai",
    "hain",
    "kab",
    "kaise",
    "kahan",
    "kaha",
    "khula",
    "khuli",
    "kitna",
    "kitne",
    "daam",
    "dukaan",
    "samay",
    "chahiye",
    "karna",
    "milega",
}

FAQ_STOP_WORDS = {
    "a",
    "an",
    "are",
    "can",
    "do",
    "does",
    "how",
    "i",
    "is",
    "the",
    "to",
    "what",
    "when",
    "where",
    "you",
    "your",
}

INTENT_KEYWORDS: list[tuple[Intent, set[str]]] = [
    (
        "timings",
        {"time", "timing", "timings", "hours", "open", "close", "kab", "khula", "khuli", "samay"},
    ),
    ("location", {"address", "location", "located", "where", "kahan", "kaha", "pata"}),
    ("booking", {"book", "booking", "appointment", "reserve", "slot"}),
    ("contact", {"contact", "phone", "call", "email", "whatsapp", "number"}),
    ("pricing", {"price", "pricing", "cost", "rate", "rates", "daam", "kitna", "charges"}),
    ("services", {"service", "services", "offer", "available", "milta", "milega"}),
    ("greeting", {"hello", "hi", "hey", "namaste", "good", "morning", "evening"}),
]


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.casefold()))


def detect_language(query: str) -> Language:
    return "hinglish" if tokenize(query) & HINGLISH_WORDS else "english"


def detect_intent(query: str) -> Intent:
    words = tokenize(query)
    for intent, keywords in INTENT_KEYWORDS:
        if words & keywords:
            return intent
    return "escalation"


def find_matching_faq(query: str, profile: BusinessProfile) -> FAQ | None:
    normalized_query = query.casefold().strip(" ?!.")
    query_words = tokenize(query) - FAQ_STOP_WORDS
    if not query_words:
        return None
    best: tuple[float, FAQ] | None = None
    for faq in profile.faqs:
        if normalized_query == faq.question.casefold().strip(" ?!."):
            return faq
        faq_words = tokenize(faq.question) - FAQ_STOP_WORDS
        if not faq_words:
            continue
        shared = query_words & faq_words
        score = len(shared) / max(1, min(len(query_words), len(faq_words)))
        if score >= 0.6 and (best is None or score > best[0]):
            best = (score, faq)
    return best[1] if best else None
