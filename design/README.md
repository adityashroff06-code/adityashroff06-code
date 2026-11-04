# Profile design source

Everything in [`../assets`](../assets) is generated from these scripts, in a dark and a light variant.
The README picks the right one with `<picture>` and `prefers-color-scheme`, which follows your GitHub theme.

## The design system: "Obsidian & Gold"

Chosen with the [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) skill (v2.15.0).
Its product rules for a personal brand and a premium brand point the same way, and the previous
"Aurora Glass" look (violet and cyan orbs on glass) is the exact anti-pattern it names for professional
pages: AI purple gradients. The replacement:

| Decision | Choice | Why |
| --- | --- | --- |
| Pattern | Storytelling-driven: masthead, statement, the build in progress, the shipped flagship, selected work, archive, toolbox, live activity, colophon | A profile is a narrative, not a dashboard |
| Style | Exaggerated minimalism on an editorial grid: oversized serif display type, generous negative space, hairline rules, square corners | The skill's recommendation for portfolios and luxury brands |
| Palette | Warm monochrome (obsidian in dark mode, paper in light) plus one champagne-gold accent | One accent only; every text token is checked for WCAG AA in `common.py` |
| Type | Playfair Display for display, Inter for body, JetBrains Mono for kickers and figures | The skill's "Classic Elegant" and "Minimalist Monochrome Editorial" pairings |
| Motion | At most one continuous animation per card, transform/opacity only, stopped under `prefers-reduced-motion` | The skill's motion rules |
| Icons | A single thin-stroke set drawn in `common.py`; no emoji, no third-party icon strips | Stroke consistency; nothing font- or vendor-dependent |

Every card carries the same signature: a 48 px gold tick on its top edge, a 6 px corner radius and a hairline border.

| File | Card |
| --- | --- |
| `hero.py` | Masthead: name, thesis, what is being built now, and the cap-inspection motif |
| `about.py` | Statement: pull quote and three columns |
| `casestudy.py` | The two large cards: Cap Vision (now building) and Sentinel (shipped) |
| `projects.py` | The four selected-work cards |
| `index.py` | The archive ledger, one row per repository so each row carries its own link |
| `section.py` | Section headers on a transparent background |
| `toolbox.py` | Categorised stack tags |
| `pills.py`, `footer.py` | Contact buttons and the colophon |
| `readme.py` | Writes `../README.md` |
| `stats_fonts.py` | Writes `../assets/fonts/metrics.json` for the live stats card |

## Rebuild after editing

```sh
pip install fonttools brotli
python design/build.py      # regenerates ../assets/*.svg
python design/readme.py     # regenerates ../README.md
```

Fonts are subset to the glyphs each card uses and embedded, so the cards render identically on every machine.
Playfair Display, Inter and JetBrains Mono are under the SIL Open Font License 1.1 (see `fonts/OFL-*.txt`).

The live **GitHub pulse** card and the **contribution snake** are not built here: `.github/workflows/refresh-stats.yml`
rebuilds them daily with `scripts/build_stats.py` and [Platane/snk](https://github.com/Platane/snk), then publishes them to the `output` branch.
The stats script shares this design system's tokens and reads `../assets/fonts/metrics.json`; to preview it offline,
pass `--fixture` with a saved GraphQL `user` object.
