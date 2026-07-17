# Persian HTML/CSS: RTL web pages, emails, and HTML→PDF

## The foundation

```html
<!DOCTYPE html>
<html dir="rtl" lang="fa">
```

`dir="rtl"` on `<html>` flips the whole layout: text flows right→left, flex/grid
main axes reverse, tables mirror, list markers move right. Most "RTL bugs" come
from fighting this with hard-coded `left`/`right` afterwards.

## CSS rules

### Use logical properties, not physical

| Physical (breaks RTL) | Logical (RTL-safe) |
|---|---|
| `margin-left` | `margin-inline-start` |
| `padding-right` | `padding-inline-end` |
| `text-align: left` | `text-align: start` |
| `border-left` | `border-inline-start` |
| `left: 0` | `inset-inline-start: 0` |

`text-align: right` is acceptable at the page level for Persian (it equals
`start` under `dir=rtl`), but inside components prefer `start`/`end` so the
component survives reuse.

### Typography

```css
body {
  font-family: "Vazirmatn", "Segoe UI", Tahoma, sans-serif;
  font-size: 17px;          /* Persian reads small — go one step larger */
  line-height: 1.8;         /* 1.6 minimum; Persian clips below that */
  letter-spacing: 0;        /* NEVER track Persian — it breaks letter joins */
}
h1, h2, h3 { line-height: 1.5; font-weight: 700; }  /* real weights, no faux bold */
```

Display headings: `font-family: "Lalezar"` — one display face per page, max.

### Mixed-direction content (the hard part)

Latin fragments (brand names, URLs, code, phone numbers) inside Persian text
disrupt bidi ordering. Tools:

```html
<!-- isolate an LTR fragment so surrounding punctuation doesn't scramble -->
<p>افزونه <bdi>WooCommerce 9.5</bdi> را نصب کنید.</p>

<!-- force a whole block LTR (code, addresses, phone) -->
<pre dir="ltr">npm install docx</pre>
<span dir="ltr">+98 912 345 6789</span>
```

CSS equivalent: `unicode-bidi: isolate` (default for `<bdi>`).
Fix stray punctuation jumping to the wrong side with `&lrm;`/`&rlm;` marks —
but if you need many of them, wrap the fragment in `<bdi>` instead.

Numbers: use Persian digits ۰-۹ in prose (they inherit RTL correctly).
Keep inputs like phone/URL fields `dir="ltr"` with `text-align: start`.

### Layout mirroring

- Flex/grid auto-mirror under `dir=rtl` — write `flex-direction: row` and let
  the browser flip it. Don't write `row-reverse` to "fix" RTL; that double-flips.
- Icons with direction (arrows, chevrons, back buttons): mirror with
  `[dir="rtl"] .icon-arrow { transform: scaleX(-1); }`. Symmetric icons stay.
- Shadows/border-radius asymmetries: use logical values or mirror per-dir.
- Carousels/sliders: reverse advance direction; "next" points left in RTL.

### Lists and tables

```css
ul, ol { padding-inline-start: 1.5em; }   /* not padding-left */
```
Ordered lists: browsers render Latin digits by default; for Persian numbering
use `list-style: arabic-indic` (`list-style-type: persian` where supported) or
generate markers manually with Persian digits.

Tables under `dir=rtl` mirror automatically: first `<th>` renders rightmost. ✓

## Persian web fonts

See fonts.md for the catalog. Online: Google Fonts serves Vazirmatn and Lalezar:

```html
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100..900&family=Lalezar&display=swap" rel="stylesheet">
```

Offline / HTML→PDF / email: embed local files from `assets/fonts/` via
`@font-face`. Never rely on system fonts for Persian — Windows falls back to
Segoe UI (passable), macOS to Geeza Pro (wrong flavor), Linux to DejaVu (broken).

## HTML email

Email clients strip `<style>` unpredictably:
- `dir="rtl"` attribute on every structural `<table>`, `<td>`, `<div>` — not CSS.
- Inline styles only: `style="font-family:Tahoma,Arial; text-align:right; direction:rtl"`.
- Web fonts don't load in most clients → Tahoma is the classic Persian-safe
  email font stack.
- Test: Gmail web strips `<head>` styles; Outlook desktop ignores web fonts.

## HTML→PDF (weasyprint / headless Chrome)

The pagination principles from docx-pdf.md, in CSS:

```css
@page { size: A4; margin: 2cm; }
h1, h2, h3, h4 { break-after: avoid; }        /* no orphan headings */
.card, .price-box, figure { break-inside: avoid; }  /* no split cards */
p { orphans: 2; widows: 2; }                   /* no lonely lines */
.divider-page { break-before: page; break-after: page; }
```

- weasyprint honors `break-*` well and embeds @font-face fonts — good default.
- Headless Chrome (`--print-to-pdf`) also works; ensure fonts are installed
  (`bash scripts/install_fonts.sh`) or referenced via @font-face with absolute
  paths.
- Verify the output exactly like a docx-derived PDF:
  `python3 scripts/verify_pdf.py out.pdf --expect-font Vazirmatn`.

## Pre-delivery checklist

1. `<html dir="rtl" lang="fa">` present.
2. No physical left/right properties that fight RTL (grep for `margin-left`,
   `text-align: left`, `padding-right` and justify each hit).
3. `letter-spacing` nowhere on Persian text.
4. Latin fragments wrapped in `<bdi>`/`dir="ltr"`.
5. Persian digits in prose; `persian_cleanup.py --edit` + `fa_lint.py --check`
   on the text content.
6. Fonts load (DevTools → Network, or pdffonts on the exported PDF).
7. If printed/PDF: break rules applied, then verify_pdf.py.
