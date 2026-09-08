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
    """Rewrite the package. Two rules keep Word happy:
    [Content_Types].xml must be the first entry, and nothing else may be
    reordered or dropped. Writes to a temp file and only replaces the original
    after the result opens cleanly, so a failed repair can't destroy the input.
    """
    tmp = path + '.tmp'
    names = list(items)
    names.sort(key=lambda n: n != '[Content_Types].xml')   # Content_Types first
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as out:
        for n in names:
            out.writestr(n, items[n])
    # sanity-gate the rewrite before it replaces anything
    with zipfile.ZipFile(tmp) as check:
        if check.testzip() is not None:
            raise IOError('rewritten package failed CRC check; original left untouched')
        if check.namelist()[0] != '[Content_Types].xml':
            raise IOError('[Content_Types].xml is not the first entry; aborting')
        if len(check.namelist()) != len(names):
            raise IOError('part count changed during rewrite; aborting')
    shutil.move(tmp, path)


def force_section_bidi(items):
    """Insert <w:bidi/> as first child of every <w:sectPr>. Returns count fixed."""
    xml = items['word/document.xml'].decode('utf-8')
    patched, n = re.subn(r'(<w:sectPr[^>]*>)(?!<w:bidi/>)', r'\1<w:bidi/>', xml)
    items['word/document.xml'] = patched.encode('utf-8')
    return n


# Parts python-docx inherits from its bundled Word-for-Mac-2011 template.
# They are dead weight in a generated document and are the exact artifacts
# blamed when Word reports "the file is corrupt".
_MAC_ARTIFACTS = ('word/stylesWithEffects.xml', 'docProps/thumbnail.jpeg')


def sanitize_package(items):
    """Remove Mac-template artifacts and their references. Returns list of actions.

    Order matters: drop the parts, then strip every reference to them from
    [Content_Types].xml and the .rels files, or the result has dangling
    relationships — which is worse than the artifacts were.
    """
    actions = []
    removed = [p for p in _MAC_ARTIFACTS if p in items]
    for p in removed:
        del items[p]
        actions.append(f'removed {p}')

    if removed and '[Content_Types].xml' in items:
        ct = items['[Content_Types].xml'].decode('utf-8')
        before = ct
        for p in removed:
            ct = re.sub(r'<Override PartName="/' + re.escape(p) + r'"[^>]*/>', '', ct)
        # thumbnail.jpeg may be covered by a Default extension rather than an Override
        if 'docProps/thumbnail.jpeg' in removed and not any(
                n.lower().endswith(('.jpeg', '.jpg')) for n in items):
            ct = re.sub(r'<Default Extension="jpeg"[^>]*/>', '', ct)
        if ct != before:
            items['[Content_Types].xml'] = ct.encode('utf-8')
            actions.append('cleaned [Content_Types].xml')

    for name in list(items):
        if not name.endswith('.rels'):
            continue
        rels = items[name].decode('utf-8')
        before = rels
        for p in removed:
            target = p.split('/')[-1] if name.startswith('word/') else p
            rels = re.sub(r'<Relationship[^>]*Target="[^"]*' + re.escape(target)
                          + r'"[^>]*/>', '', rels)
        if rels != before:
            items[name] = rels.encode('utf-8')
            actions.append(f'cleaned {name}')

    # Normalise the python-docx single-quoted XML declaration to the Office form.
    for name in list(items):
        if name.endswith(('.xml', '.rels')):
            data = items[name]
            if data[:20].startswith(b"<?xml version='1.0'"):
                items[name] = data.replace(b"<?xml version='1.0' encoding='UTF-8' standalone='yes'?>",
                                           b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', 1)
    if any(items[n][:20].startswith(b'<?xml version="1.0"') for n in items
           if n.endswith('.xml')):
        actions.append('normalised XML declarations to double quotes')
    return actions


def check_integrity(path):
    """Structural validity of the OOXML package itself — the difference between
    'Word opens it' and 'Word says the file is corrupt'. Run this before the
    Persian/RTL checks: a file Word refuses to open can't be RTL-wrong yet."""
    errors, warnings = [], []
    with open(path, 'rb') as fh:
        if fh.read(4) != b'PK\x03\x04':
            return ([f'{path} is not a ZIP container — not a valid OOXML file'], [])
    try:
        z = zipfile.ZipFile(path)
    except zipfile.BadZipFile as e:
        return ([f'unreadable ZIP: {e}'], [])
    names = z.namelist()
    if z.testzip() is not None:
        errors.append(f'CRC failure in part: {z.testzip()}')
    if not names or names[0] != '[Content_Types].xml':
        errors.append('[Content_Types].xml is not the first ZIP entry — '
                      'Word may refuse the package as non-compliant')
    dupes = {n for n in names if names.count(n) > 1}
    if dupes:
        errors.append(f'duplicate parts (only the first wins): {", ".join(sorted(dupes))}')

    import xml.dom.minidom as minidom
    for n in names:
        if n.endswith(('.xml', '.rels')):
            data = z.read(n)
            try:
                minidom.parseString(data)
            except Exception as e:
                errors.append(f'malformed XML in {n}: {str(e)[:80]}')
                continue
            ctrl = {b for b in data if b < 0x20 and b not in (9, 10, 13)}
            if ctrl:
                errors.append(f'{n} contains control characters '
                              f'({", ".join(hex(c) for c in sorted(ctrl))}) — Word rejects these')
            if b'\xef\xbf\xbd' in data:
                warnings.append(f'{n} contains U+FFFD replacement chars — encoding was corrupted '
                                f'somewhere upstream; Persian text may be damaged')

    # every relationship Target must resolve to a real part
    import posixpath
    for n in names:
        if n.endswith('.rels'):
            base = n[:n.rfind('_rels/')]
            for t in re.findall(rb'Target="([^"]+)"', z.read(n)):
                t = t.decode('utf-8')
                if t.startswith(('http://', 'https://', 'mailto:', '#', 'file:')):
                    continue
                cand = posixpath.normpath(posixpath.join(base, t)).lstrip('/')
                if cand not in names and t.lstrip('/') not in names:
                    errors.append(f'dangling relationship in {n}: Target="{t}" does not exist')

    # every part must have a declared content type
    if '[Content_Types].xml' in names:
        ct = z.read('[Content_Types].xml').decode('utf-8', 'ignore')
        exts = {e.lower() for e in re.findall(r'Extension="([^"]+)"', ct)}
        overrides = set(re.findall(r'PartName="([^"]+)"', ct))
        for n in names:
            if n.endswith('/') or n == '[Content_Types].xml':
                continue
            ext = n.rsplit('.', 1)[-1].lower() if '.' in n else ''
            if ext not in exts and '/' + n not in overrides:
                errors.append(f'no content type declared for part: {n}')

    # generator artifacts that make Word (especially on Windows) complain
    for stray in ('word/stylesWithEffects.xml', 'docProps/thumbnail.jpeg'):
        if stray in names:
            warnings.append(f'stray part {stray} (Word-for-Mac artifact) — safe to remove; '
                            f'a LibreOffice round-trip drops it')
    if 'word/document.xml' in names:
        body = z.read('word/document.xml')
        # A declared-but-unused namespace is harmless; only flag prefixes in actual use.
        for pfx in (b'mo', b'mv'):
            if b'xmlns:' + pfx + b'=' in body[:400] and (b'<' + pfx + b':') in body:
                warnings.append(f'Mac-only namespace {pfx.decode()}: is used in document.xml — '
                                f'round-trip through LibreOffice to normalise')
    return errors, warnings


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
    ap.add_argument('--sanitize', action='store_true',
                    help='also strip python-docx Mac-template artifacts '
                         '(stylesWithEffects, thumbnail, Mac namespaces)')
    args = ap.parse_args()

    # Structural validity first — an unopenable file has no RTL properties to judge.
    ierr, iwarn = check_integrity(args.docx)
    for w in iwarn:
        print(f'WARN   {w}')
    if ierr:
        for e in ierr:
            print(f'ERROR  {e}')
        print('\nPackage is structurally invalid; Word will likely refuse it. '
              'Repair first (a LibreOffice round-trip fixes most cases):\n'
              f'  soffice --headless --convert-to docx --outdir <other_dir> {args.docx}\n'
              'then re-run this check on the converted file.')
        sys.exit(1)

    if args.fix or args.sanitize:
        items = read_parts(args.docx)
        actions = []
        if args.fix:
            n = force_section_bidi(items)
            actions.append(f'inserted <w:bidi/> into {n} <w:sectPr>' if n
                           else 'section bidi already present')
        if args.sanitize:
            actions += sanitize_package(items) or ['no Mac-template artifacts found']
        if any(not a.startswith(('section bidi already', 'no Mac-template')) for a in actions):
            write_parts(args.docx, items)
        for a in actions:
            print(f'FIXED  {a}')
        post, _ = check_integrity(args.docx)   # never hand back a broken file
        if post:
            for e in post:
                print(f'ERROR  after repair: {e}')
            sys.exit(1)

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
