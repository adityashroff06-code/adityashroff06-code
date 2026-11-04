#!/usr/bin/env python3
"""Write ../README.md. Image URLs are absolute so dark/light <picture> sources resolve on the profile page."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import index  # noqa: E402

USER = "adityashroff06-code"
RAW = f"https://raw.githubusercontent.com/{USER}/{USER}/main/assets"
OUT = f"https://raw.githubusercontent.com/{USER}/{USER}/output"
GH = f"https://github.com/{USER}"


def pic(dark, light, alt, width=None, height=None, indent=""):
    size = f' width="{width}"' if width else (f' height="{height}"' if height else "")
    return (f'{indent}<picture>\n'
            f'{indent}  <source media="(prefers-color-scheme: dark)" srcset="{dark}">\n'
            f'{indent}  <img alt="{alt}" src="{light}"{size}>\n'
            f'{indent}</picture>')


def asset(name, alt, **kw):
    return pic(f"{RAW}/{name}-dark.svg", f"{RAW}/{name}-light.svg", alt, **kw)


def compact(markup):
    # No whitespace inside <a>: GitHub would underline it next to the image.
    return "".join(line.strip() for line in markup.splitlines())


def linked(url, name, alt, **kw):
    return f'<a href="{url}">{compact(asset(name, alt, **kw))}</a>'


PROJECTS = [
    ("EMS-Co-Pilot-", "project-ems", "EMS Co-Pilot: plant energy readings in, traceable energy and carbon reports out. 175,200 duplicate rows caught before reporting."),
    ("YT-Summarizer---Gen-AI-Console", "project-briefing", "GenAI Video Briefing Console: a spoken YouTube video in, a four-part executive brief out."),
    ("Clean_Air_OS", "project-cleanair", "Clean Air OS: an inspectable PM2.5 research baseline for Delhi-area stations, 9,992 validated observations from 9 stations."),
    ("Consumer-Segmentation-and-Purchase-Behavior-Analysis", "project-segmentation", "Consumer Segmentation: K-Means segments of bath-soap households, then three classifiers compared."),
]
# The live cards need .github/workflows/refresh-stats.yml in place (it builds them on the `output` branch).
LIVE_STATS = (HERE.parent / ".github" / "workflows" / "refresh-stats.yml").exists()


def block(inner, align=None):
    a = f' align="{align}"' if align else ""
    return f"<p{a}>\n{inner}\n</p>"


def build():
    rows = []
    for i in range(0, len(PROJECTS), 2):
        cells = "\n".join(linked(f"{GH}/{repo}", name, alt, width="49%") for repo, name, alt in PROJECTS[i:i + 2])
        rows.append(block(cells, "center"))
    archive = []
    for r in index.ROWS:
        alt = f'{r["title"]}: {r["desc"]}' + ("" if r["url"] else " (private repository)")
        img = linked(r["url"], f'row-{r["slug"]}', alt, width="100%") if r["url"] else compact(asset(f'row-{r["slug"]}', alt, width="100%"))
        archive.append(img)

    parts = [
        block(asset("hero", "Aditya Shroff. Computer vision and GenAI systems, measured on real hardware and shipped with their limits. Now building Cap Vision, closure inspection for a packaging line, Phase 1b.", width="100%")),
        block(linked("https://www.linkedin.com/in/aditya-shroff-8033a31b0/", "pill-linkedin", "Connect on LinkedIn", height="44")
              + "\n&nbsp;\n"
              + linked("mailto:adityashroff06@gmail.com", "pill-email", "Email adityashroff06@gmail.com", height="44"), "center"),
        block(asset("about", "Statement: I put data and AI to work where the result has to be defended. Every build ships with its evaluation, its limits and its reason codes. Focus: computer vision, GenAI and RAG, data pipelines. Based in Toronto, Canada.", width="100%")),
        "<br>",
        block(asset("case-capvision", "Now building: Cap Vision, cap and closure inspection for a packaging line. Good-only anomaly detection in the PatchCore family with explainable rule checks. 52 of 52 defects caught on 170 real photographs with 9.3 percent of good caps rejected; about 120 good photos are enough; 100 ms per cap on the laptop GPU. Phase 1b adds the camera and the operator screen. Private build.", width="100%")),
        block(linked(f"{GH}/sentinel-gujarat", "case-sentinel", "Shipped: Sentinel, integrated video management and analytics for the Gujarat Police Innovation Challenge 2026. One platform over 26 departments' CCTV; a vehicle's complete route from one registration number. 58 cameras across 5 departments, 119 MiB peak GPU memory on a GTX 1650, zero restarts in the measured window, designed for 80,000 cameras.", width="100%")),
        f'<p align="right"><sub>Hackathon submission as entered: <a href="{GH}/Sentinel_Repo"><code>Sentinel_Repo</code></a> &nbsp;·&nbsp; final structured build: <a href="{GH}/sentinel-gujarat"><code>sentinel-gujarat</code></a></sub></p>',
        "<br>",
        block(asset("section-work", "Selected work: four builds, each with its number", width="100%")),
        *rows,
        "<br>",
        block(asset("section-archive", "Archive: further repositories", width="100%")),
        block("\n".join(archive)),
        "<br>",
        block(asset("toolbox", "Toolbox: computer vision, GenAI and NLP, data and ML, engineering", width="100%")),
        *(["<br>",
        block(asset("section-pulse", "Activity: rebuilt every day by GitHub Actions", width="100%")),
        block(pic(f"{OUT}/stats-dark.svg", f"{OUT}/stats-light.svg", "GitHub pulse: contributions, streaks, commits, pull requests, repositories, stars and top languages over the last 12 months", width="100%")),
        block(pic(f"{OUT}/snake-dark.svg", f"{OUT}/snake-light.svg", "A snake eating the last year of contributions", width="100%"))] if LIVE_STATS else []),
        "<br>",
        block(asset("footer", "Thank you for reading", width="100%")),
        block(f'<img alt="Profile views" src="https://komarev.com/ghpvc/?username={USER}&label=profile%20views&color=8a6113&style=flat-square">', "center"),
    ]
    live = ("  - The GitHub pulse card and the contribution snake are rebuilt daily by\n"
            "    .github/workflows/refresh-stats.yml and published to the `output` branch."
            if LIVE_STATS else
            "  - To add the live GitHub pulse card and contribution snake, save\n"
            "    .github/workflows/refresh-stats.yml, then re-run design/readme.py.")
    header = f"""<!--
  Profile README for github.com/{USER}
  - Static cards in ./assets are generated by design/build.py (dark + light, fonts embedded).
  - Design system: "Obsidian & Gold", see design/README.md.
{live}
-->"""
    return header + "\n\n" + "\n\n".join(parts) + "\n"


if __name__ == "__main__":
    path = HERE.parent / "README.md"
    path.write_text(build(), encoding="utf-8")
    print(f"wrote {path}")
