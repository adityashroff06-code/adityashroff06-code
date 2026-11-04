"""Colophon."""
import fontkit as fk
from common import THEMES, svg_doc, text, frame_defs, frame_open, frame_close

W, H = 900, 118

def build(theme):
    t = THEMES[theme]; F = fk.Fonts()
    body = frame_open(W, H, t, mark=False)
    body += f'<rect x="{W/2-24}" y="0" width="48" height="2" fill="{t["gold"]}"/>'
    body += text(W / 2, 56, "Thank you for reading.", F, "serifi", 22, t["text"], anchor="middle")
    body += text(W / 2, 84, "Set in Playfair Display, Inter and JetBrains Mono  ·  every card drawn in SVG  ·  activity refreshed daily by GitHub Actions",
                 F, "mono", 10.5, t["muted"], anchor="middle", tracking=0.3)
    body += frame_close(W, H, t)
    return svg_doc(W, H, "Thank you for reading", body, F.css(), frame_defs(W, H, t))
