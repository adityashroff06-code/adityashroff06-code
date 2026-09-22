import fontkit as fk
from common import THEMES, svg_doc, text, rgba

W, H = 900, 150

def wave(y, amp, length, phase):
    d = f"M{-length} {y}"
    x = -length
    while x < W + length:
        d += f" q{length/4} {-amp} {length/2} 0 t{length/2} 0"
        x += length
    return d + f" V{H} H{-length} Z"

def build(theme):
    t = THEMES[theme]; F = fk.Fonts(); dark = theme == "dark"
    defs = f'''
    <linearGradient id="w1" x1="0" x2="1"><stop offset="0" stop-color="{t['orb_a']}"/><stop offset="1" stop-color="{t['orb_b']}"/></linearGradient>
    <linearGradient id="w2" x1="0" x2="1"><stop offset="0" stop-color="{t['orb_c']}"/><stop offset="1" stop-color="{t['orb_d']}"/></linearGradient>
    <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.35" stop-color="#fff" stop-opacity="1"/></linearGradient>
    <mask id="m"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
    <clipPath id="fr"><rect width="{W}" height="{H}" rx="0"/></clipPath>'''
    body = f'''
    <g mask="url(#m)" clip-path="url(#fr)">
      <path class="wv a" d="{wave(92, 22, 300, 0)}" fill="url(#w1)" fill-opacity="{0.38 if dark else 0.45}"/>
      <path class="wv b" d="{wave(104, 18, 420, 0)}" fill="url(#w2)" fill-opacity="{0.30 if dark else 0.40}"/>
      <path class="wv c" d="{wave(118, 14, 240, 0)}" fill="url(#w1)" fill-opacity="{0.22 if dark else 0.30}"/>
    </g>
    {text(W/2, 44, "Thanks for stopping by.", F, "display6", 20, t['text'], anchor='middle')}
    {text(W/2, 68, "Designed in SVG · stats and snake refreshed daily by GitHub Actions", F, "mono", 11.5, t['muted'], anchor='middle')}'''
    anim = '''
    .wv{animation:sl 14s linear infinite} .b{animation-duration:21s;animation-direction:reverse} .c{animation-duration:10s}
    .a{--d:300px} @keyframes sl{from{transform:translateX(0)}to{transform:translateX(300px)}}
    .b{animation-name:sl2} @keyframes sl2{from{transform:translateX(0)}to{transform:translateX(420px)}}
    .c{animation-name:sl3} @keyframes sl3{from{transform:translateX(0)}to{transform:translateX(240px)}}
    '''
    return svg_doc(W, H, "Thanks for stopping by", body, F.css() + anim, defs)
