# paknevis Editorial Rules — Detailed Reference

This file documents each editorial rule implemented from the paknevis project
(<https://github.com/afshin-ir/paknevis>), with before/after examples.

paknevis is a **conservative editorial pass**: it fixes Persian typography
without removing any content. Links, mentions, hashtags, emojis — all stay
where they are. Only the *form* of the text changes.

All functions below have the signature `(text: str) -> str` and are
**idempotent** (running twice gives the same result as running once).

---

## 1. ZWNJ for prefixed verbs — `fix_zwnj_verbs`

Persian verbs with the prefix `می` / `نمی` must be joined to the verb stem
with a **Zero-Width Non-Joiner** (ZWNJ, U+200C), not a regular space.

| Before | After |
|--------|-------|
| `می روم` | `می‌روم` |
| `نمی شود` | `نمی‌شود` |
| `می کند` | `می‌کند` |
| `نمی دانم` | `نمی‌دانم` |

The function inserts ZWNJ between `می`/`نمی` and the following verb stem
when a regular space is present.

---

## 2. Compound-verb prefix joining — `fix_zwnj_compound_verbs`

Some Persian verbs are formed from a preverb + verb stem, e.g. `فرا` + `گرفتن`
= `فراگرفتن`. When written with a space, they should be **joined without
any separator** (not even ZWNJ).

| Before | After |
|--------|-------|
| `فرا گرفتن` | `فراگرفتن` |
| `فرا گرفت` | `فراگرفت` |
| `باز گشتن` | `بازگشتن` |
| `باز گشت` | `بازگشت` |
| `در یافت` | `دریافت` |
| `وا گذاشت` | `واگذاشت` |

The function joins a known preverb (`فرا`, `باز`, `در`, `بر`, `بی`, `وا`)
to a known verb stem when separated by a space.

---

## 3. ZWNJ for comparative / superlative / plural suffixes — `fix_zwnj_suffixes`

The comparative suffix `تر`, superlative `ترین`, and plural `ها` / `های` /
`هایی` attach to the noun/adjective with **ZWNJ**.

| Before | After |
|--------|-------|
| `کثیف تر` | `کثیف‌تر` |
| `خوب ترین` | `خوب‌ترین` |
| `کتاب ها` | `کتاب‌ها` |
| `کتاب های` | `کتاب‌های` |
| `کتاب هایی` | `کتاب‌هایی` |

---

## 4. ZWNJ for possessive enclitics — `fix_zwnj_possessives`

Possessive enclitics (`ام`, `ات`, `اش`, `مان`, `تان`, `شان`) attach with ZWNJ.

| Before | After |
|--------|-------|
| `خانه ام` | `خانه‌ام` |
| `کتاب اش` | `کتاب‌اش` |
| `خانه مان` | `خانه‌مان` |
| `کتاب تان` | `کتاب‌تان` |
| `دوست شان` | `دوست‌شان` |

---

## 5. Arabic → Persian character mapping — `fix_arabic_chars`

Persian uses a slightly different alphabet from Arabic. Common substitutions:

| Arabic | Persian | Reason |
|--------|---------|--------|
| `ي` (U+064A) | `ی` (U+06CC) | Arabic yeh → Persian yeh |
| `ك` (U+0643) | `ک` (U+06A9) | Arabic kaf → Persian kaf |
| `ة` (U+0629) | `ه` (U+0647) | Ta marbuta → heh |
| `ؤ` (U+0624) | `و` (U+0648) | Waw with hamza → waw |
| `إ` (U+0625) | `ا` (U+0627) | Alef with hamza below → alef |
| `أ` (U+0623) | `ا` (U+0627) | Alef with hamza above → alef |
| `ٰ` (U+0670) | (removed) | Superscript alef |

---

## 6. Digit conversion — `convert_digits`

| Input | `to="fa"` | `to="en"` | `to="ar"` |
|-------|-----------|-----------|-----------|
| `123` | `۱۲۳` | `123` | `١٢٣` |
| `۱۲۳` | `۱۲۳` | `123` | `١٢٣` |
| `٠١٢` | `۰۱۲` | `012` | `٠١٢` |

Persian digits: `۰۱۲۳۴۵۶۷۸۹` (U+06F0..U+06F9)
Arabic digits: `٠١٢٣٤٥٦٧٨٩` (U+0660..U+0669)
English digits: `0123456789`

---

## 7. English → Persian punctuation — `fix_persian_punctuation`

| English | Persian | Note |
|---------|---------|------|
| `?` | `؟` | Question mark |
| `;` | `؛` | Semicolon |
| `,` | `،` | Comma |
| `"..."` | `«...»` | Double quotes → guillemets (paired) |
| `'...'` | `«...»` | Single quotes → guillemets (only at word boundary) |

Quote pairing: opens with `«`, closes with `»,` alternates correctly for
multiple pairs in the same string.

---

## 8. Punctuation spacing — `fix_punctuation_spacing`

Removes space before punctuation and collapses multiple spaces after.

| Before | After |
|--------|-------|
| `hello ? world` | `hello? world` |
| `سلام ، دنیا` | `سلام، دنیا` |
| `سلام  ،  دنیا` | `سلام، دنیا` |
| `او گفت : سلام` | `او گفت: سلام` |

---

## 9. Ezafe kasre fix — `fix_ezafe`

The Persian ezafe (کسرهٔ اضافه) is the unstressed "of" connector. When
written with ZWNJ + `ی`, it should use the **hamza-above form** (U+06C0:
ARABIC LETTER HEH WITH YEH ABOVE).

| Before | After |
|--------|-------|
| `خانه‌ی بزرگ` | `خانهۀ بزرگ` |
| `دوست‌ی وفادار` | `دوستۀ وفادار` |

---

## 10. Ellipsis normalization — `fix_ellipsis`

Replaces any sequence of 3+ dots (with optional spaces between) with the
single Unicode ellipsis character `…` (U+2026).

| Before | After |
|--------|-------|
| `و...` | `و…` |
| `و ...` | `و …` |
| `. . .` | `…` |
| `....` | `…` |
| `………` | `…` |

---

## 11. Repeated punctuation collapse — `fix_repeated_punctuation`

Collapses consecutive `?`, `!`, `?` (Persian), `!` (Persian), `،`, `,`, `.`
into a single character.

| Before | After |
|--------|-------|
| `???` | `?` |
| `!!!` | `!` |
| `؟؟؟` | `؟` |
| `،،،` | `،` |

Note: this function does **not** convert English `?` to Persian `؟`. Use
`fix_persian_punctuation` for that.

---

## 12. Extra-space removal — `remove_extra_spaces`

Collapses multiple spaces/tabs into one, trims trailing spaces per line,
and strips leading/trailing whitespace from the whole string. Preserves
newlines.

| Before | After |
|--------|-------|
| `سلام  دنیا` | `سلام دنیا` |
| `سلام\tدنیا` | `سلام دنیا` |
| `  سلام  ` | `سلام` |

---

## 13. Spell-check — `spellcheck`

Lightweight dictionary-assisted spell-checker:

1. For each word not in the dictionary, apply a curated common-misspelling
   table (fast path).
2. If still not found, search the dictionary for the closest word within
   Levenshtein distance 1.
3. Replace if a close match is found; otherwise leave the word alone.

Curated common misspellings (subset):

| Wrong | Right |
|-------|-------|
| `لطفا` | `لطفاً` |
| `انشاالله` | `ان‌شاءالله` |
| `بهرحال` | `به‌هرحال` |

For better coverage, replace the bundled mini-dictionary
(`assets/persian_words.txt`, ~500 words) with the full 453K-word list from
<https://github.com/shahind/Persian-Words-Database>.

---

## 14. Full editorial pass — `edit_persian`

Applies all paknevis rules in order:

1. `fix_arabic_chars`
2. `convert_digits` (to=fa)
3. `fix_persian_punctuation`
4. `fix_zwnj_verbs`
5. `fix_zwnj_suffixes`
6. `fix_zwnj_possessives`
7. `fix_zwnj_compound_verbs`
8. `fix_punctuation_spacing`
9. `fix_ezafe`
10. `fix_ellipsis`
11. `fix_repeated_punctuation`
12. `remove_extra_spaces`

Optional: pass `do_spellcheck=True` to also run the spell-checker at the end.

---

## Why these rules matter

Persian typography has many ambiguities that machine-written text frequently
gets wrong:

* ZWNJ vs. space — wrong choice breaks word boundaries for tokenizers
* Arabic vs. Persian characters — breaks search and deduplication
* English vs. Persian digits — breaks numerical comparisons
* English vs. Persian punctuation — looks wrong to native readers

The paknevis rules exist to enforce the **canonical Persian typographic
form**. Applying them as a pre-processing step dramatically improves
downstream quality for: search indexing, NLP tokenization, LLM prompt
quality, deduplication, and human readability.
