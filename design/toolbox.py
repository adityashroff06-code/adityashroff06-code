import fontkit as fk
from common import THEMES, svg_doc, text, rgba, chip

W = 900
GROUPS = [
    ("Computer vision", "violet2", ["OpenCV", "ONNX Runtime", "YOLOX-S", "PaddleOCR", "NumPy"]),
    ("GenAI & NLP", "pink", ["OpenAI API", "ChromaDB", "FAISS", "Sentence-Transformers", "spaCy", "NLTK", "Gradio"]),
    ("Data & ML", "cyan", ["pandas", "scikit-learn", "Matplotlib", "Seaborn", "Plotly", "Jupyter", "MySQL", "SQLite"]),
    ("Engineering", "teal", ["Python", "FastAPI", "React", "Vite", "Leaflet", "GitHub Actions", "pytest", "Claude Code"]),
]

def build(theme):
    t = THEMES[theme]; F = fk.Fonts(); dark = theme == "dark"
    L, R, gap = 32, W - 32, 18
    colw = (R - L - gap * 3) / 4
    top = 96; cols = ""; bottom = 0
    for i, (name, acc, items) in enumerate(GROUPS):
        x0 = L + i * (colw + gap); a = t[acc]
        cols += f'<rect x="{x0:.1f}" y="{top-26}" width="22" height="3" rx="1.5" fill="{a}"/>'
        cols += text(round(x0, 1), top - 6, name, F, "sans6", 14.5, t["text"])
        x, y = x0, top + 8
        for it in items:
            w = fk.width(it, "mono", 11) + 18
            if x + w > x0 + colw + 0.5:
                x, y = x0, y + 30
            s, w = chip(x, y, it, F, t, size=11, pad=9, h=24, color=a, tone=0.10 if dark else 0.08)
            cols += s; x += w + 6
        bottom = max(bottom, y + 24)
    H = int(bottom + 30)
    defs = f'''
    <clipPath id="fr"><rect width="{W}" height="{H}" rx="20"/></clipPath>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['card0']}"/><stop offset="1" stop-color="{t['card1']}"/></linearGradient>
    <radialGradient id="g1" cx="0.5" cy="0" r="0.7"><stop offset="0" stop-color="{t['orb_c']}" stop-opacity="{0.28 if dark else 0.35}"/><stop offset="1" stop-color="{t['orb_c']}" stop-opacity="0"/></radialGradient>
    '''
    head = text(L, 42, "TOOLBOX", F, "mono5", 12, t["cyan"], tracking=2.4)
    head += text(R, 42, "taken from what my repos actually import", F, "mono", 11.5, t["muted"], anchor="end")
    body = f'''
    <g clip-path="url(#fr)">
      <rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#g1)"/>
      {head}{cols}
    </g>
    <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="19.5" stroke="{t['stroke']}" stroke-opacity="{t['stroke_a']}"/>'''
    return svg_doc(W, H, "Toolbox", body, F.css(), defs,
                   desc="Toolbox. " + " ".join(f"{n}: {', '.join(it)}." for n, _, it in GROUPS))
