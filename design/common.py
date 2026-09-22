"""Shared design tokens and SVG helpers for the Aurora Glass profile."""
from xml.sax.saxutils import escape as _esc
import fontkit as fk

THEMES = {
    "dark": dict(
        page="#0d1117", bg0="#090A18", bg1="#15123B",
        card0="#0D0F24", card1="#121036", stroke="#FFFFFF", stroke_a=0.09, hi_a=0.22,
        glass="#FFFFFF", glass_a=0.045, glass_stroke_a=0.10,
        text="#EEF0FF", text2="#B6BBD8", muted="#8288AD", faint="#454A70",
        violet="#8B5CF6", violet2="#A78BFA", indigo="#818CF8", cyan="#22D3EE", teal="#2DD4BF",
        pink="#F472B6", amber="#FBBF24", green="#34D399",
        grad_a="#FFFFFF", grad_b="#C4B5FD", grad_c="#67E8F9",
        orb_a="#7C3AED", orb_b="#0891B2", orb_c="#4F46E5", orb_d="#BE185D", orb_op=0.75,
        grid="#FFFFFF", grid_a=0.055,
        code_bg="#0A0C1E", kw="#C4A7FF", cls="#67E8F9", str="#86EFAC", com="#6C7299",
        punc="#9EA4C8", num="#F9A8D4", fn="#93C5FD", attr="#F0ABFC", dots=("#FF5F57", "#FEBC2E", "#28C840"),
        shadow="#000000", shadow_a=0.0,
    ),
    "light": dict(
        page="#ffffff", bg0="#FCFBFF", bg1="#EEF0FF",
        card0="#FFFFFF", card1="#F6F4FF", stroke="#4C1D95", stroke_a=0.13, hi_a=0.9,
        glass="#FFFFFF", glass_a=0.75, glass_stroke_a=0.16,
        text="#15132E", text2="#454A6B", muted="#686E91", faint="#C3C6DB",
        violet="#7C3AED", violet2="#6D28D9", indigo="#4F46E5", cyan="#0E7490", teal="#0F766E",
        pink="#BE185D", amber="#B45309", green="#047857",
        grad_a="#1E1B4B", grad_b="#6D28D9", grad_c="#0E7490",
        orb_a="#C4B5FD", orb_b="#99F6E4", orb_c="#C7D2FE", orb_d="#FBCFE8", orb_op=0.95,
        grid="#312E81", grid_a=0.07,
        code_bg="#FFFFFF", kw="#7C3AED", cls="#0E7490", str="#15803D", com="#8B90AE",
        punc="#4B5070", num="#BE185D", fn="#1D4ED8", attr="#A21CAF", dots=("#FF5F57", "#FEBC2E", "#28C840"),
        shadow="#312E81", shadow_a=0.10,
    ),
}

def esc(s):
    return _esc(s, {'"': "&quot;"})

def rgba(hex_, a):
    h = hex_.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{a})"

REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"

def svg_doc(w, h, title, body, css="", defs="", desc=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img" aria-labelledby="t d" fill="none">'
            f'<title id="t">{esc(title)}</title><desc id="d">{esc(desc or title)}</desc>'
            f'<style>{css}{REDUCED}</style><defs>{defs}</defs>{body}</svg>')

def text(x, y, s, fonts, key, size, fill, anchor="start", tracking=0, extra=""):
    fam = fonts.use(key, s)
    ls = f' letter-spacing="{tracking}"' if tracking else ""
    return (f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}"{ls} {extra}>{esc(s)}</text>')

def glass_card(x, y, w, h, r, t, fill_id=None, extra=""):
    """A frosted card: translucent fill, hairline border and a bright top edge."""
    fill = f"url(#{fill_id})" if fill_id else rgba(t["glass"], t["glass_a"])
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" '
            f'stroke="{rgba(t["stroke"], t["glass_stroke_a"])}" {extra}/>')

def chip(x, y, label, fonts, t, key="mono", size=11.5, pad=9, h=24, color=None, tone=0.10):
    """Pill with text; returns (svg, width)."""
    w = fk.width(label, key, size) + pad * 2
    c = color or t["text2"]
    base = t["violet"] if color is None else color
    s = (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{rgba(base, tone)}" '
         f'stroke="{rgba(base, 0.28)}"/>' +
         text(round(x + pad, 1), y + h / 2 + size * 0.36, label, fonts, key, size, c))
    return s, w

def arrow_ne(x, y, s, color, sw=1.8):
    """A small north-east arrow drawn as strokes (no font glyph needed)."""
    return (f'<path d="M{x} {y+s} L{x+s} {y} M{x+s*0.35} {y} L{x+s} {y} L{x+s} {y+s*0.65}" '
            f'stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"/>')

def arrow_r(x, y, s, color, sw=1.8):
    return (f'<path d="M{x} {y} L{x+s} {y} M{x+s*0.6} {y-s*0.4} L{x+s} {y} L{x+s*0.6} {y+s*0.4}" '
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

ICONS = {
    "pin":    '<path d="M12 21s-6.2-5.4-6.2-10.2a6.2 6.2 0 0 1 12.4 0C18.2 15.6 12 21 12 21z"/><circle cx="12" cy="10.8" r="2.3"/>',
    "stream": '<rect x="3" y="5.5" width="18" height="13" rx="3"/><path d="M10.2 9.4v5.2l4.4-2.6z"/>',
    "detect": '<path d="M4 8V5h3M17 5h3v3M20 16v3h-3M7 19H4v-3"/><rect x="8.5" y="9" width="7" height="6" rx="1.2"/>',
    "plate":  '<rect x="2.8" y="7.5" width="18.4" height="9" rx="2"/><path d="M6.3 12h2.6M10.6 12h2.8M15.1 12h2.6"/>',
    "bell":   '<path d="M6.2 16.2h11.6l-1.6-2.1V10a4.2 4.2 0 0 0-8.4 0v4.1z"/><path d="M10.4 18.6a1.7 1.7 0 0 0 3.2 0"/>',
    "route":  '<path d="M5.5 18c3.2 0 3-6.1 6.6-6.1S15.3 6 18.5 6"/><circle cx="5.2" cy="18" r="1.9"/><circle cx="18.8" cy="6" r="1.9"/>',
    "mail":   '<rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="M4 7.5l8 5.6 8-5.6"/>',
    "link":   '<path d="M10 14a4 4 0 0 0 5.66 0l3-3a4 4 0 0 0-5.66-5.66l-1.2 1.2"/><path d="M14 10a4 4 0 0 0-5.66 0l-3 3a4 4 0 0 0 5.66 5.66l1.2-1.2"/>',
}

def icon(name, cx, cy, size, color, sw=1.7):
    s = size / 24
    return (f'<g transform="translate({cx - size/2:.1f} {cy - size/2:.1f}) scale({s:.4f})" stroke="{color}" '
            f'stroke-width="{sw/s:.2f}" stroke-linecap="round" stroke-linejoin="round" fill="none">{ICONS[name]}</g>')
