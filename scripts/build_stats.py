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
    FILES = {"display": "SpaceGrotesk-Bold", "sans": "Inter-Regular", "sans5": "Inter-Medium",
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
        return "".join(rules)

# --------------------------------------------------------------------------- render

THEMES = {
    "dark": dict(card0="#0D0F24", card1="#121036", stroke="#FFFFFF", stroke_a=0.09, glass_a=0.045,
                 text="#EEF0FF", text2="#B6BBD8", muted="#8288AD", faint="#2A2E52",
                 violet="#A78BFA", cyan="#22D3EE", pink="#F472B6", teal="#2DD4BF", amber="#FBBF24",
                 grad_a="#C4B5FD", grad_b="#67E8F9", glow="#7C3AED", glow_a=0.34, glow2="#0891B2", glow2_a=0.22),
    "light": dict(card0="#FFFFFF", card1="#F6F4FF", stroke="#4C1D95", stroke_a=0.13, glass_a=0.72,
                  text="#15132E", text2="#454A6B", muted="#686E91", faint="#E4E2F3",
                  violet="#7C3AED", cyan="#0E7490", pink="#BE185D", teal="#0F766E", amber="#B45309",
                  grad_a="#6D28D9", grad_b="#0E7490", glow="#C4B5FD", glow_a=0.45, glow2="#99F6E4", glow2_a=0.45),
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
    dark = theme == "dark"
    W, H, L, R = 900, 384, 32, 868
    out = []

    # header
    out.append(txt(L, 44, "GITHUB PULSE", "mono", 12, t["cyan"], tracking=2.4))
    out.append(txt(R, 44, f"last 12 months · updated {s['updated'].day} {s['updated']:%b %Y}", "mono", 11.5,
                   t["muted"], anchor="end"))

    # headline number + streaks
    total = f"{s['contributions']:,}"
    out.append(txt(L - 2, 118, total, "display", 54, "url(#num)", extra='class="up"'))
    out.append(txt(L, 144, "contributions in the last year", "sans", 13.5, t["text2"] if dark else t["muted"]))
    for i, (value, label) in enumerate([(s["current"], "current streak"), (s["longest"], "longest streak")]):
        x = L + i * 138
        num = f"{value:,}"
        out.append(txt(x, 196, num, "display", 26, t["text"]))
        out.append(txt(x + T.width(num, "display", 26) + 6, 196, "days" if value != 1 else "day", "sans5", 12.5, t["muted"]))
        out.append(txt(x, 216, label, "sans", 12, t["muted"]))

    # weekly bars
    x0, x1, base, hmax = 356.0, float(R), 176.0, 104.0
    n = max(len(s["weekly"]), 1)
    gap = 2.4
    bw = (x1 - x0 - gap * (n - 1)) / n
    peak_value = max((v for _, v in s["weekly"]), default=0)
    peak = peak_value or 1
    bars, labels, last_label_x, last_month = [], [], -99.0, None
    for i, (start, v) in enumerate(s["weekly"]):
        x = x0 + i * (bw + gap)
        h = 2.0 if v == 0 else max(4.0, hmax * v / peak)
        fill = rgba(t["muted"], 0.25) if v == 0 else "url(#bar)"
        bars.append(f'<rect class="bar" style="animation-delay:{i * 0.018:.3f}s" x="{x:.2f}" y="{base - h:.2f}" '
                    f'width="{bw:.2f}" height="{h:.2f}" rx="{min(2.5, bw / 2):.2f}" fill="{fill}"/>')
        month = start[:7]
        if month != last_month:
            last_month = month
            if x - last_label_x >= 30:
                name = dt.date.fromisoformat(start).strftime("%b")
                labels.append(txt(x, base + 18, name, "mono", 10, t["muted"]))
                last_label_x = x
    out.append(f'<line x1="{x0}" y1="{base + 0.5}" x2="{x1}" y2="{base + 0.5}" stroke="{t["stroke"]}" stroke-opacity="{t["stroke_a"]}"/>')
    out.extend(bars)
    out.extend(labels)
    out.append(txt(x0, 64, f"weekly contributions · peak {peak_value:,}", "mono", 10.5, t["muted"]))

    # tiles
    tiles = [(s["commits"], "commits"), (s["prs"], "pull requests"), (s["repos"], "public repositories"),
             (s["stars"], "stars earned")]
    ty, th, tg = 232, 64, 12
    tw = (R - L - tg * 3) / 4
    for i, (value, label) in enumerate(tiles):
        x = L + i * (tw + tg)
        out.append(f'<rect class="fade" style="animation-delay:{0.25 + i * 0.08:.2f}s" x="{x:.1f}" y="{ty}" width="{tw:.1f}" '
                   f'height="{th}" rx="14" fill="{rgba("#FFFFFF", t["glass_a"])}" stroke="{rgba(t["stroke"], t["stroke_a"] + 0.02)}"/>')
        out.append(txt(x + 16, ty + 31, f"{value:,}", "display", 22, t["text"]))
        out.append(txt(x + 16, ty + 50, label, "sans", 12, t["muted"]))

    # languages
    ly = 326
    out.append(txt(L, ly - 8, "TOP LANGUAGES", "mono", 10.5, t["muted"], tracking=1.8))
    out.append(txt(R, ly - 8, "by code size across public repos; Python includes notebooks", "mono", 10.5,
                   t["muted"], anchor="end"))
    palette = [t["violet"], t["cyan"], t["pink"], t["teal"], t["amber"], t["muted"]]
    x = float(L)
    seg = []
    for i, (name, frac) in enumerate(s["langs"]):
        w = (R - L) * frac
        seg.append(f'<rect x="{x:.2f}" y="{ly}" width="{max(w, 0.8):.2f}" height="10" fill="{palette[i % len(palette)]}"/>')
        x += w
    out.append(f'<clipPath id="lb"><rect x="{L}" y="{ly}" width="{R - L}" height="10" rx="5"/></clipPath>'
               f'<g clip-path="url(#lb)"><g class="grow">{"".join(seg)}</g></g>')
    lx = float(L)
    for i, (name, frac) in enumerate(s["langs"]):
        pct = f"{frac * 100:.1f}%" if frac >= 0.001 else "<0.1%"
        label_w = T.width(name, "sans5", 12) + 6 + T.width(pct, "mono", 11)
        if lx + 14 + label_w > R:
            break
        out.append(f'<circle cx="{lx + 4:.1f}" cy="{ly + 31}" r="4" fill="{palette[i % len(palette)]}"/>')
        out.append(txt(lx + 14, ly + 35, name, "sans5", 12, t["text"]))
        out.append(txt(lx + 14 + T.width(name, "sans5", 12) + 6, ly + 35, pct, "mono", 11, t["muted"]))
        lx += 14 + label_w + 22

    defs = f"""
    <clipPath id="fr"><rect width="{W}" height="{H}" rx="20"/></clipPath>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['card0']}"/><stop offset="1" stop-color="{t['card1']}"/></linearGradient>
    <radialGradient id="g1" cx="0" cy="0" r="0.6"><stop offset="0" stop-color="{t['glow']}" stop-opacity="{t['glow_a']}"/><stop offset="1" stop-color="{t['glow']}" stop-opacity="0"/></radialGradient>
    <radialGradient id="g2" cx="1" cy="0.4" r="0.55"><stop offset="0" stop-color="{t['glow2']}" stop-opacity="{t['glow2_a']}"/><stop offset="1" stop-color="{t['glow2']}" stop-opacity="0"/></radialGradient>
    <linearGradient id="num" x1="0" x2="1"><stop offset="0" stop-color="{t['grad_a']}"/><stop offset="1" stop-color="{t['grad_b']}"/></linearGradient>
    <linearGradient id="bar" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{t['violet']}"/><stop offset="1" stop-color="{t['cyan']}"/></linearGradient>
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
            f'<rect width="{W}" height="{H}" fill="url(#g1)"/><rect width="{W}" height="{H}" fill="url(#g2)"/>'
            + "".join(out) +
            f'</g><rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="19.5" stroke="{t["stroke"]}" '
            f'stroke-opacity="{t["stroke_a"]}"/></svg>')


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
