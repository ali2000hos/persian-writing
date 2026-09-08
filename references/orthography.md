# Persian orthography: the mechanical layer

Correct orthography is what separates a professional Persian document from a
typed-in-a-hurry one. Readers may not name the rule, but they feel it. All of
this is enforceable: `scripts/persian_cleanup.py --edit` fixes the mechanical
layer automatically; `scripts/fa_lint.py --check` reports what needs judgment.

## 1. ZWNJ — نیم‌فاصله (U+200C)

The zero-width non-joiner separates morphemes *without* a visual gap while
preventing letter joining. Writing a full space (or nothing) instead is the
most common Persian typing error, and AI-generated Persian gets it wrong both
ways. In source: `‌`, HTML `&zwnj;`, or the literal character `‌`.

Required ZWNJ positions:

| Pattern | Wrong | Right |
|---|---|---|
| می/نمی + verb | می شود، نمی توانم، میشود* | می‌شود، نمی‌توانم |
| Plural ها | کتاب ها، سایت های | کتاب‌ها، سایت‌های |
| تر / ترین | بزرگ تر، مهم ترین | بزرگ‌تر، مهم‌ترین |
| Enclitic pronouns after ه | خانه ام، پروژه اش | خانه‌ام، پروژه‌اش |
| Compound prefixes | بی دقت، هم زمان | بی‌دقت، هم‌زمان |
| Compound words | وب سایت، صفحه بندی، نرم افزار | وب‌سایت، صفحه‌بندی، نرم‌افزار |
| ای after ه | حرفه ای، هفته ای | حرفه‌ای، هفته‌ای |

*میشود (fully attached) is acceptable only in colloquial register (میشه);
in formal text always می‌شود.

Lexicalized exceptions stay solid: همکار، بهتر، کمتر، بیشتر، امروزه، آنها
(آن‌ها also correct — pick one per document).

## 2. Persian characters, not Arabic

Keyboard/copy-paste contamination. These pairs look similar but are different
codepoints, break search, and render dotted/undotted wrongly:

| Use (Persian) | Never (Arabic) |
|---|---|
| ی U+06CC | ي U+064A |
| ک U+06A9 | ك U+0643 |
| ۀ/هٔ (or ه‌ی) | ة U+0629 |
| ۴۵۶ U+06F4.. | ٤٥٦ U+0664.. |

ه with hamza: خانهٔ من or خانه‌ی من — both accepted; be consistent per document.

## 3. Digits

- Persian digits ۰۱۲۳۴۵۶۷۸۹ everywhere inside Persian prose: dates
  (۱۴۰۴/۰۴/۱۷), prices (۲۵٬۰۰۰٬۰۰۰ تومان), counts, list numbers.
- Latin digits stay Latin inside: URLs, emails, phone numbers meant for
  international dialing (+98...), code, version strings (WordPress 6.5),
  file names.
- Never Arabic-Indic variants (٤ ٥ ٦).
- Percent: «۲۰٪» (U+066A) or «۲۰ درصد». In RTL both orders render fine if the
  digits are Persian; with Latin digits «20%» the run flips LTR.
- Thousands separator: ٬ (U+066C) or، comma-free spacing — one style per doc.

## 4. Punctuation

| Persian | Replaces | Note |
|---|---|---|
| ، U+060C | , | comma |
| ؛ U+061B | ; | semicolon |
| ؟ U+061F | ? | question mark |
| «...» | "..." | quotes (گیومه) |
| … | ... | ellipsis, or سه‌نقطه |

Rules:
- No space *before* punctuation, one space *after*: «درست، مثل این.»
- ! stays ! — but one, never !!!
- Em/en dashes: not used in Persian prose. Use «،» «؛» ( ) or restructure.
- Latin fragments inside Persian (brand names, code) keep Latin punctuation
  *inside the fragment*: «افزونه WooCommerce، نسخه‌ی ۹».

## 5. Ezafe (کسره‌ی اضافه)

The unwritten -e linking noun+modifier is usually implicit (کتابِ خوب → کتاب خوب).
Write it explicitly only where the host word demands it:
- After silent ه: خانه‌ی من / خانهٔ من
- After ا and و: صدای بلند، عموی من (the ی is mandatory)
- Diacritic کسره (ِ) only for disambiguation in formal/educational text.

### 5.1 هکسره — the error Iranians mock most

Two different things sound identical at the end of a word, so writers swap them.
Getting this wrong in public copy is the single fastest way to look careless:
Iranians screenshot هکسره mistakes off billboards and brand accounts for sport.

| | What it is | Written | Example |
|---|---|---|---|
| **کسره‌ی اضافه** | links a noun to what follows (ezafe) | kasre — usually left unwritten, never «ه» | کتابِ من / کتاب من |
| **«ـه» clitic** | colloquial short form of «است» (predicate) | attached «ه» | این کتابه = این کتاب است |

**The test that always works:** replace the ending with «است» and read it aloud.
If the sentence still makes sense, the correct spelling is «ـه». If it turns to
nonsense, you need a kasre (and usually write nothing at all).

- «این کتابه» ← «این کتاب است» ✓ → «ـه» correct
- «کتابه من» ← «کتاب است من» ✗ → ezafe needed: **کتابِ من** (or plain «کتاب من»)

**Wrong → right:**

| ❌ | ✅ | Why |
|---|---|---|
| کتابه من رو ندیدی؟ | کتابِ من رو ندیدی؟ | ezafe, not «است» |
| کلاسه زبان می‌رم | کلاسِ زبان می‌رم | ezafe |
| قیمته این محصول چنده؟ | قیمتِ این محصول چنده؟ | first is ezafe, second («چنده») is «است» ✓ |
| سایته شرکت بالا نمیاد | سایتِ شرکت بالا نمیاد | ezafe |
| هوا خیلی خوبِ | هوا خیلی خوبه | predicate «است» — the reverse error |
| ماشینه من خرابه | ماشینِ من خرابه | ezafe first, «است» second ✓ |

**Careful — these are NOT errors.** Many nouns simply end in ه, and they take a
normal ezafe like any other word: خانه، نامه، برنامه، پروژه، مقاله، هفته، تجربه،
شماره، بچه. «نامه شما رسید» and «پروژه‌ی شما» are both fine; nothing was swapped.

**Register note:** the «ـه» clitic belongs to colloquial writing only. In formal
or academic text write «است» in full — «این کتاب است»، not «این کتابه». So a
formal document that contains «ـه» clitics has a register problem, not just an
orthography one (see writing-style.md).

`scripts/fa_lint.py --check` flags probable هکسره in both directions. It reports
rather than auto-fixes, because only context decides which of two identical
sounds the writer meant — and a wrong "fix" here changes the meaning.

## 6. Spacing hygiene

- Exactly one space between words; no double spaces (common AI artifact).
- No space inside «گیومه» : «درست»، نه « غلط ».
- Parentheses: بیرون فاصله، داخل نه (مثل این).
- Latin↔Persian boundary: one space — «پلتفرم WordPress برای...».

## 7. Numbers as words

Formal prose: one-word numbers under eleven often spelled out (سه پیشنهاد،
پنج مرحله). Tables, prices, stats: always digits. Don't mix styles in one list.

## 8. Common corrections table

| Wrong | Right | Why |
|---|---|---|
| میخواهم | می‌خواهم | ZWNJ after می |
| آنها را دیدم ولی کتابها نه | آن‌ها ... کتاب‌ها | ZWNJ before ها (if using آن‌ها style) |
| عليرضا | علیرضا | Arabic ي |
| لطفا | لطفاً | tanvin on Arabic loan |
| گاهاً | گاهی | tanvin on Persian word — always wrong |
| دوماً | دوم اینکه / ثانیاً | same |
| بсمت | به سمت / به‌سمت | mashed preposition |
| "نقل قول" | «نقل قول» | گیومه |
| 20 درصد | ۲۰ درصد | Persian digits |
| سال 2026 | سال ۲۰۲۶ | Persian digits |
