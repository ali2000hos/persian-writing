# davat API Reference

This file documents the davat-style API (`github.com/mh-salari/davat`),
implemented in `persian_cleanup.py`.

davat is an **aggressive cleaning** library: it removes noise (links,
mentions, hashtags, emojis, markdown) and normalizes Persian text for
downstream processing. Unlike paknevis (conservative editorial pass), davat
**does remove content** by design.

---

## Design principle: composable single-purpose functions

Every function has signature `(text: str) -> str` (or close to it). They do
**one thing** and can be composed into a pipeline:

```python
from persian_cleanup import clean, remove_links, remove_emojis, normalize_persian

steps = [remove_links, remove_emojis, normalize_persian]
clean("text", steps=steps)
```

This is the core davat pattern: small composable functions + a `clean()`
runner.

---

## Function reference

### `convert_digits(text, to="fa")`

Convert digits between Persian / English / Arabic.

```python
>>> convert_digits("123", to="fa")
'۱۲۳'
>>> convert_digits("۱۲۳", to="en")
'123'
>>> convert_digits("٠١٢", to="fa")  # Arabic → Persian
'۰۱۲'
```

### `remove_links(text)`

Remove `http://`, `https://`, and `www.` URLs.

```python
>>> remove_links("سلام https://example.com دنیا")
'سلام  دنیا'
>>> remove_links("سلام www.example.com دنیا")
'سلام  دنیا'
```

### `remove_mentions(text)`

Remove `@username` mentions (max 32 chars).

```python
>>> remove_mentions("سلام @user دنیا")
'سلام  دنیا'
```

### `remove_hashtags(text, keep_text=True)`

Remove `#` from hashtags. If `keep_text=True` (default), the hashtag body
text is preserved. If `False`, the whole hashtag is removed.

```python
>>> remove_hashtags("#سلام دنیا")
'سلام دنیا'                    # body kept, # removed
>>> remove_hashtags("#سلام دنیا", keep_text=False)
' دنیا'                        # whole hashtag removed
```

### `remove_emojis(text)`

Remove emoji and pictographic symbols across all Unicode emoji ranges
(emoticons, pictographs, transport, flags, supplemental symbols, variation
selectors, ZWJ).

```python
>>> remove_emojis("سلام 😀 دنیا")
'سلام  دنیا'
>>> remove_emojis("نسخه ۲.۰ 🚀🎉")
'نسخه ۲.۰ '
```

### `remove_markdown(text)`

Strip common Markdown formatting, keeping the text content. Handles:
`**bold**`, `*italic*`, `__bold__`, `_italic_`, `~~strike~~`, `` `code` ``,
`[link](url)`, `![alt](url)`, headings (`#`), and list markers.

```python
>>> remove_markdown("**bold** and [link](http://x.com)")
'bold and link'
>>> remove_markdown("# Heading\n- item")
'Heading\nitem'
```

### `remove_punctuations(text)`

Remove ALL punctuation (Persian + English). Replaces with space. Keeps
letters, digits, and whitespace.

```python
>>> remove_punctuations("سلام! دنیا؟")
'سلام  دنیا '
```

### `fix_multiple_punctuations(text)`

Collapse repeated punctuation marks: `???→?`, `!!!→!`, `؟؟؟→؟`, `،،،→،`.

```python
>>> fix_multiple_punctuations("چطوری???")
'چطوری?'
>>> fix_multiple_punctuations("وای!!!")
'وای!'
```

### `remove_ellipsis(text)`

Remove ellipses entirely (`...` or `…`).

```python
>>> remove_ellipsis("و... خداحافظ")
'و  خداحافظ'
```

### `strip_characters(text, keep="fa")`

Keep only letters from the specified script(s). Replace everything else
(digits, punctuation, other scripts) with space.

`keep` may be a string `"fa"`, `"en"`, `"ar"`, or a list `["fa", "en"]`.

```python
>>> strip_characters("hello سلام world", keep="fa")
' سلام '
>>> strip_characters("hello سلام world", keep=["fa", "en"])
'hello سلام world'
>>> strip_characters("hello سلام مرحبا שלום", keep=["fa", "ar"])
' سلام مرحبا '
```

### `remove_extra_spaces(text)`

Collapse multiple spaces/tabs into one. Trim per-line trailing spaces and
whole-string leading/trailing whitespace. Preserve newlines.

```python
>>> remove_extra_spaces("سلام  دنیا")
'سلام دنیا'
>>> remove_extra_spaces("سلام\t\tدنیا")
'سلام دنیا'
```

### `normalize_persian(text, use_dictionary=False)`

Comprehensive Persian normalization. Applies (in order):

1. Unicode NFC normalization
2. Arabic → Persian character mapping (`ي→ی`, `ك→ک`, `ة→ه`, ...)
3. Diacritic removal (harakat: fatha, kasra, damma, shadda, sukun, ...)
4. Keshide (tatweel `ـ`) removal
5. Digit conversion to Persian
6. Quotation marks → `«»`
7. Punctuation spacing fix
8. ZWNJ fixes for verbs / suffixes / possessives / compound verbs (paknevis rules)
9. Ezafe kasre fix (`خانه‌ی → خانهۀ`)
10. Ellipsis normalization (`... → …`)
11. Repeated-letter collapse (`عاااالی → عالی`)
12. Extra space collapse

```python
>>> normalize_persian("بِسْمِ اللَّهِ الرَّحْمنِ الرَّحِيمِ")
'بسم الله الرحمن الرحیم'

>>> normalize_persian("كيك 123 مي رود")
'کیک ۱۲۳ می‌رود'

>>> normalize_persian("ســــــــلام")  # keshide removed
'سلام'
```

**Dictionary-aware collapse (`use_dictionary=True`):**

By default, 3+ repeated characters collapse to a single character
(`عاااالی → عالی`). This can break legitimate doubled letters in words like
`الله` (which contains `لل`).

Setting `use_dictionary=True` enables dictionary-aware collapse: it tries
multiple collapse lengths (4+→2, 3+→2, 3+→1) and picks the first one that
matches a dictionary word.

```python
# Without dictionary
>>> normalize_persian("اللله")           # 3+ → 1, breaks لل
'اله'

# With dictionary
>>> normalize_persian("اللله", use_dictionary=True)
'الله'                                   # preserved — dict knows الله has لل

>>> normalize_persian("موسسسسسه", use_dictionary=True)
'موسسه'                                  # preserved

>>> normalize_persian("تردددد", use_dictionary=True)
'تردد'                                   # preserved
```

**Tradeoff:** The dictionary lookup means some informal/slang words may not
collapse to what you'd expect. For example, `نههههه` collapses to `نهه`
(not `نه`) because `نهه` is a valid word in the dictionary. This is the
price of preserving legitimate doubles.

---

## Pipeline runner

### `clean(text, steps=None)`

Apply a sequence of cleanup functions in order.

If `steps` is `None`, uses `PERSIAN_STEPS` (the davat default).

```python
>>> clean("سلام https://x.com 😀 @user #هشتگ")
'سلام هشتگ'

# Custom pipeline
>>> from functools import partial
>>> clean(
...     "hello سلام مرحبا https://x.com 😀 שלום",
...     steps=[
...         remove_links,
...         remove_emojis,
...         partial(strip_characters, keep=["fa", "en", "ar"]),
...         remove_extra_spaces,
...     ],
... )
'hello سلام مرحبا'
```

---

## Preset pipelines

### `PERSIAN_STEPS` (default)

Full Persian cleaning pipeline. Aggressive.

```python
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
```

Effect: removes links, mentions, hashtags (keeps body text), emojis;
normalizes Persian; strips non-Persian characters; collapses spaces.

### `MINIMAL_STEPS`

Just structural cleanup. Does NOT normalize Persian or strip characters.

```python
MINIMAL_STEPS = [
    remove_links,
    remove_emojis,
    remove_extra_spaces,
]
```

### `EDITOR_STEPS` (paknevis-style)

Conservative editorial pass. Does NOT remove any content. See
`paknevis-rules.md` for details.

---

## Common pipeline patterns

### Social-media sentiment analysis

Strip all noise (links, mentions, emojis), keep hashtag body text for
context:

```python
steps = [
    remove_links,
    remove_mentions,
    remove_emojis,
    normalize_persian,
    remove_extra_spaces,
]
clean(tweet, steps=steps)
```

### Search indexing

Normalize aggressively, keep all content:

```python
steps = [
    normalize_persian,
    remove_extra_spaces,
]
clean(doc, steps=steps)
```

### Multilingual document processing

Keep Persian, English, and Arabic; drop everything else:

```python
from functools import partial
steps = [
    remove_links,
    remove_emojis,
    partial(strip_characters, keep=["fa", "en", "ar"]),
    remove_extra_spaces,
]
clean(doc, steps=steps)
```

### LLM prompt preprocessing

Conservative editorial pass to improve tokenization:

```python
# Use the paknevis-style editorial pass
from persian_cleanup import edit_persian
clean_prompt = edit_persian(user_input)
```

---

## Credits

The davat project: <https://github.com/mh-salari/davat>

davat's bundled dictionary comes from
<https://github.com/shahind/Persian-Words-Database>.
