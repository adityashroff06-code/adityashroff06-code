"""The two large case-study cards: the build in progress (Cap Vision) and the shipped flagship (Sentinel)."""
import fontkit as fk
from common import (THEMES, svg_doc, text, rgba, kicker, chip, gold_chip, figure, arrow_ne, wrap, rule, icon,
                    frame_defs, frame_open, frame_close)

W, H = 900, 500
CASES = {
    "capvision": dict(
        kicker="NOW BUILDING  ·  PHASE 1B", badge="PRIVATE BUILD  ·  v0.1.2",
        title="Cap Vision", subtitle="Cap and closure inspection for a packaging line",
        lead=("Good-only anomaly detection in the PatchCore family. About 120 photographs of good caps define "
              "normal, a frozen WideResNet-50-2 turns each cap into patch features, and classical CV adds twelve "
              "explainable rule checks with reason codes. Nothing is trained by gradient descent."),
        nodes=[("crop", "Find and crop", "Hough + RANSAC ellipse"),
               ("rules", "Rule checks", "12 checks, reason codes"),
               ("patch", "Patch features", "frozen WideResNet-50-2"),
               ("bank", "Memory bank", "coreset of good caps only"),
               ("verdict", "Verdict", "score against threshold")],
        facts=[("52 / 52", "defects caught on the\n170 real photographs"),
               ("9.3 %", "good caps rejected\nat that threshold"),
               ("~120", "good photos are enough;\nno gradient training"),
               ("100 ms", "per cap, one at a time,\non the laptop GPU")],
        stack=["Python", "PyTorch", "OpenCV", "WideResNet-50-2", "PatchCore", "pytest"],
        tail="Next: camera, operator screen, shadow mode", link=None,
        desc_extra="Phase 1a, the offline pipeline, is done; Phase 1b adds the camera and the operator screen.",
    ),
    "sentinel": dict(
        kicker="SHIPPED  ·  GUJARAT POLICE INNOVATION CHALLENGE 2026", badge="SEPTEMBER 2026",
        title="Sentinel", subtitle="Integrated video management and analytics",
        lead=("One platform over 26 departments' CCTV systems without changing any of them: a single camera "
              "registry with GIS, continuous ANPR and video analytics, watchlist alerts, and a vehicle's complete "
              "timestamped route from one registration number. Video becomes permanent only where a logged "
              "watchlist match justifies it."),
        nodes=[("pin", "Camera registry", "GIS control plane"),
               ("stream", "Stream ingest", "RTSP / HLS"),
               ("detect", "Detect and track", "YOLOX-S on ONNX Runtime"),
               ("plate", "Read plates", "PaddleOCR"),
               ("bell", "Watchlist match", "alert and evidence"),
               ("route", "Route rebuild", "one plate, full path")],
        facts=[("58", "cameras onboarded\nacross 5 departments"),
               ("119 MiB", "peak GPU memory,\nYOLOX-S on a GTX 1650"),
               ("0", "restarts in the measured\nlive window"),
               ("80,000", "cameras the design\nis sized for")],
        stack=["Python", "FastAPI", "ONNX Runtime", "YOLOX-S", "PaddleOCR", "OpenCV", "React", "Leaflet", "SQLite"],
        tail=None, link="View repository",
        desc_extra="Measured on the live government sandbox feed on one laptop.",
    ),
}

def build(slug, theme):
    c = CASES[slug]; t = THEMES[theme]; F = fk.Fonts(); dark = theme == "dark"
    L, R = 56, W - 56
    defs = frame_defs(W, H, t)
    # header
    head, _ = kicker(L, 58, c["kicker"], F, t)
    bc, bw = gold_chip(0, 44, c["badge"], F, t)
    head += gold_chip(R - bw, 44, c["badge"], F, t)[0]
    tw = fk.width(c["title"], "serif6", 44, -0.8)
    head += text(L - 2, 118, c["title"], F, "serif6", 44, t["text"], tracking=-0.8)
    head += text(round(L + tw + 18, 1), 116, c["subtitle"], F, "serifi", 17, t["muted"])
    assert L + tw + 18 + fk.width(c["subtitle"], "serifi", 17) <= R
    lead = wrap(c["lead"], "sans", 14.5, R - L)
    assert len(lead) <= 3, (slug, lead)
    for i, ln in enumerate(lead):
        head += text(L, 150 + i * 22, ln, F, "sans", 14.5, t["text2"])
    # pipeline
    y0 = 266; n = len(c["nodes"]); r = 23
    span = R - L - 2 * 70
    xs = [L + 70 + i * span / (n - 1) for i in range(n)]
    pipe = rule(xs[0], y0, xs[-1], t, strong=True)
    run, total = 5.0, 6.4
    for i, (ic, ttl, sub) in enumerate(c["nodes"]):
        x = xs[i]
        pipe += (f'<circle cx="{x:.1f}" cy="{y0}" r="{r}" fill="{t["plate"]}" stroke="{t["line"]}" stroke-opacity="{t["line_a2"]}"/>'
                 + icon(ic, x, y0, 20, t["gold"]))
        fs = 13
        while fk.width(ttl, "sans6", fs) > span / (n - 1) - 8: fs -= 0.5
        pipe += text(round(x, 1), y0 + r + 24, ttl, F, "sans6", fs, t["text"], anchor="middle")
        pipe += text(round(x, 1), y0 + r + 41, sub, F, "mono", 10.5, t["muted"], anchor="middle")
    pipe += (f'<circle r="4" cy="{y0}" fill="{t["gold"]}"><animate attributeName="cx" values="{xs[0]:.1f};{xs[-1]:.1f};{xs[-1]:.1f}" '
             f'keyTimes="0;{run/total:.3f};1" dur="{total}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{run/total:.3f};{(run+0.3)/total:.3f};1" dur="{total}s" repeatCount="indefinite"/></circle>')
    # facts
    fy, fh, gap = 356, 76, 14
    fw = (R - L - gap * 3) / 4
    facts = ""
    for i, (num, lab) in enumerate(c["facts"]):
        fx = L + i * (fw + gap)
        facts += (f'<rect x="{fx:.1f}" y="{fy}" width="{fw:.1f}" height="{fh}" rx="3" fill="{rgba(t["wash"], t["wash_a"])}" '
                  f'stroke="{t["line"]}" stroke-opacity="{t["line_a"]}"/>')
        facts += figure(round(fx + 16, 1), fy + 34, num, F, t, size=26)
        for j, ln in enumerate(lab.split("\n")[:2]):
            assert fk.width(ln, "sans", 11.8) <= fw - 28, ln
            facts += text(round(fx + 16, 1), fy + 52 + j * 15, ln, F, "sans", 11.8, t["muted"])
    # stack + tail
    cx, cy = L, 456; chips = ""
    for s in c["stack"]:
        k, w = chip(cx, cy, s, F, t, size=10.5, pad=8, h=24); chips += k; cx += w + 6
    if c["link"]:
        chips += text(R - 16, cy + 16.5, c["link"], F, "sans6", 13, t["gold_ink"], anchor="end")
        chips += arrow_ne(R - 10, cy + 7, 8, t["gold_ink"])
    if c["tail"]:
        assert cx + 24 + fk.width(c["tail"], "mono", 10.5) <= R, c["tail"]
        chips += text(R, cy + 16, c["tail"], F, "mono", 10.5, t["muted"], anchor="end")
    body = frame_open(W, H, t) + head + pipe + facts + chips + frame_close(W, H, t)
    desc = (f'{c["title"]}: {c["subtitle"]}. {c["lead"]} Pipeline: ' + ", ".join(n[1] for n in c["nodes"]) + ". "
            + " ".join(f'{n} {l.replace(chr(10), " ")}.' for n, l in c["facts"]) + " " + c["desc_extra"])
    return svg_doc(W, H, f'{c["title"]} — {c["subtitle"]}', body, F.css(), defs, desc=desc)
