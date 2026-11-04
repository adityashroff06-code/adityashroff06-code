"""Masthead: name, one-line thesis, what is being built now, and a cap-inspection motif."""
import math
import fontkit as fk
from common import THEMES, svg_doc, text, rgba, esc, kicker, wrap, frame_defs, frame_open, frame_close

W, H = 900, 360
EYEBROW = "AI ENABLEMENT  ·  COMPUTER VISION  ·  TORONTO"
NAME = "Aditya Shroff"
THESIS = "Computer vision and GenAI systems, measured on real hardware and shipped with their limits."
NOW = ("Now building ", "Cap Vision", "  ·  closure inspection for a packaging line, Phase 1b")

def motif(t, F, cx, cy, dark):
    """A cap seen from above: rim, induction-seal liner, the patch grid the model scores, one scan band."""
    ink = t["text"]; gold = t["gold"]
    s = f'<clipPath id="liner"><circle cx="{cx}" cy="{cy}" r="72"/></clipPath>'
    body = ""
    # ticks and rings
    for a in range(0, 360, 15):
        L = 8 if a % 90 == 0 else 3
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        body += (f'<line x1="{cx+112*ca:.1f}" y1="{cy+112*sa:.1f}" x2="{cx+(112+L)*ca:.1f}" y2="{cy+(112+L)*sa:.1f}" '
                 f'stroke="{ink}" stroke-opacity="{0.4 if a%90==0 else 0.16}"/>')
    body += f'<circle cx="{cx}" cy="{cy}" r="108" stroke="{ink}" stroke-opacity="0.22"/>'
    body += f'<circle cx="{cx}" cy="{cy}" r="100" stroke="{ink}" stroke-opacity="0.08"/>'
    body += f'<circle cx="{cx}" cy="{cy}" r="74" stroke="{gold}" stroke-opacity="0.9" stroke-width="1.2"/>'
    body += f'<circle cx="{cx}" cy="{cy}" r="60" stroke="{ink}" stroke-opacity="0.08" stroke-dasharray="2 6"/>'
    # patch grid inside the liner
    grid = ""
    step = 16
    for k in range(-5, 6):
        p = k * step
        grid += f'<line x1="{cx+p}" y1="{cy-80}" x2="{cx+p}" y2="{cy+80}" stroke="{ink}" stroke-opacity="0.10"/>'
        grid += f'<line x1="{cx-80}" y1="{cy+p}" x2="{cx+80}" y2="{cy+p}" stroke="{ink}" stroke-opacity="0.10"/>'
    # three patches with a higher score, and the scanning band
    for (i, j, a) in ((1, -2, 0.55), (2, -2, 0.3), (-3, 1, 0.22)):
        grid += (f'<rect x="{cx+i*step}" y="{cy+j*step}" width="{step}" height="{step}" fill="{gold}" '
                 f'fill-opacity="{a}"/>')
    grid += (f'<rect class="scan" x="{cx-80}" y="{cy-86}" width="160" height="14" fill="url(#scanfill)"/>'
             f'<rect class="scan" x="{cx-80}" y="{cy-72}" width="160" height="1" fill="{gold}" fill-opacity="0.9"/>')
    body += f'<g clip-path="url(#liner)">{grid}</g>'
    # verdict tag, bottom right of the cap
    lab = "GOOD  ·  score 0.91  <  threshold 1.71"
    fs = 10.5; tw = fk.width(lab, "mono5", fs, tracking=0.4) + 32
    tx, ty = cx - tw / 2, cy + 124
    body += (f'<rect x="{tx:.1f}" y="{ty}" width="{tw:.1f}" height="24" rx="3" fill="{t["plate"]}" '
             f'stroke="{gold}" stroke-opacity="0.55"/>'
             f'<circle cx="{tx+13:.1f}" cy="{ty+12}" r="3" fill="{gold}"/>'
             + text(round(tx + 23, 1), ty + 12 + fs * 0.36, lab, F, "mono5", fs, t["gold_ink"], tracking=0.4))
    # frame label, top left of the cap
    body += text(cx - 112, cy - 126, "cap_vision  ·  512 px  ·  top-down", F, "mono", 10.5, t["muted"], tracking=0.4)
    return s, body

def build(theme):
    t = THEMES[theme]; F = fk.Fonts(); dark = theme == "dark"
    cx, cy = 724, 182
    defs = frame_defs(W, H, t)
    defs += (f'<linearGradient id="scanfill" x1="0" y1="0" x2="0" y2="1">'
             f'<stop offset="0" stop-color="{t["gold"]}" stop-opacity="0"/>'
             f'<stop offset="1" stop-color="{t["gold"]}" stop-opacity="{0.45 if dark else 0.35}"/></linearGradient>')
    mdefs, mbody = motif(t, F, cx, cy, dark)
    defs += mdefs
    # ---------- type
    L = 56
    eyebrow, _ = kicker(L, 86, EYEBROW, F, t)
    name = text(L - 3, 178, NAME, F, "serif", 80, t["text"], tracking=-1.6)
    assert fk.width(NAME, "serif", 80, -1.6) < 560
    thesis = ""
    for i, ln in enumerate(wrap(THESIS, "serifi", 21, 500)):
        thesis += text(L, 220 + i * 30, ln, F, "serifi", 21, t["text2"])
    # ---------- now line
    fs = 13.5; ny = 300
    p1, p2, p3 = NOW
    now = (f'<circle cx="{L+5}" cy="{ny-4.5}" r="4" fill="{t["gold"]}"/>'
           f'<circle class="pulse" cx="{L+5}" cy="{ny-4.5}" r="4" stroke="{t["gold"]}" stroke-width="1.2"/>'
           f'<text x="{L+20}" y="{ny}" font-size="{fs}">'
           f'<tspan font-family="{F.use("sans5", p1)}" fill="{t["text2"]}">{esc(p1)}</tspan>'
           f'<tspan font-family="{F.use("sans6", p2)}" fill="{t["text"]}">{esc(p2)}</tspan>'
           f'<tspan font-family="{F.use("sans", p3)}" fill="{t["muted"]}" xml:space="preserve">{esc(p3)}</tspan></text>')
    anim = f'''
    .scan{{animation:scan 7s cubic-bezier(.45,0,.55,1) infinite alternate}}
    @keyframes scan{{from{{transform:translateY(0)}}to{{transform:translateY(144px)}}}}
    .pulse{{transform-box:fill-box;transform-origin:center;animation:pulse 2.4s ease-out infinite}}
    @keyframes pulse{{0%{{transform:scale(1);opacity:.9}}100%{{transform:scale(3.2);opacity:0}}}}
    .rise{{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}} .r2{{animation-delay:.1s}} .r3{{animation-delay:.2s}} .r4{{animation-delay:.3s}}
    @keyframes rise{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
    '''
    body = frame_open(W, H, t)
    body += f'<g opacity="{0.95 if dark else 0.9}">{mbody}</g>'
    body += (f'<g class="rise">{eyebrow}</g><g class="rise r2">{name}</g>'
             f'<g class="rise r3">{thesis}</g><g class="rise r4">{now}</g>')
    body += frame_close(W, H, t)
    return svg_doc(W, H, "Aditya Shroff — AI enablement and computer vision, Toronto", body, F.css() + anim, defs,
                   desc=f"Masthead. Aditya Shroff. {THESIS} {''.join(NOW)}. Motif: a cap seen from above with the patch grid the inspection model scores.")
