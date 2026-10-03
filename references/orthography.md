# Persian orthography: the mechanical layer

Correct orthography is what separates a professional Persian document from a
typed-in-a-hurry one. Readers may not name the rule, but they feel it. All of
this is enforceable: `scripts/persian_cleanup.py --edit` fixes the mechanical
layer automatically; `scripts/fa_lint.py --check` reports what needs judgment.

When *you* write documentation that must show a wrong form on purpose — as the
tables below do — suppress the linter on it rather than softening the example:

```markdown
<!-- fa-lint-ignore-next-line -->
یک خط با خطای عمدی

<!-- fa-lint-ignore-start -->
چند خط، مثلاً یک جدول کامل «غلط ← درست»
<!-- fa-lint-ignore-end -->
```

`--fix` puts suppressed lines back after the fix pass, so a deliberate error
survives. Codepoint notation such as `U+06CC` is never rewritten.

## 1. ZWNJ — نیم‌فاصله (U+200C)

The zero-width non-joiner separates morphemes *without* a visual gap while
preventing letter joining. Writing a full space (or nothing) instead is the
most common Persian typing error, and AI-generated Persian gets it wrong both
ways. In source: `‌`, HTML `&zwnj;`, or the literal character `‌`.

Required ZWNJ positions:

<!-- fa-lint-ignore-start -->

| Pattern | Wrong | Right |
|---|---|---|
| می/نمی + verb | می شود، نمی توانم، میشود* | می‌شود، نمی‌توانم |
| Plural ها | کتاب ها، سایت های | کتاب‌ها، سایت‌های |
| تر / ترین | بزرگ تر، مهم ترین | بزرگ‌تر، مهم‌ترین |
| Enclitic pronouns after ه | خانه ام، پروژه اش | خانه‌ام، پروژه‌اش |
| Compound prefixes | بی دقت، هم زمان | بی‌دقت، هم‌زمان |
| Compound words | وب سایت، صفحه بندی، نرم افزار | وب‌سایت، صفحه‌بندی، نرم‌افزار |
| ای after ه | حرفه ای، هفته ای | حرفه‌ای، هفته‌ای |

<!-- fa-lint-ignore-end -->

<!-- fa-lint-ignore-next-line -->
*میشود (fully attached) is acceptable only in colloquial register (میشه);
in formal text always می‌شود.

Lexicalized exceptions stay solid: همکار، بهتر، کمتر، بیشتر، امروزه، آنها
(آن‌ها also correct — pick one per document).

## 2. Persian characters, not Arabic

Keyboard/copy-paste contamination. These pairs look similar but are different
codepoints, break search, and render dotted/undotted wrongly:

<!-- fa-lint-ignore-start -->

| Use (Persian) | Never (Arabic) |
|---|---|
| ی U+06CC | ي U+064A |
| ک U+06A9 | ك U+0643 |
| ۀ/هٔ (or ه‌ی) | ة U+0629 |
| ۴۵۶ U+06F4.. | ٤٥٦ U+0664.. |

<!-- fa-lint-ignore-end -->

ه with hamza: خانهٔ من or خانه‌ی من — both accepted; be consistent per document.

## 3. Digits

- Persian digits ۰۱۲۳۴۵۶۷۸۹ everywhere inside Persian prose: dates
  (۱۴۰۴/۰۴/۱۷), prices (۲۵٬۰۰۰٬۰۰۰ تومان), counts, list numbers.
- Latin digits stay Latin inside: URLs, emails, phone numbers meant for
  international dialing (+98...), code, version strings (WordPress 6.5),
  file names.
<!-- fa-lint-ignore-next-line -->
- Never Arabic-Indic variants (٤ ٥ ٦).
- Percent: «۲۰٪» (U+066A) or «۲۰ درصد». In RTL both orders render fine if the
  digits are Persian; with Latin digits «20%» the run flips LTR.
- Thousands separator: ٬ (U+066C) or، comma-free spacing — one style per doc.

## 4. Punctuation

<!-- fa-lint-ignore-start -->

| Persian | Replaces | Note |
|---|---|---|
| ، U+060C | , | comma |
| ؛ U+061B | ; | semicolon |
| ؟ U+061F | ? | question mark |
| «...» | "..." | quotes (گیومه) |
| … | ... | ellipsis, or سه‌نقطه |

<!-- fa-lint-ignore-end -->

Rules:
- No space *before* punctuation, one space *after*: «درست، مثل این.»
<!-- fa-lint-ignore-next-line -->
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

<!-- fa-lint-ignore-start -->

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

<!-- fa-lint-ignore-end -->

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

<!-- fa-lint-ignore-start -->

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

<!-- fa-lint-ignore-end -->

## 9. Mixed Persian–English text: direction (bidi)

The most visible failure in mixed text is not a spelling error — it is a line
that renders backwards. Readers report it as «متن چپ‌چین شده و قابل خواندن
نیست», and they have to fix it by hand.

**Why it happens.** Most surfaces that show plain text or Markdown — chat apps,
GitHub, Telegram, note apps, Markdown previews, many editors — decide each
paragraph's direction from its **first strong letter** (the Unicode bidi
algorithm with `dir="auto"`). Persian letters are right-to-left, Latin letters
left-to-right, while digits, spaces and punctuation are neutral and take the
direction of what surrounds them. So:

<!-- fa-lint-ignore-start -->

| Line | First strong letter | Renders as |
|---|---|---|
| React یک کتابخانه است. | R of React → LTR | left-aligned, period jumps, words reorder |
| - Docker لازم است. | D → LTR | the bullet flips sides |
| ## API چیست؟ | A → LTR | the heading flips sides |
| ۲۰۲۶ سال خوبی بود. | digits are neutral → سال → RTL | correct |
| کتابخانه‌ی React را نصب کنید. | ک → RTL | correct |

<!-- fa-lint-ignore-end -->

**Rule 1: lead with a Persian word.** Every sentence, bullet, heading, table
cell, caption and message must start with a Persian word. The fix is almost
always natural Persian anyway, because Persian names a thing by its kind:

<!-- fa-lint-ignore-start -->

| ❌ Starts with Latin | ✅ Starts with Persian |
|---|---|
| React یک کتابخانه‌ی جاوااسکریپت است. | کتابخانه‌ی React برای ساخت رابط کاربری است. |
| Docker را نصب کنید. | ابتدا Docker را نصب کنید. |
| - API پاسخ را برمی‌گرداند. | - رابط API پاسخ را برمی‌گرداند. |
| ## SEO چیست؟ | ## سئو (SEO) چیست؟ |
| `npm install` را اجرا کنید. | دستور `npm install` را اجرا کنید. |
| Google Analytics داده‌ها را نشان می‌دهد. | ابزار Google Analytics داده‌ها را نشان می‌دهد. |

<!-- fa-lint-ignore-end -->

Useful leading words: ابزار، کتابخانه‌ی، فریم‌ورک، سرویس، دستور، فایل، نسخه‌ی،
شرکت، برند، زبان، افزونه‌ی، پلتفرم، سامانه‌ی، رابط. If the term has a common
Persian form, prefer it (سئو، ایمیل، اینستاگرام) and keep the Latin in
parentheses on first mention.

**Rule 2: keep each Latin run whole.** A Latin run stays left-to-right inside
the Persian line, so «نسخه‌ی Python 3.11» is fine. Problems come from splitting a
Latin phrase with Persian words or punctuation, or from a Persian word ending
in Latin punctuation. Write the run in one piece and use Persian punctuation
after it: «از React، Vue و Svelte» (Persian «،», not «,»).

**Rule 3: when a line must start with Latin** — a code identifier at the head
of a list, a product name in a table cell, a reply that quotes a command —
and the output is plain text or Markdown, run:

```bash
python3 scripts/persian_cleanup.py --bidi --in text.md --out text.md
python3 scripts/persian_cleanup.py --edit --bidi --in text.md --out text.md
```

`--bidi` puts an invisible RIGHT-TO-LEFT MARK (U+200F, RLM) at the start of only
those lines and table cells, after any Markdown marker (`- `, `## `, `> `,
`1. `). It skips code blocks and English lines, and running it twice changes
nothing. `fa_lint.py --check` reports the lines that need it as `bidi-start`.

It is opt-in, not part of `--edit`, because invisible characters have costs:
they break exact-match search, and pasted into code or a filename they cause
errors that cannot be seen. Use it for text meant to be **read**. Never use it
for code, data, filenames or URLs. It changes how a text displays, never what
it says, and has nothing to do with hiding authorship.

**Formats that carry direction in markup do not need marks.** Set the direction
there instead: HTML `dir="rtl"` plus `<bdi>` around Latin fragments
(html-css.md), DOCX `<w:bidi/>` and `<w:rtl/>` (docx-pdf.md), PowerPoint
`rtl="1"` (pptx.md), Excel `rightToLeft`. A correctly built document never
needs RLM.
