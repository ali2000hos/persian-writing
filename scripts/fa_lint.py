#!/usr/bin/env python3
"""
fa_lint.py — LINT Persian text: report orthography and register issues.

Primary role is the --check report: it finds problems that need contextual
judgment (em dashes, attached میشود forms, fake tanvin, stacked !!) that
automated fixers skip. For automated FIXING prefer persian_cleanup.py --edit
(the bundled paknevis+davat toolkit); this script's --fix covers a smaller
safe subset plus tanvin restoration (لطفا → لطفاً).

Usage:
  python3 fa_lint.py --check file.txt [file2.md ...]   # report issues (default)
  python3 fa_lint.py --fix file.txt                     # apply SAFE fixes in place
  python3 fa_lint.py --fix --aggressive file.txt        # also riskier fixes
  python3 fa_lint.py --fix --digits file.txt            # also convert digits
  cat text | python3 fa_lint.py --fix -                 # stdin → stdout

Safe fixes (--fix):
  * Arabic ي ك → Persian ی ک ; Arabic-Indic digits ٤٥٦ → Persian ۴۵۶
  * ZWNJ: «می / نمی + verb», plural « ها», enclitics «خانه ام → خانه‌ام»
  * Latin , ; ? between Persian text → ، ؛ ؟
  * Double spaces, space before punctuation

Aggressive fixes (--aggressive):
  * " تر/ترین" → ‌تر/‌ترین   (rare false positives: «تر و تازه»)
  * "quoted Persian" → «quoted Persian»

Report-only (never auto-fixed — need human/context judgment):
  * em/en dashes, ة, tanvin-on-Persian words (گاهاً…), attached می (میشود),
    stacked !!, ASCII digits (unless --digits)

Exit code: 0 = clean, 1 = issues found (check) / unfixable issues remain (fix).
"""
import argparse, re, sys, unicodedata

PERSIAN = r'؀-ۿ‌'
FA_LETTER = r'[ء-غف-ئپچژکگیة]'
ZWNJ = '‌'

ISSUES = []

def record(kind, line_no, snippet, suggestion):
    ISSUES.append((kind, line_no, snippet.strip()[:80], suggestion))

# ---------- safe fixes ----------

ARABIC_MAP = {'ي': 'ی', 'ك': 'ک', 'ىٰ': 'ی', 'ى': 'ی',
              '٠': '۰', '١': '۱', '٢': '۲', '٣': '۳', '٤': '۴',
              '٥': '۵', '٦': '۶', '٧': '۷', '٨': '۸', '٩': '۹'}

ENCLITIC_BLACKLIST = {'به', 'که', 'چه', 'نه', 'سه', 'آنچه', 'اینکه', 'گه'}

# Arabic loans that REQUIRE tanvin (safe to fix when missing)
TANVIN_NEEDED = {'لطفا': 'لطفاً', 'حتما': 'حتماً', 'واقعا': 'واقعاً', 'اصلا': 'اصلاً',
                 'کاملا': 'کاملاً', 'مثلا': 'مثلاً', 'معمولا': 'معمولاً',
                 'تقریبا': 'تقریباً', 'دقیقا': 'دقیقاً', 'فعلا': 'فعلاً',
                 'قطعا': 'قطعاً', 'اتفاقا': 'اتفاقاً', 'احتمالا': 'احتمالاً',
                 'مخصوصا': 'مخصوصاً', 'اساسا': 'اساساً', 'عملا': 'عملاً'}
FA_B_L = r'(?<![؀-ۿ‌])'   # Persian-aware word boundaries
FA_B_R = r'(?![؀-ۿًٌٍَُِّ‌])'

def fix_safe(text):
    # Arabic characters → Persian
    for a, p in ARABIC_MAP.items():
        text = text.replace(a, p)
    # می / نمی + following Persian word  →  ZWNJ
    text = re.sub(r'\b(ن?می) (?=' + FA_LETTER + ')', r'\1' + ZWNJ, text)
    # plural ها / های / هایی after a Persian word (space → ZWNJ)
    text = re.sub(r'(' + FA_LETTER + r') (ها(?:ی|یی)?)(?![' + PERSIAN.strip('[]') + r'])',
                  r'\1' + ZWNJ + r'\2', text)
    # enclitics after final ه: خانه ام → خانه‌ام  (skip به/که/چه/نه/سه…)
    def _encl(m):
        w = m.group(1)
        return m.group(0) if w in ENCLITIC_BLACKLIST else w + ZWNJ + m.group(2)
    text = re.sub(r'\b(' + FA_LETTER + r'+ه) (ام|ات|اش|ای|اید|اند)\b', _encl, text)
    # Latin punctuation in Persian context
    text = re.sub(r'(?<=[' + PERSIAN + r'])\s*\?', '؟', text)
    text = re.sub(r'(?<=[' + PERSIAN + r'])\s*,\s*(?=[' + PERSIAN + r'])', '، ', text)
    text = re.sub(r'(?<=[' + PERSIAN + r'])\s*;\s*(?=[' + PERSIAN + r'])', '؛ ', text)
    # spacing hygiene: no space before Persian punctuation, one after
    text = re.sub(r' +([،؛؟!])', r'\1', text)
    text = re.sub(r'([،؛])(?=[' + PERSIAN + r'])', r'\1 ', text)
    # double spaces (not at line start = keep markdown indents)
    text = re.sub(r'(?<=\S)  +(?=\S)', ' ', text)
    # missing tanvin on common Arabic loans: لطفا → لطفاً
    for bare, correct in TANVIN_NEEDED.items():
        text = re.sub(FA_B_L + bare + FA_B_R, correct, text)
    return text

def fix_aggressive(text):
    # comparative/superlative: بزرگ تر → بزرگ‌تر (skip «تر و تازه»)
    text = re.sub(r'(' + FA_LETTER + r'{2,}) (تر|ترین)\b(?! و تازه)',
                  r'\1' + ZWNJ + r'\2', text)
    # straight quotes wrapping Persian → گیومه
    text = re.sub(r'"([^"\n]*' + FA_LETTER + r'[^"\n]*)"', r'«\1»', text)
    return text

def _skip_token(tok):
    """Tokens whose digits must stay Latin: URLs, emails, paths, versions, code."""
    return bool(re.search(r'https?://|www\.|@|[/\\]|\.[a-z]{2,}|`', tok)
                or re.fullmatch(r'\+?\d+(\.\d+)+[.,;،]?', tok))   # versions like 6.5

def fix_digits(text):
    """ASCII digits → Persian on Persian lines, skipping protected tokens."""
    def conv(tok):
        return tok.translate(str.maketrans('0123456789', '۰۱۲۳۴۵۶۷۸۹'))
    out_lines = []
    for line in text.split('\n'):
        has_fa = re.search(FA_LETTER, line)
        out_lines.append(' '.join(
            conv(t) if has_fa and re.search(r'[0-9]', t) and not _skip_token(t) else t
            for t in line.split(' ')))
    return '\n'.join(out_lines)

# ---------- report-only checks ----------

ATTACHED_MI = re.compile(r'\b(می(?:شود|شوند|شد|کند|کنند|کرد|گوید|گویند|گفت|باشد|باشند|'
                         r'تواند|توانند|توانید|خواهد|خواهند|خواهیم|رود|روند|آید|آیند|'
                         r'دهد|دهند|گیرد|گیرند|ماند|شویم|کنیم|رویم|بینید|بینیم|دانید|دانیم))\b')
TANVIN_FA = {'گاهاً': 'گاهی', 'گاها': 'گاهی', 'دوماً': 'دوم اینکه / ثانیاً',
             'سوماً': 'سوم اینکه / ثالثاً', 'ناچاراً': 'به‌ناچار', 'زباناً': 'به زبان',
             'تلفناً': 'تلفنی', 'خواهشاً': 'خواهش می‌کنم'}

def check_remaining(text):
    for i, line in enumerate(text.split('\n'), 1):
        if not re.search(FA_LETTER, line):
            continue
        for ch, name in [('—', 'em dash'), ('–', 'en dash')]:
            if ch in line:
                record('dash', i, line, f'{name}: replace with «،»/«؛»/() or restructure')
        if 'ة' in line:
            record('arabic-teh', i, line, 'ة: use ه/هٔ unless quoting Arabic')
        for m in ATTACHED_MI.finditer(line):
            record('attached-mi', i, line, f'{m.group(0)}: formal register needs می‌{m.group(0)[2:]}')
        scratch = line
        for bad in sorted(TANVIN_FA, key=len, reverse=True):
            if bad in scratch:
                record('fake-tanvin', i, line, f'{bad} → {TANVIN_FA[bad]}')
                scratch = scratch.replace(bad, '')
        for bare, correct in TANVIN_NEEDED.items():
            if re.search(FA_B_L + bare + FA_B_R, line):
                record('missing-tanvin', i, line, f'{bare} → {correct}')
        if re.search(r'!{2,}', line):
            record('multi-bang', i, line, 'one ! maximum')
        for m in re.finditer(r'\b(می‌گردد|می‌گردند|گردید(?:ه است)?|گردیدند)\b', line):
            record('bureaucratic-verb', i, line,
                   f'{m.group(0)}: fossil register — use می‌شود/شد (unless گردیدن = چرخیدن)')
        if re.search(r'(?<=[' + PERSIAN + r'])\s*[,;?]|[,;?]\s*(?=[' + PERSIAN + r'])', line):
            record('latin-punct', i, line, 'Latin ,;? in Persian context → ، ؛ ؟')
        for a in ARABIC_MAP:
            if a in line:
                record('arabic-char', i, line, f'{a} → {ARABIC_MAP[a]}')
        if re.search(r'\b(ن?می) ' + FA_LETTER, line):
            record('zwnj-mi', i, line, 'می + space → می + ZWNJ (نیم‌فاصله)')
        if re.search(r'(' + FA_LETTER + r') ها\b', line):
            record('zwnj-ha', i, line, 'plural ها: use ZWNJ (کتاب‌ها) — ignore if emphasis particle')
        if re.search(r'(' + FA_LETTER + r'{2,}) (تر|ترین)\b(?! و تازه)', line):
            record('zwnj-tar', i, line, 'comparative تر/ترین: use ZWNJ (بزرگ‌تر)')
        if re.search(r'"[^"\n]*' + FA_LETTER, line):
            record('quotes', i, line, 'straight quotes around Persian → «گیومه»')
        # ASCII digits touching Persian words (not urls/emails/versions/code)
        for tok in line.split():
            if (re.search(r'[0-9]', tok) and re.search(FA_LETTER, line)
                    and not _skip_token(tok)):
                record('latin-digits', i, line, f'{tok}: Persian digits in Persian prose (or --digits)')
                break

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('files', nargs='+', help="files to process, or '-' for stdin")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true', help='report only (default)')
    mode.add_argument('--fix', action='store_true', help='apply safe fixes in place')
    ap.add_argument('--aggressive', action='store_true', help='with --fix: riskier fixes too')
    ap.add_argument('--digits', action='store_true', help='with --fix: ASCII → Persian digits')
    args = ap.parse_args()

    exit_code = 0
    for path in args.files:
        ISSUES.clear()
        if path == '-':
            text = sys.stdin.read()
        else:
            with open(path, encoding='utf-8') as f:
                text = f.read()
        text = unicodedata.normalize('NFC', text)

        if args.fix:
            text = fix_safe(text)
            if args.aggressive:
                text = fix_aggressive(text)
            if args.digits:
                text = fix_digits(text)
            if path == '-':
                sys.stdout.write(text)
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(text)
            check_remaining(text)
            label = 'remaining (need manual/contextual fixes)'
        else:
            check_remaining(text)
            # also surface what --fix WOULD change
            fixed = fix_safe(text)
            if fixed != text:
                record('fixable', 0, '(multiple)', 'safe auto-fixes available: rerun with --fix')
            label = 'issues'

        header = f'== {path}: {len(ISSUES)} {label} =='
        print(header, file=sys.stderr)
        by_kind = {}
        for kind, ln, snip, sug in ISSUES:
            by_kind.setdefault(kind, []).append((ln, snip, sug))
        for kind, items in sorted(by_kind.items()):
            print(f'  [{kind}] ×{len(items)}', file=sys.stderr)
            for ln, snip, sug in items[:5]:
                print(f'    L{ln}: {snip}\n        → {sug}', file=sys.stderr)
            if len(items) > 5:
                print(f'    … {len(items)-5} more', file=sys.stderr)
        if ISSUES:
            exit_code = 1
    sys.exit(exit_code)

if __name__ == '__main__':
    main()
