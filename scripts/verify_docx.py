#!/usr/bin/env python3
"""
verify_docx.py — check a .docx for Persian/RTL correctness BEFORE converting to PDF.

Catches the failures that are invisible in source code and only show up when
someone opens the file: dropped section bidi, Latin list numbering, missing
complex-script fonts, Arabic characters, unstyled headings.

Usage:
  python3 verify_docx.py file.docx [--expect-font Vazirmatn] [--fix]

  --fix   repair what is safely repairable (inserts <w:bidi/> into every
          <w:sectPr>), then re-check.

Exit code: 0 clean (warnings allowed), 1 if errors found.
"""
import argparse, re, shutil, sys, zipfile

W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def read_parts(path):
    with zipfile.ZipFile(path) as z:
        return {n: z.read(n) for n in z.namelist()}


def write_parts(path, items):
    tmp = path + '.tmp'
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as out:
        for n, d in items.items():
            out.writestr(n, d)
    shutil.move(tmp, path)


def force_section_bidi(items):
    """Insert <w:bidi/> as first child of every <w:sectPr>. Returns count fixed."""
    xml = items['word/document.xml'].decode('utf-8')
    patched, n = re.subn(r'(<w:sectPr[^>]*>)(?!<w:bidi/>)', r'\1<w:bidi/>', xml)
    items['word/document.xml'] = patched.encode('utf-8')
    return n


def check(path, expect_fonts):
    items = read_parts(path)
    doc = items['word/document.xml'].decode('utf-8')
    errors, warnings, notes = [], [], []

    # 1. section bidi, in the schema-correct position
    sects = re.findall(r'<w:sectPr[^>]*>(.{0,40})', doc, re.S)
    bad = [s for s in sects if not s.lstrip().startswith('<w:bidi')]
    notes.append(f'sections: {len(sects)}')
    if bad:
        errors.append(f'{len(bad)}/{len(sects)} <w:sectPr> missing <w:bidi/> as first child '
                      f'— base direction is LTR; tables without bidiVisual will reverse. '
                      f'Re-run with --fix')

    # 2. paragraph-level bidi coverage
    n_par = doc.count('<w:p ') + doc.count('<w:p>')
    n_bidi = len(re.findall(r'<w:bidi\b', doc))
    n_rtl = len(re.findall(r'<w:rtl\b', doc))
    notes.append(f'paragraphs: {n_par} | w:bidi: {n_bidi} | w:rtl runs: {n_rtl}')
    if n_par and n_bidi < n_par * 0.5:
        warnings.append(f'only {n_bidi} of ~{n_par} paragraphs carry <w:bidi> — '
                        f'unflagged paragraphs inherit section direction')
    if n_rtl == 0:
        errors.append('no <w:rtl/> runs — Persian text will not shape as complex script')

    # 3. RIGHT alignment on bidi paragraphs (the classic trap)
    n_right = len(re.findall(r'<w:jc w:val="(?:right|end)"', doc))
    if n_right:
        warnings.append(f'{n_right} paragraph(s) use jc=right/end — in RTL this means the '
                        f'VISUAL LEFT. Use w:val="start"')

    # 4. complex-script font on runs
    cs = re.findall(r'w:cs="([^"]+)"', doc)
    if not cs:
        errors.append('no w:cs (complex-script) font set — Word/LibreOffice will pick '
                      'its own font for Persian')
    elif expect_fonts:
        wrong = {f for f in cs if not any(e.lower() in f.lower() for e in expect_fonts)}
        if wrong:
            warnings.append(f'unexpected complex-script font(s): {", ".join(sorted(wrong))}')
    if '<w:szCs' not in doc:
        warnings.append('no <w:szCs> — complex-script text may ignore your font sizes')

    # 5. built-in list numbering (renders Latin digits, wrong side, OpenSymbol bullets)
    if '<w:numPr>' in doc:
        errors.append('document uses built-in list numbering (<w:numPr>) — numbering.xml '
                      'carries no bidi: renders Latin "1." on the wrong side and pulls in '
                      'a fallback bullet font. Write markers as runs («۱.  », «•  »)')

    # 6. Arabic characters / Latin digits in body text
    body = ' '.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', doc))
    ar = sorted(set(re.findall(r'[يكة٠-٩]', body)))
    if ar:
        errors.append(f'Arabic characters in text: {" ".join(ar)} — use ی ک ه and Persian digits')
    if re.search(r'[؀-ۿ]', body):
        # ASCII 0-9 only; Persian ۰-۹ are fine. Skip versions/URLs/emails.
        latin = [d for d in re.findall(r'(?<![\w./@-])[0-9][0-9,]*(?![\w./@-])', body)
                 if not re.fullmatch(r'[0-9]+(\.[0-9]+)+', d)]
        if latin:
            warnings.append(f'Latin digits in Persian text: {", ".join(latin[:5])} — '
                            f'use ۰-۹ (keep Latin in URLs/versions/codes)')

    # 7. heading styles: Persian font + no inherited color
    styles = items.get('word/styles.xml', b'').decode('utf-8', 'ignore')
    if styles:
        # Only judge styles the document actually uses — an unused Heading 9 is noise.
        used = set(re.findall(r'<w:pStyle w:val="([^"]+)"', doc))
        nofont, colored = [], []
        for m in re.finditer(r'<w:style [^>]*w:styleId="(Heading\d)"[^>]*>(.*?)</w:style>',
                             styles, re.S):
            sid, blk = m.groups()
            if sid not in used:
                continue
            if 'w:cs=' not in blk:
                nofont.append(sid)
            col = re.search(r'<w:color w:val="([0-9A-Fa-f]{6})"', blk)
            if col and col.group(1).lower() not in ('000000', 'auto'):
                colored.append(f'{sid} #{col.group(1)}')
        if nofont:
            warnings.append(f'heading style(s) with no complex-script font: '
                            f'{", ".join(nofont)} — Persian headings fall back to a Latin face')
        if colored:
            warnings.append(f'heading style(s) carrying a template color: {", ".join(colored)} '
                            f'— an accent nobody asked for; set black or your brief\'s color')

    # 8. headers/footers must be RTL too (separate parts)
    for name in items:
        if re.match(r'word/(header|footer)\d*\.xml', name):
            part = items[name].decode('utf-8', 'ignore')
            if re.search(r'<w:t[^>]*>[^<]*[؀-ۿ]', part) and '<w:bidi' not in part:
                warnings.append(f'{name} has Persian text but no <w:bidi> — '
                                f'headers/footers inherit nothing from the body')

    return errors, warnings, notes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('docx')
    ap.add_argument('--expect-font', action='append', default=[])
    ap.add_argument('--fix', action='store_true',
                    help='insert missing <w:bidi/> into every <w:sectPr>, then re-check')
    args = ap.parse_args()

    if args.fix:
        items = read_parts(args.docx)
        n = force_section_bidi(items)
        if n:
            write_parts(args.docx, items)
            print(f'FIXED  inserted <w:bidi/> into {n} <w:sectPr>')
        else:
            print('nothing to fix: all sections already have <w:bidi/>')

    errors, warnings, notes = check(args.docx, args.expect_font)
    for n in notes:
        print(f'       {n}')
    for w in warnings:
        print(f'WARN   {w}')
    for e in errors:
        print(f'ERROR  {e}')
    if not errors and not warnings:
        print('OK — all RTL checks passed')
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
