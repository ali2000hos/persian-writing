# Persian DOCX + PDF: RTL and pagination recipes

Battle-tested fixes from real Persian proposal production. The docx-js (npm `docx`)
examples are the reference implementation; python-docx equivalents follow at the
end. Read the whole file before generating a Persian Word document — most of these
failures are invisible until you convert to PDF and look.

**Pick your library FIRST, in 10 seconds:** if `docx` (npm) is already importable,
use the docx-js recipes. If not — and in sandboxed environments npm installs are
often blocked — do NOT spend time fighting the package manager: go straight to
python-docx (§6), which ships in most sandboxes and sets the exact same OOXML
flags. The concepts in §1–§5 (START-not-RIGHT, bidi, cs fonts, keepNext,
cantSplit) apply identically to both libraries.

**Colors in this file are placeholders.** Where an example sets `color`, a
border, or a fill, it uses neutral grey/black purely to show the property's
position. Do NOT reproduce these values as a look. Default to unstyled (black
text, no accent). Pull real colors only from the user's request, an attached
brand skill, or a template you're matching. The RTL/pagination structure is the
reusable part; the styling is not.

## Table of contents

1. RTL: alignment, runs, tables, numbers, symbols, sections, styles
2. Divider/full-bleed pages (empty headers, titlePage, white-bar fix)
3. Pagination: orphan headings, unsplittable cards, blank pages, FAQ/tables
4. Fonts and PDF conversion workflow
5. Verification checklist (mandatory)
6. python-docx equivalents

---

## 1. RTL correctness

### 1.1 The core trap: RIGHT means visual LEFT in RTL

In OOXML, when `bidirectional: true` is set, `AlignmentType.RIGHT` is interpreted
as "end of text" — and in RTL, "end" is the **visual left**. Persian text aligned
RIGHT renders left-aligned. Use `START`, which in RTL always means visual right.

```javascript
// ❌ WRONG — left-aligns Persian in RTL
new Paragraph({
  alignment: AlignmentType.RIGHT,
  bidirectional: true,
  children: [new TextRun({ text: "متن فارسی", font: { name: "Vazirmatn" } })]
})

// ✅ RIGHT — visually right-aligned
new Paragraph({
  alignment: AlignmentType.START,
  bidirectional: true,
  children: [new TextRun({
    text: "متن فارسی",
    font: { name: "Vazirmatn", hint: "cs" },
    rightToLeft: true
  })]
})
```

`hint: "cs"` (Complex Script) tells Word this font applies to the Persian/Arabic
script run. Without it Word may pick a different font for Persian glyphs.
Audit rule: **grep your generator for `AlignmentType.RIGHT` — every hit is a bug**
(use `END` only when you deliberately want visual left, e.g. a Latin code block).

Define a helper once and use it for all Persian runs:

```javascript
const fa = (text, opts = {}) => new TextRun({
  text,
  rightToLeft: true,
  font: { name: "Vazirmatn", hint: "cs" },
  ...opts,
});
```

### 1.2 Tables must flow right→left

For any table where the first column belongs on the right (all Persian tables):

```javascript
new Table({
  width: { size: 100, type: WidthType.PERCENTAGE },
  visuallyRightToLeft: true,  // ← the key: first cell = visual right
  borders: allNoBorders,
  rows: [new TableRow({
    cantSplit: true,
    children: [
      new TableCell({ children: [/* first item — visual RIGHT */] }),
      new TableCell({ children: [/* second item — visual LEFT */] }),
    ]
  })]
})
```

Without `visuallyRightToLeft`, a two-column module list reads backwards.

### 1.3 Persian digits keep paragraphs RTL

A Latin digit at paragraph start flips the bidi direction of the line. Use
Persian digits in all Persian text, including list numbering:

```javascript
// ❌ Latin digit makes the paragraph LTR
fa((i + 1) + ".  ", { bold: true })

// ✅ Persian digit preserves RTL
const faDigits = "۰۱۲۳۴۵۶۷۸۹";
const toFa = (n) => String(n).replace(/[0-9]/g, d => faDigits[+d]);
fa(toFa(i + 1) + ".  ", { bold: true })
```

Prices too: «۲۵٬۰۰۰٬۰۰۰ تومان» (U+066C or ، as thousands separator — pick one
and be consistent).

### 1.4 Symbols: verify glyphs exist

Persian fonts miss many symbols; missing glyphs silently fall back to an ugly
substitute font in the PDF. Check before using:

```python
from fontTools.ttLib import TTFont
cmap = TTFont("Vazirmatn-Regular.ttf").getBestCmap()
print(0x2299 in cmap)  # ⊙ supported?
```

Verified safe in the bundled Vazirmatn and Lalezar: `•` (U+2022), `·` (U+00B7).
NOT in Vazirmatn/Lalezar (falls back to DejaVu): ▪ ■ ⊙ ◆ ✓ ✕ ● ○ and emoji.
Other Persian fonts have different coverage — run the check above before using
any symbol; a fallback shows up later as a DejaVu row in `pdffonts`.

### 1.5 Every section: bidi — and VERIFY it reached the XML

```javascript
sections.push({
  properties: {
    page: { size: { width: 11906, height: 16838 } },  // A4 portrait, twips
    bidi: true,  // ← required per section
  },
  children: [...]
})
```

**Setting it is not the same as it being written.** Some docx-js versions
silently drop `bidi` from section properties, and in python-docx it is easy to
append `<w:bidi/>` in the wrong position. `<w:bidi/>` must be the FIRST child
of `<w:sectPr>` (OOXML enforces child order — appended at the end, renderers
ignore it). Always check the produced file, not your source code:

```bash
unzip -p output.docx word/document.xml | grep -o '<w:sectPr[^>]*>.\{0,20\}'
# want: <w:sectPr ...><w:bidi/><w:pgSz .../>
# a sectPr going straight to <w:pgSz/> means the flag was dropped
```

**What section bidi actually controls** (measured, LibreOffice render):
it sets the section's BASE direction, which every element without its own
explicit direction inherits. A table with no `bidiVisual` renders its first
column on the LEFT without section bidi, and on the RIGHT with it — a silent
column-order reversal. Paragraphs and runs that DO carry their own
`bidirectional`/`rightToLeft` flags render correctly either way, so a
fully-flagged document may look fine and still be a trap: the first element
someone adds later without flags inherits the wrong direction.

Treat section bidi as the safety net, not the mechanism: set it, verify it in
the XML, AND set the per-paragraph/run/table flags. Belt and braces, because
each covers what the other misses.

**Patch it post-generation when the library drops it** — language-agnostic,
works on any .docx from any toolchain:

```python
import zipfile, re, shutil

def force_section_bidi(docx_path):
    """Insert <w:bidi/> as the first child of every <w:sectPr>. Idempotent."""
    tmp = docx_path + '.tmp'
    zin = zipfile.ZipFile(docx_path)
    items = {n: zin.read(n) for n in zin.namelist()}
    zin.close()
    xml = items['word/document.xml'].decode('utf-8')
    xml = re.sub(r'(<w:sectPr[^>]*>)(?!<w:bidi/>)', r'\1<w:bidi/>', xml)
    items['word/document.xml'] = xml.encode('utf-8')
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for n, d in items.items():
            zout.writestr(n, d)
    shutil.move(tmp, docx_path)
    return xml.count('<w:sectPr')
```

Node equivalent if you're in docx-js: same regex over `word/document.xml`
using `adm-zip` (`zip.readAsText` → replace → `zip.updateFile` → `writeZip`).
The `(?!<w:bidi/>)` guard keeps it safe to run twice.

### 1.6 Document default styles

```javascript
styles: {
  default: {
    document: {
      run: {
        font: { name: "Vazirmatn", hint: "cs" },
        size: 22,            // 11pt — half-points
        rightToLeft: true,
      },
      paragraph: {
        spacing: { line: 312 },   // ≈1.3 lines; Persian needs ≥1.3, tight leading clips
        bidirectional: true,
      },
    },
  },
}
```

---

## 2. Divider / full-bleed pages (OPTIONAL — only if the design calls for them)

This whole section is a technique, not a recommendation. Plain documents need
no divider pages. Build them only when the user's design or brand asks for
full-bleed color pages; otherwise skip §2 entirely.

Full-color divider pages must not show the running header/footer. Headers
inherit from the previous section unless you override with an *empty* header:

```javascript
const emptyPara = [new Paragraph({
  spacing: { before: 0, after: 0, line: 1, lineRule: "exact" },
  children: [new TextRun({ text: "", size: 1 })]
})];
const emptyHeader = {
  first: new Header({ children: emptyPara }),
  default: new Header({ children: emptyPara })
};
const emptyFooter = {
  first: new Footer({ children: emptyPara }),
  default: new Footer({ children: emptyPara })
};

sections.push({
  properties: {
    page: { margin: { top: 0, bottom: 0, left: 0, right: 0 } },
    bidi: true,
    titlePage: true,  // ← required for the empty first-page header to apply
  },
  headers: emptyHeader,
  footers: emptyFooter,
  children: buildDivider(...)
});
```

### White bars on dark pages (LibreOffice)

LibreOffice enforces a minimum header/footer margin, leaving white strips on
full-bleed dark pages. Fix in PDF post-processing with PyMuPDF — paint the
background color over the strips (set `BG` to the page's own color):

```python
import fitz  # PyMuPDF

BG = (r/255, g/255, b/255)  # set to the divider page's own background color

def fix_white_bars(pdf_path, is_dark_bg_page):
    doc = fitz.open(pdf_path)
    for page in doc:
        if is_dark_bg_page(page.get_text()):   # detect by known divider text
            r, over, bar, edge = page.rect, 5, 85, 5
            for box in [
                fitz.Rect(-over, -over, r.width + over, bar),                      # top
                fitz.Rect(-over, r.height - bar, r.width + over, r.height + over), # bottom
                fitz.Rect(-over, -over, edge, r.height + over),                    # left
                fitz.Rect(r.width - edge, -over, r.width + over, r.height + over), # right
            ]:
                page.draw_rect(box, color=BG, fill=BG, width=0)
    tmp = pdf_path + ".tmp"
    doc.save(tmp, deflate=True); doc.close()
    import os; os.replace(tmp, pdf_path)
```

---

## 3. Pagination

Four failure modes: orphan headings, split cards, blank pages, mid-sentence
breaks. All preventable at generation time.

### 3.1 No orphan headings

Every heading paragraph gets `keepNext` (stays with following content) and
`keepLines` (its own lines don't split):

```javascript
function sectionHeading(text) {
  return new Paragraph({
    alignment: AlignmentType.START,
    bidirectional: true,
    spacing: { before: 480, after: 280, line: 600, lineRule: "atLeast" },
    keepNext: true,
    keepLines: true,
    // border/color OPTIONAL and neutral — omit for plain output; set only
    // from the user's brief or brand. Structure is what matters here.
    children: [
      fa("•  ", { size: 32, bold: true }),   // • verified in Vazirmatn; ▪ is NOT
      fa(text, { size: 36, bold: true }),
    ],
  });
}
```

Apply to every heading level, FAQ questions (keep with their answer), and
workflow-step titles (keep with their description).

### 3.2 Unsplittable cards

Wrap each card/box in a single-cell table with `cantSplit` — if it doesn't fit,
the whole card moves to the next page instead of tearing in half:

```javascript
const cardChildren = [
  new Paragraph({ /* card title */ }),
  new Paragraph({ /* description */ }),
  new Paragraph({ /* price */ }),
  new Table({ /* module list */ }),
  new Paragraph({ /* delivery time */ }),
];

items.push(new Table({
  width: { size: 100, type: WidthType.PERCENTAGE },
  borders: allNoBorders,
  rows: [new TableRow({
    cantSplit: true,  // ← the whole card stays together
    children: [new TableCell({
      width: { size: 100, type: WidthType.PERCENTAGE },
      borders: allNoBorders,
      margins: { top: 0, bottom: 0, left: 0, right: 0 },
      children: cardChildren,
    })],
  })],
}));
```

Caveat: a card taller than one page will overflow — keep cards under ~¾ page.

### 3.3 No blank pages

Two causes. First, separators added after the *last* item:

```javascript
for (let i = 0; i < list.length; i++) {
  items.push(buildCard(list[i]));
  if (i < list.length - 1) {          // ← separator only BETWEEN items
    items.push(new Paragraph({
      spacing: { before: 100, after: 0 },
      // separator line optional; neutral grey placeholder if used at all
      border: { bottom: { style: BorderStyle.SINGLE, size: 3, color: "CCCCCC", space: 2 } },
      children: [new TextRun({ text: "" })],
    }));
  }
}
```

Second, manual `PageBreak` right before a section break:

```javascript
// ❌ empty paragraph + PageBreak at section end = blank page
items.push(new Paragraph({ children: [new TextRun({ text: "" })] }));
items.push(new Paragraph({ children: [new PageBreak()] }));

// ✅ a new section already starts a new page — no PageBreak needed
```

### 3.4 Paragraph integrity

```javascript
// Important/short paragraphs: don't strand them
new Paragraph({ keepNext: true, keepLines: true, /* ... */ });

// FAQ: question stays with answer
items.push(new Paragraph({
  keepNext: true, keepLines: true,
  children: [fa("۱. ", { bold: true }), fa(question, { bold: true })],
}));
items.push(new Paragraph({ children: [fa(answer)] }));
```

### 3.5 Multi-page data tables

```javascript
new TableRow({ tableHeader: true, cantSplit: true, children: headerCells }); // header repeats per page
new TableRow({ cantSplit: true, children: dataCells });                      // rows never split
```

---

## 4. Fonts and PDF conversion

1. Install fonts BEFORE converting (else LibreOffice substitutes silently):
   ```bash
   bash scripts/install_fonts.sh && fc-list | grep -i vazir
   ```
2. Convert: `soffice --headless --convert-to pdf output.docx`
3. Post-process white bars if you have full-bleed pages (§2).
4. Verify (§5).

Persian sizing guidance: body 11–12pt, line spacing ≥1.3 (`line: 312+`);
headings need `lineRule: "atLeast"` with generous values — Persian ascenders/
descenders clip in tight exact line heights.

---

## 5. Verification checklist (run every time)

`python3 scripts/verify_pdf.py output.pdf --expect-font Vazirmatn` automates
these; the manual equivalents:

```bash
# 1. Near-empty pages (orphaned headings / stray breaks)
pdftotext -layout output.pdf check.txt
python3 - <<'EOF'
pages = open('check.txt').read().split('\x0c')
for i, p in enumerate(pages, 1):
    lines = [l.strip() for l in p.split('\n') if l.strip()]
    content = [l for l in lines if not l.isdigit()]   # drop bare page numbers
    if len(content) < 3 and i < len(pages):
        print(f'page {i}: possibly empty ({len(content)} content lines)')
EOF

# 2. Template leaks
grep -iE "undefined|NaN|null" check.txt

# 3. Fonts actually embedded (every row should say your font, emb=yes;
#    any DejaVu/Liberation row = fallback happened somewhere)
pdffonts output.pdf

# 4. Page count sanity
python3 -c "from pypdf import PdfReader; print(len(PdfReader('output.pdf').pages))"
```

Then open the PDF (or render pages to PNG with PyMuPDF and *look*): right
alignment on every page, no orphan headings, no split cards, digits Persian.

---

## 6. python-docx equivalents

python-docx has no first-class RTL API; set the OOXML elements directly.

```python
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

def _set(el, parent):
    parent.append(el); return el

def rtl_paragraph(p):
    """bidi paragraph; leave w:jc unset (bidi default start = visual right),
    or set start explicitly. NEVER set alignment RIGHT on a bidi paragraph."""
    pPr = p._p.get_or_add_pPr()
    if pPr.find(qn('w:bidi')) is None:
        bidi = OxmlElement('w:bidi'); bidi.set(qn('w:val'), '1'); pPr.append(bidi)
    jc = pPr.find(qn('w:jc'))
    if jc is None:
        jc = _set(OxmlElement('w:jc'), pPr)
    jc.set(qn('w:val'), 'start')

def fa_run(p, text, font='Vazirmatn', size=11, bold=False):
    run = p.add_run(text)
    run.bold = bold
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts')) or _set(OxmlElement('w:rFonts'), rPr)
    for attr in ('w:ascii', 'w:hAnsi', 'w:cs'):
        rFonts.set(qn(attr), font)
    _set(OxmlElement('w:rtl'), rPr)                       # complex-script run
    szCs = _set(OxmlElement('w:szCs'), rPr)               # CS size (else tiny/huge)
    szCs.set(qn('w:val'), str(int(size * 2)))
    run.font.size = Pt(size)
    if bold:
        _set(OxmlElement('w:bCs'), rPr)                    # CS bold
    return run

def rtl_table(table):
    tblPr = table._tbl.tblPr
    if tblPr.find(qn('w:bidiVisual')) is None:
        tblPr.append(OxmlElement('w:bidiVisual'))          # first col = visual right

def rtl_section(section):
    sectPr = section._sectPr
    if sectPr.find(qn('w:bidi')) is None:
        sectPr.append(OxmlElement('w:bidi'))

def keep_with_next(p):
    pPr = p._p.get_or_add_pPr()
    pPr.append(OxmlElement('w:keepNext'))
    pPr.append(OxmlElement('w:keepLines'))

def cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:cantSplit'))

def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = OxmlElement('w:tblHeader'); tblHeader.set(qn('w:val'), 'true')
    trPr.append(tblHeader)
```

Notes that bite in python-docx specifically:
- `w:szCs` matters: without it, complex-script text ignores your size.
- `w:bCs` matters: bold Persian needs it, or only Latin runs embolden.
- The unsplittable-card trick is identical: 1×1 table + `cant_split(row)`.
- Same digits/symbols/verification rules as above — they're format rules,
  not library rules.

### 6.1 Three failures the per-paragraph helpers do NOT fix

Setting bidi on every paragraph you create still leaves three holes, because
Word/LibreOffice pull from `styles.xml` and `numbering.xml`, which python-docx
generates from a Latin default template. All three are verified failures, not
theory: without the fix below, a test document rendered `.1` (Latin digit,
wrong side) for list items, a blue Heading nobody asked for, and pulled DejaVu +
OpenSymbol into the PDF. With it: Persian «۱.», black heading, Vazirmatn only.

**Run this once, right after `Document()`, before adding content:**

```python
from docx.shared import Pt, RGBColor

def persianize_styles(doc, font='Vazirmatn', size=11):
    """Fix the document-wide defaults python-docx inherits from its Latin template.
    Without this: Latin list numbers, Word's blue headings, DejaVu fallback."""
    st = doc.styles['Normal']
    st.font.name = font
    st.font.size = Pt(size)
    rPr = st.element.get_or_add_rPr()
    rF = rPr.find(qn('w:rFonts'))
    if rF is None:
        rF = _set(OxmlElement('w:rFonts'), rPr)
    for a in ('w:ascii', 'w:hAnsi', 'w:cs'):
        rF.set(qn(a), font)                       # cs = the Persian-shaping slot
    _set(OxmlElement('w:rtl'), rPr)
    _set(OxmlElement('w:szCs'), rPr).set(qn('w:val'), str(int(size * 2)))
    _set(OxmlElement('w:bidi'), st.element.get_or_add_pPr())

    # Built-in Heading styles: Persian font, bidi, and NO inherited color.
    # Word's Heading 1-4 default to blue — an accent the user never asked for.
    for i in range(1, 5):
        try:
            h = doc.styles[f'Heading {i}']
        except KeyError:
            continue
        h.font.name = font
        h.font.color.rgb = RGBColor(0, 0, 0)      # neutral; see SKILL.md visual neutrality
        hr = h.element.get_or_add_rPr()
        hf = hr.find(qn('w:rFonts'))
        if hf is None:
            hf = _set(OxmlElement('w:rFonts'), hr)
        for a in ('w:ascii', 'w:hAnsi', 'w:cs'):
            hf.set(qn(a), font)
        _set(OxmlElement('w:rtl'), hr)
        _set(OxmlElement('w:bidi'), h.element.get_or_add_pPr())
```

**Numbered and bulleted lists: do NOT use the built-in list styles.**
`doc.add_paragraph(style='List Number')` writes numbering into `numbering.xml`,
which carries no bidi and renders Latin `1.` on the wrong side; the `List
Bullet` glyph comes from OpenSymbol and drags a fallback font into the PDF.
Number manually instead — the marker becomes a normal Persian run you control:

```python
FA_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
to_fa = lambda n: str(n).translate(str.maketrans("0123456789", FA_DIGITS))

for i, item in enumerate(items, 1):
    p = rtl_paragraph(doc.add_paragraph())
    fa_run(p, f"{to_fa(i)}.  ")     # ۱.  ۲.  ۳. — stays RTL, right side
    fa_run(p, item)

for item in bullets:
    p = rtl_paragraph(doc.add_paragraph())
    fa_run(p, "•  ")                # • verified in Vazirmatn; ▪ is NOT
    fa_run(p, item)
```
Indent with `p.paragraph_format.right_indent` (RTL side), not `left_indent`.

**Headers and footers are separate XML parts** (`header1.xml`, `footer1.xml`)
and inherit nothing from the body — apply `rtl_paragraph` + `fa_run` to each:

```python
for section in doc.sections:
    for part in (section.header, section.footer):
        for p in part.paragraphs:
            rtl_paragraph(p)
            # rebuild text through fa_run so the cs font/rtl flags exist
```
Page numbers in footers: a Latin field digit flips the line — prefer a Persian
literal, or accept Latin numerals in the footer only.

**Confirm the fix in the output, not the code:** `pdffonts out.pdf` must list
your Persian font and nothing else. A `DejaVu` or `OpenSymbol` row means a
glyph fell back — usually a list bullet or a symbol from §1.4.
`scripts/verify_pdf.py` flags this automatically.
