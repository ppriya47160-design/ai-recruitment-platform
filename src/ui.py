"""Custom UI layer: theme CSS + small HTML components (no leading indentation, so Markdown won't treat them as code)."""
from html import escape

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif; }
.stApp {
  background:
    radial-gradient(900px 500px at 10% -10%, rgba(20,184,166,.22), transparent 60%),
    radial-gradient(800px 500px at 100% 0%, rgba(96,165,250,.14), transparent 55%),
    linear-gradient(160deg, #0B1020 0%, #0E1530 100%);
}
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 1.6rem; max-width: 1250px; }
section[data-testid="stSidebar"] { background: #0F1630; border-right: 1px solid rgba(255,255,255,.06); }

.hero { padding: 28px 32px; border-radius: 20px; margin-bottom: 22px;
  background: linear-gradient(135deg, rgba(20,184,166,.28), rgba(96,165,250,.12));
  border: 1px solid rgba(255,255,255,.10); box-shadow: 0 10px 40px rgba(0,0,0,.35); }
.hero h1 { margin: 0; font-size: 2.1rem; font-weight: 800; letter-spacing: -.5px;
  background: linear-gradient(90deg, #FFFFFF, #99F6E4 60%, #93C5FD); -webkit-background-clip: text;
  -webkit-text-fill-color: transparent; }
.hero p { margin: 8px 0 14px; color: #A9B3D6; font-size: 1rem; }
.pill { display: inline-block; padding: 4px 12px; margin: 0 6px 4px 0; border-radius: 999px; font-size: .75rem;
  font-weight: 600; color: #CCFBF1; background: rgba(20,184,166,.16); border: 1px solid rgba(20,184,166,.35); }

.kpi { padding: 18px 20px; border-radius: 16px; background: rgba(255,255,255,.04);
  border: 1px solid rgba(255,255,255,.08); backdrop-filter: blur(6px); }
.kpi .label { color: #8F9AC2; font-size: .78rem; text-transform: uppercase; letter-spacing: .08em; font-weight: 600; }
.kpi .value { font-size: 2rem; font-weight: 800; color: #fff; margin-top: 4px; }
.kpi .sub { color: #7C86AE; font-size: .78rem; }

.section { font-size: 1.15rem; font-weight: 700; color: #fff; margin: 26px 0 12px; display: flex; align-items: center; gap: 10px; }
.section:before { content: ""; width: 5px; height: 20px; border-radius: 4px; background: linear-gradient(#14B8A6, #60A5FA); }

.card { padding: 20px 22px; border-radius: 16px; background: rgba(255,255,255,.04); border: 1px solid rgba(255,255,255,.08); }
.rank-row { display: flex; align-items: center; gap: 16px; padding: 16px 20px; margin-bottom: 12px; border-radius: 16px;
  background: rgba(255,255,255,.04); border: 1px solid rgba(255,255,255,.08); transition: all .2s; }
.rank-row:hover { transform: translateY(-2px); border-color: rgba(20,184,166,.55); background: rgba(20,184,166,.07); }
.rank-badge { width: 44px; height: 44px; border-radius: 12px; display: flex; align-items: center; justify-content: center;
  font-weight: 800; font-size: 1.1rem; color: #fff; background: linear-gradient(135deg, #14B8A6, #3B82F6); flex-shrink: 0; }
.rank-badge.gold { background: linear-gradient(135deg, #FFD166, #F59E0B); color: #231a00; }
.rank-main { flex: 1; min-width: 0; }
.rank-name { font-weight: 700; color: #fff; font-size: 1.02rem; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.verdict { font-size: .68rem; font-weight: 700; padding: 3px 9px; border-radius: 999px; letter-spacing: .04em; text-transform: uppercase; }
.v-strong { color: #4ADE80; background: rgba(74,222,128,.12); border: 1px solid rgba(74,222,128,.35); }
.v-good { color: #38BDF8; background: rgba(56,189,248,.12); border: 1px solid rgba(56,189,248,.35); }
.v-part { color: #FBBF24; background: rgba(251,191,36,.12); border: 1px solid rgba(251,191,36,.35); }
.v-weak { color: #F87171; background: rgba(248,113,113,.12); border: 1px solid rgba(248,113,113,.35); }
.bar { height: 8px; border-radius: 99px; background: rgba(255,255,255,.08); margin: 9px 0 7px; overflow: hidden; }
.bar .fill { height: 100%; border-radius: 99px; }
.mini { color: #8F9AC2; font-size: .78rem; }
.score { font-size: 1.9rem; font-weight: 800; color: #fff; min-width: 84px; text-align: right; }
.score span { font-size: .9rem; color: #8F9AC2; font-weight: 600; }

.chip { display: inline-block; padding: 5px 12px; margin: 0 6px 8px 0; border-radius: 999px; font-size: .8rem; font-weight: 600; }
.chip.ok { color: #4ADE80; background: rgba(74,222,128,.10); border: 1px solid rgba(74,222,128,.35); }
.chip.miss { color: #F87171; background: rgba(248,113,113,.10); border: 1px solid rgba(248,113,113,.35); }
.chip.extra { color: #93C5FD; background: rgba(147,197,253,.10); border: 1px solid rgba(147,197,253,.30); }
.chip-title { color: #8F9AC2; font-size: .75rem; text-transform: uppercase; letter-spacing: .08em; font-weight: 700; margin: 10px 0 8px; }
.flag { margin-top: 12px; padding: 10px 14px; border-radius: 12px; color: #FBBF24; font-size: .85rem;
  background: rgba(251,191,36,.08); border: 1px solid rgba(251,191,36,.3); }
.gap { padding: 12px 16px; margin-bottom: 10px; border-radius: 12px; background: rgba(255,255,255,.03);
  border-left: 3px solid #14B8A6; color: #C9D1EE; font-size: .9rem; }
.gap b { color: #fff; }

.stButton > button[kind="primary"], .stDownloadButton > button { border: 0; border-radius: 12px; font-weight: 700;
  padding: .6rem 1.4rem; color: #fff; background: linear-gradient(90deg, #14B8A6, #3B82F6); box-shadow: 0 6px 20px rgba(20,184,166,.35); }
.stButton > button[kind="primary"]:hover, .stDownloadButton > button:hover { filter: brightness(1.1); transform: translateY(-1px); }
.stTabs [data-baseweb="tab-list"] { gap: 6px; border-bottom: 1px solid rgba(255,255,255,.08); }
.stTabs [data-baseweb="tab"] { padding: 10px 18px; border-radius: 10px 10px 0 0; font-weight: 600; }
textarea, input { border-radius: 12px !important; }
[data-testid="stFileUploader"] section { border-radius: 14px; border: 1px dashed rgba(20,184,166,.5); background: rgba(20,184,166,.05); }
</style>
"""


def hero(engine: str) -> str:
    return (
        '<div class="hero"><h1>🎯 AI Recruitment Intelligence</h1>'
        '<p>Semantic resume ranking with explainable scores, bias masking and skill-gap analysis.</p>'
        '<span class="pill">Semantic Matching</span><span class="pill">Explainable AI</span>'
        '<span class="pill">Bias Masking</span><span class="pill">Evidence Check</span>'
        f'<span class="pill">Engine: {escape(engine)}</span></div>'
    )


def kpi(label: str, value, sub: str = "") -> str:
    return f'<div class="kpi"><div class="label">{escape(label)}</div><div class="value">{escape(str(value))}</div><div class="sub">{escape(sub)}</div></div>'


def section(title: str) -> str:
    return f'<div class="section">{escape(title)}</div>'


def score_color(s: float) -> str:
    return "#4ADE80" if s >= 70 else "#38BDF8" if s >= 45 else "#FBBF24" if s >= 25 else "#F87171"


def verdict(s: float):
    return ("Strong match", "v-strong") if s >= 70 else ("Good match", "v-good") if s >= 45 else \
           ("Partial", "v-part") if s >= 25 else ("Weak", "v-weak")


def rank_card(rank: int, r: dict) -> str:
    label, cls = verdict(r["final"])
    gold = " gold" if rank == 1 else ""
    c = score_color(r["final"])
    return (
        f'<div class="rank-row"><div class="rank-badge{gold}">{rank}</div><div class="rank-main">'
        f'<div class="rank-name">{escape(r["candidate"])}<span class="verdict {cls}">{label}</span></div>'
        f'<div class="bar"><div class="fill" style="width:{min(r["final"],100)}%;background:linear-gradient(90deg,{c}88,{c})"></div></div>'
        f'<div class="mini">Semantic {r["semantic"]}% · Skills {r["skills"]}% · Experience {r["experience"]}% · Evidence {r["evidence"]}%</div>'
        f'</div><div class="score">{r["final"]}<span>%</span></div></div>'
    )


def chips(title: str, items: list, kind: str) -> str:
    body = "".join(f'<span class="chip {kind}">{escape(i)}</span>' for i in items) or '<span class="mini">none</span>'
    return f'<div class="chip-title">{title}</div>{body}'


def gap_item(skill: str) -> str:
    return (f'<div class="gap"><b>{escape(skill)}</b> → Build a small project using <i>{escape(skill)}</i> and add it to the resume.<br>'
            f'Interview Q: <i>"Where have you used {escape(skill)}, or how would you learn it quickly?"</i></div>')
