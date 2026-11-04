#!/usr/bin/env python3
"""Write ../assets/fonts/metrics.json for scripts/build_stats.py (which runs in Actions without fontTools).

    python design/stats_fonts.py

For each font file in ../assets/fonts it records units-per-em and the advance width of every Latin glyph.
Playfair's figures are exported lining (the `lnum` feature), which is how the stats card sets them.
"""
import json
from pathlib import Path
from fontTools.ttLib import TTFont

FD = Path(__file__).resolve().parent.parent / "assets" / "fonts"

def lnum_map(f):
    out = {}
    if "GSUB" not in f: return out
    gsub = f["GSUB"].table
    for fr in gsub.FeatureList.FeatureRecord:
        if fr.FeatureTag != "lnum": continue
        for li in fr.Feature.LookupListIndex:
            for st in gsub.LookupList.Lookup[li].SubTable:
                if hasattr(st, "mapping"): out.update(st.mapping)
    return out

def main():
    metrics = {}
    for path in sorted(FD.glob("*.woff2")):
        f = TTFont(str(path)); cmap = f.getBestCmap(); hmtx = f["hmtx"].metrics; sub = lnum_map(f)
        adv = {}
        for cp in range(0x20, 0x17F):
            g = cmap.get(cp)
            if g: adv[chr(cp)] = hmtx[sub.get(g, g)][0]
        for cp in (0xB7, 0x2013, 0x2014, 0x2019, 0x2026):
            g = cmap.get(cp)
            if g: adv[chr(cp)] = hmtx[sub.get(g, g)][0]
        metrics[path.stem] = {"upm": f["head"].unitsPerEm, "adv": adv}
    (FD / "metrics.json").write_text(json.dumps(metrics, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
    print("wrote", FD / "metrics.json", "for", ", ".join(metrics))

if __name__ == "__main__":
    main()
