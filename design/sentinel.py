import fontkit as fk
from common import THEMES, svg_doc, text, rgba, esc, chip, arrow_ne, wrap, icon

W, H = 900, 468
NODES = [("pin", "Camera registry", "GIS control plane"),
         ("stream", "Stream ingest", "HLS / RTSP"),
         ("detect", "Detect + track", "YOLOX-S on ONNX"),
         ("plate", "Read plates", "PaddleOCR"),
         ("bell", "Watchlist match", "alert + evidence"),
         ("route", "Route rebuild", "one plate, full path")]
FACTS = [("30", "cameras onboarded\nacross 5 departments"),
         ("3", "pipelines off one\nstream pull"),
         ("4 GB", "laptop GPU (GTX 1650)\nruns the whole stack"),
         ("80,000", "cameras the design\nis sized for")]
STACK = ["Python", "FastAPI", "ONNX Runtime", "YOLOX-S", "PaddleOCR", "OpenCV", "React", "Leaflet", "SQLite"]

def build(theme):
    t = THEMES[theme]; F = fk.Fonts(); dark = theme == "dark"
    L, R = 36, W - 36
    defs = f'''
    <clipPath id="fr"><rect width="{W}" height="{H}" rx="22"/></clipPath>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['card0']}"/><stop offset="1" stop-color="{t['card1']}"/></linearGradient>
    <radialGradient id="g1" cx="0.08" cy="0" r="0.6"><stop offset="0" stop-color="{t['orb_a']}" stop-opacity="{0.42 if dark else 0.45}"/><stop offset="1" stop-color="{t['orb_a']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="g2" cx="1" cy="1" r="0.55"><stop offset="0" stop-color="{t['orb_b']}" stop-opacity="{0.28 if dark else 0.5}"/><stop offset="1" stop-color="{t['orb_b']}" stop-opacity="0"/></radialGradient>
    <linearGradient id="flow" x1="95" x2="805" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{t['violet2']}"/><stop offset="0.5" stop-color="{t['indigo']}"/><stop offset="1" stop-color="{t['cyan']}"/></linearGradient>
    <linearGradient id="num" x1="0" x2="1"><stop offset="0" stop-color="{t['grad_b']}"/><stop offset="1" stop-color="{t['grad_c']}"/></linearGradient>
    <radialGradient id="halo"><stop offset="0" stop-color="{t['cyan']}" stop-opacity="0.55"/><stop offset="1" stop-color="{t['cyan']}" stop-opacity="0"/></radialGradient>
    <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="{0.35 if dark else 0.9}"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    '''
    # header
    head = text(L, 58, "NOW BUILDING", F, "mono5", 12, t["cyan"], tracking=2.4)
    badge = "Gujarat Police Innovation Challenge 2026"
    bw = fk.width(badge, "mono", 11) + 20
    c, _ = chip(R - bw, 42, badge, F, t, size=11, pad=10, h=24, color=t["violet2"], tone=0.12)
    head += c
    title_w = fk.width("Sentinel", "display", 40)
    head += text(L - 1, 110, "Sentinel", F, "display", 40, t["text"], tracking=-0.5)
    head += text(L + title_w + 18, 108, "Integrated Video Management & Analytics Platform", F, "sans5", 15.5, t["text2"])
    tag = ("One platform over 26 departments' CCTV systems. Hand it a registration number, "
           "get back that vehicle's complete timestamped route across the whole camera network.")
    for i, ln in enumerate(wrap(tag, "sans", 15, R - L)):
        head += text(L, 144 + i * 23, ln, F, "sans", 15, t["text2"] if dark else t["muted"])
    # pipeline
    y0, x0, step, r = 232, 95, 142, 25
    xs = [x0 + i * step for i in range(len(NODES))]
    pipe = (f'<line x1="{xs[0]}" y1="{y0}" x2="{xs[-1]}" y2="{y0}" stroke="{t["stroke"]}" stroke-opacity="{t["stroke_a"]*1.3:.2f}" stroke-width="2"/>'
            f'<line class="flow" x1="{xs[0]}" y1="{y0}" x2="{xs[-1]}" y2="{y0}" stroke="url(#flow)" stroke-width="2" stroke-dasharray="4 10" stroke-linecap="round"/>')
    run = 5.4; total = 6.6
    for i, (ic, ttl, sub) in enumerate(NODES):
        x = xs[i]; col = [t["violet2"], t["violet"], t["indigo"], t["indigo"], t["cyan"], t["cyan"]][i]
        delay = run * (x - xs[0]) / (xs[-1] - xs[0])
        pipe += (f'<circle cx="{x}" cy="{y0}" r="{r+10}" fill="url(#halo)" class="hal" style="animation-delay:{delay:.2f}s"/>'
                 f'<circle cx="{x}" cy="{y0}" r="{r}" fill="{t["card0"]}" />'
                 f'<circle cx="{x}" cy="{y0}" r="{r}" fill="{rgba(col, 0.12 if dark else 0.08)}" stroke="{rgba(col, 0.55)}" stroke-width="1.4"/>'
                 + icon(ic, x, y0, 22, col, 1.7))
        fs = 13.5
        while fk.width(ttl, "sans6", fs) > step - 12: fs -= 0.5
        pipe += text(x, y0 + r + 26, ttl, F, "sans6", fs, t["text"], anchor="middle")
        pipe += text(x, y0 + r + 44, sub, F, "mono", 11, t["muted"], anchor="middle")
    pipe += (f'<circle r="5" cy="{y0}" fill="{t["cyan"]}"><animate attributeName="cx" values="{xs[0]};{xs[-1]};{xs[-1]}" '
             f'keyTimes="0;{run/total:.3f};1" dur="{total}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{run/total:.3f};{(run+0.3)/total:.3f};1" dur="{total}s" repeatCount="indefinite"/></circle>')
    # facts
    fy, fh, gap = 330, 76, 12
    fw = (R - L - gap * 3) / 4
    facts = ""
    for i, (num, lab) in enumerate(FACTS):
        fx = L + i * (fw + gap)
        facts += (f'<rect x="{fx:.1f}" y="{fy}" width="{fw:.1f}" height="{fh}" rx="14" fill="{rgba(t["glass"], t["glass_a"])}" '
                  f'stroke="{rgba(t["stroke"], t["glass_stroke_a"])}"/>')
        facts += text(round(fx + 16, 1), fy + 34, num, F, "display", 25, "url(#num)")
        lines = lab.split("\n")
        assert all(fk.width(l, "sans", 12.2) <= fw - 28 for l in lines), lab
        for j, ln in enumerate(lines[:2]):
            facts += text(round(fx + 16, 1), fy + 54 + j * 15, ln, F, "sans", 12.2, t["muted"])
    # stack chips + link
    cx_, cy_ = L, 426; chips = ""
    for s in STACK:
        c, w = chip(cx_, cy_, s, F, t, size=11, pad=9, h=24); chips += c; cx_ += w + 6
    link = "View repository"
    lw = fk.width(link, "sans6", 13)
    chips += text(R - 16, cy_ + 16.5, link, F, "sans6", 13, t["violet2"] if dark else t["violet"], anchor="end")
    chips += arrow_ne(R - 10, cy_ + 7, 8, t["violet2"] if dark else t["violet"], 1.8)
    anim = f'''
    .flow{{animation:fl 1.2s linear infinite}} @keyframes fl{{to{{stroke-dashoffset:-14}}}}
    .hal{{opacity:0;animation:hal {total}s ease-out infinite}}
    @keyframes hal{{0%{{opacity:.95}}14%{{opacity:0}}100%{{opacity:0}}}}
    '''
    body = f'''
    <g clip-path="url(#fr)">
      <rect width="{W}" height="{H}" fill="url(#bg)"/>
      <rect width="{W}" height="{H}" fill="url(#g1)"/><rect width="{W}" height="{H}" fill="url(#g2)"/>
      {head}{pipe}{facts}{chips}
      <rect x="40" y="0.5" width="{W-80}" height="1" fill="url(#edge)"/>
    </g>
    <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="21.5" stroke="{t['stroke']}" stroke-opacity="{t['stroke_a']}"/>'''
    return svg_doc(W, H, "Sentinel — Integrated Video Management & Analytics Platform", body, F.css() + anim, defs,
                   desc="Sentinel pipeline: camera registry and GIS, stream ingest, detection and tracking with YOLOX-S on ONNX Runtime, plate reading with PaddleOCR, watchlist match with alerts and evidence, route reconstruction from one plate. 30 cameras across 5 departments; runs on a 4 GB laptop GPU; designed for 80,000 cameras.")
