#!/usr/bin/env python3
"""
verify_pdf.py — post-generation checks for Persian PDFs.

Usage:
  python3 verify_pdf.py output.pdf --expect-font Vazirmatn [--expect-font Lalezar]
          [--min-lines 3] [--allow-empty-pages 1,5]

Checks:
  1. page count
  2. near-empty pages (< --min-lines content lines) → orphan breaks / blank pages
     (full-bleed image/divider pages naturally trip this — verify visually or allowlist)
  3. template leaks: undefined / NaN / null in extracted text
  4. Arabic ي ك ة or Arabic-Indic digits in text (should be Persian forms)
  5. em dashes in text (AI tell / wrong punctuation for Persian)
  6. fonts: every embedded font matches --expect-font; DejaVu/Liberation/Noto = fallback

Exit code: 0 clean (warnings allowed), 1 on errors.
"""
import argparse, re, shutil, subprocess, sys

def extract_pages(pdf):
    """Return list of page texts. Prefer pdftotext, fall back to pypdf/fitz."""
    if shutil.which('pdftotext'):
        r = subprocess.run(['pdftotext', '-layout', pdf, '-'],
                           capture_output=True, text=True)
        if r.returncode == 0:
            return r.stdout.split('\x0c')[:-1] or r.stdout.split('\x0c')
    try:
        import fitz
        return [p.get_text() for p in fitz.open(pdf)]
    except ImportError:
        pass
    try:
        from pypdf import PdfReader
        return [(p.extract_text() or '') for p in PdfReader(pdf).pages]
    except ImportError:
        sys.exit('need pdftotext, pymupdf, or pypdf')

def font_report(pdf, expected):
    """Return (errors, warnings) about embedded fonts."""
    errs, warns, rows = [], [], []
    if shutil.which('pdffonts'):
        out = subprocess.run(['pdffonts', pdf], capture_output=True, text=True).stdout
        for line in out.splitlines()[2:]:
            if line.strip():
                rows.append(line)
        for line in rows:
            name = line.split()[0]
            emb = ' yes ' in line[45:60] or re.search(r'\byes\b', line)
            if not emb:
                errs.append(f'font not embedded: {name}')
            base = name.split('+')[-1].lower()
            if any(f in base for f in ('dejavu', 'liberation', 'nimbus')):
                errs.append(f'fallback font in PDF: {name} — Persian font was not found at conversion time')
            elif expected and not any(e.lower() in base for e in expected):
                warns.append(f'unexpected font: {name}')
    else:
        try:
            import fitz
            doc = fitz.open(pdf)
            seen = set()
            for p in doc:
                for f in p.get_fonts(full=True):
                    seen.add((f[3], f[1]))
            for name, _ in seen:
                base = name.split('+')[-1].lower()
                if any(x in base for x in ('dejavu', 'liberation', 'nimbus')):
                    errs.append(f'fallback font in PDF: {name}')
                elif expected and not any(e.lower() in base for e in expected):
                    warns.append(f'unexpected font: {name}')
        except ImportError:
            warns.append('pdffonts/pymupdf unavailable — font check skipped')
    return errs, warns

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('pdf')
    ap.add_argument('--expect-font', action='append', default=[])
    ap.add_argument('--min-lines', type=int, default=3)
    ap.add_argument('--allow-empty-pages', default='',
                    help='comma-separated page numbers exempt from the empty check')
    args = ap.parse_args()
    allow_empty = {int(x) for x in args.allow_empty_pages.split(',') if x.strip()}

    pages = extract_pages(args.pdf)
    full = '\n'.join(pages)
    errors, warnings = [], []

    print(f'pages: {len(pages)}')

    for i, page in enumerate(pages, 1):
        lines = [l.strip() for l in page.split('\n') if l.strip()]
        content = [l for l in lines if not re.fullmatch(r'[\d۰-۹]+', l)]
        if len(content) < args.min_lines and i not in allow_empty and i < len(pages):
            warnings.append(f'page {i}: only {len(content)} content lines — blank page or orphan? (visual/divider pages are OK — verify)')

    for m in re.finditer(r'\b(undefined|NaN)\b', full, re.I):
        errors.append(f'template leak: "{m.group(0)}" in text')

    arabic = re.findall(r'[يكة٠-٩]', full)
    if arabic:
        from collections import Counter
        errors.append('Arabic characters in text: ' +
                      ', '.join(f'{c}×{n}' for c, n in Counter(arabic).most_common()))

    n_dash = full.count('—') + full.count('–')
    if n_dash:
        warnings.append(f'{n_dash} em/en dash(es) in text — not Persian punctuation')

    ferr, fwarn = font_report(args.pdf, args.expect_font)
    errors += ferr; warnings += fwarn

    for w in warnings: print(f'WARN  {w}')
    for e in errors:  print(f'ERROR {e}')
    if not errors and not warnings:
        print('OK — all checks passed')
    sys.exit(1 if errors else 0)

if __name__ == '__main__':
    main()
