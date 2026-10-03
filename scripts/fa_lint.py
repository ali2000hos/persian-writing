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
  * bidi-start: a Persian line opening with a Latin word (renders LTR),
  * em/en dashes, ة, tanvin-on-Persian words (گاهاً…), attached می (میشود),
    stacked !!, ASCII digits (unless --digits)

Exit code: 0 = clean, 1 = issues found (check) / unfixable issues remain (fix).
"""
import argparse, os, re, sys, unicodedata

try:
    from scripts.persian_cleanup import protect_regions, restore_regions, needs_rlm, is_rtl_dominant, _LINE_PREFIX
except ImportError:
    try:
        from persian_cleanup import protect_regions, restore_regions, needs_rlm, is_rtl_dominant, _LINE_PREFIX
    except ImportError:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from persian_cleanup import protect_regions, restore_regions, needs_rlm, is_rtl_dominant, _LINE_PREFIX

PERSIAN = r'؀-ۿ‌'
FA_LETTER = r'[ء-غف-ئپچژکگیة]'
ZWNJ = '‌'

_LEXICAL_COMPARATIVES = {"بهتر", "بیشتر", "کمتر", "پیشتر", "بدتر", "مهتر", "کهتر"}
_COORD_COMP_AHEAD = re.compile(r"^\s+و\s+([ء-یء-۾]+)(?:\s+تر\b|\u200cتر\b)")

def _is_coord_comparative(tail: str) -> bool:
    if _COORD_COMP_AHEAD.match(tail):
        return True
    m_lex = re.match(r"^\s+و\s+([ء-یء-۾]+)\b", tail)
    return bool(m_lex and m_lex.group(1) in _LEXICAL_COMPARATIVES)

ISSUES = []
CURRENT_TOKENS = []

def record(kind, line_no, snippet, suggestion):
    if CURRENT_TOKENS:
        snippet = restore_regions(snippet, CURRENT_TOKENS)
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

# ---------- هکسره detection ----------
# Persian's most-mocked writing error: confusing the ezafe kasre (کتابِ من) with
# the colloquial clitic «ـه» that stands for «است» (این کتابه = این کتاب است).
# They sound identical, so writers swap them. Detection has to be contextual:
# «کتابه» ending a clause is correct; «کتابه من» is the error.

_HE_NOUNS = set("""خانه خونه نامه برنامه هفته پروژه مدرسه نقشه جمعه قهوه بچه شنبه دقیقه
ثانیه پنجره اندازه سفره کوچه میوه لحظه جمله مرحله نتیجه مقاله هزینه گزینه نمونه زمینه
دسته بسته پوشه شبکه حوزه دوره چهره سلیقه علاقه سابقه تجربه قطعه منطقه فاصله مجموعه
موسسه مسئله مساله وسیله هدیه اجاره اداره اشاره ستاره کناره ساده آماده ایده شماره
اجازه انگیزه اندیشه ترانه بهانه نشانه خاطره پرونده آینده گذشته رابطه ضابطه قاعده
مبادله معامله محاسبه مطالعه مراجعه مصاحبه مقایسه مناقصه مزایده""".split())

_PRON = r'(?:من|تو|ما|شما|او|اون|ایشون|اونا|اینا|خودم|خودت|خودش|این|آن)'

_DICT_RANK_FA: dict = {}


def _resolve_dictionary():
    """Locate the single bundled word list.

    Delegates to persian_cleanup so both scripts agree on where the dictionary
    lives; falls back to the repo layout if that module is not importable.
    """
    import os, sys
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    try:
        from persian_cleanup import resolve_dictionary_path
        return resolve_dictionary_path()
    except Exception:
        path = os.path.join(os.path.dirname(here), 'assets', 'persian_words.txt')
        return path if os.path.isfile(path) else None


def _load_ranks():
    """Load the bundled frequency-ordered word list (rank = line number)."""
    global _DICT_RANK_FA
    if _DICT_RANK_FA:
        return _DICT_RANK_FA
    path = _resolve_dictionary()
    if path:
        with open(path, encoding='utf-8') as fh:
            for i, line in enumerate(fh):
                w = line.strip()
                if w and w not in _DICT_RANK_FA:
                    _DICT_RANK_FA[w] = i
    return _DICT_RANK_FA


def find_hekasre(text):
    """Return [(matched_text, suggestion, tier)] for probable هکسره errors.

    Tier A (high confidence): «Xه» is not a word at all while «X» is, and it sits
    before another word — so the ه can only be a misplaced ezafe.
    Tier B (medium): «Xه» exists but is far rarer than «X», and a pronoun follows.
    Precision is favoured over recall: a lint that cries wolf gets ignored.
    """
    rank = _load_ranks()
    INF = 10 ** 9
    if not rank:
        return []
    r = lambda w: rank.get(w, INF)
    out = []
    for m in re.finditer(r'(?<![‌آ-ی])([آ-ی]{2,})ه\s+([آ-ی]{2,})', text):
        stem, nxt = m.group(1), m.group(2)
        whole = stem + 'ه'
        if whole.endswith('انه') or whole in _HE_NOUNS or r(stem) == INF:
            continue
        if r(whole) == INF:
            out.append((m.group(0), f'{stem}ِ {nxt}', 'A'))
    for m in re.finditer(r'(?<![‌آ-ی])([آ-ی]{2,})ه\s+(' + _PRON + r')(?![آ-ی])', text):
        stem, nxt = m.group(1), m.group(2)
        whole = stem + 'ه'
        if whole.endswith('انه') or whole in _HE_NOUNS or r(stem) == INF or r(whole) == INF:
            continue
        if r(whole) > r(stem) * 3 and r(whole) > 20000:
            out.append((m.group(0), f'{stem}ِ {nxt}', 'B'))
    return out

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
    # Spacing hygiene: no space before Persian punctuation, one after.
    # The space must belong to a WORD, not to Markdown structure: a bullet
    # «- ! ...», a table cell «| ؟ |» or an indent are separators, and gluing
    # the mark to them («-!») silently breaks the document's structure.
    text = re.sub(r'(?<=[\w)\]»"\'])[ \t]+([،؛؟!])', r'\1', text)
    text = re.sub(r'([،؛])(?=' + FA_LETTER + r')', r'\1 ', text)
    # double spaces (not at line start = keep markdown indents)
    text = re.sub(r'(?<=\S)  +(?=\S)', ' ', text)
    # missing tanvin on common Arabic loans: لطفا → لطفاً
    for bare, correct in TANVIN_NEEDED.items():
        text = re.sub(FA_B_L + bare + FA_B_R, correct, text)
    return text

def fix_aggressive(text):
    # comparative/superlative: بزرگ تر → بزرگ‌تر
    text = re.sub(r'(' + FA_LETTER + r'{2,}) ترین\b', r'\1' + ZWNJ + 'ترین', text)

    def _join_tar(m):
        w = m.group(1)
        tail = text[m.end():m.end() + 40]
        if tail.startswith(" و "):
            if _is_coord_comparative(tail):
                return w + ZWNJ + "تر"
            return m.group(0)
        return w + ZWNJ + "تر"

    text = re.sub(r'(' + FA_LETTER + r'{2,})\s+تر\b', _join_tar, text)
    # straight quotes wrapping Persian → گیومه
    text = re.sub(r'"([^"\n]*' + FA_LETTER + r'[^"\n]*)"', r'«\1»', text)
    return text

_CODEPOINT = re.compile(r'U\+[0-9A-Fa-f]{4,6}(?:\.\.)?')

def _skip_token(tok):
    """Tokens whose digits must stay Latin, or that are codepoint notation.

    Unicode codepoint notation (U+06CC, U+200C, U+066A) is metalanguage, not
    prose: converting its digits would destroy the thing being named. It can
    appear glued to Markdown punctuation or inside a table cell, so match it
    anywhere in the token rather than as the whole token.
    """
    if _CODEPOINT.search(tok):
        return True
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

IGNORE_NEXT = '<!-- fa-lint-ignore-next-line -->'
IGNORE_START = '<!-- fa-lint-ignore-start -->'
IGNORE_END = '<!-- fa-lint-ignore-end -->'

def _lint_ignored_lines(text):
    """Line numbers suppressed by an explicit fa-lint directive.

    Documentation has to show wrong forms in order to teach them: a table of
    «کتابه من ✗ → کتابِ من ✓» must contain the error. Without a way to say so,
    the skill can never pass its own linter, and a linter its own author
    ignores is a linter nobody runs.

    Two forms, because this skill's docs are largely Wrong/Right tables and
    marking every row one at a time buries the content in directives:

        <!-- fa-lint-ignore-next-line -->     one line
        <!-- fa-lint-ignore-start -->  …  <!-- fa-lint-ignore-end -->
    """
    lines = text.split('\n')
    ignored = set()
    in_block = False
    for i, line in enumerate(lines):
        if IGNORE_START in line:
            in_block = True
        elif IGNORE_END in line:
            in_block = False
        elif in_block:
            ignored.add(i + 1)
        elif IGNORE_NEXT in line and i + 1 < len(lines):
            ignored.add(i + 2)
    return ignored

def _preserve_ignored(original, fixed):
    """Restore suppressed lines after a fix pass.

    Without this, `--fix` silently repairs the error examples it was told to
    leave alone: the row «| ی U+06CC | ي U+064A |» loses the Arabic ي that is
    the whole point of the row. Fixes still run over the full text, so no rule
    changes behaviour; only the marked lines are put back.
    """
    ignored = _lint_ignored_lines(original)
    if not ignored:
        return fixed
    old, new = original.split('\n'), fixed.split('\n')
    if len(old) != len(new):
        return fixed          # line count moved; mapping would be guesswork
    return '\n'.join(old[i - 1] if i in ignored else new[i - 1]
                     for i in range(1, len(new) + 1))

def _is_fa_word(word):
    """A word written in Persian script and not part of a Latin token."""
    return bool(word) and bool(re.search(FA_LETTER, word)) and not re.search(r'[A-Za-z]', word)

def _is_fa_dominant(line):
    """True when the line is Persian prose rather than English quoting Persian."""
    fa = len(re.findall(FA_LETTER, line))
    latin = len(re.findall(r'[A-Za-z]', line))
    return fa > latin

def _neighbours(line, idx, length=1):
    """The whitespace-delimited words immediately left and right of a mark."""
    left = line[:idx].split()
    right = line[idx + length:].split()
    return (left[-1] if left else ''), (right[0] if right else '')

def check_remaining(text):
    ignored = _lint_ignored_lines(text)
    # bidi-start only matters in a Persian document. In an English guide that
    # quotes Persian (like this skill's own references), an English-led line
    # is SUPPOSED to render left-to-right.
    fa_document = is_rtl_dominant(text)
    for i, line in enumerate(text.split('\n'), 1):
        if i in ignored:
            continue
        if not re.search(FA_LETTER, line):
            continue
        # Paragraph direction: renderers take it from the FIRST strong letter,
        # so a Persian line that opens with a Latin word displays left-to-right.
        segments = line.split('|') if line.lstrip().startswith('|') else \
            [line[len(_LINE_PREFIX.match(line).group(1)):]]
        if fa_document and any(needs_rlm(seg) for seg in segments):
            record('bidi-start', i, line,
                   'Persian line starts with a Latin word → renders LTR in chat/GitHub/'
                   'Telegram. Start with a Persian word («کتابخانه‌ی React…»), or '
                   'run persian_cleanup.py --bidi for plain-text output')
        # Dashes are flagged only INSIDE Persian prose. In a bilingual document
        # an em dash usually joins a term to its gloss («ZWNJ — نیم‌فاصله») or
        # sits in an English sentence that happens to quote one Persian word;
        # both are correct English typography. Requiring Persian on both sides
        # targets the actual fault without forcing the English prose to degrade.
        for ch, name in [('—', 'em dash'), ('–', 'en dash')]:
            for m in re.finditer(re.escape(ch), line):
                left, right = _neighbours(line, m.start())
                if _is_fa_word(left) and _is_fa_word(right):
                    record('dash', i, line, f'{name}: replace with «،»/«؛»/() or restructure')
                    break
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
        for hit, fix, tier in find_hekasre(line):
            conf = 'likely' if tier == 'A' else 'possible'
            record('hekasre', i, line,
                   f'«{hit}» → «{fix}» ({conf} هکسره: ezafe kasre written as ـه)')
        # reverse هکسره: explicit kasre where the «است» clitic belongs
        for m in re.finditer(r'([آ-ی]{2,})ِ\s*(?=[.!؟\n]|$)', line):
            record('hekasre', i, line,
                   f'«{m.group(0).strip()}» ends a clause with a kasre — predicate «است» '
                   f'is written «{m.group(1)}ه» (خوبه), not with ـِ')
        # Latin punctuation counts as an error when a PERSIAN word carries it —
        # not when Persian merely follows an English clause that ended in a
        # comma. End of line still counts («چطوری?» is the classic case) but
        # only on a Persian line, or every English sentence that happens to
        # close on a quoted Persian word gets flagged.
        fa_line = _is_fa_dominant(line)
        for m in re.finditer(r'[,;?]', line):
            left, right = _neighbours(line, m.start())
            if _is_fa_word(left) and (_is_fa_word(right) or (right == '' and fa_line)):
                record('latin-punct', i, line, 'Latin ,;? in Persian context → ، ؛ ؟')
                break
        for a in ARABIC_MAP:
            if a in line:
                record('arabic-char', i, line, f'{a} → {ARABIC_MAP[a]}')
        if re.search(r'\b(ن?می) ' + FA_LETTER, line):
            record('zwnj-mi', i, line, 'می + space → می + ZWNJ (نیم‌فاصله)')
        if re.search(r'(' + FA_LETTER + r') ها\b', line):
            record('zwnj-ha', i, line, 'plural ها: use ZWNJ (کتاب‌ها) — ignore if emphasis particle')
        if re.search(r'(' + FA_LETTER + r'{2,}) ترین\b', line):
            record('zwnj-tar', i, line, 'comparative ترین: use ZWNJ (بزرگ‌ترین)')
        for m in re.finditer(r'(' + FA_LETTER + r'{2,})\s+تر\b', line):
            tail = line[m.end():m.end() + 40]
            if tail.startswith(" و ") and not _is_coord_comparative(tail):
                continue
            record('zwnj-tar', i, line, 'comparative تر: use ZWNJ (بزرگ‌تر)')
            break
        if re.search(r'"[^"\n]*' + FA_LETTER, line):
            record('quotes', i, line, 'straight quotes around Persian → «گیومه»')
        # ASCII digits touching Persian words (not urls/emails/versions/code).
        # Markdown heading and list numbering is document structure, not prose:
        # «## 1. عنوان» is numbered by the renderer, and Persian digits there
        # break ordered-list parsing.
        digit_line = re.sub(r'^\s{0,3}#{1,6}\s+\d+[.)]\s+', '', line)
        digit_line = re.sub(r'^\s*\d+[.)]\s+', '', digit_line)
        for tok in digit_line.split():
            if (re.search(r'[0-9]', tok) and re.search(FA_LETTER, line)
                    and not _skip_token(tok)):
                record('latin-digits', i, line, f'{tok}: Persian digits in Persian prose (or --digits)')
                break

def rhythm_report(text):
    """Editorial hints about sentence rhythm — NOT an AI-detector score.

    Measured on real Persian samples: an AI-sounding page and its humanised
    rewrite scored CV 0.39 vs 0.65, so uniform sentence length is a genuine
    (if secondary) symptom of machine-flat prose. The decisive signal is always
    the lexical/rhetorical tells the linter already reports; treat rhythm as a
    prompt to reread, never as a verdict on authorship.
    """
    import statistics as stats
    fa_sents = [s.strip() for s in re.split(r'[.!?؟\n]+', re.sub(r'[#*>`]', ' ', text))
                if len(s.strip().split()) >= 2 and re.search(FA_LETTER, s)]
    lengths = [len(s.split()) for s in fa_sents]
    out = []
    if len(lengths) < 8:
        return [('too-short', f'{len(lengths)} sentences — rhythm needs ~8+ to mean anything')]
    mean = stats.mean(lengths)
    cv = stats.pstdev(lengths) / mean if mean else 0
    short = sum(1 for x in lengths if x < 8)
    long_ = sum(1 for x in lengths if x > 25)
    out.append(('measured', f'{len(lengths)} sentences | mean {mean:.1f} words | '
                            f'variation {cv:.2f} | range {min(lengths)}–{max(lengths)}'))
    if cv < 0.35:
        out.append(('uniform-rhythm',
                    f'variation {cv:.2f} is low — sentences sit in a narrow band, which is '
                    f'what makes prose feel machine-flat. Break one long sentence in two, '
                    f'or let one land short.'))
    if short == 0:
        out.append(('no-short-sentence',
                    'no sentence under 8 words. A short one after a long one is how Persian '
                    'prose breathes and where emphasis comes from.'))
    is_technical = bool(re.search(r'```', text) or len(re.findall(r'`[^`\n]+`', text)) >= 3)
    if long_ == 0 and mean < 20 and not is_technical:
        out.append(('no-long-sentence',
                    'every sentence is short-to-medium. One longer, flowing sentence adds '
                    'range — uniformity in either direction reads as generated.'))
    starts = [s.split()[0] for s in fa_sents if s.split()]
    if starts and len(set(starts)) < len(starts) * 0.6:
        rep = max(set(starts), key=starts.count)
        out.append(('repeated-openings',
                    f'sentences repeat their opening word ("{rep}" ×{starts.count(rep)}). '
                    f'Vary how sentences begin.'))
    paras = [p for p in text.split('\n\n') if len(p.split()) > 15]
    if len(paras) >= 4:
        plen = [len(p.split()) for p in paras]
        pcv = stats.pstdev(plen) / stats.mean(plen)
        if pcv < 0.2:
            out.append(('uniform-paragraphs',
                        f'paragraphs are all about the same size ({pcv:.2f} variation) — '
                        f'real sections differ in weight because real ideas do.'))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('files', nargs='+', help="files to process, or '-' for stdin")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument('--check', action='store_true', help='report only (default)')
    mode.add_argument('--fix', action='store_true', help='apply safe fixes in place')
    ap.add_argument('--aggressive', action='store_true', help='with --fix: riskier fixes too')
    ap.add_argument('--digits', action='store_true', help='with --fix: ASCII → Persian digits')
    ap.add_argument('--rhythm', action='store_true',
                    help='report sentence-rhythm hints (uniform length, missing short/long '
                         'sentences, repeated openings) — editorial guidance, not a score')
    args = ap.parse_args()

    exit_code = 0
    global CURRENT_TOKENS
    for path in args.files:
        ISSUES.clear()
        if path == '-':
            text = sys.stdin.read()
        else:
            with open(path, encoding='utf-8') as f:
                text = f.read()
        text = unicodedata.normalize('NFC', text)
        masked, tokens = protect_regions(text)
        CURRENT_TOKENS = tokens

        if args.fix:
            original = text
            masked = fix_safe(masked)
            if args.aggressive:
                masked = fix_aggressive(masked)
            if args.digits:
                masked = fix_digits(masked)
            text = restore_regions(masked, tokens)
            text = _preserve_ignored(original, text)
            if path == '-':
                sys.stdout.write(text)
            else:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(text)
            re_masked, _ = protect_regions(text)
            check_remaining(re_masked)
            label = 'remaining (need manual/contextual fixes)'
        else:
            check_remaining(masked)
            # Also surface what --fix WOULD change — but blank out suppressed
            # lines first, or a deliberate error example keeps advertising a
            # fix that must never be applied to it.
            ignored = _lint_ignored_lines(masked)
            preview = '\n'.join('' if i in ignored else line
                                for i, line in enumerate(masked.split('\n'), 1))
            if fix_safe(preview) != preview:
                record('fixable', 0, '(multiple)', 'safe auto-fixes available: rerun with --fix')
            label = 'issues'

        header = f'== {path}: {len(ISSUES)} {label} =='
        print(header, file=sys.stderr)
        if args.rhythm:
            print('  -- rhythm (editorial hints, not an authorship score) --', file=sys.stderr)
            for kind, msg in rhythm_report(text):
                print(f'    [{kind}] {msg}', file=sys.stderr)
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
