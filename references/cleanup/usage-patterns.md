# Usage Patterns for AI Agents

This file collects common usage patterns for AI agents working with Persian
text. Each pattern includes: when to use it, the recommended command, and
expected behavior.

---

## Pattern 1: User pastes Persian text and asks to "ویرایش" / "fix" / "edit"

**Use:** paknevis-style conservative editorial pass.

```bash
python3 persian_cleanup.py --edit --in input.txt --out output.txt
```

Or as a one-liner:

```bash
python3 persian_cleanup.py --edit "من می روم و خانه ام و 123"
```

**What it does:** Fixes ZWNJ, Arabic→Persian chars, digits, punctuation,
ezafe, ellipsis, repeated marks, extra spaces — **without removing any
content**. The user gets back the same text with correct Persian typography.

**Why this mode:** When a user says "ویرایش" they want their text fixed,
not gutted. Links, mentions, hashtags, emojis all stay where they are.

---

## Pattern 2: User wants to clean text for NLP / ML / search indexing

**Use:** davat-style aggressive clean.

```bash
python3 persian_cleanup.py --preset persian --in input.txt --out output.txt
```

**What it does:** Removes links, mentions, hashtags (body kept), emojis;
normalizes Persian (NFC, diacritics, keshide, Arabic→Persian, digits, ZWNJ,
ezafe, ellipsis, repeated-letter collapse); strips non-Persian characters;
collapses extra spaces.

**Why this mode:** For downstream processing, you want clean normalized
text without noise. Non-Persian characters (English, Hebrew, etc.) are
typically not relevant for Persian NLP and inflate the vocabulary.

---

## Pattern 3: User wants Persian text ready for an LLM prompt

**Use:** paknevis-style editorial pass + normalize_persian.

```bash
# Two-pass: first editorial, then normalize
python3 persian_cleanup.py --edit --in input.txt --out /tmp/step1.txt
python3 persian_cleanup.py --normalize --in /tmp/step1.txt --out output.txt
```

Or in one pass with a custom pipeline:

```bash
python3 persian_cleanup.py --steps "normalize_persian,remove_extra_spaces" --in input.txt --out output.txt
```

**What it does:** Normalizes typography (ZWNJ, Arabic chars, digits,
punctuation) without removing content. LLM tokenizers handle normalized
Persian much better than mixed-form Persian.

**Why this mode:** LLMs benefit from consistent input. ZWNJ placement
especially matters — without it, `می‌روم` may tokenize as two separate
tokens `می` and `روم`, doubling the token count for verbs.

---

## Pattern 4: User wants to convert only digits to Persian

**Use:** Single-function call.

```bash
python3 persian_cleanup.py --fn convert_digits --to fa "page 123 of 456"
# → page ۱۲۳ of ۴۵۶
```

For mixed-language text, this preserves non-digit characters.

---

## Pattern 5: User wants to convert only punctuation to Persian

**Use:** Single-function call.

```bash
python3 persian_cleanup.py --fn fix_persian_punctuation 'او گفت "سلام"?'
# → او گفت «سلام»؟
```

---

## Pattern 6: User wants to fix ZWNJ only

**Use:** Combine the three ZWNJ fixers.

```bash
python3 persian_cleanup.py --steps "fix_zwnj_verbs,fix_zwnj_suffixes,fix_zwnj_possessives,fix_zwnj_compound_verbs" "من می روم و خانه ام و کثیف تر"
# → من می‌روم و خانه‌ام و کثیف‌تر
```

---

## Pattern 7: User wants to remove noise (links/mentions/emojis) but keep Persian text intact

**Use:** Custom pipeline.

```bash
python3 persian_cleanup.py --steps "remove_links,remove_mentions,remove_emojis,normalize_persian,remove_extra_spaces" "tweet text"
```

This is the right pattern for social-media analysis where you want clean
text but don't want to strip non-Persian characters (the tweet may contain
English/Arabic words that are part of the content).

---

## Pattern 8: User wants to spell-check Persian text

**Use:** Editorial pass with spell-check.

```bash
python3 persian_cleanup.py --edit --spellcheck "متن با غلط املایی"
```

**Note:** The bundled dictionary has only ~500 words. For serious
spell-checking, replace `assets/persian_words.txt` with the full 453K-word
list:

```bash
curl -L https://raw.githubusercontent.com/shahind/Persian-Words-Database/master/words.txt \
  -o skills/persian-text-cleanup/assets/persian_words.txt
```

---

## Pattern 9: User wants to preserve legitimate doubled letters (الله, موسسه, تردد)

**Use:** normalize_persian with dictionary awareness.

```bash
python3 persian_cleanup.py --normalize --use-dictionary "اللله موسسسسسه تردددد"
# → الله موسسه تردد
```

Without `--use-dictionary`, the same input becomes `اله موسه ترد` — broken.

---

## Pattern 10: User pastes a tweet and asks for "ویرایش"

**Use:** paknevis-style editorial pass. **Do NOT** strip mentions/hashtags —
they're part of the tweet content.

```bash
python3 persian_cleanup.py --edit "سلام @user! چطوری? #هشتگ https://x.com"
# → سلام @user! چطوری؟ #هشتگ https://x.com
#   (only the ? → ؟ conversion happens, content preserved)
```

**Why this mode:** The user wants the tweet edited, not sanitized. They
explicitly wrote the @mention and #hashtag — don't delete them.

---

## Pattern 11: Batch processing multiple files

**Use:** Shell loop with the CLI.

```bash
for f in inputs/*.txt; do
  python3 persian_cleanup.py --edit --in "$f" --out "outputs/$(basename "$f")"
done
```

---

## Pattern 12: JSON output for programmatic use

**Use:** `--json` flag.

```bash
python3 persian_cleanup.py --edit --json "می روم"
# {
#   "input": "می روم",
#   "output": "می‌روم",
#   "steps_applied": ["edit_persian"]
# }
```

Useful when the agent needs to know which steps were applied (e.g. to
report to the user what was changed).

---

## Anti-patterns to avoid

### Don't use `--preset persian` for "ویرایش" requests

The persian preset removes links, mentions, hashtags, emojis, and strips
non-Persian characters. If the user wants their text "edited" (not
"cleaned"), they'll be surprised to see their @mentions and links
disappear.

### Don't use `--edit` for NLP preprocessing

The editorial pass preserves all content, including links and emojis. For
NLP tasks, you typically want them removed.

### Don't run spellcheck without a real dictionary

The bundled mini-dictionary (~500 words) is enough for common cases but
will mis-correct rare words. For production spell-checking, always swap in
the full 453K-word list.

### Don't combine `--edit` with `--use-dictionary`

`--edit` uses `EDITOR_STEPS` which does NOT include `normalize_persian`. The
`--use-dictionary` flag only affects `normalize_persian`. If you want
dictionary-aware collapse, use `--normalize --use-dictionary` instead.

---

## Decision flowchart

```
User request
    │
    ├─ "ویرایش" / "اصلاح" / "fix" / "edit"
    │       → use --edit (paknevis)
    │
    ├─ "پاکسازی" / "نرمالایز" / "clean" / "normalize"
    │       → use --normalize  (or --preset persian for aggressive)
    │
    ├─ "آماده برای NLP/ML/search/LLM"
    │       → use --preset persian (aggressive) or --steps custom
    │
    ├─ "فقط اعداد/علائم/نیم‌فاصله"
    │       → use --fn <specific_function>
    │
    ├─ "غلط‌گیری املایی"
    │       → use --edit --spellcheck (or --normalize --spellcheck)
    │
    └─ Unclear
            → default to --edit (conservative, preserves content)
```
