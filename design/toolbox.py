"""Toolbox: categorised tags, taken from what the repositories actually import."""
import fontkit as fk
from common import THEMES, svg_doc, text, kicker, chip, frame_defs, frame_open, frame_close

W = 900
GROUPS = [
    ("Computer vision", ["OpenCV", "PyTorch", "ONNX Runtime", "YOLOX-S", "PaddleOCR", "PatchCore", "NumPy"]),
    ("GenAI and NLP", ["OpenAI API", "ChromaDB", "FAISS", "Sentence-Transformers", "spaCy", "NLTK", "Gradio"]),
    ("Data and ML", ["pandas", "scikit-learn", "Matplotlib", "Seaborn", "Plotly", "Jupyter", "MySQL", "SQLite"]),
    ("Engineering", ["Python", "FastAPI", "React", "TypeScript", "Vite", "Leaflet", "GitHub Actions", "pytest"]),
]

def build(theme):
    t = THEMES[theme]; F = fk.Fonts()
    L, R, gap = 56, W - 56, 24
    colw = (R - L - gap * 3) / 4
    head, _ = kicker(L, 58, "TOOLBOX", F, t)
    head += text(R, 58, "taken from what the repositories actually import", F, "serifi", 14, t["muted"], anchor="end")
    top = 108; cols = ""; bottom = 0
    for i, (name, items) in enumerate(GROUPS):
        x0 = L + i * (colw + gap)
        cols += text(round(x0, 1), top, name, F, "sans6", 14, t["text"])
        cols += f'<rect x="{x0:.1f}" y="{top+12}" width="{colw:.1f}" height="1" fill="{t["line"]}" fill-opacity="{t["line_a"]}"/>'
        x, y = x0, top + 28
        for it in items:
            w = fk.width(it, "mono", 10.5) + 16
            if x + w > x0 + colw + 0.5:
                x, y = x0, y + 30
            s, w = chip(x, y, it, F, t, size=10.5, pad=8, h=24)
            cols += s; x += w + 6
        bottom = max(bottom, y + 24)
    H = int(bottom + 40)
    body = frame_open(W, H, t) + head + cols + frame_close(W, H, t)
    return svg_doc(W, H, "Toolbox", body, F.css(), frame_defs(W, H, t),
                   desc="Toolbox. " + " ".join(f"{n}: {', '.join(it)}." for n, it in GROUPS))
