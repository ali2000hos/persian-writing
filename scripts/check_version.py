#!/usr/bin/env python3
"""
check_version.py — verify the version number is identical everywhere.

Version strings live in four places that are easy to update separately and
then forget. A mismatch is invisible until someone installs the package and
reports a version that doesn't exist. Run this before every release.

Usage:
  python3 scripts/check_version.py            # report; exit 1 on mismatch
  python3 scripts/check_version.py --set 1.4.0  # write the same version to all
"""
import argparse, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (path, regex with one capture group for the version, template for --set)
SITES = [
    ('SKILL.md',
     re.compile(r'^(\s*version:\s*)([0-9]+\.[0-9]+\.[0-9]+)\s*$', re.M), r'\g<1>{v}'),
    ('.claude-plugin/plugin.json',
     re.compile(r'("version"\s*:\s*")([0-9]+\.[0-9]+\.[0-9]+)(")'), r'\g<1>{v}\g<3>'),
    ('scripts/persian_cleanup.py',
     re.compile(r'(__version__\s*=\s*")([0-9]+\.[0-9]+\.[0-9]+)(")'), r'\g<1>{v}\g<3>'),
]

README_ENTRY = re.compile(r'^- \*\*([0-9]+\.[0-9]+\.[0-9]+)\*\*', re.M)


def read_all():
    found = {}
    for rel, pat, _ in SITES:
        p = ROOT / rel
        if not p.exists():
            found[rel] = None
            continue
        m = pat.search(p.read_text(encoding='utf-8'))
        found[rel] = m.group(2) if m else None
    readme = ROOT / 'README.md'
    if readme.exists():
        m = README_ENTRY.search(readme.read_text(encoding='utf-8'))
        found['README.md (newest entry)'] = m.group(1) if m else None
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--set', metavar='X.Y.Z', help='write this version everywhere')
    args = ap.parse_args()

    if args.set:
        if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', args.set):
            sys.exit('version must look like 1.4.0')
        for rel, pat, repl in SITES:
            p = ROOT / rel
            if not p.exists():
                print(f'SKIP   {rel} (missing)')
                continue
            text = p.read_text(encoding='utf-8')
            new, n = pat.subn(repl.replace('{v}', args.set), text)
            if n:
                p.write_text(new, encoding='utf-8')
                print(f'SET    {rel} → {args.set}')
            else:
                print(f'WARN   {rel}: no version pattern found')
        print('\nREADME.md is not auto-edited — add the Version history entry by hand.\n')

    found = read_all()
    versions = {v for v in found.values() if v}
    width = max(len(k) for k in found)
    for k, v in found.items():
        print(f'  {k:<{width}}  {v or "NOT FOUND"}')

    if len(versions) == 1 and None not in found.values():
        print(f'\nOK — every site reports {versions.pop()}')
        return 0
    print('\nERROR — versions disagree (or a site is missing). '
          'Fix with: python3 scripts/check_version.py --set X.Y.Z')
    return 1


if __name__ == '__main__':
    sys.exit(main())
