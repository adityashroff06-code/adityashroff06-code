"""Section headers: a kicker, an italic note and a hairline, on a transparent background."""
import fontkit as fk
from common import THEMES, svg_doc, text, kicker, rule

W, H = 900, 44
SECTIONS = {
    "work": ("SELECTED WORK", "four builds, each with its number"),
    "archive": ("ARCHIVE", "further repositories, newest first"),
    "pulse": ("ACTIVITY", "rebuilt every day by GitHub Actions"),
}

def build(slug, theme):
    t = THEMES[theme]; F = fk.Fonts()
    label, note = SECTIONS[slug]
    L, R = 36, W - 36
    k, kw = kicker(L, 30, label, F, t)
    body = k + text(round(L + kw + 16, 1), 30, note, F, "serifi", 15, t["muted"])
    body += rule(L, H - 0.5, R, t, strong=True)
    return svg_doc(W, H, f"{label}: {note}", body, F.css(), "", desc=f"{label}: {note}")
