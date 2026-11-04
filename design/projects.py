"""Selected work: four compact project cards (two per row in the README)."""
import fontkit as fk
from common import THEMES, svg_doc, text, kicker, chip, figure, arrow_ne, wrap, frame_defs, frame_open, frame_close

W, H = 440, 256
PROJECTS = [
    dict(slug="ems", label="ENERGY  ·  CARBON  ·  RAG", title="EMS Co-Pilot",
         desc="Plant energy readings in, traceable energy and carbon reports out: deterministic SQLite analytics, a Gradio dashboard and AI drafts that cite their sources.",
         metric="175,200", mlabel="duplicate rows caught before reporting",
         chips=["Python", "SQLite", "ChromaDB", "OpenAI", "Gradio"],
         url="https://github.com/adityashroff06-code/EMS-Co-Pilot-"),
    dict(slug="briefing", label="GENAI  ·  SPEECH TO BRIEF", title="GenAI Video Briefing Console",
         desc="Turns a spoken YouTube video into an executive summary, key ideas, takeaways and a one-line TL;DR. One shared pipeline behind a Gradio app, a CLI and a notebook.",
         metric="4-part", mlabel="brief from up to 30 minutes of audio",
         chips=["Python", "yt-dlp", "OpenAI", "Gradio", "FAISS"],
         url="https://github.com/adityashroff06-code/YT-Summarizer---Gen-AI-Console"),
    dict(slug="cleanair", label="AIR QUALITY  ·  OPEN DATA", title="Clean Air OS",
         desc="An inspectable PM2.5 research baseline for Delhi-area stations: validated readings, preserved gaps and station-level summaries that state their own coverage.",
         metric="9,992", mlabel="validated observations from 9 stations",
         chips=["pandas", "NumPy", "Matplotlib", "pytest"],
         url="https://github.com/adityashroff06-code/Clean_Air_OS"),
    dict(slug="segmentation", label="MACHINE LEARNING  ·  MARKETING", title="Consumer Segmentation",
         desc="Segments bath-soap households by purchase behaviour: EDA, K-Means checked by elbow and silhouette, then classifiers predicting segment membership.",
         metric="4", mlabel="segments, then three classifiers compared",
         chips=["pandas", "scikit-learn", "Seaborn", "K-Means"],
         url="https://github.com/adityashroff06-code/Consumer-Segmentation-and-Purchase-Behavior-Analysis"),
]

def build(p, theme):
    t = THEMES[theme]; F = fk.Fonts()
    L, R = 32, W - 32
    body, _ = kicker(L, 50, p["label"], F, t, size=10.5)
    body += arrow_ne(R - 11, 40, 10, t["muted"])
    fs = 25
    while fk.width(p["title"], "serif6", fs, -0.4) > R - L - 24: fs -= 0.5
    body += text(L - 1, 88, p["title"], F, "serif6", fs, t["text"], tracking=-0.4)
    lines = wrap(p["desc"], "sans", 13, R - L)
    assert len(lines) <= 3, (p["slug"], lines)
    for i, ln in enumerate(lines):
        body += text(L, 115 + i * 19.5, ln, F, "sans", 13, t["text2"])
    mw = fk.width(p["metric"], "serif6", 26, -0.5, lnum=True)
    body += figure(L, 194, p["metric"], F, t, size=26)
    assert mw + 12 + fk.width(p["mlabel"], "sans", 12) <= R - L, p["slug"]
    body += text(round(L + mw + 12, 1), 193, p["mlabel"], F, "sans", 12, t["muted"])
    cx = L
    for c in p["chips"]:
        s, w = chip(cx, 212, c, F, t, size=10.5, pad=8, h=22); body += s; cx += w + 6
    body = frame_open(W, H, t) + body + frame_close(W, H, t)
    return svg_doc(W, H, p["title"], body, F.css(), frame_defs(W, H, t),
                   desc=f'{p["title"]}: {p["desc"]} {p["metric"]} {p["mlabel"]}.')
