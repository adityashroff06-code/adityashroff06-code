#!/usr/bin/env python3
"""Regenerate every static SVG in ../assets (dark + light).

    pip install fonttools brotli
    python design/build.py

Text lives in the per-card modules (hero.py, about.py, sentinel.py, projects.py, toolbox.py).
Fonts are subset to the exact glyphs each SVG uses and embedded, so the cards look identical everywhere.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import about, footer, hero, pills, projects, sentinel, toolbox  # noqa: E402

OUT = HERE.parent / "assets"


def main():
    OUT.mkdir(exist_ok=True)
    jobs = {}
    for theme in ("dark", "light"):
        jobs[f"hero-{theme}.svg"] = hero.build(theme)
        jobs[f"about-{theme}.svg"] = about.build(theme)
        jobs[f"sentinel-{theme}.svg"] = sentinel.build(theme)
        jobs[f"toolbox-{theme}.svg"] = toolbox.build(theme)
        jobs[f"footer-{theme}.svg"] = footer.build(theme)
        for p in projects.PROJECTS:
            jobs[f"project-{p['slug']}-{theme}.svg"] = projects.build(p, theme)
        for kind in pills.PILLS:
            jobs[f"pill-{kind}-{theme}.svg"] = pills.build(kind, theme)
    for name, svg in jobs.items():
        (OUT / name).write_text(svg, encoding="utf-8")
    print(f"wrote {len(jobs)} SVGs to {OUT}")


if __name__ == "__main__":
    main()
