import fontkit as fk
from common import THEMES, svg_doc, text, rgba, esc

W, H = 900, 320
ROLES = [
    "computer vision on live CCTV feeds",
    "GenAI + RAG with cited sources",
    "analytics that show their coverage",
    "ANPR on a 4 GB laptop GPU",
]

def typing_timeline(roles, cw, x0, t_type=0.055, hold=2.1, t_del=0.026, gap=0.45):
    """Per-role discrete width events and a combined cursor-x track, all in seconds."""
    per_role, cursor, t = [], [(0.0, x0)], 0.0
    for r in roles:
        n = len(r); ev = [(0.0, 0.0)]
        for k in range(1, n + 1):
            ev.append((t + k * t_type, k * cw)); cursor.append((t + k * t_type, x0 + k * cw))
        t_end_type = t + n * t_type
        t_del0 = t_end_type + hold
        for k in range(1, n + 1):
            ev.append((t_del0 + k * t_del, (n - k) * cw)); cursor.append((t_del0 + k * t_del, x0 + (n - k) * cw))
        t = t_del0 + n * t_del + gap
        per_role.append(ev)
    return per_role, cursor, t

def smil_discrete(attr, events, total):
    ev = sorted(events)
    kt, vals, last = [], [], None
    for time, v in ev:
        k = round(time / total, 5)
        if last is not None and k <= last:
            kt[-1] = f"{k:.5f}"; vals[-1] = f"{v:.2f}"; continue
        kt.append(f"{k:.5f}"); vals.append(f"{v:.2f}"); last = k
    kt[0] = "0"
    return (f'<animate attributeName="{attr}" dur="{total:.3f}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{";".join(kt)}" values="{";".join(vals)}"/>')

def build(theme):
    t = THEMES[theme]; F = fk.Fonts(); dark = theme == "dark"
    cx, cy = 722, 160
    # ---------- defs
    defs = f'''
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="24"/></clipPath>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['bg0']}"/><stop offset="1" stop-color="{t['bg1']}"/></linearGradient>
    <radialGradient id="oa"><stop offset="0" stop-color="{t['orb_a']}" stop-opacity="{t['orb_op']}"/><stop offset="1" stop-color="{t['orb_a']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="ob"><stop offset="0" stop-color="{t['orb_b']}" stop-opacity="{t['orb_op']}"/><stop offset="1" stop-color="{t['orb_b']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="oc"><stop offset="0" stop-color="{t['orb_c']}" stop-opacity="{t['orb_op']*0.9:.2f}"/><stop offset="1" stop-color="{t['orb_c']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="od"><stop offset="0" stop-color="{t['orb_d']}" stop-opacity="{t['orb_op']*0.6:.2f}"/><stop offset="1" stop-color="{t['orb_d']}" stop-opacity="0"/></radialGradient>
    <pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse">
      <path d="M36 0H0V36" stroke="{t['grid']}" stroke-opacity="{t['grid_a']}" stroke-width="1"/></pattern>
    <radialGradient id="gridfade" cx="0.72" cy="0.5" r="0.62">
      <stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
    <mask id="gm"><rect width="{W}" height="{H}" fill="url(#gridfade)"/></mask>
    <linearGradient id="name" x1="56" y1="0" x2="480" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{t['grad_a']}"/><stop offset="0.55" stop-color="{t['grad_b']}"/><stop offset="1" stop-color="{t['grad_c']}"/></linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="{0.45 if dark else 0.9}"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['violet2']}"/><stop offset="1" stop-color="{t['cyan']}"/></linearGradient>
    <linearGradient id="sweep" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{t['cyan']}" stop-opacity="0"/><stop offset="1" stop-color="{t['cyan']}" stop-opacity="{0.35 if dark else 0.22}"/></linearGradient>
    <filter id="grain" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch"/>
      <feColorMatrix values="0 0 0 0 {1 if dark else 0}  0 0 0 0 {1 if dark else 0}  0 0 0 0 {1 if dark else 0}  0 0 0 0.9 0"/></filter>
    <filter id="soft" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
    '''
    # ---------- typing
    cw = fk.width("M", "mono", 19); x_prompt = 58; x_type = 84; y_type = 208
    per_role, cursor, total = typing_timeline(ROLES, cw, x_type)
    for i, ev in enumerate(per_role):
        defs += (f'<clipPath id="tc{i}"><rect x="{x_type}" y="{y_type-20}" width="0" height="28">'
                 f'{smil_discrete("width", ev, total)}</rect></clipPath>')
    typing = text(x_prompt, y_type, ">", F, "mono5", 19, t['violet2'])
    for i, r in enumerate(ROLES):
        typing += text(x_type, y_type, r, F, "mono", 19, t['text2'], extra=f'clip-path="url(#tc{i})"')
    typing += (f'<rect class="blink" x="{x_type}" y="{y_type-17}" width="2.5" height="21" rx="1" fill="{t["cyan"]}">'
               f'{smil_discrete("x", cursor, total)}</rect>')
    # ---------- status pill
    p1, p2, p3 = "Now building ", "Sentinel", " · city-scale CCTV analytics"
    fs = 13.5
    w1, w2, w3 = fk.width(p1, "sans5", fs), fk.width(p2, "sans6", fs), fk.width(p3, "sans5", fs)
    px, py, ph = 56, 238, 34; pw = 40 + w1 + w2 + w3 + 16
    pill = (f'<rect x="{px}" y="{py}" width="{pw:.1f}" height="{ph}" rx="17" fill="{rgba(t["glass"], t["glass_a"] + (0.03 if dark else 0))}" '
            f'stroke="{rgba(t["stroke"], t["glass_stroke_a"])}"/>'
            f'<circle cx="{px+20}" cy="{py+ph/2}" r="4" fill="{t["green"]}"/>'
            f'<circle cx="{px+20}" cy="{py+ph/2}" r="4" fill="none" stroke="{t["green"]}" stroke-width="1.5">'
            f'<animate attributeName="r" values="4;11" dur="2s" repeatCount="indefinite"/>'
            f'<animate attributeName="stroke-opacity" values="0.8;0" dur="2s" repeatCount="indefinite"/></circle>'
            f'<text x="{px+34}" y="{py+ph/2+fs*0.36:.1f}" font-size="{fs}">'
            f'<tspan font-family="{F.use("sans5", p1)}" fill="{t["text2"]}">{esc(p1)}</tspan>'
            f'<tspan font-family="{F.use("sans6", p2)}" fill="{t["text"]}">{esc(p2)}</tspan>'
            f'<tspan font-family="{F.use("sans5", p3)}" fill="{t["text2"]}" xml:space="preserve">{esc(p3)}</tspan></text>')
    # ---------- vision scope motif
    ticks = ""
    for a in range(0, 360, 10):
        import math
        L = 9 if a % 90 == 0 else 4
        r0, r1 = 118, 118 + L
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        ticks += f'<line x1="{cx+r0*ca:.1f}" y1="{cy+r0*sa:.1f}" x2="{cx+r1*ca:.1f}" y2="{cy+r1*sa:.1f}" stroke="{t["text"]}" stroke-opacity="{0.35 if a%90==0 else 0.14}" stroke-width="1"/>'
    wedge_r = 112
    import math
    ex, ey = cx + wedge_r * math.cos(math.radians(-50)), cy + wedge_r * math.sin(math.radians(-50))
    boxes = ""
    for i, (bx, by, bw, bh, lab, col) in enumerate([
            (660, 112, 58, 40, "car 0.94", t["cyan"]), (742, 170, 66, 30, "plate 0.97", t["violet2"]),
            (690, 196, 40, 34, "bus 0.88", t["pink"])]):
        c = 9
        br = (f'M{bx} {by+c}V{by}H{bx+c} M{bx+bw-c} {by}H{bx+bw}V{by+c} M{bx+bw} {by+bh-c}V{by+bh}H{bx+bw-c} '
              f'M{bx+c} {by+bh}H{bx}V{by+bh-c}')
        boxes += (f'<g class="det d{i}"><path d="{br}" stroke="{col}" stroke-width="1.6" stroke-linecap="round"/>'
                  f'<rect x="{bx}" y="{by-15}" width="{fk.width(lab,"mono5",9.5)+10:.1f}" height="13" rx="3" fill="{col}" fill-opacity="{0.9 if dark else 0.95}"/>'
                  + text(bx + 5, by - 5.5, lab, F, "mono5", 9.5, "#0B0B1A" if dark else "#FFFFFF") + '</g>')
    stars = ""
    for i, (sx, sy, sr) in enumerate([(610, 52, 1.4), (850, 70, 1.8), (872, 248, 1.3), (588, 262, 1.6), (820, 292, 1.2),
                                       (640, 300, 1.1), (560, 120, 1.0), (880, 150, 1.2)]):
        stars += f'<circle class="tw w{i%4}" cx="{sx}" cy="{sy}" r="{sr}" fill="{t["text"]}"/>'
    scope = f'''
    <g opacity="{0.95 if dark else 0.9}">
      <circle cx="{cx}" cy="{cy}" r="118" stroke="{t['text']}" stroke-opacity="0.10"/>
      <g class="spin-slow"><circle cx="{cx}" cy="{cy}" r="104" stroke="{t['text']}" stroke-opacity="0.18" stroke-dasharray="2 7"/></g>
      <circle cx="{cx}" cy="{cy}" r="88" stroke="url(#ring)" stroke-opacity="0.55" stroke-width="1.3"/>
      <circle cx="{cx}" cy="{cy}" r="58" stroke="{t['text']}" stroke-opacity="0.10"/>
      <line x1="{cx-128}" y1="{cy}" x2="{cx+128}" y2="{cy}" stroke="{t['text']}" stroke-opacity="0.07"/>
      <line x1="{cx}" y1="{cy-128}" x2="{cx}" y2="{cy+128}" stroke="{t['text']}" stroke-opacity="0.07"/>
      {ticks}
      <g class="sweep"><path d="M{cx} {cy} L{cx+wedge_r} {cy} A{wedge_r} {wedge_r} 0 0 0 {ex:.1f} {ey:.1f} Z" fill="url(#sweep)"/></g>
      {boxes}
      <circle cx="{cx}" cy="{cy}" r="3.2" fill="{t['cyan']}"/>
      <circle cx="{cx}" cy="{cy}" r="3.2" stroke="{t['cyan']}" fill="none"><animate attributeName="r" values="3;16" dur="2.6s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values="0.7;0" dur="2.6s" repeatCount="indefinite"/></circle>
    </g>'''
    anim = f'''
    .orb{{transform-box:fill-box;transform-origin:center;animation:dr 22s ease-in-out infinite alternate}}
    .o2{{animation-duration:27s;animation-name:dr2}} .o3{{animation-duration:31s}} .o4{{animation-duration:19s;animation-name:dr2}}
    @keyframes dr{{0%{{transform:translate(0,0) scale(1)}}50%{{transform:translate(70px,-26px) scale(1.18)}}100%{{transform:translate(-40px,22px) scale(.92)}}}}
    @keyframes dr2{{0%{{transform:translate(0,0) scale(1.05)}}50%{{transform:translate(-80px,18px) scale(.9)}}100%{{transform:translate(30px,-30px) scale(1.15)}}}}
    .spin-slow{{transform-origin:{cx}px {cy}px;animation:rot 60s linear infinite}}
    .sweep{{transform-origin:{cx}px {cy}px;animation:rot 7s linear infinite}}
    @keyframes rot{{to{{transform:rotate(360deg)}}}}
    .blink{{animation:bl 1.05s steps(1) infinite}} @keyframes bl{{50%{{opacity:0}}}}
    .det{{opacity:0;animation:det 7s ease-in-out infinite}} .d1{{animation-delay:2.3s}} .d2{{animation-delay:4.6s}}
    @keyframes det{{0%,100%{{opacity:0}}8%,38%{{opacity:1}}48%{{opacity:0}}}}
    .tw{{animation:tw 3.4s ease-in-out infinite}} .w1{{animation-delay:.8s}} .w2{{animation-delay:1.7s}} .w3{{animation-delay:2.5s}}
    @keyframes tw{{0%,100%{{opacity:.15}}50%{{opacity:.8}}}}
    .rise{{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}} .r2{{animation-delay:.12s}} .r3{{animation-delay:.24s}} .r4{{animation-delay:.36s}}
    @keyframes rise{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
    '''
    eyebrow = text(57, 94, "DIGITAL TRANSFORMATION  ·  AI ENABLEMENT", F, "mono5", 12.5, t["cyan"], tracking=2.6)
    name_txt = "Aditya Shroff"
    name = ""
    if dark:
        name += text(54, 162, name_txt, F, "display", 64, t["violet"], extra='filter="url(#soft)" opacity="0.55"')
    name += text(54, 162, name_txt, F, "display", 64, "url(#name)", tracking=-1)
    body = f'''
    <g clip-path="url(#frame)">
      <rect width="{W}" height="{H}" fill="url(#bg)"/>
      <ellipse class="orb" cx="660" cy="40" rx="280" ry="190" fill="url(#oa)"/>
      <ellipse class="orb o2" cx="880" cy="300" rx="250" ry="170" fill="url(#ob)"/>
      <ellipse class="orb o3" cx="170" cy="330" rx="300" ry="160" fill="url(#oc)"/>
      <ellipse class="orb o4" cx="430" cy="-30" rx="200" ry="120" fill="url(#od)"/>
      <rect width="{W}" height="{H}" fill="url(#grid)" mask="url(#gm)"/>
      <rect width="{W}" height="{H}" filter="url(#grain)" opacity="{0.05 if dark else 0.035}"/>
      {stars}
      {scope}
      <g class="rise">{eyebrow}</g>
      <g class="rise r2">{name}</g>
      <g class="rise r3">{typing}</g>
      <g class="rise r4">{pill}</g>
      <rect x="24" y="0.5" width="{W-48}" height="1" fill="url(#edge)"/>
    </g>
    <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="23.5" stroke="{t['stroke']}" stroke-opacity="{t['stroke_a']}"/>'''
    css = F.css() + anim
    return svg_doc(W, H, "Aditya Shroff — Digital Transformation & AI Enablement Specialist", body, css, defs,
                   desc="Animated banner: Aditya Shroff, building Sentinel, city-scale CCTV analytics. Rotating focus areas: " + "; ".join(ROLES))
