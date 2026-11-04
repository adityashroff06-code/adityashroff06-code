"""Archive: one ledger row per further repository. Each row is its own SVG so each can carry its own link."""
import fontkit as fk
from common import THEMES, svg_doc, text, arrow_ne, icon, rule

W, H = 900, 54
ROWS = [
    dict(slug="productarmor", title="Product Armor website", desc="Company website, built as a TypeScript monorepo",
         tag="TypeScript  ·  React", url="https://github.com/adityashroff06-code/Company-Website"),
    dict(slug="mrdental", title="M R Dental website", desc="Client site for a dental-materials maker, brand to build",
         tag="Client  ·  HTML/CSS", url=None),
    dict(slug="posner", title="POS and NER on BBC News", desc="Part-of-speech and entity analysis of 1,000 headlines",
         tag="spaCy  ·  NLTK", url="https://github.com/adityashroff06-code/POS-NER-Tagging"),
    dict(slug="igsql", title="Instagram clone, SQL analytics", desc="Product questions, bot detection included, on a 7-table schema",
         tag="MySQL", url="https://github.com/adityashroff06-code/IG_Clone_SQL_Assignment"),
    dict(slug="textprep", title="Text preprocessing with NLTK", desc="Stop words, tokens, stemming, lemmatisation, n-grams",
         tag="NLTK  ·  pandas", url="https://github.com/adityashroff06-code/TEXT-PREPROCESSING-WITH-NLTK-AND-PANDAS"),
    dict(slug="webanalysis", title="Web and social media analysis", desc="Case studies: Charles Book Club, Tayko, eBay",
         tag="Python  ·  Analytics", url="https://github.com/adityashroff06-code/Business-Web-and-Social-Media-Analysis"),
]

def build(i, r, theme):
    t = THEMES[theme]; F = fk.Fonts()
    L, R = 36, W - 36; y = 33
    body = text(L, y, f"{i+1:02d}", F, "mono5", 11, t["gold_ink"], tracking=1)
    body += text(L + 40, y, r["title"], F, "sans6", 14.5, t["text"])
    assert fk.width(r["title"], "sans6", 14.5) <= 250, r["title"]
    body += text(L + 304, y, r["desc"], F, "sans", 13, t["muted"])
    tagw = fk.width(r["tag"], "mono", 10.5, 0.4)
    assert L + 304 + fk.width(r["desc"], "sans", 13) < R - tagw - 60, r["slug"]
    if r["url"]:
        body += text(R - 22, y, r["tag"], F, "mono", 10.5, t["muted"], anchor="end", tracking=0.4)
        body += arrow_ne(R - 9, y - 9, 8, t["gold_ink"])
    else:
        body += text(R - 24, y, r["tag"], F, "mono", 10.5, t["muted"], anchor="end", tracking=0.4)
        body += icon("lock", R - 8, y - 4, 14, t["muted"])
    body += rule(L, H - 0.5, R, t)
    title = f'{r["title"]}: {r["desc"]}' + ("" if r["url"] else " (private repository)")
    return svg_doc(W, H, title, body, F.css(), "", desc=title)
