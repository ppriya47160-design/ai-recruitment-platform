"""Resume text extraction + light structured parsing."""
import re
import io


def extract_text(uploaded) -> str:
    """Accepts a Streamlit UploadedFile or a path. Supports PDF and TXT."""
    name = getattr(uploaded, "name", str(uploaded)).lower()
    data = uploaded.read() if hasattr(uploaded, "read") else open(uploaded, "rb").read()
    if name.endswith(".pdf"):
        import pdfplumber
        with pdfplumber.open(io.BytesIO(data)) as pdf:
            return "\n".join((p.extract_text() or "") for p in pdf.pages).strip()
    return data.decode("utf-8", errors="ignore").strip()


def guess_name(text: str, fallback: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line and len(line.split()) <= 4 and not re.search(r"[@\d]", line):
            return line.title()
    return fallback


def years_of_experience(text: str) -> float:
    explicit = [int(x) for x in re.findall(r"(\d{1,2})\+?\s*(?:years|yrs)", text, re.I)]
    if explicit:
        return float(max(explicit))
    total = 0.0
    for a, b in re.findall(r"((?:19|20)\d{2})\s*[-–to]+\s*((?:19|20)\d{2}|present)", text, re.I):
        end = 2026 if b.lower() == "present" else int(b)
        if 0 < end - int(a) <= 10:
            total += end - int(a)
    return min(total, 15.0)


def project_count(text: str) -> int:
    return min(len(re.findall(r"\bproject", text, re.I)), 10)


def required_years(jd: str) -> float:
    m = re.findall(r"(\d{1,2})\+?\s*(?:years|yrs)", jd, re.I)
    return float(min(int(x) for x in m)) if m else 0.0
