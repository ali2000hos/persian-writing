# Persian PowerPoint: RTL slides with python-pptx

PowerPoint has no document-level RTL switch — direction is set per paragraph
and per run, which is why half-fixed Persian decks are so common. Every text
frame needs the treatment below.

## Core helpers (python-pptx)

```python
from pptx.util import Pt
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree

def rtl_paragraph(paragraph, align=PP_ALIGN.RIGHT):
    """RTL direction + visual-right alignment for a pptx paragraph.
    In DrawingML (unlike OOXML/docx!) algn='r' is PHYSICAL right — safe to use."""
    paragraph.alignment = align
    pPr = paragraph._p.get_or_add_pPr()
    pPr.set('rtl', '1')

def fa_run(run, font='Vazirmatn', size=18, bold=False, color=None):
    run.font.name = font          # sets latin typeface
    run.font.size = Pt(size)
    run.font.bold = bold
    if color: run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    rPr.set('lang', 'fa-IR')
    cs = rPr.find(qn('a:cs'))
    if cs is None:
        cs = etree.SubElement(rPr, qn('a:cs'))
    cs.set('typeface', font)      # complex-script typeface — REQUIRED for Persian

def fa_text_frame(tf, font='Vazirmatn', size=18):
    """Apply to every paragraph+run in a text frame."""
    for p in tf.paragraphs:
        rtl_paragraph(p)
        for r in p.runs:
            fa_run(r, font=font, size=size)
```

Key facts:
- `a:cs` typeface is what actually renders Persian glyphs. Setting only
  `run.font.name` leaves Persian on the theme's default CS font.
- DrawingML `algn="r"` is physical right (the docx START/RIGHT trap does
  NOT apply to pptx). `rtl="1"` controls word order/bidi, `algn` controls
  which edge. Persian body/title: `rtl='1'` + `PP_ALIGN.RIGHT`.
  Centered titles: `rtl='1'` + `PP_ALIGN.CENTER` is fine.

## Layout mirroring

Persian slides mirror LTR conventions:
- Title right-aligned (or centered), content starts at the top-right.
- Two-column "image + text": image LEFT, text RIGHT (reader enters from right).
- Process/timeline arrows flow right→left; flip arrow glyphs (→ becomes ←).
- Agenda/bullet columns: rightmost column is "first".
- Logos: keep brand corner conventions, but nav-like elements mirror.

## Bullets and numbering

```python
# Persian-safe bullet char (theme bullets often lack Persian-font glyphs).
# • is verified in Vazirmatn/Lalezar; ▪ is NOT (falls back to DejaVu).
pPr = paragraph._p.get_or_add_pPr()
buFont = etree.SubElement(pPr, qn('a:buFont')); buFont.set('typeface', 'Vazirmatn')
buChar = etree.SubElement(pPr, qn('a:buChar')); buChar.set('char', '•')
```

Numbered lists: `buAutoNum` renders Latin digits only. For Persian numbering,
disable auto bullets (`a:buNone`) and prefix runs manually: «۱. »، «۲. » —
Persian digits keep the line RTL (same rule as docx).

## Tables

`a:tbl` has no bidiVisual equivalent that survives PowerPoint round-trips.
Build RTL tables by **reversing column order yourself** (first data column =
rightmost cell) and applying `rtl_paragraph`/`fa_run` to every cell. Header
row: bold + fill; keep rows short — pptx tables don't paginate.

## Fonts and delivery

- Use bundled Vazirmatn (+ Lalezar for title slides) — see fonts.md pairings.
- PowerPoint font embedding is flaky cross-platform (and python-pptx can't do
  it). If the deck travels beyond machines with the fonts installed, ALWAYS
  ship a PDF export alongside: install fonts (`bash scripts/install_fonts.sh`),
  then `soffice --headless --convert-to pdf deck.pptx`, then
  `python3 scripts/verify_pdf.py deck.pdf --expect-font Vazirmatn`.
- No letter-spacing on Persian, real bold weights only, line spacing ≥1.3
  (`paragraph.line_spacing = 1.3`).

## If building via the pptx skill's HTML pipeline (html2pptx)

Apply html-css.md rules in the source HTML: `<html dir="rtl" lang="fa">`,
Vazirmatn @font-face, `text-align: right`, Persian digits, no letter-spacing.
Then visually verify a rendered screenshot of at least the first 3 slides —
bidi bugs in HTML pipelines show up as scrambled punctuation at line edges.

## Checklist

1. Every paragraph: `rtl='1'`; every run: `a:cs` typeface set.
2. Persian digits in all visible numbers (slide numbers can stay Latin).
3. Layout mirrored (text right, flow right→left).
4. Bullets use verified glyphs (• · in Vazirmatn), numbering manual Persian.
5. Tables column-reversed.
6. PDF exported with fonts installed + verify_pdf.py clean.
