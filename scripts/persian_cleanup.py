#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
persian_cleanup.py
==================

A self-contained Persian-text cleanup, normalization, and editorial toolkit
that merges two open-source projects:

* **paknevis** (https://github.com/afshin-ir/paknevis) — a LibreOffice macro
  for conservative Persian copy-editing: ZWNJ fixing for verbs / suffixes /
  possessives, Arabic→Persian character mapping, English→Persian punctuation
  and digits, ezafe kasre fixing, ellipsis fixing, repeated punctuation
  collapsing, and dictionary-assisted spell-checking.

* **davat** (https://github.com/mh-salari/davat) — a Python library for
  aggressive Persian-text cleaning: link / mention / hashtag / emoji /
  markdown removal, multi-script stripping, extra-space collapsing, and a
  composable pipeline (`clean()` + `PERSIAN_STEPS` / `MINIMAL_STEPS`).

Design goals
------------
* **Zero external dependencies** — only Python 3.8+ and the standard library.
* **Both APIs available** — call `clean()` (davat-style aggressive pipeline)
  or `edit_persian()` (paknevis-style conservative editorial pass), or any
  individual function.
* **CLI-friendly** — every function is reachable from the command line so an
  AI agent can shell out without writing Python.
* **Idempotent** — running `edit_persian()` twice gives the same output as
  running it once.

Usage as a Python module
------------------------
    from persian_cleanup import (
        clean, edit_persian, normalize_persian, convert_digits,
        remove_links, remove_mentions, remove_hashtags, remove_emojis,
        remove_markdown, remove_punctuations, fix_multiple_punctuations,
        remove_ellipsis, strip_characters, remove_extra_spaces,
        fix_zwnj_verbs, fix_zwnj_suffixes, fix_zwnj_possessives,
        fix_arabic_chars, fix_persian_punctuation,
        fix_punctuation_spacing, fix_ezafe, fix_ellipsis,
        fix_repeated_punctuation, spellcheck,
        PERSIAN_STEPS, MINIMAL_STEPS, EDITOR_STEPS,
    )

Usage from CLI
--------------
    # Full aggressive clean (davat PERSIAN_STEPS)
    python3 persian_cleanup.py "متنی برای پاکسازی"

    # Paknevis-style editorial pass (conservative)
    python3 persian_cleanup.py --edit "می رود و خانه اش و 123 و ?"

    # Single function
    python3 persian_cleanup.py --fn convert_digits --to fa "123"
    python3 persian_cleanup.py --fn remove_links "سلام https://x.com"

    # Custom pipeline (comma-separated)
    python3 persian_cleanup.py --steps "remove_links,remove_emojis,normalize_persian" "..."

    # Read input from file, write output to file
    python3 persian_cleanup.py --edit --in input.txt --out output.txt

    # JSON output (also reports which steps were applied)
    python3 persian_cleanup.py --edit --json "..."
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from functools import partial
from typing import Callable, Iterable, List, Optional, Sequence, Union

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

__version__ = "1.0.0"

# Zero-Width Non-Joiner (نیم‌فاصله) — the heart of Persian typography
ZWNJ = "\u200c"

# Persian digit map (Western Arabic → Persian)
FA_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
EN_DIGITS = "0123456789"
AR_DIGITS = "٠١٢٣٤٥٦٧٨٩"

_EN_TO_FA = {ord(e): f for e, f in zip(EN_DIGITS, FA_DIGITS)}
_AR_TO_FA = {ord(a): f for a, f in zip(AR_DIGITS, FA_DIGITS)}
_FA_TO_EN = {ord(f): e for f, e in zip(FA_DIGITS, EN_DIGITS)}

# Arabic characters that have canonical Persian equivalents
_ARABIC_TO_PERSIAN = {
    ord("ي"): "ی",  # Arabic yeh → Persian yeh
    ord("ك"): "ک",  # Arabic kaf → Persian kaf
    ord("ؤ"): "و",
    ord("إ"): "ا",
    ord("أ"): "ا",
    ord("آ"): "آ",
    ord("ة"): "ه",  # ta marbuta → heh
    ord("ٰ"): "",    # superscript alef
}

# Persian diacritics (harakat) — removed by normalize_persian()
_DIACRITICS = (
    "\u064b",  # fathatan
    "\u064c",  # dammatan
    "\u064d",  # kasratan
    "\u064e",  # fatha
    "\u064f",  # damma
    "\u0650",  # kasra
    "\u0651",  # shadda
    "\u0652",  # sukun
    "\u0653",  # maddah above
    "\u0654",  # hamza above
    "\u0655",  # hamza below
    "\u0670",  # superscript alef
    "\u0640",  # tatweel/keshide
)

# English → Persian punctuation
_PUNCT_TO_FA = {
    "?": "؟",
    ";": "؛",
    ",": "،",
    '"': None,  # handled separately for paired guillemets
}

# Common Persian verb prefixes that take ZWNJ
_VERB_PREFIXES = ("می", "نمی", "بر", "باز", "بی", "می\u200c")  # last one is already-correct

# Preverb particles that join the verb stem with ZWNJ removal (compound verbs)
_COMPOUND_PREFIXES = ("فرا", "باز", "در", "فرورد", "بر", "بی", "وا")

# Suffixes that attach with ZWNJ
_SUFFIXES = ("تر", "ترین", "ها", "های", "هایی", "هایی که", "ام", "ات", "اش")

# Possessive enclitics that attach with ZWNJ
_POSSESSIVES = ("ام", "ات", "اش", "مان", "تان", "شان")

# URL regex (http/https/www)
_URL_RE = re.compile(
    r"(https?://[^\s\u060c\u061b\u061f]+|www\.[^\s\u060c\u061b\u061f]+)",
    flags=re.IGNORECASE,
)

# Mention regex (@username, max 32 chars)
_MENTION_RE = re.compile(r"@[A-Za-z0-9_]{1,32}")

# Hashtag regex
_HASHTAG_RE = re.compile(r"#[^\s\u060c\u061b\u061f@#]+")

# Markdown regexes (bold/italic/strike/code/link/image/list/headings)
_MD_BOLD = re.compile(r"\*\*([^*]+)\*\*|__([^_]+)__")
_MD_ITALIC = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)|(?<!_)_([^_]+)_(?!_)")
_MD_STRIKE = re.compile(r"~~([^~]+)~~")
_MD_CODE = re.compile(r"`([^`]+)`")
_MD_LINK = re.compile(r"\[([^\]]+)\]\([^)]+\)")
_MD_IMAGE = re.compile(r"!\[([^\]]*)\]\([^)]+\)")
_MD_HEADING = re.compile(r"^#{1,6}\s+", flags=re.MULTILINE)
_MD_LIST = re.compile(r"^\s*[-*+]\s+|^\s*\d+\.\s+", flags=re.MULTILINE)

# Ellipsis regexes (3+ dots with optional spaces → single …)
# We don't consume trailing whitespace — that's remove_extra_spaces's job.
_ELLIPSIS_DOTS = re.compile(r"(?:\.\s*){2,}\.")        # ... or . . .
_ELLIPSIS_MANY = re.compile(r"\.{4,}")                  # 4+ raw dots → …
_ELLIPSIS_COLLAPSE = re.compile(r"\u2026{2,}")          # ……… → …

# Repeated punctuation: ???→? !!!→! ؟؟؟→؟
_REPEATED_PUNCT = re.compile(r"([!?؟])\1+")

# Extra spaces around punctuation: "hello ? world" → "hello? world"
_PUNCT_SPACE_BEFORE = re.compile(r"\s+([!?؟:;,؛،.])")
_PUNCT_SPACE_AFTER_DOT = re.compile(r"([،؛:!؟.])\s{2,}")

# Multiple consecutive spaces (preserve newlines)
_MULTI_SPACE = re.compile(r"[ \t]{2,}")

# Collapsed-letter pattern: عااااللللیییی → عالی (3+ repeats → 1)
_REPEATED_LETTER = re.compile(r"(.)\1{2,}")
_REPEATED_LETTER_DICT = re.compile(r"(.)\1+")

# Common Persian misspellings → correct form (curated subset for spellcheck)
# This is NOT a full dictionary — it covers frequent mistakes.
_COMMON_MISSPELLINGS = {
    "بهشتی": "بهشتی",
    "لطفا": "لطفاً",
    "ممنون": "ممنون",
    "متشکرم": "متشکرم",
    "انشاالله": "ان‌شاءالله",
    "انشاءالله": "ان‌شاءالله",
    "ان شا الله": "ان‌شاءالله",
    "بهرحال": "به‌هرحال",
    "به هر حال": "به‌هرحال",
    "میتوان": "می‌توان",
    "می‌توانم": "می‌توانم",
    "چطور": "چطور",
    "کی": "کی",
    "که": "که",
    "است": "است",
    "هست": "هست",
    "بود": "بود",
    "شد": "شد",
    "داد": "داد",
    "خواست": "خواست",
    "رفت": "رفت",
    "آمد": "آمد",
    "دید": "دید",
    "گفت": "گفت",
    "کرد": "کرد",
    "داد": "داد",
    "زد": "زد",
    "خورد": "خورد",
    "نوشت": "نوشت",
    "دانست": "دانست",
    "شناخت": "شناخت",
    "فهمید": "فهمید",
    "بخشود": "بخشود",
}


# ---------------------------------------------------------------------------
# Bundle dictionary loading (optional, for dictionary-aware collapse + spellcheck)
# ---------------------------------------------------------------------------

_BUNDLED_DICT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets",
    "persian_words.txt",
)


def load_dictionary(path: Optional[str] = None) -> set:
    """Load a Persian word list (one word per line).

    If `path` is None, loads the bundled mini-dictionary. Returns an empty
    set if no file is found — callers should treat this as "no dictionary".
    """
    if path is None:
        path = _BUNDLED_DICT_PATH
    if not os.path.isfile(path):
        return set()
    words = set()
    rank = {}
    with open(path, "r", encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            w = line.strip()
            if w and w not in words:
                words.add(w)
                rank[w] = i
    # Frequency ranking: bundled dictionary is frequency-ordered (most common
    # first), so file position doubles as a frequency rank for spellcheck.
    global _DICT_RANK
    _DICT_RANK = rank
    return words


_DICT_RANK: dict = {}


# ---------------------------------------------------------------------------
# Individual functions (davat-style API)
# Each function: (str) -> str  (one job, composable)
# ---------------------------------------------------------------------------

def convert_digits(text: str, to: str = "fa") -> str:
    """Convert digits between Persian, Arabic, and English.

    `to="fa"` → Persian (default)
    `to="en"` → English
    `to="ar"` → Arabic
    """
    if not isinstance(text, str):
        raise TypeError("text must be str")
    if to == "fa":
        return text.translate(_EN_TO_FA).translate(_AR_TO_FA)
    if to == "en":
        return text.translate(_FA_TO_EN).translate(
            {ord(a): e for a, e in zip(AR_DIGITS, EN_DIGITS)}
        )
    if to == "ar":
        en_to_ar = {ord(e): a for e, a in zip(EN_DIGITS, AR_DIGITS)}
        fa_to_ar = {ord(f): a for f, a in zip(FA_DIGITS, AR_DIGITS)}
        return text.translate(en_to_ar).translate(fa_to_ar)
    raise ValueError(f"to must be 'fa', 'en', or 'ar', got {to!r}")


def remove_links(text: str) -> str:
    """Remove http(s):// and www. URLs."""
    return _URL_RE.sub("", text)


def remove_mentions(text: str) -> str:
    """Remove @username mentions."""
    return _MENTION_RE.sub("", text)


def remove_hashtags(text: str, keep_text: bool = True) -> str:
    """Remove hashtags. If keep_text=True (default), the hashtag body is
    preserved (just the # is stripped). If False, the whole hashtag is removed.
    """
    if keep_text:
        # Replace '#' with empty — leaves the word behind
        return re.sub(r"#(\S+)", r"\1", text)
    return _HASHTAG_RE.sub("", text)


def remove_emojis(text: str) -> str:
    """Remove emoji and pictographic symbols.

    Removes Unicode ranges commonly used for emojis: emoticons, pictographs,
    transport/map, supplemental symbols, flags, variation selectors, ZWJ.
    """
    # Range covers: Emoticons, Misc Symbols & Pictographs, Transport & Map,
    # Supplemental Symbols, Flags, Variation Selector-16, ZWJ.
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map
        "\U0001F1E0-\U0001F1FF"  # flags (regional indicators)
        "\U00002500-\U00002BEF"  # chinese char / box drawing subset
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"  # supplemental symbols and pictographs
        "\U0001FA70-\U0001FAFF"  # symbols and pictographs extended-A
        "\U0001F000-\U0001F02F"  # mahjong / dominoes
        "\U00002600-\U000026FF"  # misc symbols (☀ ☂ ☎ etc.)
        "\U00002700-\U000027BF"  # dingbats
        "\u200d"                  # zero-width joiner (part of emoji sequences)
        "\ufe0f"                  # variation selector-16
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text)


def remove_markdown(text: str) -> str:
    """Strip common Markdown formatting, keeping the text content."""
    text = _MD_IMAGE.sub(r"\1", text)
    text = _MD_LINK.sub(r"\1", text)
    text = _MD_BOLD.sub(r"\1\2", text)
    text = _MD_ITALIC.sub(r"\1\2", text)
    text = _MD_STRIKE.sub(r"\1", text)
    text = _MD_CODE.sub(r"\1", text)
    text = _MD_HEADING.sub("", text)
    text = _MD_LIST.sub("", text)
    return text


def remove_punctuations(text: str) -> str:
    """Remove ALL punctuation (Persian + English). Keeps letters, digits, spaces."""
    return re.sub(r"[!-/:-@\[-`{-~\u00A1-\u00BF\u2000-\u206F\u2018-\u201F\u2026\u060c\u061b\u061f\u066a\u066b\u066c\u06d4\u066a\u060d\u066d\uff00-\uffef]+", " ", text)


def fix_multiple_punctuations(text: str) -> str:
    """Collapse repeated punctuation marks: ??? → ?, !!! → !, ؟؟؟ → ؟."""
    text = _REPEATED_PUNCT.sub(r"\1", text)
    # Also collapse multiple commas / periods
    text = re.sub(r"([،,.])\1+", r"\1", text)
    return text


def remove_ellipsis(text: str) -> str:
    """Remove ellipses (... or …) entirely."""
    text = _ELLIPSIS_DOTS.sub(" ", text)
    text = _ELLIPSIS_MANY.sub(" ", text)
    text = _ELLIPSIS_COLLAPSE.sub(" ", text)
    # Also drop any single U+2026 left over
    text = text.replace("\u2026", " ")
    return text


def strip_characters(text: str, keep: Union[str, Sequence[str]] = "fa") -> str:
    """Keep only letters from the specified scripts. Drops everything else
    (digits, punctuation, etc.) — replace with space.

    `keep` may be "fa", "en", "ar", or a list like ["fa", "en"].
    """
    if isinstance(keep, str):
        keep = [keep]
    keep = set(keep)

    # Build allowed character ranges
    ranges = []
    if "fa" in keep or "ar" in keep:
        # Arabic block (covers Persian too)
        ranges.append(("\u0600", "\u06FF"))
        ranges.append(("\u0750", "\u077F"))  # Arabic Supplement
        ranges.append(("\uFB50", "\uFDFF"))  # Arabic Presentation-A
        ranges.append(("\uFE70", "\uFEFF"))  # Arabic Presentation-B
    if "en" in keep:
        ranges.append(("\u0000", "\u007F"))  # Basic Latin
        ranges.append(("\u00C0", "\u024F"))  # Latin Extended

    # Build a regex of disallowed characters
    if not ranges:
        return text  # nothing to keep

    # Build negated class: keep whitespace + ranges, drop everything else.
    # We use chr() to insert literal characters (not \x escape sequences,
    # which collide with f-string parsing).
    keep_pattern_parts = [r"\s"]
    for lo, hi in ranges:
        keep_pattern_parts.append(f"{lo}-{hi}")
    keep_pattern = "".join(keep_pattern_parts)
    drop_pattern = re.compile(f"[^{keep_pattern}]", flags=re.UNICODE)
    return drop_pattern.sub(" ", text)


def remove_extra_spaces(text: str) -> str:
    """Collapse multiple spaces/tabs into one. Preserve newlines."""
    text = _MULTI_SPACE.sub(" ", text)
    # Trim trailing spaces at end of each line
    text = re.sub(r" +\n", "\n", text)
    # Trim leading/trailing whitespace per the whole string
    text = text.strip()
    return text


# ---------------------------------------------------------------------------
# paknevis-style editorial fixes (typographic, conservative, idempotent)
# ---------------------------------------------------------------------------

def fix_arabic_chars(text: str) -> str:
    """Map Arabic ي/ك/ة/ؤ/إ/أ to their Persian equivalents."""
    return text.translate(_ARABIC_TO_PERSIAN)


def fix_persian_punctuation(text: str) -> str:
    """Convert English punctuation to Persian equivalents:
    ? → ؟, ; → ؛, , → ،, and "..." → «...» (paired guillemets).
    """
    text = text.replace("?", "؟").replace(";", "؛").replace(",", "،")
    # Paired double quotes → guillemets
    # Find pairs of " and replace them with « »
    out = []
    open_quote = True
    for ch in text:
        if ch == '"':
            out.append("«" if open_quote else "»")
            open_quote = not open_quote
        else:
            out.append(ch)
    # Single quotes '...' → «» too (common Persian style)
    result = "".join(out)
    # Convert '...' (apostrophe-wrapped) → «...», but skip apostrophes used as
    # English possessives (after a letter): only convert when the opening quote
    # is at start-of-string or preceded by whitespace.
    result = re.sub(r"(^|\s)'([^']+)'", r"\1«\2»", result)
    return result


def fix_punctuation_spacing(text: str) -> str:
    """Remove space before punctuation: 'hello ?' → 'hello?'.
    Collapse multiple spaces after punctuation to a single space.
    """
    text = _PUNCT_SPACE_BEFORE.sub(r"\1", text)
    text = _PUNCT_SPACE_AFTER_DOT.sub(r"\1 ", text)
    return text


def fix_ezafe(text: str) -> str:
    """Convert the ezafe marker 'ی' (when written as a separate ZWNJ-joined
    character) to the proper 'ـِ' kasre or simply to 'ی' without ZWNJ.

    Paknevis rule: خانه‌ی → خانهٔ (hamza above)
    We use the Unicode 'ARABIC LETTER HEH WITH YEH ABOVE' (U+06C0) which is
    the typographically correct Persian ezafe form.
    """
    # خانه‌ی → خانهٔ  (U+06C0 = ARABIC LETTER HEH WITH YEH ABOVE)
    text = re.sub(r"(\S)" + ZWNJ + r"ی\b", r"\1" + "\u06C0", text)
    # Also handle خانه ی (with regular space) → خانهٔ only when the next
    # word starts with a non-Persian-letter boundary.
    return text


def fix_ellipsis(text: str) -> str:
    """Normalize ellipsis to a single U+2026 (…).
    '...' or '. . .' or '……' → '…'. Does NOT consume surrounding whitespace.
    """
    text = _ELLIPSIS_DOTS.sub("…", text)
    text = _ELLIPSIS_MANY.sub("…", text)
    text = _ELLIPSIS_COLLAPSE.sub("…", text)
    return text


def fix_repeated_punctuation(text: str) -> str:
    """Collapse repeated ?/!/?/? marks: ??? → ?, !!! → !, ؟؟؟ → ؟."""
    return fix_multiple_punctuations(text)


def fix_zwnj_verbs(text: str) -> str:
    """Insert ZWNJ between verb prefix and verb stem.
    'می روم' → 'می‌روم', 'نمی شود' → 'نمی‌شود'.
    """
    # Handle می / نمی followed by space then a verb stem (Persian letters).
    # The verb stem should be at least 2 letters and word-bounded.
    text = re.sub(r"\b(ن?می)\s+([ء-ی]{2,})", r"\1" + ZWNJ + r"\2", text)
    return text


def fix_zwnj_compound_verbs(text: str) -> str:
    """Remove the space inside compound verbs formed from preverb + verb stem.
    'فرا گرفتن' → 'فراگرفتن', 'باز گشتن' → 'بازگشتن'.
    """
    # We only join when followed by a known verb-stem pattern. Conservative:
    # join prefix + space + stem when stem is a common verb root.
    common_stems = (
        "گرفتن|گرفت|می‌گیرم|گرفته|برداشتن|گشتن|گشت|گشتم|نشست|نشستن|ایستاد|ایستادن|"
        "آمد|آمدن|رفت|رفتن|داشت|داشتن|شد|شدن|کرد|کردن|زد|زدن|خورد|خوردن|"
        "یافت|یافتن|گذاشت|گذاشتن|داد|دادن|گفت|گفتن|دید|دیدن|دانست|دانستن"
    )
    pattern = re.compile(
        r"\b(" + "|".join(_COMPOUND_PREFIXES) + r")\s+(" + common_stems + r")\b"
    )
    return pattern.sub(r"\1\2", text)


def fix_zwnj_suffixes(text: str) -> str:
    """Insert ZWNJ before comparative/superlative/plural suffixes.
    'کثیف تر' → 'کثیف‌تر', 'کتاب ها' → 'کتاب‌ها', 'خوب ترین' → 'خوب‌ترین'.
    """
    # Match a Persian word followed by space + suffix at word boundary.
    # Avoid inserting ZWNJ if it's already there.
    suffix_alt = "تر|ترین|ها|های|هایی"
    pattern = re.compile(
        r"([ء-یء-۾][ء-یء-۾]*?)\s+(" + suffix_alt + r")\b"
    )
    return pattern.sub(r"\1" + ZWNJ + r"\2", text)


def fix_zwnj_possessives(text: str) -> str:
    """Insert ZWNJ before possessive enclitics.
    'خانه ام' → 'خانه‌ام', 'کتابت' (no space — already joined correctly).
    """
    pattern = re.compile(
        r"([ء-یء-۾][ء-یء-۾]*?)\s+(" + "|".join(_POSSESSIVES) + r")\b"
    )
    return pattern.sub(r"\1" + ZWNJ + r"\2", text)


# ---------------------------------------------------------------------------
# normalize_persian (davat-style comprehensive normalization)
# ---------------------------------------------------------------------------

def normalize_persian(
    text: str,
    use_dictionary: bool = False,
    dictionary: Optional[set] = None,
) -> str:
    """Comprehensive Persian normalization.

    Steps (in order):
      1. Unicode NFC normalization
      2. Arabic → Persian character mapping (ي/ك/ة/...)
      3. Diacritic removal (harakat)
      4. Keshide (tatweel ـ) removal
      5. Digit conversion to Persian
      6. Quotation marks → «»
      7. Punctuation spacing fix
      8. ZWNJ fixes for verbs / suffixes / possessives (paknevis rules)
      9. Ezafe kasre fix
     10. Ellipsis normalization
     11. Repeated-letter collapse (عاااالی → عالی)
     12. Extra space collapse

    If `use_dictionary=True`, the repeated-letter collapse becomes
    dictionary-aware: legitimate doubled letters in words like الله, موسسه,
    تردد are preserved. The dictionary is loaded from the bundled
    `assets/persian_words.txt` (or override with `dictionary=set(...)`).
    """
    if not isinstance(text, str):
        return text

    # 1. NFC
    text = unicodedata.normalize("NFC", text)

    # 2. Arabic → Persian
    text = fix_arabic_chars(text)

    # 3-4. Diacritics + keshide removal
    for d in _DIACRITICS:
        text = text.replace(d, "")
    text = text.replace("\u0640", "")  # tatweel/keshide

    # 5. Digits → Persian
    text = convert_digits(text, to="fa")

    # 6. Quotes → guillemets (only paired)
    text = fix_persian_punctuation(text)

    # 7. Punctuation spacing
    text = fix_punctuation_spacing(text)

    # 8. ZWNJ fixes (paknevis)
    text = fix_zwnj_verbs(text)
    text = fix_zwnj_suffixes(text)
    text = fix_zwnj_possessives(text)
    text = fix_zwnj_compound_verbs(text)

    # 9. Ezafe
    text = fix_ezafe(text)

    # 10. Ellipsis
    text = fix_ellipsis(text)

    # 11. Repeated-letter collapse
    if use_dictionary:
        if dictionary is None:
            dictionary = load_dictionary()
        text = _dict_aware_collapse(text, dictionary)
    else:
        text = _REPEATED_LETTER.sub(r"\1", text)

    # 12. Extra spaces
    text = remove_extra_spaces(text)
    return text


def _dict_aware_collapse(text: str, dictionary: set) -> str:
    """Collapse 3+ repeated letters, but preserve legitimate doubles that the
    dictionary knows about (الله, موسسه, تردد, محقق).

    Algorithm per word:
      1. If word is already in dictionary → leave alone.
      2. Try least-aggressive collapse (4+ → 2) — preserves legitimate doubles.
      3. Try 3+ → 2 — preserves legitimate doubles in 3-letter runs.
      4. Try 3+ → 1 — most aggressive, may break legitimate doubles.
      5. Pick the first candidate that's in the dictionary; else fall back to (4).
    """
    if not dictionary:
        return _REPEATED_LETTER.sub(r"\1", text)

    def _collapse_word(w: str) -> str:
        m = re.match(r"^(\W*)(\S+?)(\W*)$", w)
        if not m:
            return _REPEATED_LETTER.sub(r"\1", w)
        pre, core, post = m.groups()
        if core in dictionary:
            return w
        # Build candidates from least to most aggressive
        c_4to2 = re.sub(r"(.)\1{3,}", r"\1\1", core)         # 4+ → 2
        c_3to2 = re.sub(r"(.)\1{2,}", r"\1\1", core)         # 3+ → 2
        c_3to1 = _REPEATED_LETTER.sub(r"\1", core)             # 3+ → 1
        for c in (c_4to2, c_3to2, c_3to1):
            if c != core and c in dictionary:
                return pre + c + post
        # No candidate in dict → use most-aggressive collapse
        return pre + (c_3to1 if c_3to1 != core else core) + post

    return " ".join(_collapse_word(w) for w in text.split(" "))


# ---------------------------------------------------------------------------
# Spellcheck (paknevis-style, dictionary-assisted)
# ---------------------------------------------------------------------------

def spellcheck(
    text: str,
    dictionary: Optional[set] = None,
    max_distance: int = 1,
) -> str:
    """Lightweight spell-checker. For each word not in the dictionary, find
    the closest dictionary word within edit distance `max_distance` and
    replace. Leaves correctly-spelled words untouched.

    Notes:
      * Uses Levenshtein distance with early termination.
      * Applies curated common-misspelling fixes first (fast path).
      * Dictionary is the bundled mini-dictionary by default; pass your own
        set for production use.
    """
    if dictionary is None:
        dictionary = load_dictionary()
    if not dictionary:
        # No dictionary — only apply curated common-misspelling table
        for wrong, right in _COMMON_MISSPELLINGS.items():
            text = re.sub(r"\b" + re.escape(wrong) + r"\b", right, text)
        return text

    def _fix_token(tok: str) -> str:
        # Strip surrounding punctuation for lookup
        m = re.match(r"^(\W*)(\S+?)(\W*)$", tok)
        if not m:
            return tok
        pre, core, post = m.groups()
        if not core or core in dictionary:
            return tok
        # Curated table first
        if core in _COMMON_MISSPELLINGS:
            return pre + _COMMON_MISSPELLINGS[core] + post
        # Levenshtein search within max_distance. Ranking among candidates:
        #   1. smaller edit distance
        #   2. "doubled-letter collapse" candidates (متتن → متن) — the classic
        #      fat-finger typo — beat everything else at the same distance
        #   3. more frequent word (dictionary file order)
        collapsed = re.sub(r"(.)\1+", r"\1", core)
        best = None
        best_key = (max_distance + 1, 1, float("inf"))
        for w in dictionary:
            if abs(len(w) - len(core)) > max_distance:
                continue
            d = _levenshtein(core, w, max_distance=max_distance + 1)
            if d <= max_distance:
                key = (d, 0 if (w == collapsed and w != core) else 1,
                       _DICT_RANK.get(w, float("inf")))
                if key < best_key:
                    best_key = key
                    best = w
        if best is not None:
            return pre + best + post
        return tok

    return " ".join(_fix_token(t) for t in text.split(" "))


def _levenshtein(a: str, b: str, max_distance: int = 2) -> int:
    """Levenshtein distance with early termination."""
    if abs(len(a) - len(b)) > max_distance:
        return max_distance + 1
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        best = i
        for j, cb in enumerate(b, 1):
            ins = curr[j - 1] + 1
            dele = prev[j] + 1
            sub = prev[j - 1] + (0 if ca == cb else 1)
            curr.append(min(ins, dele, sub))
            best = min(best, curr[-1])
        if best > max_distance:
            return max_distance + 1
        prev = curr
    return prev[-1]


# ---------------------------------------------------------------------------
# Pipelines
# ---------------------------------------------------------------------------

# davat-style: aggressive cleaning (removes content)
PERSIAN_STEPS = [
    remove_links,
    remove_mentions,
    remove_hashtags,
    remove_emojis,
    normalize_persian,
    fix_multiple_punctuations,
    partial(strip_characters, keep="fa"),
    remove_extra_spaces,
]

# Minimal: only structural cleanup
MINIMAL_STEPS = [
    remove_links,
    remove_emojis,
    remove_extra_spaces,
]

# paknevis-style: conservative editorial pass (preserves content)
EDITOR_STEPS = [
    fix_arabic_chars,
    convert_digits,            # default to=fa
    fix_persian_punctuation,
    fix_zwnj_verbs,
    fix_zwnj_suffixes,
    fix_zwnj_possessives,
    fix_zwnj_compound_verbs,
    fix_punctuation_spacing,
    fix_ezafe,
    fix_ellipsis,
    fix_repeated_punctuation,
    remove_extra_spaces,
]


def edit_persian(text: str, do_spellcheck: bool = False) -> str:
    """Paknevis-style editorial pass. Conservative — preserves all content
    (links, mentions, hashtags, emojis all stay) but fixes typography:
    ZWNJ placement, Arabic→Persian chars, digits, punctuation, ezafe,
    ellipsis, repeated marks, extra spaces.

    If `do_spellcheck=True`, also runs the spell-checker at the end.
    """
    for step in EDITOR_STEPS:
        text = step(text)
    if do_spellcheck:
        text = spellcheck(text)
    return text


def clean(
    text: str,
    steps: Optional[Sequence[Callable[[str], str]]] = None,
) -> str:
    """Apply a pipeline of cleanup functions in order.

    If `steps` is None, uses PERSIAN_STEPS (the davat default).
    """
    if steps is None:
        steps = PERSIAN_STEPS
    for step in steps:
        text = step(text)
    return text


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

_FN_REGISTRY = {
    "convert_digits": convert_digits,
    "remove_links": remove_links,
    "remove_mentions": remove_mentions,
    "remove_hashtags": remove_hashtags,
    "remove_emojis": remove_emojis,
    "remove_markdown": remove_markdown,
    "remove_punctuations": remove_punctuations,
    "fix_multiple_punctuations": fix_multiple_punctuations,
    "remove_ellipsis": remove_ellipsis,
    "strip_characters": strip_characters,
    "remove_extra_spaces": remove_extra_spaces,
    "normalize_persian": normalize_persian,
    "fix_arabic_chars": fix_arabic_chars,
    "fix_persian_punctuation": fix_persian_punctuation,
    "fix_punctuation_spacing": fix_punctuation_spacing,
    "fix_ezafe": fix_ezafe,
    "fix_ellipsis": fix_ellipsis,
    "fix_repeated_punctuation": fix_repeated_punctuation,
    "fix_zwnj_verbs": fix_zwnj_verbs,
    "fix_zwnj_suffixes": fix_zwnj_suffixes,
    "fix_zwnj_possessives": fix_zwnj_possessives,
    "fix_zwnj_compound_verbs": fix_zwnj_compound_verbs,
    "edit_persian": edit_persian,
    "spellcheck": spellcheck,
    "clean": clean,
}

_PRESETS = {
    "persian": PERSIAN_STEPS,
    "minimal": MINIMAL_STEPS,
    "editor": EDITOR_STEPS,
}


def _parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="persian_cleanup",
        description="Persian text cleanup, normalization, and editorial toolkit "
                    "(merges paknevis + davat).",
    )
    p.add_argument("text", nargs="?", help="Input text. If omitted, read from --in or stdin.")
    p.add_argument("--in", dest="in_path", help="Read input from this file.")
    p.add_argument("--out", dest="out_path", help="Write output to this file (default: stdout).")
    p.add_argument(
        "--edit", action="store_true",
        help="Paknevis-style editorial pass (conservative, preserves content).",
    )
    p.add_argument(
        "--normalize", action="store_true",
        help="Run normalize_persian() (davat-style comprehensive normalization).",
    )
    p.add_argument(
        "--spellcheck", action="store_true",
        help="Also run spell-checker (only meaningful with --edit or --normalize).",
    )
    p.add_argument(
        "--fn", help="Run a single function by name. Use --list to see all.",
    )
    p.add_argument(
        "--to", default="fa", choices=("fa", "en", "ar"),
        help="For convert_digits: target script (default: fa).",
    )
    p.add_argument(
        "--keep", default="fa",
        help="For strip_characters: comma-separated scripts (e.g. 'fa,en').",
    )
    p.add_argument(
        "--keep-hashtag-text", action="store_true", default=True,
        help="For remove_hashtags: keep the hashtag body text (default).",
    )
    p.add_argument(
        "--drop-hashtag-text", dest="keep_hashtag_text", action="store_false",
        help="For remove_hashtags: drop the whole hashtag.",
    )
    p.add_argument(
        "--use-dictionary", action="store_true",
        help="For normalize_persian: enable dictionary-aware collapse.",
    )
    p.add_argument(
        "--steps",
        help="Comma-separated pipeline of function names (e.g. 'remove_links,remove_emojis').",
    )
    p.add_argument(
        "--preset", choices=tuple(_PRESETS.keys()),
        help="Use a preset pipeline.",
    )
    p.add_argument("--json", action="store_true", help="Output JSON with input/output/steps.")
    p.add_argument("--list", action="store_true", help="List all available functions and exit.")
    p.add_argument("--version", action="version", version=f"persian_cleanup {__version__}")
    return p.parse_args(argv)


def _read_input(args: argparse.Namespace) -> str:
    if args.text is not None:
        return args.text
    if args.in_path:
        with open(args.in_path, "r", encoding="utf-8") as fh:
            return fh.read()
    # Read from stdin if it's not a TTY (piped input)
    if not sys.stdin.isatty():
        return sys.stdin.read()
    sys.stderr.write("error: no input provided. Pass text as arg, --in FILE, or pipe via stdin.\n")
    sys.exit(2)


def _write_output(args: argparse.Namespace, text: str) -> None:
    if args.out_path:
        with open(args.out_path, "w", encoding="utf-8") as fh:
            fh.write(text)
    else:
        sys.stdout.write(text)
        if not text.endswith("\n"):
            sys.stdout.write("\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = _parse_args(argv)

    if args.list:
        for name in sorted(_FN_REGISTRY):
            print(name)
        print()
        print("Presets: " + ", ".join(_PRESETS))
        return 0

    text = _read_input(args)
    applied = []

    if args.fn:
        if args.fn not in _FN_REGISTRY:
            sys.stderr.write(f"error: unknown function {args.fn!r}. Use --list.\n")
            return 2
        fn = _FN_REGISTRY[args.fn]
        # Bind extra args for specific functions
        if args.fn == "convert_digits":
            out = fn(text, to=args.to)
        elif args.fn == "strip_characters":
            keep = [k.strip() for k in args.keep.split(",")]
            out = fn(text, keep=keep)
        elif args.fn == "remove_hashtags":
            out = fn(text, keep_text=args.keep_hashtag_text)
        elif args.fn == "normalize_persian":
            out = fn(text, use_dictionary=args.use_dictionary)
        else:
            out = fn(text)
        applied = [args.fn]
    elif args.preset:
        out = clean(text, steps=_PRESETS[args.preset])
        applied = [args.preset]
    elif args.steps:
        names = [s.strip() for s in args.steps.split(",") if s.strip()]
        steps = []
        for n in names:
            if n not in _FN_REGISTRY:
                sys.stderr.write(f"error: unknown function {n!r}. Use --list.\n")
                return 2
            steps.append(_FN_REGISTRY[n])
        out = clean(text, steps=steps)
        applied = names
    elif args.edit:
        out = edit_persian(text, do_spellcheck=args.spellcheck)
        applied = ["edit_persian"] + (["spellcheck"] if args.spellcheck else [])
    elif args.normalize:
        out = normalize_persian(text, use_dictionary=args.use_dictionary)
        if args.spellcheck:
            out = spellcheck(out)
        applied = ["normalize_persian"] + (["spellcheck"] if args.spellcheck else [])
    else:
        # Default: davat-style aggressive clean
        out = clean(text)
        applied = ["PERSIAN_STEPS"]

    if args.json:
        payload = {
            "input": text,
            "output": out,
            "steps_applied": applied,
        }
        sys.stdout.write(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    else:
        _write_output(args, out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
