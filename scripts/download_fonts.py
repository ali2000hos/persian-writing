#!/usr/bin/env python3
"""
download_fonts.py — fetch Persian font families into assets/fonts/.

NOTE: requires direct access to github.com. In sandboxed/allowlisted
environments (e.g. Cowork) this WILL fail with 403 — that is expected: use the
fonts already bundled in assets/fonts/, or ask the user to download the release
zip on their machine and drop it into the project folder.

Usage:
  python3 download_fonts.py sahel shabnam        # specific families
  python3 download_fonts.py --all
  python3 download_fonts.py --list
"""
import argparse, io, sys, zipfile
from pathlib import Path
from urllib.request import urlopen, Request

# Pinned releases (update versions here when upstream releases)
FAMILIES = {
    'vazirmatn': 'https://github.com/rastikerdar/vazirmatn/releases/download/v33.003/vazirmatn-v33.003.zip',
    'shabnam':   'https://github.com/rastikerdar/shabnam-font/releases/download/v5.0.1/shabnam-font-v5.0.1.zip',
    'sahel':     'https://github.com/rastikerdar/sahel-font/releases/download/v3.4.0/sahel-font-v3.4.0.zip',
    'samim':     'https://github.com/rastikerdar/samim-font/releases/download/v4.0.5/samim-font-v4.0.5.zip',
    'parastoo':  'https://github.com/rastikerdar/parastoo-font/releases/download/v2.0.1/parastoo-font-v2.0.1.zip',
    'tanha':     'https://github.com/rastikerdar/tanha-font/releases/download/v0.9/tanha-font-v0.9.zip',
    'gandom':    'https://github.com/rastikerdar/gandom-font/releases/download/v0.6/gandom-font-v0.6.zip',
    # single TTF, served from the google/fonts repo
    'lalezar':   'https://raw.githubusercontent.com/google/fonts/main/ofl/lalezar/Lalezar-Regular.ttf',
}

DEST = Path(__file__).resolve().parent.parent / 'assets' / 'fonts'

def fetch(name, url):
    print(f'{name}: downloading …')
    req = Request(url, headers={'User-Agent': 'persian-writing-skill'})
    try:
        data = urlopen(req, timeout=60).read()
    except Exception as e:
        print(f'{name}: FAILED ({e}).\n'
              f'  If you are in a sandboxed environment, GitHub is likely blocked.\n'
              f'  Download manually: {url}\n'
              f'  and place the .ttf files in {DEST}', file=sys.stderr)
        return False
    DEST.mkdir(parents=True, exist_ok=True)
    if url.endswith('.ttf'):
        (DEST / url.rsplit('/', 1)[-1]).write_bytes(data)
        print(f'{name}: 1 file → {DEST}')
        return True
    n = 0
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for info in z.infolist():
            fn = info.filename
            if fn.lower().endswith('.ttf') and '__MACOSX' not in fn and '/fd/' not in fn.lower():
                (DEST / Path(fn).name).write_bytes(z.read(info))
                n += 1
    print(f'{name}: {n} ttf file(s) → {DEST}')
    return n > 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('families', nargs='*', choices=[*FAMILIES, []], help='family names')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--list', action='store_true')
    args = ap.parse_args()
    if args.list:
        print('\n'.join(FAMILIES)); return
    targets = list(FAMILIES) if args.all else args.families
    if not targets:
        ap.error('name families, or use --all / --list')
    ok = all([fetch(t, FAMILIES[t]) for t in targets])
    sys.exit(0 if ok else 1)

if __name__ == '__main__':
    main()
