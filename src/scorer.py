"""Explainable scoring: Final = w1*semantic + w2*skill coverage + w3*experience/project relevance."""
import re
from .skills import extract_skills
from .parser import years_of_experience, project_count, required_years


def analyse_jd(jd: str) -> dict:
    return {"skills": extract_skills(jd), "years": required_years(jd)}


def _evidence(text: str, matched: list) -> float:
    """Share of matched skills that also appear OUTSIDE the skills list (i.e. backed by projects/experience)."""
    if not matched:
        return 0.0
    parts = re.split(r"\n\s*(?:technical\s+)?skills[^\n]*\n", text, maxsplit=1, flags=re.I)
    if len(parts) < 2:
        return 1.0
    rest = re.split(r"\n\s*(?:projects?|experience|work experience|internships?)\b", parts[1], maxsplit=1, flags=re.I)
    body = rest[1] if len(rest) > 1 else ""
    proven = extract_skills(body)
    return sum(1 for s in matched if s in proven) / len(matched)


def score_candidate(jd_info: dict, text: str, semantic: float, weights=(0.5, 0.3, 0.2)) -> dict:
    cand = extract_skills(text)
    req = jd_info["skills"]
    matched = sorted(req & cand)
    missing = sorted(req - cand)
    coverage = len(matched) / len(req) if req else 0.0

    yrs = years_of_experience(text)
    need = jd_info["years"] or 2.0
    exp = 0.6 * min(yrs / need, 1.0) + 0.4 * min(project_count(text) / 3, 1.0)
    evidence = _evidence(text, matched)

    w_sem, w_sk, w_exp = weights
    final = w_sem * semantic + w_sk * coverage + w_exp * exp
    return {
        "final": round(final * 100, 1), "semantic": round(semantic * 100, 1),
        "skills": round(coverage * 100, 1), "experience": round(exp * 100, 1),
        "evidence": round(evidence * 100, 1), "years": yrs,
        "matched": matched, "missing": missing,
        "extra": sorted(cand - req),
        "flag": "Skills claimed but not backed by projects/experience" if matched and evidence < 0.4 else "",
    }
