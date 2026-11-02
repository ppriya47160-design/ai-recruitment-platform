# 🎯 AI Recruitment Intelligence Platform

Ranks resumes against a job description using **semantic embeddings + skill coverage + experience**, with explainable scores, PII masking (bias reduction), skill-gap reports and resume Q&A.

## Run (VS Code terminal)
```bash
python -m venv .venv
.venv\Scripts\activate        # Windows   (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
streamlit run app.py
```
First run downloads the MiniLM model (~90 MB). If it can't download, the app automatically falls back to TF-IDF.

Optional: copy `.env.example` to `.env` and add `ANTHROPIC_API_KEY` for Claude-powered Q&A.

## Structure
```
app.py            Streamlit UI
src/ui.py         custom dark theme + UI components
src/skills.py     skill taxonomy + synonyms
src/parser.py     PDF/TXT parsing, experience extraction
src/masking.py    PII masking
src/matcher.py    embeddings / TF-IDF similarity
src/scorer.py     explainable scoring + evidence check
src/llm.py        resume Q&A (Claude or offline)
data/             sample JD + resumes
```

## Score formula
`Final = 0.5 × semantic + 0.3 × required-skill coverage + 0.2 × experience/projects` (adjustable in sidebar).
**Evidence %** = share of matched skills that are backed by projects/experience, not just listed in the Skills line.

## Ideas for v2
Multi-agent screening, FAISS candidate-pool search, GitHub verification, NDCG evaluation vs. human ranking, FastAPI + Docker deploy.
