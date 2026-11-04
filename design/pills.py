"""Contact buttons."""
import fontkit as fk
from common import THEMES, svg_doc, text, rgba, arrow_ne, icon

PILLS = {
    "linkedin": ("link", "Connect on LinkedIn", True),
    "email": ("mail", "adityashroff06@gmail.com", False),
}

def build(kind, theme):
    t = THEMES[theme]; F = fk.Fonts()
    ic, label, ext = PILLS[kind]
    fs, H = 13.5, 44
    tw = fk.width(label, "sans5", fs)
    W = int(18 + 18 + 12 + tw + (24 if ext else 0) + 20)
    body = (f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="3" fill="{rgba(t["wash"], t["wash_a"])}" '
            f'stroke="{t["gold"]}" stroke-opacity="0.7" stroke-width="1.2"/>'
            + icon(ic, 18 + 9, H / 2, 18, t["gold"])
            + text(18 + 18 + 12, round(H / 2 + fs * 0.36, 1), label, F, "sans5", fs, t["text"]))
    if ext:
        body += arrow_ne(W - 20 - 8, H / 2 - 4, 8, t["gold_ink"])
    return svg_doc(W, H, label, body, F.css(), "")
