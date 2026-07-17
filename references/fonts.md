# Persian fonts: catalog, pairing, embedding

All fonts here are SIL OFL — free for commercial use, embedding allowed.
Bundled families live in `assets/fonts/`. The rest need
`scripts/download_fonts.py` (requires GitHub access — will NOT work in
offline/allowlisted sandboxes; in that case use only what's bundled, or ask
the user to drop TTFs into the project folder).

## Catalog

| Font | Personality | Use for | Avoid for | Weights |
|---|---|---|---|---|
| **Vazirmatn** ★bundled | Neutral, clean, contemporary; the Persian Inter | Body text, UI, documents, anything | — (the safe default) | 9 (Thin–Black) |
| **Lalezar** ★bundled | Loud, friendly, poster/tabloid display | Headlines, covers, banners, campaign titles | Body text, long headings | 1 |
| **Shabnam** | Softer, rounder Vazir sibling | Body alternative, friendly docs | — | 5 + FD variants |
| **Sahel** | Modern, slightly condensed | Headings, dashboards, UI labels | Dense long-form body | 3 + FD |
| **Samim** | Sober text face tuned for reading | Long reports, articles, books | Display sizes | 3 + FD |
| **Parastoo** | Bookish, literary, mild serif flavor | Formal letters, literary/academic docs | Modern tech branding | 2 + FD |
| **Tanha** | Thin, elegant, airy display | Pull quotes, elegant covers, invitations | Body text (too light) | 1 |
| **Gandom** | Warm, rounded, approachable | Casual brochures, kids/food/lifestyle content | Corporate formal docs | 2 + FD |

("FD" variants ship with built-in Farsi digit glyphs mapped to ASCII digits —
prefer real Persian digit characters instead; see orthography.md.)

Sources (for `download_fonts.py` or manual download):
- Vazirmatn: github.com/rastikerdar/vazirmatn (also on Google Fonts)
- Lalezar: fonts.google.com/specimen/Lalezar (github.com/BornaIz/Lalezar)
- Others: github.com/rastikerdar/{shabnam,sahel,samim,parastoo,tanha,gandom}-font

## Pairings that work

| Deliverable | Headings | Body |
|---|---|---|
| Business proposal / invoice | Vazirmatn Bold/Black | Vazirmatn Regular |
| Marketing one-pager, poster | Lalezar | Vazirmatn |
| Long report / whitepaper | Vazirmatn Bold | Samim or Vazirmatn |
| Product docs / dashboard | Sahel Bold | Shabnam or Vazirmatn |
| Literary / formal letter | Parastoo Bold | Parastoo |
| Elegant cover + quote | Tanha (display) | Vazirmatn |

One display font per document, maximum. When in doubt: Vazirmatn everywhere,
weights for hierarchy.

## Typography rules for Persian

- **Line height:** Persian needs more leading than Latin — 1.6–2.0 in CSS,
  `line: 312+` (≥1.3) in docx, more for headings. Tight leading clips
  ascenders and dots.
- **Size:** Persian x-height runs small; bump body ~1pt/10% over the Latin
  equivalent (11–12pt docx body, 16–18px web).
- **Never letter-space** (`letter-spacing`/character spacing) — Persian letters
  join; tracking tears the joins apart. Not even for headings. Use size/weight/
  color for emphasis instead.
- **Never fake bold/italic.** Use real weights. Italic barely exists in Persian
  type; for emphasis use bold, color, or «گیومه».
- **Kashida (کشیده):** justification by stretching connections. Word processors
  do it automatically with justify; don't insert manual ـ characters.
- **Justified text** is traditional for print Persian body; START-aligned
  (ragged left) is fine for web and modern docs. Headings: never justify.

## Embedding per format

### docx (docx-js / python-docx)
Font name exactly as the family name: `"Vazirmatn"`, `"Lalezar"`.
Always with `hint: "cs"` (docx-js) or `w:rFonts w:cs=` (python-docx) — see
docx-pdf.md. The font must be installed on the converting machine
(`bash scripts/install_fonts.sh`) or LibreOffice substitutes DejaVu.

### HTML / CSS
```css
@font-face {
  font-family: "Vazirmatn";
  src: url("fonts/Vazirmatn-Regular.woff2") format("woff2"),
       url("fonts/Vazirmatn-Regular.ttf") format("truetype");
  font-weight: 400; font-display: swap;
}
body {
  font-family: "Vazirmatn", "Segoe UI", Tahoma, sans-serif; /* Tahoma = classic Persian-safe fallback */
  line-height: 1.8;
}
```
Online pages can use Google Fonts (`family=Vazirmatn:wght@100..900` or
`family=Lalezar`); offline/PDF-print pages must reference local files —
copy them from `assets/fonts/`.

### pptx
Set the font on both latin and cs typefaces of every run (see pptx.md).
PowerPoint font embedding is unreliable cross-platform; if the deck must
travel, export a PDF (with fonts installed) alongside it.

### Checking a glyph exists (before using any symbol)
```python
from fontTools.ttLib import TTFont
cmap = TTFont("assets/fonts/Vazirmatn-Regular.ttf").getBestCmap()
ok = all(ord(c) in cmap for c in "•·۱۲۳؟،؛«»٪٬")
```
Known result for the bundled fonts: • · and all Persian punctuation/digits are
present; ▪ ■ ✓ ● ◆ are NOT (they silently fall back to DejaVu in PDFs). Check
before using anything fancier than • — `verify_pdf.py` will catch the fallback
after the fact, but checking first is cheaper.
