"""Font helpers: measure text with real advance widths, subset + embed as WOFF2.

Typefaces (all SIL Open Font License 1.1, see fonts/OFL-*.txt):
  Playfair Display  display serif for names, titles, pull quotes and the large figures
  Inter             body copy and labels
  JetBrains Mono    kickers, tags and tabular figures
"""
import base64, io, functools
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools import subset

FD = Path(__file__).resolve().parent / "fonts"
FONTS = {
    # key: (family name used in CSS, file, weight)
    "serif":   ("PF7", FD / "playfair-display-latin-700-normal.woff2", 700),
    "serif6":  ("PF6", FD / "playfair-display-latin-600-normal.woff2", 600),
    "serif5":  ("PF5", FD / "playfair-display-latin-500-normal.woff2", 500),
    "serif4":  ("PF4", FD / "playfair-display-latin-400-normal.woff2", 400),
    "serifi":  ("PFI", FD / "playfair-display-latin-400-italic.woff2", 400),
    "serifi5": ("PFI5", FD / "playfair-display-latin-500-italic.woff2", 500),
    "sans":    ("IN",  FD / "inter-latin-400-normal.woff2", 400),
    "sans5":   ("IN5", FD / "inter-latin-500-normal.woff2", 500),
    "sans6":   ("IN6", FD / "inter-latin-600-normal.woff2", 600),
    "mono":    ("JB",  FD / "jetbrains-mono-latin-400-normal.woff2", 400),
    "mono5":   ("JB5", FD / "jetbrains-mono-latin-500-normal.woff2", 500),
}
# Playfair's default figures are old-style; the cards set large figures lining via `lnum`.
LNUM_KEYS = {k for k in FONTS if k.startswith("serif")}
LAYOUT_FEATURES = ["kern", "liga", "calt", "lnum"]

@functools.lru_cache(None)
def _font(key):
    return TTFont(str(FONTS[key][1]))

@functools.lru_cache(None)
def _metrics(key):
    f = _font(key)
    cmap = f.getBestCmap(); hmtx = f["hmtx"].metrics; upm = f["head"].unitsPerEm
    return cmap, hmtx, upm

@functools.lru_cache(None)
def _lnum_map(key):
    """glyph -> lining-figure glyph, from the font's `lnum` single substitutions."""
    f = _font(key); out = {}
    if "GSUB" not in f: return out
    gsub = f["GSUB"].table
    for fr in gsub.FeatureList.FeatureRecord:
        if fr.FeatureTag != "lnum": continue
        for li in fr.Feature.LookupListIndex:
            for st in gsub.LookupList.Lookup[li].SubTable:
                if hasattr(st, "mapping"): out.update(st.mapping)
    return out

def width(text, key, size, tracking=0.0, lnum=False):
    """Advance width in px of `text` set in font `key` at `size` px, with letter-spacing `tracking` px."""
    cmap, hmtx, upm = _metrics(key)
    sub = _lnum_map(key) if lnum else {}
    total = 0
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None:
            raise ValueError(f"glyph missing for {ch!r} (U+{ord(ch):04X}) in {key}")
        total += hmtx[sub.get(g, g)][0]
    return total * size / upm + tracking * max(len(text) - 1, 0)

def family(key):
    return FONTS[key][0]

def face_css(key, text):
    """@font-face rule embedding `key` subset to the characters in `text`."""
    opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = LAYOUT_FEATURES
    opts.name_IDs = []; opts.notdef_outline = True; opts.drop_tables += ["DSIG"]
    f = TTFont(str(FONTS[key][1]))
    s = subset.Subsetter(options=opts); s.populate(text=text + " "); s.subset(f)
    buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    fam, _, weight = FONTS[key]
    style = "italic" if "italic" in FONTS[key][1].name else "normal"
    return (f"@font-face{{font-family:{fam};font-weight:{weight};font-style:{style};"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}")

class Fonts:
    """Collects the text used per font inside one SVG, then emits minimal @font-face CSS."""
    def __init__(self):
        self.used = {}
    def use(self, key, text):
        self.used.setdefault(key, set()).update(text)
        return family(key)
    def css(self):
        return "".join(face_css(k, "".join(sorted(v))) for k, v in sorted(self.used.items()))
