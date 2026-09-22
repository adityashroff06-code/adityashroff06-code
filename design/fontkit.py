"""Font helpers: measure text with real advance widths, subset + embed as WOFF2."""
import base64, io, functools
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools import subset

FD = Path(__file__).resolve().parent / "fonts"
FONTS = {
    # key: (family name used in CSS, file, weight)
    "display":  ("SG",  FD / "space-grotesk-latin-700-normal.woff2", 700),
    "display6": ("SG6", FD / "space-grotesk-latin-600-normal.woff2", 600),
    "sans":     ("IN",  FD / "inter-latin-400-normal.woff2", 400),
    "sans5":    ("IN5", FD / "inter-latin-500-normal.woff2", 500),
    "sans6":    ("IN6", FD / "inter-latin-600-normal.woff2", 600),
    "mono":     ("JB",  FD / "jetbrains-mono-latin-400-normal.woff2", 400),
    "mono5":    ("JB5", FD / "jetbrains-mono-latin-500-normal.woff2", 500),
}

@functools.lru_cache(None)
def _font(key):
    return TTFont(str(FONTS[key][1]))

@functools.lru_cache(None)
def _metrics(key):
    f = _font(key)
    cmap = f.getBestCmap(); hmtx = f["hmtx"].metrics; upm = f["head"].unitsPerEm
    return cmap, hmtx, upm

def width(text, key, size, tracking=0.0):
    """Advance width in px of `text` set in font `key` at `size` px, with letter-spacing `tracking` px."""
    cmap, hmtx, upm = _metrics(key)
    total = 0
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None:
            raise ValueError(f"glyph missing for {ch!r} (U+{ord(ch):04X}) in {key}")
        total += hmtx[g][0]
    return total * size / upm + tracking * max(len(text) - 1, 0)

def family(key):
    return FONTS[key][0]

def face_css(key, text):
    """@font-face rule embedding `key` subset to the characters in `text`."""
    chars = sorted(set(text) | set(" "))
    opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["kern", "liga", "calt"]
    opts.name_IDs = []; opts.notdef_outline = True; opts.drop_tables += ["DSIG"]
    f = TTFont(str(FONTS[key][1]))
    s = subset.Subsetter(options=opts); s.populate(text="".join(chars)); s.subset(f)
    buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"@font-face{{font-family:{family(key)};src:url(data:font/woff2;base64,{b64}) format('woff2');font-display:block}}"

def ascii_woff2(key, extra=""):
    """Subset to printable ASCII (+extra) for the runtime stats renderer; returns bytes."""
    text = "".join(chr(c) for c in range(32, 127)) + extra
    opts = subset.Options(); opts.flavor = "woff2"; opts.name_IDs = []; opts.notdef_outline = True
    f = TTFont(str(FONTS[key][1]))
    s = subset.Subsetter(options=opts); s.populate(text=text); s.subset(f)
    buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf)
    return buf.getvalue()

class Fonts:
    """Collects the text used per font inside one SVG, then emits minimal @font-face CSS."""
    def __init__(self):
        self.used = {}
    def use(self, key, text):
        self.used.setdefault(key, set()).update(text)
        return family(key)
    def css(self):
        return "".join(face_css(k, "".join(sorted(v))) for k, v in sorted(self.used.items()))
