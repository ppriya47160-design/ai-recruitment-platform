import os
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv

from src.parser import extract_text, guess_name
from src.masking import mask_pii
from src.matcher import Embedder
from src.scorer import analyse_jd, score_candidate
from src.llm import ask
from src import ui

load_dotenv()
st.set_page_config(page_title="AI Recruitment Intelligence", page_icon="🎯", layout="wide")
st.markdown(ui.CSS, unsafe_allow_html=True)


@st.cache_resource
def get_embedder():
    return Embedder()


def read_sample_jd():
    p = os.path.join("data", "sample_jd.txt")
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


emb = get_embedder()
st.markdown(ui.hero(emb.kind), unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    mask = st.toggle("Mask PII (name, gender, college, contact)", value=True)
    st.markdown("**Score weights**")
    w_sem = st.slider("Semantic similarity", 0.0, 1.0, 0.5, 0.05)
    w_sk = st.slider("Required-skill coverage", 0.0, 1.0, 0.3, 0.05)
    w_exp = st.slider("Experience / projects", 0.0, 1.0, 0.2, 0.05)
    total = (w_sem + w_sk + w_exp) or 1.0
    weights = (w_sem / total, w_sk / total, w_exp / total)
    st.caption("Weights are auto-normalised to 100%.")

st.markdown(ui.section("1 · Input"), unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    jd = st.text_area("Job description", value=read_sample_jd(), height=240)
with col2:
    files = st.file_uploader("Upload resumes (PDF / TXT)", type=["pdf", "txt"], accept_multiple_files=True)
    use_samples = st.checkbox("Use sample resumes from data/sample_resumes")

if st.button("🚀 Rank candidates", type="primary"):
    docs = [(f.name, extract_text(f)) for f in (files or [])]
    if use_samples:
        d = os.path.join("data", "sample_resumes")
        for fn in sorted(os.listdir(d)):
            docs.append((fn, open(os.path.join(d, fn), encoding="utf-8").read()))
    if not jd.strip() or not docs:
        st.warning("Add a job description and at least one resume.")
    else:
        with st.spinner("Analysing candidates..."):
            jd_info = analyse_jd(jd)
            names = [guess_name(t, fn) for fn, t in docs]
            scoring_texts = [mask_pii(t, n) if mask else t for (_, t), n in zip(docs, names)]
            sems = emb.semantic_scores(jd, scoring_texts)
            rows = []
            for i, ((fn, raw), n) in enumerate(zip(docs, names)):
                r = score_candidate(jd_info, scoring_texts[i], sems[i], weights)
                r.update({"candidate": f"Candidate {i + 1}" if mask else n, "file": fn, "text": scoring_texts[i]})
                rows.append(r)
            rows.sort(key=lambda r: r["final"], reverse=True)
            st.session_state["rows"], st.session_state["jd_skills"] = rows, sorted(jd_info["skills"])

rows = st.session_state.get("rows")
if rows:
    st.markdown(ui.section("2 · Results"), unsafe_allow_html=True)
    scores = [r["final"] for r in rows]
    k = st.columns(4)
    k[0].markdown(ui.kpi("Candidates screened", len(rows), "resumes analysed"), unsafe_allow_html=True)
    k[1].markdown(ui.kpi("Top score", f"{max(scores)}%", rows[0]["candidate"]), unsafe_allow_html=True)
    k[2].markdown(ui.kpi("Average score", f"{sum(scores) / len(scores):.1f}%", "across all candidates"), unsafe_allow_html=True)
    k[3].markdown(ui.kpi("Shortlisted", sum(s >= 45 for s in scores), "score ≥ 45%"), unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🏆 Ranking", "🔍 Candidate insights", "💬 Ask the resume"])

    with tab1:
        st.markdown(ui.chips("Skills detected in job description", st.session_state["jd_skills"], "extra"), unsafe_allow_html=True)
        for i, r in enumerate(rows, 1):
            st.markdown(ui.rank_card(i, r), unsafe_allow_html=True)
        df = pd.DataFrame([{
            "Rank": i + 1, "Candidate": r["candidate"], "Final %": r["final"], "Semantic %": r["semantic"],
            "Skills %": r["skills"], "Experience %": r["experience"], "Evidence %": r["evidence"],
            "Matched": ", ".join(r["matched"]), "Missing": ", ".join(r["missing"]), "Flag": r["flag"],
        } for i, r in enumerate(rows)])
        st.download_button("⬇️ Export shortlist (CSV)", df.to_csv(index=False), "shortlist.csv", "text/csv")

    with tab2:
        pick = st.selectbox("Select candidate", [r["candidate"] for r in rows])
        r = next(x for x in rows if x["candidate"] == pick)
        c1, c2 = st.columns([1, 1])
        with c1:
            cats = ["Semantic", "Skills", "Experience", "Evidence"]
            vals = [r["semantic"], r["skills"], r["experience"], r["evidence"]]
            fig = go.Figure(go.Scatterpolar(r=vals + vals[:1], theta=cats + cats[:1], fill="toself",
                                            line=dict(color="#7DA9A4", width=3), fillcolor="rgba(20,184,166,0.35)"))
            fig.update_layout(
                polar=dict(bgcolor="rgba(255,255,255,0.03)",
                           radialaxis=dict(range=[0, 100], gridcolor="rgba(255,255,255,.12)", tickfont=dict(color="#D0DCD0")),
                           angularaxis=dict(gridcolor="rgba(255,255,255,.12)", tickfont=dict(color="#DCDDE1", size=13))),
                paper_bgcolor="rgba(0,0,0,0)", showlegend=False, height=360, margin=dict(l=50, r=50, t=30, b=30))
            st.plotly_chart(fig, width="stretch")
        with c2:
            label, cls = ui.verdict(r["final"])
            st.markdown(
                f'<div class="card"><div class="mini">FINAL SCORE</div>'
                f'<div class="score" style="text-align:left;color:{ui.score_color(r["final"])}">{r["final"]}<span>%</span></div>'
                f'<span class="verdict {cls}">{label}</span>'
                + ui.chips("Matched skills", r["matched"], "ok")
                + ui.chips("Missing skills", r["missing"], "miss")
                + (ui.chips("Extra skills", r["extra"], "extra") if r["extra"] else "")
                + (f'<div class="flag">⚠️ {r["flag"]}</div>' if r["flag"] else "")
                + '</div>', unsafe_allow_html=True)
        st.markdown(ui.section("Skill-gap report & interview questions"), unsafe_allow_html=True)
        if r["missing"]:
            st.markdown("".join(ui.gap_item(s) for s in r["missing"]), unsafe_allow_html=True)
        else:
            st.success("No gaps vs. the job description 🎉")

    with tab3:
        who = st.selectbox("Candidate", [r["candidate"] for r in rows], key="qa_pick")
        rr = next(x for x in rows if x["candidate"] == who)
        q = st.text_input("Ask anything", placeholder="e.g. Does this candidate have deployment experience?")
        if q:
            st.markdown(f'<div class="card">{ask(q, rr["text"], emb)}</div>', unsafe_allow_html=True)
else:
    st.info("Add a job description and resumes, then click **Rank candidates**.")
