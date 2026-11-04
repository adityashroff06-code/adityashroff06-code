#!/usr/bin/env python3
"""Render the "GitHub pulse" card (dark + light) for this profile README.

Runs in GitHub Actions with the built-in GITHUB_TOKEN. Standard library only.

    python3 scripts/build_stats.py --user <login> --out dist            # live, needs GITHUB_TOKEN
    python3 scripts/build_stats.py --fixture data.json --out dist       # offline, from a saved response

Writes <out>/stats-dark.svg and <out>/stats-light.svg.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "assets" / "fonts"

QUERY = """
query($login: String!) {
  user(login: $login) {
    login
    repositories(first: 100, ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC) {
      totalCount
      nodes {
        name
        stargazerCount
        languages(first: 15, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}
"""

# --------------------------------------------------------------------------- data

def fetch(login: str, token: str) -> dict:
    body = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Authorization": f"bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": f"{login}-profile-stats",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.load(resp)
    except urllib.error.HTTPError as err:
        sys.exit(f"GitHub API returned HTTP {err.code}: {err.read()[:300]!r}")
    if payload.get("errors"):
        sys.exit(f"GitHub API errors: {json.dumps(payload['errors'])[:500]}")
    user = (payload.get("data") or {}).get("user")
    if not user:
        sys.exit(f"No user data returned for {login!r}")
    return user


def streaks(days: list[dict], today: dt.date) -> tuple[int, int]:
    """(current, longest) runs of consecutive days with at least one contribution.

    A day with no contributions *today* does not break the current streak;
    the day is not over yet.
    """
    counts = {dt.date.fromisoformat(d["date"]): d["contributionCount"] for d in days}
    if not counts:
        return 0, 0
    longest = run = 0
    prev = None
    for day in sorted(counts):
        adjacent = prev is not None and day - prev == dt.timedelta(days=1)
        run = (run + 1 if adjacent else 1) if counts[day] > 0 else 0
        longest = max(longest, run)
        prev = day
    day = max(d for d in counts if d <= today) if any(d <= today for d in counts) else max(counts)
    if counts.get(day, 0) == 0:
        day -= dt.timedelta(days=1)
    current = 0
    while counts.get(day, 0) > 0:
        current += 1
        day -= dt.timedelta(days=1)
    return current, longest


def summarize(user: dict, today: dt.date) -> dict:
    cc = user["contributionsCollection"]
    weeks = cc["contributionCalendar"]["weeks"]
    days = [d for w in weeks for d in w["contributionDays"]]
    current, longest = streaks(days, today)
    weekly = [(w["contributionDays"][0]["date"], sum(d["contributionCount"] for d in w["contributionDays"]))
              for w in weeks if w["contributionDays"]][-52:]

    repos = user["repositories"]["nodes"]
    sizes: dict[str, int] = {}
    for repo in repos:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            name = "Python" if name == "Jupyter Notebook" else name  # notebooks here are Python
            sizes[name] = sizes.get(name, 0) + edge["size"]
    total = sum(sizes.values()) or 1
    ranked = sorted(sizes.items(), key=lambda kv: -kv[1])
    langs = [(n, v / total) for n, v in ranked[:5]]
    rest = sum(v for _, v in ranked[5:]) / total
    if rest > 0:
        langs.append(("Other", rest))

    return {
        "contributions": cc["contributionCalendar"]["totalContributions"],
        "current": current,
        "longest": longest,
        "weekly": weekly,
        "commits": cc["totalCommitContributions"],
        "prs": cc["totalPullRequestContributions"],
        "repos": user["repositories"]["totalCount"],
        "stars": sum(r["stargazerCount"] for r in repos),
        "langs": langs,
        "updated": today,
    }

# --------------------------------------------------------------------------- type

class Type:
    FILES = {"display": "PlayfairDisplay-SemiBold", "sans": "Inter-Regular", "sans5": "Inter-Medium",
             "mono": "JetBrainsMono-Regular"}

    def __init__(self) -> None:
        self.metrics = json.loads((FONT_DIR / "metrics.json").read_text())

    def width(self, text: str, font: str, size: float, tracking: float = 0) -> float:
        m = self.metrics[self.FILES[font]]
        adv = m["adv"]
        fallback = adv.get("n", m["upm"] // 2)
        return sum(adv.get(ch, fallback) for ch in text) * size / m["upm"] + tracking * max(len(text) - 1, 0)

    def css(self) -> str:
        rules = []
        for key, name in self.FILES.items():
            b64 = base64.b64encode((FONT_DIR / f"{name}.woff2").read_bytes()).decode()
            rules.append(f"@font-face{{font-family:f-{key};src:url(data:font/woff2;base64,{b64}) format('woff2')}}")
        # Playfair's default figures are old-style; the card sets them lining.
        rules.append('text[font-family="f-display"]{font-feature-settings:"lnum"}')
        return "".join(rules)

# --------------------------------------------------------------------------- render

THEMES = {
    # "Obsidian & Gold": the same tokens as design/common.py.
    "dark": dict(card0="#15120F", card1="#0C0B09", plate="#0B0A08", line="#F4EFE6", line_a=0.12, line_a2=0.22,
                 wash="#F4EFE6", wash_a=0.035, text="#F4EFE6", text2="#CFC7BA", muted="#9C9285", faint="#3F3A33",
                 gold="#D4B06A", gold_ink="#D4B06A",
                 langs=["#D4B06A", "#A98A52", "#CFC7BA", "#8E8579", "#5E5750", "#3F3A33"]),
    "light": dict(card0="#FFFFFF", card1="#F7F4EE", plate="#FFFFFF", line="#15120E", line_a=0.13, line_a2=0.24,
                  wash="#15120E", wash_a=0.03, text="#15120E", text2="#46403A", muted="#6B635A", faint="#DAD3C8",
                  gold="#AE8836", gold_ink="#8A6113",
                  langs=["#8A6113", "#C4A565", "#46403A", "#8E8579", "#B9B0A4", "#DAD3C8"]),
}


def rgba(hex_: str, a: float) -> str:
    h = hex_.lstrip("#")
    return f"rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{a})"


def txt(x, y, s, font, size, fill, anchor="start", tracking=0, extra=""):
    ls = f' letter-spacing="{tracking}"' if tracking else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="f-{font}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}"{ls} {extra}>{escape(s)}</text>')


def render(s: dict, theme: str, T: Type) -> str:
    t = THEMES[theme]
    W, H, L, R = 900, 384, 56, 844
    out = []

    def kicker(x, y, label, anchor="start", size=11):
        tw = T.width(label, "mono", size, tracking=2.2) + 18
        x0 = x if anchor == "start" else x - tw
        return (f'<rect x="{x0:.1f}" y="{y - size * 0.36:.1f}" width="12" height="1.2" fill="{t["gold_ink"]}"/>'
                + txt(x0 + 18, y, label, "mono", size, t["gold_ink"], tracking=2.2))

    # header
    out.append(kicker(L, 58, "GITHUB PULSE"))
    peak_value = max((v for _, v in s["weekly"]), default=0)
    out.append(txt(R, 58, f"last 12 months, weekly, peak {peak_value:,}  ·  updated {s['updated'].day} {s['updated']:%B %Y}",
                   "mono", 10.5, t["muted"], anchor="end", tracking=0.3))

    # headline number + streaks
    total = f"{s['contributions']:,}"
    out.append(txt(L - 2, 126, total, "display", 56, t["text"], extra='class="up"', tracking=-1))
    out.append(txt(L, 150, "contributions in the last year", "sans", 13.5, t["text2"]))
    for i, (value, label) in enumerate([(s["current"], "current streak"), (s["longest"], "longest streak")]):
        x = L + i * 138
        num = f"{value:,}"
        out.append(txt(x, 200, num, "display", 26, t["text"]))
        out.append(txt(x + T.width(num, "display", 26) + 6, 200, "days" if value != 1 else "day", "sans5", 12.5, t["muted"]))
        out.append(txt(x, 219, label, "sans", 12, t["muted"]))

    # weekly bars
    x0, x1, base, hmax = 372.0, float(R), 176.0, 100.0
    n = max(len(s["weekly"]), 1)
    gap = 2.4
    bw = (x1 - x0 - gap * (n - 1)) / n
    peak = peak_value or 1
    bars, labels, last_label_x, last_month = [], [], -99.0, None
    for i, (start, v) in enumerate(s["weekly"]):
        x = x0 + i * (bw + gap)
        h = 2.0 if v == 0 else max(4.0, hmax * v / peak)
        fill = rgba(t["muted"], 0.3) if v == 0 else t["gold"]
        bars.append(f'<rect class="bar" style="animation-delay:{i * 0.018:.3f}s" x="{x:.2f}" y="{base - h:.2f}" '
                    f'width="{bw:.2f}" height="{h:.2f}" fill="{fill}" fill-opacity="{0.5 + 0.5 * (v / peak):.2f}"/>')
        month = start[:7]
        if month != last_month:
            last_month = month
            if x - last_label_x >= 30:
                name = dt.date.fromisoformat(start).strftime("%b").upper()
                labels.append(txt(x, base + 18, name, "mono", 9.5, t["muted"], tracking=1))
                last_label_x = x
    out.append(f'<line x1="{x0}" y1="{base + 0.5}" x2="{x1}" y2="{base + 0.5}" stroke="{t["line"]}" stroke-opacity="{t["line_a2"]}"/>')
    out.extend(bars)
    out.extend(labels)

    # tiles
    tiles = [(s["commits"], "commits"), (s["prs"], "pull requests"), (s["repos"], "public repositories"),
             (s["stars"], "stars earned")]
    ty, th, tg = 236, 64, 14
    tw = (R - L - tg * 3) / 4
    for i, (value, label) in enumerate(tiles):
        x = L + i * (tw + tg)
        out.append(f'<rect class="fade" style="animation-delay:{0.25 + i * 0.08:.2f}s" x="{x:.1f}" y="{ty}" width="{tw:.1f}" '
                   f'height="{th}" rx="3" fill="{rgba(t["wash"], t["wash_a"])}" stroke="{t["line"]}" stroke-opacity="{t["line_a"]}"/>')
        out.append(txt(x + 16, ty + 31, f"{value:,}", "display", 22, t["text"]))
        out.append(txt(x + 16, ty + 50, label, "sans", 12, t["muted"]))

    # languages
    ly = 334
    out.append(kicker(L, ly - 10, "TOP LANGUAGES", size=10.5))
    out.append(txt(R, ly - 10, "by code size across public repos; Python includes notebooks", "mono", 10.5,
                   t["muted"], anchor="end", tracking=0.3))
    palette = t["langs"]
    x = float(L)
    seg = []
    for i, (name, frac) in enumerate(s["langs"]):
        w = (R - L) * frac
        seg.append(f'<rect x="{x:.2f}" y="{ly}" width="{max(w, 0.8):.2f}" height="6" fill="{palette[i % len(palette)]}"/>')
        x += w
    out.append(f'<clipPath id="lb"><rect x="{L}" y="{ly}" width="{R - L}" height="6" rx="1.5"/></clipPath>'
               f'<g clip-path="url(#lb)"><g class="grow">{"".join(seg)}</g></g>')
    lx = float(L)
    for i, (name, frac) in enumerate(s["langs"]):
        pct = f"{frac * 100:.1f}%" if frac >= 0.001 else "<0.1%"
        label_w = T.width(name, "sans5", 12) + 6 + T.width(pct, "mono", 11)
        if lx + 14 + label_w > R:
            break
        out.append(f'<rect x="{lx:.1f}" y="{ly + 24}" width="8" height="8" fill="{palette[i % len(palette)]}"/>')
        out.append(txt(lx + 14, ly + 32, name, "sans5", 12, t["text"]))
        out.append(txt(lx + 14 + T.width(name, "sans5", 12) + 6, ly + 32, pct, "mono", 11, t["muted"]))
        lx += 14 + label_w + 22

    defs = f"""
    <clipPath id="fr"><rect width="{W}" height="{H}" rx="6"/></clipPath>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{t['card0']}"/><stop offset="1" stop-color="{t['card1']}"/></linearGradient>
    """
    css = T.css() + """
    .bar{transform-box:fill-box;transform-origin:50% 100%;animation:grow .9s cubic-bezier(.2,.7,.2,1) both}
    @keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
    .grow{transform-box:fill-box;transform-origin:0 50%;animation:gx 1.2s cubic-bezier(.2,.7,.2,1) .3s both}
    @keyframes gx{from{transform:scaleX(0)}to{transform:scaleX(1)}}
    .fade{animation:fd .7s ease both} @keyframes fd{from{opacity:0}to{opacity:1}}
    .up{animation:up .8s cubic-bezier(.2,.7,.2,1) both} @keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
    @media (prefers-reduced-motion: reduce){*{animation:none!important}}
    """
    desc = (f"{s['contributions']:,} contributions in the last year; current streak {s['current']} days, "
            f"longest {s['longest']} days; {s['commits']:,} commits, {s['prs']:,} pull requests, "
            f"{s['repos']} public repositories, {s['stars']} stars. Top languages: "
            + ", ".join(f"{n} {f * 100:.1f}%" for n, f in s["langs"]) + ".")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
            f'aria-labelledby="t d" fill="none"><title id="t">GitHub pulse</title><desc id="d">{escape(desc)}</desc>'
            f'<style>{css}</style><defs>{defs}</defs>'
            f'<g clip-path="url(#fr)"><rect width="{W}" height="{H}" fill="url(#bg)"/>'
            f'<rect x="36" y="0" width="48" height="2" fill="{t["gold"]}"/>'
            + "".join(out) +
            f'</g><rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="5.5" stroke="{t["line"]}" '
            f'stroke-opacity="{t["line_a"]}"/></svg>')


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--user", default=os.environ.get("GITHUB_REPOSITORY_OWNER"))
    ap.add_argument("--fixture", type=Path, help="render from a saved GraphQL `user` object instead of the API")
    ap.add_argument("--out", type=Path, default=Path("dist"))
    args = ap.parse_args()

    if args.fixture:
        user = json.loads(args.fixture.read_text())
    else:
        token = os.environ.get("GITHUB_TOKEN")
        if not (token and args.user):
            sys.exit("Set GITHUB_TOKEN and pass --user (or use --fixture).")
        user = fetch(args.user, token)

    stats = summarize(user, dt.datetime.now(dt.timezone.utc).date())
    args.out.mkdir(parents=True, exist_ok=True)
    T = Type()
    for theme in THEMES:
        path = args.out / f"stats-{theme}.svg"
        path.write_text(render(stats, theme, T), encoding="utf-8")
        print(f"wrote {path} ({path.stat().st_size // 1024} KB)")
    printable = {k: (v if k != "weekly" else f"{len(v)} weeks") for k, v in stats.items()}
    print(json.dumps(printable, default=str))


if __name__ == "__main__":
    main()
