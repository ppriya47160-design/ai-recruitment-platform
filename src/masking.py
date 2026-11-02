"""PII masking to reduce bias before scoring (name, contact, gender words, institution)."""
import re


def mask_pii(text: str, name: str = "") -> str:
    t = text
    t = re.sub(r"[\w.+-]+@[\w-]+\.[\w.-]+", "[EMAIL]", t)
    t = re.sub(r"(?:https?://|www\.)\S+|(?:linkedin|github)\.com\S*", "[LINK]", t, flags=re.I)
    t = re.sub(r"\+?\d[\d\s().-]{8,}\d", "[PHONE]", t)
    t = re.sub(r"\b(he|she|his|her|him|mr|mrs|ms|male|female)\b\.?", "[GENDER]", t, flags=re.I)
    t = re.sub(r"[^\n,]*\b(?:University|College|Institute|IIT|NIT|School)\b[^\n,]*", "[INSTITUTION]", t)
    if name:
        t = re.sub(re.escape(name), "[CANDIDATE]", t, flags=re.I)
    return t
