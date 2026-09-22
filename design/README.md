# Profile design source

Everything in [`../assets`](../assets) is generated from these scripts, in a dark and a light variant.
The README picks the right one with `<picture>` and `prefers-color-scheme`, which follows your GitHub theme.

| File | Card |
| --- | --- |
| `hero.py` | Animated banner: name, typed focus areas, "now building" status, vision-scope motif |
| `about.py` | `aditya.py` code card |
| `sentinel.py` | Sentinel pipeline card with the animated data flow |
| `projects.py` | The four project cards (text, metric and stack for each) |
| `toolbox.py` | Categorised stack chips |
| `pills.py`, `footer.py` | Contact buttons and footer |
| `readme.py` | Writes `../README.md` |

## Rebuild after editing

```sh
pip install fonttools brotli
python design/build.py      # regenerates ../assets/*.svg
python design/readme.py     # regenerates ../README.md
```

Fonts are subset to the glyphs each card uses and embedded, so the cards render identically on every machine.
Space Grotesk, Inter and JetBrains Mono are under the SIL Open Font License 1.1 (see `fonts/OFL-*.txt`).

The live **GitHub pulse** card and the **contribution snake** are not built here: `.github/workflows/refresh-stats.yml`
rebuilds them daily with `scripts/build_stats.py` and [Platane/snk](https://github.com/Platane/snk), then publishes them to the `output` branch.
