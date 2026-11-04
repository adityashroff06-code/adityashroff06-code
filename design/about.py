"""Statement card: a pull quote and three short columns."""
import fontkit as fk
from common import THEMES, svg_doc, text, kicker, wrap, rule, frame_defs, frame_open, frame_close

W = 900
QUOTE = ("I put data and AI to work where the result has to be defended: a packaging line, a police "
         "control room, an energy report. Every build ships with its evaluation, its limits and its reason codes.")
COLS = [
    ("FOCUS", ["Computer vision on live feeds", "GenAI and RAG with cited sources", "Data pipelines that show coverage"]),
    ("HOW I WORK", ["Tested, CI-checked code", "Docs that state their limits", "Measured and estimated, labelled"]),
    ("BASED IN", ["Toronto, Canada", "Digital Transformation and", "AI Enablement Specialist"]),
]

def build(theme):
    t = THEMES[theme]; F = fk.Fonts()
    L, R = 56, W - 56
    head, _ = kicker(L, 58, "STATEMENT", F, t)
    lines = wrap(QUOTE, "serifi", 24, R - L)
    assert len(lines) <= 3, lines
    quote = "".join(text(L - 1, 106 + i * 34, ln, F, "serifi", 24, t["text"]) for i, ln in enumerate(lines))
    y = 106 + (len(lines) - 1) * 34 + 42
    cols = rule(L, y, R, t)
    gap = 28; cw = (R - L - gap * 2) / 3
    for i, (name, items) in enumerate(COLS):
        x = L + i * (cw + gap)
        k, _ = kicker(round(x, 1), y + 34, name, F, t, size=10.5)
        cols += k
        for j, it in enumerate(items):
            assert fk.width(it, "sans", 13.5) <= cw, it
            cols += text(round(x, 1), y + 62 + j * 21, it, F, "sans", 13.5, t["text2"])
    H = int(y + 62 + 2 * 21 + 34)
    body = frame_open(W, H, t) + head + quote + cols + frame_close(W, H, t)
    return svg_doc(W, H, "Statement", body, F.css(), frame_defs(W, H, t),
                   desc=QUOTE + " " + " ".join(f"{n}: {', '.join(it)}." for n, it in COLS))
