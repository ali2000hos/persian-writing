# Classic literary register (نثر فاخر)

Some Persian has to be more than correct. A letter to an elder, a founder's
foreword, a memorial note, an announcement that carries an organization's
dignity — plain formal-but-human handles these, but they read better
elevated and still clear: **نثر فاخر، سلیس، استوار و در عین حال قابل فهم**.
This file defines that register.

It is a flavor of formal-but-human, not a separate register: Part 1 of
writing-style.md still decides the register, every ban in Part 2 still holds,
and this layer only changes how the clear sentence sounds. Reach for it when
the text itself is the gesture: letters that must stay human under ceremony,
prefaces and forewords, memorials and congratulations, storytelling for a
brand with a story worth telling. Do not reach for it in proposals, invoices
or working reports; elevation there is noise the reader pays for.

## The five sources

The register is learned from five books, named here as style sources. The
features are paraphrased, and quoting is limited to the attributed snippet
below.

- **سیر حکمت در اروپا (محمدعلی فروغی)**: the lucid scholarly voice.
  Definitions come before judgments; sentences link causally and explicitly
  (زیرا، از این‌رو); a long sentence never loses the thread because every
  clause has its place; a new term gets a plain Iranian word, not a rare one.
- **دو قرن سکوت و پله‌پله تا ملاقات خدا (عبدالحسین زرین‌کوب)**: the
  resonant literary voice. The rhythm comes from paired words, not from
  decoration («دل از یار و دیار برکنند» carries its music in the pair
  «یار و دیار»); a short punchy sentence lands next to a long flowing one;
  and in پله‌پله the same pen turns plain: the metaphor lives at the level
  of the idea, the sentence stays simple.
- **سووشون (سیمین دانشور)**: the steady narrative voice. Prose that is
  simple to read and masterful to make (سهل و ممتنع); verbs and nouns carry
  the meaning, not stacked adjectives; emotion is held, not displayed; the
  vocabulary comes from daily life.
- **چشمه روشن (غلامحسین یوسفی)**: the clean critical voice. Few words,
  each earning its place; criticism without jargon; the warmth of a teacher.

## The rules

1. **Short active sentences, one idea each.** Elevation never means length.
   A sentence that needs three که-clauses is three sentences, and the
   register's dignity survives the cut.
2. **The verb and the noun do the work.** Stacked adjectives are the cheap
   imitation of this register; the real one trusts a bare verb.
3. **Pure, plain Persian.** No archaic words, no thick Arabic loans, no
   invented compound coinages. A word that needs a gloss for a general
   reader is the wrong word; the plain word for the real thing beats a
   coined abstraction.
4. **Dignity from structure, not from vocabulary.** A balanced pair
   («یار و دیار»، «گوشه و کنار») where it sits naturally, never forced;
   weight from rhythm, a four-word sentence after a long one, never from
   rare words. `fa_lint.py --check --rhythm` flags a flat cadence; the
   short/long alternation is this register's spine.
5. **Link sentences logically.** زیرا، از این‌رو، پس. Define a term before
   judging with it.
6. **Formal, respectful, alive.** The می‌باشد family is banned as everywhere;
   so are the dry administrative drone (لازم به ذکر است، در راستای) and the
   colloquial slide (میشه، رو). Full written forms, respect without ceremony.

## Worked example

<!-- fa-lint-ignore-start -->
**Before — plain formal-but-human, correct but flat:**

> جناب آقای دکتر رهنما؛ با سلام و احترام. کتاب شما را دریافت کردم و آن
> را خواندم. مطالب آن برای کار من سودمند بود. از شما سپاسگزارم و
> امیدوارم باز هم از نظرات شما استفاده کنم.

**After — the classic register, same content:**

> جناب آقای دکتر رهنما؛
> با سلام و احترام. کتاب شما رسید و با کمال میل خواندم؛ چند شب
> پیاپی، تا واپسین صفحه. سخن شما روشن است و مثال‌ها از زندگی
> روزمره‌اند؛ همین دو چیز کتاب را خواندنی کرده. از شما سپاسگزارم و
> امیدوارم پرسش‌های تازه‌ام را باز با شما در میان بگذارم.
<!-- fa-lint-ignore-end -->

What moved: the summary claim becomes a lived particular; the praise gets
its cause, carried by a verb; the sentences shorten.

A second pairing, the congratulation:

<!-- fa-lint-ignore-start -->
**Before:**

> به مناسبت روز تولدتان، صمیمانه متولد شدن شما را تبریک می‌گوییم و
> برای شما آرزوی سلامتی و شادی داریم.

**After:**

> تولدتان مبارک؛ آرزوی ما روشنیِ روزهایتان و شادیِ دلتان است.
<!-- fa-lint-ignore-end -->

## What this register is not

- Not ornament. Archaic words, forced rhymes, decoration: every ban in
  writing-style.md Part 2 still holds, and elevation never buys a banned
  tell back.
- Not longer. Most sentences in this register end up shorter than their
  flat versions. If «elevated» grew the text, the wrong thing was elevated.
- Not for everything. Chat replies stay colloquial; papers stay academic;
  proposals and working reports stay plain formal-but-human.
