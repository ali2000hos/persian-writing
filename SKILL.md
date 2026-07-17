---
name: persian-writing
description: >
  Write natural, human-sounding Persian (Farsi) and build correct right-to-left
  Persian deliverables. Use for ANY task involving Persian text or an Iranian
  audience: writing, editing, translating, humanizing, SEO content and
  copywriting (سئو، کپی‌رایتینگ، لندینگ), academic papers/theses, and Persian
  output in Word/.docx, PDF, PowerPoint, HTML, Excel, images/posters, emails,
  social posts. Covers register detection (رسمی/اداری/محاوره/علمی — errors here
  are costly), Persian AI-tell removal, orthography (نیم‌فاصله/ZWNJ، اعداد
  فارسی، «گیومه»), cleanup and spell-check (ویرایش، پاکسازی — bundled
  paknevis+davat toolkit), RTL layout/pagination fixes, and Persian fonts
  (Vazirmatn bundled). Trigger whenever you see Persian/Arabic script or words
  like فارسی, Farsi, Persian, Iran, RTL, راست‌چین, نیم‌فاصله, ویرایش, مقاله,
  پایان‌نامه, سئو, کپشن, Vazirmatn — even if the user never mentions this skill.
metadata:
  version: 1.0.0
license: MIT (bundled fonts under SIL OFL)
compatibility: >
  Any agent that reads Markdown skills (Claude, Claude Code, Cursor, Codex,
  custom harnesses; chat-only AIs via universal/persian-writing-universal.md).
  Scripts: Python 3.8+ stdlib only. docx/pptx→PDF conversion: LibreOffice +
  installed fonts. PDF checks: poppler-utils, pypdf, or PyMuPDF (any one).
---

# Persian Writing & RTL Documents

Two failure modes make Persian output look machine-made, and they are independent:

1. **The prose sounds like AI.** Technically correct, but stiff, کتابی, inflated —
   no Iranian would write it that way.
2. **The layout betrays the text.** Persian rendered left-aligned, Arabic ي/ك glyphs,
   Latin digits breaking RTL flow, headings orphaned at page bottoms, fonts falling
   back to DejaVu.

Fixing one without the other still produces something a native reader screenshots
and laughs at. This skill fixes both. Work through the two checklists below, and
read the reference file for your output format before generating anything.

## Step 0: Route by task

| Task | Read |
|---|---|
| Any Persian prose (always) | `references/writing-style.md` |
| Mechanical correctness (always) | `references/orthography.md` |
| Academic: paper, thesis, report, مقاله/پایان‌نامه | `references/academic.md` |
| SEO content, blog for search, landing/ad copy, کپشن فروش | `references/seo-copywriting.md` |
| Cleanup/normalize/spell-check existing text (ویرایش، پاکسازی) | `references/cleanup/paknevis-rules.md` + `usage-patterns.md` |
| Choosing/embedding fonts | `references/fonts.md` |
| Word/.docx or docx→PDF | `references/docx-pdf.md` |
| PowerPoint/.pptx | `references/pptx.md` |
| HTML, email templates, HTML→PDF | `references/html-css.md` |
| Images/posters (PIL), new PDFs (reportlab), Excel | `references/format-skills-fa.md` |

**Visual neutrality — read before copying any code example.** This skill styles
NOTHING. It governs direction, spacing, fonts-for-shaping and text — never
colors, accent bars, card backgrounds, or a house look. Every hex, border, and
fill in the code examples is a stand-in written in plain grey/black; they exist
to show WHERE a property goes, not what value to use. Default output is black
text on default background, no accent color. Take colors and visual form ONLY
from: the user's explicit request, an attached brand/theme skill, or an input
template being matched. Absent those, do not invent a palette and do not carry
one over from example to example — unstyled is the correct default, and a
surprise purple heading is a bug.

This skill composes with the general docx/pptx/pdf skills: those handle file
mechanics; this one overrides and extends them for Persian. When both disagree
about RTL behavior, this skill wins — its rules come from debugging real Persian
documents. If another active skill or the user specifies particular fonts or
colors, those win on aesthetics; this skill still governs RTL mechanics and
orthography. This skill itself is brand-neutral: colors in the code examples are
placeholders, and Vazirmatn is just the default font, not a requirement.

## Writing: the five-second summary

Full guide in `references/writing-style.md`. The core moves:

1. **Detect register before writing a word — a register error is the costliest
   mistake this skill can make.** Follow the 6-step detection procedure in
   writing-style.md Part 1. The core rules: classify the DELIVERABLE, not the
   tone the user typed in (a casual «یه پروپوزال بنویس» still needs a formal
   proposal); when the text goes to a third party and signals conflict, ask
   ONE short question instead of guessing; no signal at all → formal-but-human.
   - Proposal, invoice, report, official email, website copy → **formal-but-human**:
     full written forms (می‌شود نه میشه), شما, zero slang — but است نه می‌باشد,
     short sentences, concrete claims. Human ≠ خودمونی: proposals/contracts keep
     formal vocabulary (no «جور است»-style idioms); warmth comes from clarity,
     numbers, and one warm closing line (writing-style.md, "warmth trap").
   - نامه اداری → formal + letter conventions (honorifics, «با سلام و احترام؛»
     — writing-style.md).
   - Instagram/Telegram, chat, friendly email → **colloquial written Persian**
     (محاوره‌نویسی): میشه، می‌خوام، رو، particles like دیگه/که/مگه.
   - Blog, newsletter → between: written forms, warm direct voice.
   - Paper, thesis, university report → **academic** (نگارش علمی): measured,
     hedged, passive acceptable, zero تعارف — read `references/academic.md`.
   - SEO/sales copy → register per artifact as above, plus `references/seo-copywriting.md`.
2. **Ban the bureaucratic tells:** می‌باشد، لازم به ذکر است، در راستای،
   از اهمیت ویژه‌ای برخوردار است، نقش بسزایی ایفا می‌کند.
3. **Ban the AI tells:** em dashes (—), rule-of-three triads (سریع، آسان و مطمئن),
   نه تنها ... بلکه, tacked-on «که نشان‌دهنده‌ی ... است», vague «کارشناسان معتقدند»,
   generic «در دنیای امروز» openers, «در نهایت می‌توان گفت» closers.
4. **The native test:** would an Iranian screenshot this as «متن هوش مصنوعی»?
   If yes, rewrite before delivering.
5. **Numbers, punctuation, spacing** must be Persian — next section.

## Orthography: non-negotiables

Full rules in `references/orthography.md`. These six apply to every deliverable:

1. **ZWNJ (نیم‌فاصله, U+200C)** — می‌شود نه می شود؛ کتاب‌ها نه کتاب ها؛
   بزرگ‌تر، خانه‌ام، به‌عنوان. In code: `‌` or HTML `&zwnj;`.
2. **Persian characters only:** ی (U+06CC) not ي، ک (U+06A9) not ك.
3. **Persian digits** ۰۱۲۳۴۵۶۷۸۹ inside Persian text. Latin digits stay in URLs,
   emails, codes, version numbers. Never Arabic-Indic ٤٥٦ forms.
4. **Persian punctuation:** ، ؛ ؟ and «گیومه» for quotes. No space before, one after.
5. **No em/en dashes** in Persian prose — use «،» or restructure.
6. **Never letter-space Persian** (it breaks letter joining), never fake bold/italic.

Two scripts enforce this mechanically — use both before delivering Persian text:

```bash
# 1. FIX: paknevis-style editorial pass (ZWNJ, chars, digits, punctuation, گیومه)
python3 scripts/persian_cleanup.py --edit --in text.md --out text.md
# 2. LINT: report what still needs contextual judgment (dashes, میشود forms,
#    fake tanvin, register issues) — fix these by hand
python3 scripts/fa_lint.py --check text.md
```

`persian_cleanup.py` is a full toolkit (paknevis + davat merged): aggressive
cleaning for NLP (`--preset persian`), single functions (`--fn convert_digits`),
spell-check against the bundled 453K-word frequency dictionary
(`--edit --spellcheck`), custom pipelines. Persian «ویرایش» requests → `--edit`
(conservative, content preserved); «پاکسازی/نرمالایز» → `--preset persian`
(strips links/mentions/emojis). Details: `references/cleanup/`. Note: `--edit`
applies the خانهٔ ezafe style; drop `fix_ezafe` from `--steps` to keep خانه‌ی.

## Fonts

Bundled in `assets/fonts/` (SIL OFL — free for commercial use):

- **Vazirmatn** — the default for everything: body, UI, documents. 9 weights.
- **Lalezar** — display font for headlines, covers, posters. One weight; never body.

Other families (Shabnam, Sahel, Samim, Parastoo, Tanha, Gandom) and pairing advice:
`references/fonts.md`. In offline sandboxes only bundled fonts exist —
`scripts/download_fonts.py` works only where GitHub is reachable.

**Before any docx→PDF or pptx→PDF conversion, install the fonts:**

```bash
bash scripts/install_fonts.sh   # copies assets/fonts → ~/.fonts, runs fc-cache
fc-list | grep -i vazir         # verify — else LibreOffice silently falls back
```

Skipping this is the #1 cause of broken Persian PDFs: conversion "succeeds" but
every glyph is DejaVu tofu or disconnected letters.

## Documents: the rules that always apply

Format-specific recipes live in the reference files. The universal ones:

1. **RTL means START, not RIGHT.** In OOXML, with `bidirectional: true`,
   `AlignmentType.RIGHT` renders at the *visual left*. Always align `START`.
2. Every Persian run: `rightToLeft: true` + font with `hint: "cs"` (Complex Script).
3. Every section: `bidi: true`. Tables that must flow right-to-left:
   `visuallyRightToLeft: true`.
4. **Persian digits in numbered content** — a Latin "1." flips the paragraph LTR.
5. **Pagination:** headings get `keepNext + keepLines` (no orphan headings);
   cards/boxes go inside a single-cell table with `cantSplit: true` (never split
   across pages); no separator after the last list item; no stray `PageBreak`
   before a section break (blank pages).
6. **Symbols:** Persian fonts miss many glyphs. In bundled Vazirmatn/Lalezar
   only • and · are verified; ▪ ■ ✓ ✕ ● ◆ ⊙ fall back to DejaVu. For any other
   symbol/font, check the cmap first (fonts.md shows how).

## Verify before delivering

Never hand over a Persian PDF you haven't checked:

```bash
python3 scripts/verify_pdf.py output.pdf --expect-font Vazirmatn
```

It checks: near-empty pages, "undefined"/template leaks, non-embedded or fallback
fonts, Arabic ي/ك in extracted text, and page count. Fix every warning, regenerate,
re-verify. For prose, re-read your final text against the native test — one pass of
`persian_cleanup.py --edit` + `fa_lint.py --check` plus one honest read-aloud
catches most disasters.

## Files

```
persian-writing/
├── SKILL.md                    ← you are here
├── references/
│   ├── writing-style.md        ← registers, Persian AI tells, colloquial patterns
│   ├── academic.md             ← نگارش علمی: papers, theses, citations, formulas
│   ├── orthography.md          ← ZWNJ, characters, digits, punctuation, ezafe
│   ├── cleanup/                ← paknevis rules, davat API, usage patterns
│   ├── fonts.md                ← catalog, personalities, pairings, embedding
│   ├── seo-copywriting.md      ← Persian SEO writing + کپی‌رایتینگ
│   ├── docx-pdf.md             ← RTL docx recipes, pagination, PDF post-processing
│   ├── pptx.md                 ← RTL PowerPoint via python-pptx / html2pptx
│   ├── html-css.md             ← RTL web, mixed-direction text, print CSS
│   └── format-skills-fa.md     ← PIL posters, reportlab PDFs, Excel RTL
├── scripts/
│   ├── persian_cleanup.py      ← FIX: edit/clean/normalize/spell-check (paknevis+davat)
│   ├── fa_lint.py              ← LINT: report issues needing contextual judgment
│   ├── verify_pdf.py           ← post-generation PDF checks
│   ├── install_fonts.sh        ← bundled fonts → ~/.fonts (run before PDF export)
│   └── download_fonts.py       ← fetch extra families (needs GitHub access)
└── assets/
    ├── fonts/                  ← Vazirmatn + Lalezar TTFs
    └── persian_words.txt       ← 453K-word frequency dictionary (spell-check)
```
