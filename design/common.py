"""Shared design tokens and SVG helpers for the "Obsidian & Gold" profile.

Design system (chosen with the UI/UX Pro Max skill, v2.15.0):
  pattern   Storytelling-driven: masthead, statement, the build in progress, the shipped flagship,
            selected work, archive, toolbox, live pulse, colophon.
  style     Exaggerated minimalism with an editorial grid: oversized serif display type, generous
            negative space, hairline rules, square corners, a single accent colour, no decorative
            gradients and no emoji icons.
  palette   Warm monochrome (obsidian in dark mode, paper in light) plus one champagne-gold accent.
            Every text colour below clears WCAG AA (4.5:1) on its card; see check_contrast().
  type      Playfair Display (display), Inter (body), JetBrains Mono (kickers and figures).
  motion    At most one continuous animation per card, transform/opacity only, stopped under
            prefers-reduced-motion.
"""
from xml.sax.saxutils import escape as _esc
import fontkit as fk

THEMES = {
    "dark": dict(
        page="#0d1117",
        card0="#15120F", card1="#0C0B09",
        text="#F4EFE6", text2="#CFC7BA", muted="#9C9285", faint="#3F3A33",
        line="#F4EFE6", line_a=0.12, line_a2=0.22,
        gold="#D4B06A", gold2="#B48A3C", gold_ink="#D4B06A",
        wash="#F4EFE6", wash_a=0.035,
        plate="#0B0A08",
    ),
    "light": dict(
        page="#ffffff",
        card0="#FFFFFF", card1="#F7F4EE",
        text="#15120E", text2="#46403A", muted="#6B635A", faint="#DAD3C8",
        line="#15120E", line_a=0.13, line_a2=0.24,
        gold="#AE8836", gold2="#8A6113", gold_ink="#8A6113",
        wash="#15120E", wash_a=0.03,
        plate="#FFFFFF",
    ),
}
RX = 6  # corner radius of every card

def esc(s):
    return _esc(s, {'"': "&quot;"})

def rgba(hex_, a):
    h = hex_.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{a})"

def luminance(hex_):
    h = hex_.lstrip("#")
    def ch(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(int(h[i:i + 2], 16)) for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(fg, bg):
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)

def check_contrast():
    """Assert the text tokens meet WCAG AA against both card ends of each theme."""
    for name, t in THEMES.items():
        for key, floor in (("text", 7), ("text2", 4.5), ("muted", 4.5), ("gold_ink", 4.5)):
            for bg in (t["card0"], t["card1"]):
                c = contrast(t[key], bg)
                assert c >= floor, f"{name}.{key} on {bg}: {c:.2f} < {floor}"

REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"

def svg_doc(w, h, title, body, css="", defs="", desc=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="t d" fill="none">'
            f'<title id="t">{esc(title)}</title><desc id="d">{esc(desc or title)}</desc>'
            f'<style>{css}{REDUCED}</style><defs>{defs}</defs>{body}</svg>')

def text(x, y, s, fonts, key, size, fill, anchor="start", tracking=0, extra="", lnum=False):
    fam = fonts.use(key, s)
    ls = f' letter-spacing="{tracking}"' if tracking else ""
    ff = ' style="font-feature-settings:&quot;lnum&quot;"' if lnum else ""
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}"{ls}{ff} {extra}>{esc(s)}</text>')

def frame_defs(w, h, t, uid="fr"):
    return (f'<clipPath id="{uid}"><rect width="{w}" height="{h}" rx="{RX}"/></clipPath>'
            f'<linearGradient id="{uid}bg" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{t["card0"]}"/><stop offset="1" stop-color="{t["card1"]}"/></linearGradient>')

def frame_open(w, h, t, uid="fr", mark=True):
    """Card background inside the clip, plus the gold signature tick at the top-left edge."""
    s = f'<g clip-path="url(#{uid})"><rect width="{w}" height="{h}" fill="url(#{uid}bg)"/>'
    if mark:
        s += f'<rect x="36" y="0" width="48" height="2" fill="{t["gold"]}"/>'
    return s

def frame_close(w, h, t):
    return (f'</g><rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{RX-0.5}" '
            f'stroke="{t["line"]}" stroke-opacity="{t["line_a"]}"/>')

def rule(x1, y, x2, t, strong=False):
    a = t["line_a2"] if strong else t["line_a"]
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{t["line"]}" stroke-opacity="{a}"/>'

def vrule(x, y1, y2, t):
    return f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="{t["line"]}" stroke-opacity="{t["line_a"]}"/>'

def kicker(x, y, label, fonts, t, anchor="start", size=11, color=None, dash=True):
    """Tracked mono label in gold, led by a short gold rule. Returns (svg, width)."""
    c = color or t["gold_ink"]
    tw = fk.width(label, "mono5", size, tracking=2.2)
    lead = 18 if dash else 0
    total = lead + tw
    x0 = x if anchor == "start" else x - total
    s = ""
    if dash:
        s += f'<rect x="{x0:.1f}" y="{y - size*0.36:.1f}" width="12" height="1.2" fill="{c}"/>'
    s += text(round(x0 + lead, 1), y, label, fonts, "mono5", size, c, tracking=2.2)
    return s, total

def chip(x, y, label, fonts, t, key="mono", size=11, pad=9, h=24, color=None):
    """Square-cornered tag with a hairline. Returns (svg, width)."""
    w = fk.width(label, key, size) + pad * 2
    c = color or t["text2"]
    s = (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="3" fill="{rgba(t["wash"], t["wash_a"])}" '
         f'stroke="{t["line"]}" stroke-opacity="{t["line_a2"]}"/>'
         + text(round(x + pad, 1), y + h / 2 + size * 0.36, label, fonts, key, size, c))
    return s, w

def gold_chip(x, y, label, fonts, t, size=11, pad=10, h=24):
    w = fk.width(label, "mono5", size, tracking=0.6) + pad * 2
    s = (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="3" fill="{rgba(t["gold"], 0.12)}" '
         f'stroke="{t["gold"]}" stroke-opacity="0.6"/>'
         + text(round(x + pad, 1), y + h / 2 + size * 0.36, label, fonts, "mono5", size, t["gold_ink"], tracking=0.6))
    return s, w

def figure(x, y, num, fonts, t, size=30, anchor="start", fill=None):
    """A large lining figure in the display serif."""
    return text(x, y, num, fonts, "serif6", size, fill or t["text"], anchor=anchor, lnum=True, tracking=-0.5)

def arrow_ne(x, y, s, color, sw=1.5):
    """A small north-east arrow drawn as strokes (no font glyph needed)."""
    return (f'<path d="M{x} {y+s} L{x+s} {y} M{x+s*0.35} {y} L{x+s} {y} L{x+s} {y+s*0.65}" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')

def wrap(s, key, size, maxw):
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fk.width(trial, key, size) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

# Thin-stroke icons on a 24-unit grid; one stroke weight (1.5) across the whole set.
ICONS = {
    "pin":    '<path d="M12 21s-6.2-5.4-6.2-10.2a6.2 6.2 0 0 1 12.4 0C18.2 15.6 12 21 12 21z"/><circle cx="12" cy="10.8" r="2.3"/>',
    "stream": '<rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="M10.2 9.4v5.2l4.4-2.6z"/>',
    "detect": '<path d="M4 8V5h3M17 5h3v3M20 16v3h-3M7 19H4v-3"/><rect x="8.5" y="9" width="7" height="6" rx="1"/>',
    "plate":  '<rect x="2.8" y="7.5" width="18.4" height="9" rx="1.5"/><path d="M6.3 12h2.6M10.6 12h2.8M15.1 12h2.6"/>',
    "bell":   '<path d="M6.2 16.2h11.6l-1.6-2.1V10a4.2 4.2 0 0 0-8.4 0v4.1z"/><path d="M10.4 18.6a1.7 1.7 0 0 0 3.2 0"/>',
    "route":  '<path d="M5.5 18c3.2 0 3-6.1 6.6-6.1S15.3 6 18.5 6"/><circle cx="5.2" cy="18" r="1.9"/><circle cx="18.8" cy="6" r="1.9"/>',
    "mail":   '<rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="M4 7.5l8 5.6 8-5.6"/>',
    "link":   '<path d="M10 14a4 4 0 0 0 5.66 0l3-3a4 4 0 0 0-5.66-5.66l-1.2 1.2"/><path d="M14 10a4 4 0 0 0-5.66 0l-3 3a4 4 0 0 0 5.66 5.66l1.2-1.2"/>',
    "crop":   '<circle cx="12" cy="12" r="6.5"/><path d="M4 8V5h3M17 5h3v3M20 16v3h-3M7 19H4v-3"/>',
    "rules":  '<path d="M5 7h14M5 12h14M5 17h9"/><path d="M17.5 15.5l1.6 1.6 2.9-3"/>',
    "patch":  '<rect x="4" y="4" width="16" height="16" rx="1.5"/><path d="M4 9.3h16M4 14.7h16M9.3 4v16M14.7 4v16"/>',
    "bank":   '<path d="M4 9.5l8-4.5 8 4.5v1H4z"/><path d="M6.5 11v6M11 11v6M15.5 11v6M4 18.5h16"/>',
    "verdict":'<circle cx="12" cy="12" r="8"/><path d="M8.5 12.2l2.4 2.4 4.8-5"/>',
    "camera": '<rect x="3" y="7" width="13" height="10" rx="2"/><path d="M16 10.5l5-2.5v8l-5-2.5z"/>',
    "screen": '<rect x="3" y="5" width="18" height="12" rx="1.5"/><path d="M8 20h8M12 17v3"/>',
    "lock":   '<rect x="5.5" y="10.5" width="13" height="9" rx="1.5"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/>',
}

def icon(name, cx, cy, size, color, sw=1.5):
    s = size / 24
    return (f'<g transform="translate({cx - size/2:.1f} {cy - size/2:.1f}) scale({s:.4f})" stroke="{color}" '
            f'stroke-width="{sw/s:.2f}" stroke-linecap="round" stroke-linejoin="round" fill="none">{ICONS[name]}</g>')

check_contrast()
