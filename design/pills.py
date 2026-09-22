import fontkit as fk
from common import THEMES, svg_doc, text, rgba, arrow_ne, icon

PILLS = {
    "linkedin": ("link", "Connect on LinkedIn", True),
    "email": ("mail", "adityashroff06@gmail.com", False),
}

def build(kind, theme):
    t = THEMES[theme]; F = fk.Fonts(); dark = theme == "dark"
    ic, label, ext = PILLS[kind]
    fs, H = 14, 44
    tw = fk.width(label, "sans5", fs)
    W = int(18 + 20 + 10 + tw + (26 if ext else 0) + 20)
    a = t["violet2"] if kind == "linkedin" else t["cyan"]
    defs = f'''<linearGradient id="bg" x1="0" x2="1"><stop offset="0" stop-color="{rgba(a, 0.16 if dark else 0.10)}"/><stop offset="1" stop-color="{rgba(t['cyan'] if kind=='linkedin' else t['violet2'], 0.10 if dark else 0.06)}"/></linearGradient>'''
    body = (f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="{(H-2)/2}" fill="url(#bg)" stroke="{rgba(a, 0.45)}" stroke-width="1.2"/>'
            + icon(ic, 18 + 10, H / 2, 20, a, 1.8)
            + text(18 + 20 + 10, round(H / 2 + fs * 0.36, 1), label, F, "sans5", fs, t["text"]))
    if ext:
        body += arrow_ne(W - 20 - 9, H / 2 - 4.5, 9, a, 1.8)
    return svg_doc(W, H, label, body, F.css(), defs)
