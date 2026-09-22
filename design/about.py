import re
import fontkit as fk
from common import THEMES, svg_doc, text, rgba, esc

W = 900
CODE = [
    'class Aditya:',
    '    """Digital Transformation & AI Enablement Specialist."""',
    '',
    '    focus    = ["computer vision", "GenAI + RAG", "data engineering"]',
    '    building = "Sentinel: live ANPR and vehicle routes over city CCTV"',
    '    projects = ["EMS Co-Pilot", "GenAI Video Briefing", "Clean Air OS"]',
    '    habits   = ["tested, CI-checked code", "docs that state their limits"]',
    '',
    '    def reach_out(self) -> dict:',
    '        return {"linkedin": "in/aditya-shroff-8033a31b0",',
    '                "email": "adityashroff06@gmail.com"}',
]
KW = {"class", "def", "return", "self"}

def tokens(line):
    """Tiny Python highlighter for this snippet: yields (text, role)."""
    if line.strip().startswith('"""'):
        i = len(line) - len(line.lstrip())
        return [(line[:i], "punc"), (line[i:], "com")]
    out, pos = [], 0
    for m in re.finditer(r'("[^"]*")|([A-Za-z_]\w*)|(\s+)|([^\w\s"])', line):
        s = m.group(0)
        if m.group(1): role = "str"
        elif m.group(2):
            if s in KW: role = "attr" if s == "self" else "kw"
            elif s == "Aditya" or s == "dict": role = "cls"
            elif s == "reach_out": role = "fn"
            else: role = "text"
        elif m.group(3): role = "ws"
        else: role = "punc"
        out.append((s, role))
    return out

def build(theme):
    t = THEMES[theme]; F = fk.Fonts(); dark = theme == "dark"
    fs, lh = 14.5, 25
    top = 44; pad_b = 22
    H = top + 14 + lh * len(CODE) + pad_b
    colors = dict(kw=t["kw"], cls=t["cls"], str=t["str"], com=t["com"], punc=t["punc"], text=t["text"],
                  fn=t["fn"], attr=t["attr"], ws=t["text"])
    cw = fk.width("M", "mono", fs)
    lines = ""
    for i, ln in enumerate(CODE):
        y = top + 14 + lh * (i + 0.72)
        num = text(34, round(y, 1), str(i + 1), F, "mono", 12.5, t["faint"] if dark else "#B0B4CC", anchor="end")
        spans = ""
        for s, role in tokens(ln):
            if role == "ws":
                spans += s; F.use("mono", " "); continue
            key = "mono5" if role in ("kw", "cls", "fn") else "mono"
            spans += f'<tspan font-family="{F.use(key, s)}" fill="{colors[role]}">{esc(s)}</tspan>'
        lines += (f'<g class="ln" style="animation-delay:{0.15 + i*0.07:.2f}s">{num}'
                  f'<text x="52" y="{y:.1f}" font-size="{fs}" font-family="{F.use("mono", " ")}" xml:space="preserve" style="white-space:pre">{spans}</text></g>')
    mini = ""
    for i, ln in enumerate(CODE):
        x = W - 92; y = top + 18 + i * 7
        for tok, role in tokens(ln):
            wlen = len(tok) * 0.9
            if role != "ws" and tok.strip():
                mini += f'<rect x="{x:.1f}" y="{y}" width="{wlen:.1f}" height="3" rx="1" fill="{colors[role]}" fill-opacity="{0.55 if dark else 0.5}"/>'
            x += wlen
    mini = f'<g opacity="0.9">{mini}</g><rect x="{W-100}" y="{top+10}" width="84" height="{len(CODE)*7+14}" rx="6" fill="{rgba(t["stroke"], 0.03)}" stroke="{t["stroke"]}" stroke-opacity="{t["stroke_a"]*0.7:.3f}"/>'
    # caret after the final line
    last = CODE[-1]; cx = 52 + cw * len(last) + 3; cy = top + 14 + lh * (len(CODE) - 1) + 5
    caret = f'<rect class="blink" x="{cx:.1f}" y="{cy:.1f}" width="8.5" height="17" rx="1.5" fill="{t["cyan"]}" fill-opacity="0.85"/>'
    tab_label = "aditya.py"
    defs = f'''
    <clipPath id="fr"><rect width="{W}" height="{H}" rx="18"/></clipPath>
    <linearGradient id="win" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{t['code_bg'] if not dark else '#0E1030'}"/><stop offset="1" stop-color="{t['code_bg']}"/></linearGradient>
    <radialGradient id="glow" cx="0.92" cy="0.05" r="0.55">
      <stop offset="0" stop-color="{t['orb_a']}" stop-opacity="{0.35 if dark else 0.28}"/><stop offset="1" stop-color="{t['orb_a']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="glow2" cx="0.05" cy="1" r="0.5">
      <stop offset="0" stop-color="{t['orb_b']}" stop-opacity="{0.18 if dark else 0.3}"/><stop offset="1" stop-color="{t['orb_b']}" stop-opacity="0"/></radialGradient>
    <linearGradient id="tabline" x1="0" x2="1"><stop offset="0" stop-color="{t['violet2']}"/><stop offset="1" stop-color="{t['cyan']}"/></linearGradient>
    '''
    tab_w = fk.width(tab_label, "mono5", 12.5) + 44
    chrome = f'''
      <rect width="{W}" height="44" fill="{rgba(t['stroke'], 0.035 if dark else 0.025)}"/>
      <line x1="0" y1="44" x2="{W}" y2="44" stroke="{t['stroke']}" stroke-opacity="{t['stroke_a']}"/>
      <circle cx="24" cy="22" r="6" fill="{t['dots'][0]}" fill-opacity="0.85"/><circle cx="44" cy="22" r="6" fill="{t['dots'][1]}" fill-opacity="0.85"/><circle cx="64" cy="22" r="6" fill="{t['dots'][2]}" fill-opacity="0.85"/>
      <rect x="92" y="8" width="{tab_w:.1f}" height="36" rx="8" fill="{rgba(t['stroke'], 0.06 if dark else 0.035)}"/>
      <rect x="92" y="42" width="{tab_w:.1f}" height="2" fill="url(#tabline)"/>
      <path d="M106 18h8l4 4v10h-12z" stroke="{t['violet2']}" stroke-width="1.4" stroke-linejoin="round"/>
      {text(126, 30.5, tab_label, F, "mono5", 12.5, t['text'])}
      {text(W-24, 30, "about.me", F, "mono", 12, t['muted'], anchor="end")}
    '''
    anim = '''
    .ln{opacity:0;animation:ln .6s cubic-bezier(.2,.7,.2,1) forwards}
    @keyframes ln{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}
    .blink{animation:bl 1.1s steps(1) infinite 1.2s} @keyframes bl{50%{opacity:0}}
    '''
    body = f'''
    <g clip-path="url(#fr)">
      <rect width="{W}" height="{H}" fill="url(#win)"/>
      <rect width="{W}" height="{H}" fill="url(#glow)"/><rect width="{W}" height="{H}" fill="url(#glow2)"/>
      {chrome}
      <rect x="44" y="45" width="1" height="{H-45}" fill="{t['stroke']}" fill-opacity="{t['stroke_a']*0.8:.3f}"/>
      {mini}{lines}{caret}
    </g>
    <rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="17.5" stroke="{t['stroke']}" stroke-opacity="{t['stroke_a']}"/>'''
    return svg_doc(W, H, "About Aditya", body, F.css() + anim, defs,
                   desc="Code-style card: Digital Transformation & AI Enablement Specialist. Focus: computer vision, GenAI + RAG, data engineering. Building Sentinel. Projects: EMS Co-Pilot, GenAI Video Briefing, Clean Air OS.")
