import fontkit as fk
from common import THEMES, svg_doc, text, rgba, esc, chip, arrow_ne, wrap

W, H = 440, 262
PROJECTS = [
    dict(slug="ems", accent="teal", label="ENERGY · CARBON · RAG", title="EMS Co-Pilot",
         desc="Plant energy readings in, traceable energy and carbon reports out: deterministic SQLite analytics, a Gradio dashboard and optional AI drafts that cite source pages.",
         metric="175,200", mlabel="duplicate rows caught before reporting",
         chips=["Python", "SQLite", "ChromaDB", "OpenAI", "Gradio"],
         url="https://github.com/adityashroff06-code/EMS-Co-Pilot-"),
    dict(slug="briefing", accent="pink", label="GENAI · SPEECH TO BRIEF", title="GenAI Video Briefing Console",
         desc="Turns a spoken YouTube video into an executive summary, key ideas, takeaways and a one-line TL;DR. One shared pipeline behind a Gradio app, a CLI and a notebook.",
         metric="4-part", mlabel="brief from up to 30 minutes of audio",
         chips=["Python", "yt-dlp", "OpenAI", "Gradio", "FAISS"],
         url="https://github.com/adityashroff06-code/YT-Summarizer---Gen-AI-Console"),
    dict(slug="cleanair", accent="cyan", label="AIR QUALITY · OPEN DATA", title="Clean Air OS",
         desc="An inspectable PM2.5 research baseline for Delhi-area stations: validated readings, preserved gaps and station-level summaries that state their own coverage.",
         metric="9,992", mlabel="validated observations from 9 stations",
         chips=["pandas", "NumPy", "Matplotlib", "pytest"],
         url="https://github.com/adityashroff06-code/Clean_Air_OS"),
    dict(slug="segmentation", accent="violet2", label="ML · MARKETING ANALYTICS", title="Consumer Segmentation",
         desc="Segments bath-soap households by purchase behaviour: EDA, K-Means checked by elbow and silhouette, then classifiers predicting segment membership.",
         metric="4", mlabel="segments, then 3 classifiers compared",
         chips=["pandas", "scikit-learn", "Seaborn", "K-Means"],
         url="https://github.com/adityashroff06-code/Consumer-Segmentation-and-Purchase-Behavior-Analysis"),
]

def build(p, theme):
    t = THEMES[theme]; F = fk.Fonts(); dark = theme == "dark"
    a = t[p["accent"]]; L, R = 28, W - 28
    defs = f'''
    <clipPath id="fr"><rect width="{W}" height="{H}" rx="20"/></clipPath>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['card0']}"/><stop offset="1" stop-color="{t['card1']}"/></linearGradient>
    <radialGradient id="glow" cx="1" cy="0" r="0.75"><stop offset="0" stop-color="{a}" stop-opacity="{0.30 if dark else 0.20}"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></radialGradient>
    <linearGradient id="num" x1="0" x2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{t['grad_b']}"/></linearGradient>
    <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{a}" stop-opacity="0"/><stop offset="0.5" stop-color="{a}" stop-opacity="0.9"/><stop offset="1" stop-color="{a}" stop-opacity="0"/></linearGradient>
    '''
    body = text(L, 46, p["label"], F, "mono5", 10.5, a, tracking=1.8)
    body += arrow_ne(R - 12, 36, 11, t["muted"], 1.8)
    fs = 23
    while fk.width(p["title"], "display6", fs) > R - L: fs -= 0.5
    body += text(L - 1, 80, p["title"], F, "display6", fs, t["text"], tracking=-0.3)
    lines = wrap(p["desc"], "sans", 13.2, R - L)
    assert len(lines) <= 3, (p["slug"], lines)
    for i, ln in enumerate(lines):
        body += text(L, 108 + i * 20, ln, F, "sans", 13.2, t["text2"] if dark else t["muted"])
    mw = fk.width(p["metric"], "display", 25)
    body += text(L, 196, p["metric"], F, "display", 25, "url(#num)")
    assert mw + 12 + fk.width(p["mlabel"], "sans5", 12.2) <= R - L, p["slug"]
    body += text(round(L + mw + 12, 1), 195, p["mlabel"], F, "sans5", 12.2, t["muted"])
    cx = L
    for c in p["chips"]:
        s, w = chip(cx, 214, c, F, t, size=10.5, pad=8, h=22, color=None); body += s; cx += w + 6
    body = f'''
    <g clip-path="url(#fr)">
      <rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#glow)"/>
      {body}
      <rect x="30" y="0.5" width="{W-60}" height="1.2" fill="url(#edge)"/>
    </g>
    <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="19.5" stroke="{t['stroke']}" stroke-opacity="{t['stroke_a']}"/>'''
    return svg_doc(W, H, p["title"], body, F.css(), defs, desc=f'{p["title"]}: {p["desc"]} {p["metric"]} {p["mlabel"]}.')
