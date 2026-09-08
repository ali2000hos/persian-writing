# Persian social channels: Telegram, Instagram, and repurposing

Channel craft, not channel decoration. Register comes from writing-style.md,
structure and honesty from content-structures.md; this file adds what changes
when the text is consumed on a phone, in a feed, in seconds.

The formats and signatures here are patterns, not house style. Length caps,
emoji conventions, and closing lines belong to whoever owns the channel — ask
for theirs, and if none exists, the defaults below are safe.

## 1. Rules shared by every channel

- **One central topic per piece.** A post that covers two subjects gets read as
  neither.
- **The opening states the subject.** No greeting, no «در این پست می‌خواهیم...»,
  no restating the title, no rhetorical question standing in for content.
- **Never hide the answer to create suspense.** «تا آخر بخونید» is a tax on the
  reader that costs more attention than it buys.
- **Every paragraph carries one idea** and stays short enough to scan on a
  phone — without becoming a stack of disconnected fragments.
- **Critical information is never only in the image, only in the audio, or only
  behind a link.** Each surface should stand on its own to the extent it can.
- **Warnings go beside the relevant step**, not collected at the end or buried
  in a caption.
- **The closing gives the answer, the decision criterion, or the next step** —
  not a slogan and not a summary of what was just said.
- **One call to action**, with its destination and outcome named.
- **Publish-ready output only.** Internal labels like «مقدمه»، «بدنه»،
  «جمع‌بندی» are scaffolding for the writer, and must not survive into the
  posted text.

### Emoji — and why the first word after one matters in Persian

Default to no emoji. Where a channel's style uses them, they are for **semantic
separation**, not decoration: at most one (or one fixed combination) at the
start of a block, used consistently for the same meaning throughout.

There is also a genuinely technical reason to be careful. In an RTL paragraph,
an emoji is direction-neutral, so the first *strong* character after it decides
how the line is laid out. If a Latin word follows the emoji, the line can flip
to LTR and the punctuation jumps to the wrong side. **Keep the first word after
an emoji (and the first word of every paragraph) Persian**, or wrap the Latin
fragment as described in html-css.md. This is the same bidi rule that governs
Persian digits — orthography.md §3.

A workable emoji scheme, if one is wanted: numbered markers for sequence
(1️⃣ 2️⃣ 3️⃣), one consistent symbol family for risks and limits (🛑 ⚠️), another
for benefits, results and conclusions (✅ 🟢). What matters is that a symbol
means the same thing every time it appears.

## 2. Telegram

### Structure

عنوان → شروع مستقیم → زمینه‌ی لازم → بدنه → نکته/محدودیت/هشدار → جمع‌بندی →
اقدام یا لینک در صورت نیاز.

Don't let a post become a truncated article, a compressed ad, or a loose pile
of bullet points.

**Title:** short, direct, matching the content. A question, a problem, a
comparison, a guide, or an exact count of points («۴ نکته...»). Name the brand
only when the brand or its product *is* the subject.

**Opening:** one or two paragraphs establishing the problem, why it matters,
where it applies, the misconception being corrected, or the outcome of reading.

**Body:** use whichever pattern from content-structures.md §5 fits —
step-by-step, tips, comparison, concept, troubleshooting, or product
introduction. Each carries its own internal order.

**Headings and lists:** in medium or long posts, use real subheadings.
Numbered lists for sequence, bulleted for independent items. Bold only for
headings, key concepts, warnings and results.

### Length

- **Short:** one definition, tip, warning, change, or answer.
- **Medium:** a concept, a few criteria, a short comparison, a multi-step
  procedure, or one capability.
- **Long:** a full guide, troubleshooting, or multi-criteria comparison. If it
  outgrows the format, split it into a series rather than compressing it.

A practical ceiling many Persian tech channels use is roughly **۱۷۰۰ characters
including spaces، ~۴۰۰ کلمه، ~۱۶ پاراگراف** — sized so the post is consumable on
a single phone screen without endless scrolling. Treat it as a default, not a
law; the channel owner's spec wins.

### Common Telegram post types

**آموزشی پرسش‌محور** — title as a question, numbered points, risks marked,
benefits marked, a highlighted final result. A closing «تذکر مهم» block that
names the *plausible but wrong* conclusions a reader might draw and corrects
them is unusually valuable: it is where content earns trust rather than clicks.

**اطلاعیه‌ی قابلیت جدید** — greeting (if the channel uses one) → clear headline
→ short explanation of what it does → benefits or use cases as separate items →
how to use it, in steps → link to official documentation.

**خبر** — headline carrying the actual event → the news and its source, briefly
→ details as separate items → practical implications or steps if any → source
link → the misreading-correction block.

**هشدار** — an imperative headline naming the required action → what happened,
why it matters, and the source → the conditions that make a reader affected →
required actions as ordered steps → source → misreading correction.

For news and warnings especially: keep every fact traceable to the input
sources, and never invent an ID, form, URL, or contact that wasn't given.

### Links

Keep every link from the source; create none. Give each link a clear title and
attach the URL to that title as anchor text rather than pasting a long raw URL
mid-sentence.

## 3. Instagram

Instagram content is not a shortened article. It is built for visual
consumption, and the format is chosen from the content's shape:

| Format | Use it for |
|---|---|
| **کاروسل** | several steps, tips, criteria, a comparison, or a gradual explanation |
| **تک‌تصویر** | one definition, tip, warning, data point, or standalone message |
| **اینفوگرافیک** | a set of data or components and the relationships between them |
| **ریلز** | showing a process, an interface, movement, an example, before/after |
| **استوری** | short, time-bound messages, reminders, links, feedback, quick sequences |

One central topic per piece, one message per slide or frame, one clear
takeaway per reel.

**Hook:** the first slide, frame, or second must state the question, problem,
difference, result, warning, or exact number of points. No vagueness, no fear
bait, no exaggeration, no withheld answer.

**General path:** هوک → زمینه‌ی ضروری → آموزش یا پاسخ → محدودیت یا هشدار →
نتیجه → اقدام مرتبط در صورت نیاز.

### Carousel

کاور → اسلاید زمینه → اسلایدهای میانی → هشدار یا مثال → جمع‌بندی → CTA.

- **Cover:** short direct title, one subject, visible value, understandable
  *without* the caption. No paragraph, no extra promise.
- **Context slide:** the problem, its importance, the misconception, the
  audience, or the prerequisite — in the least space that works. Never a
  restatement of the cover.
- **Middle slides:** one definition, step, tip, criterion, cause, benefit,
  limitation, comparison, example, or warning each. Title states the message;
  body explains it.
- **Never split a sentence across two slides.** Move secondary detail to the
  caption instead.
- Put an important warning on its own slide or next to the action it concerns —
  not hidden in the caption.
- Slide count follows complexity. If the content gets dense or very long, split
  it into more than one post.

### Reels

هوک → مسئله → توضیح یا نمایش → مثال یا راهکار → محدودیت → جمع‌بندی → CTA.

- Open directly with the subject; no greeting or long introduction.
- One idea per sentence, one function per scene.
- On-screen text and narration should complement each other, not duplicate.
- Numbers, commands, option names, paths, warnings and the key result should
  appear **on screen**, not only in audio.
- Show interface steps slowly enough to follow, with the click target visible.
- Assume the sound is off: subtitles matter, and the essential information must
  survive muting.
- End on the result, the decision criterion, or the next action.

### Stories

- **Single frame:** one message — عنوان/پیام → توضیح کوتاه → اقدام یا لینک.
  Understandable at a glance; not several paragraphs.
- **Sequence:** frame 1 the subject or question, frame 2 the context, middle
  frames one point each, a limitation frame if needed, a final frame with the
  result or action. Don't split sentences across frames or pad the count.
- **Interactive stickers** are for gauging knowledge, identifying needs,
  quizzes, collecting questions, or choosing a topic — single-subject question,
  real options, and explain the correct answer afterwards. Never request
  sensitive data.
- **Before a link**, say where it goes and why it is relevant; send people to
  the most specific page.

### Captions and hashtags

The caption complements the visual, it doesn't repeat it:
جمله‌ی آغازین مشخص → زمینه → توضیح تکمیلی یا مراحل یا مثال → محدودیت →
جمع‌بندی → CTA و منبع در صورت نیاز.

Short paragraphs, one idea each. Don't put essential information only in the
caption. Avoid generic openings and endings that carry no information.
Hashtags: few, relevant, used for categorisation — not generic, repetitive, or
promotional. Brand hashtags follow the brand's own fixed policy, if it has one.

### Text on images and accessibility

- Images, charts and screenshots must aid understanding, not decorate.
- Text inside an image: short, hierarchical, large enough, high contrast, away
  from the edges. Break lines by meaning, not to fill space.
- Few fonts, few emphasis styles (fonts.md; and never letter-space Persian).
- Provide subtitles for speech, alt text for images where the platform allows,
  and explain charts in the caption.
- Don't encode meaning in colour alone; avoid fast or flashing motion.

## 4. Announcements and product introductions

**Announcement (change, incident, event):** موضوع → زمان → دامنه‌ی اثر →
وضعیت فعلی → اقدام انجام‌شده → اقدام لازم مخاطب → مسیر به‌روزرسانی.
State incomplete information as incomplete, and announce a definite resolution
time only when it is actually confirmed. Under-promising here is credibility;
over-promising is a support ticket.

**Product or capability introduction:** نیاز → راهکار → کاربرد → مخاطب مناسب →
قابلیت مرتبط → محدودیت و پیش‌نیاز → تفاوت با نزدیک‌ترین گزینه → مسیر جزئیات.
Verify price, capacity and any changeable condition before publishing, and
don't let a purchase invitation replace the explanation of *who this is
actually for*.

## 5. Repurposing between formats

Rewriting for the destination format, not copying into it:

- **Telegram → carousel:** extract the core message, move secondary detail to
  the caption, turn each section into an independent slide.
- **Article → reel:** keep one sub-topic, one definition, one example, one
  result — and rewrite the text for speech, which is a different rhythm than
  prose.
- **Carousel → story:** reduce the text and the number of messages. Never post
  screenshots of the slides as stories.
- **Article → Telegram:** keep the answer and the decision criteria; drop the
  background the format has no room for, rather than compressing everything
  uniformly into an unreadable block.

In a series, keep the overall topic, the part number, and each part's own
title — and make every part understandable without having seen the previous
ones.

## 6. Pre-publish checks

**Telegram:** one central topic; accurate title; opening free of filler;
logical structure; short paragraphs; clear steps; complete but not padded;
claims current; limitations and sources present; problem-centred tone;
result-oriented conclusion; no internal labels left in the text.

**Instagram:** format matches the content and audience; subject clear
immediately; hook precise and not misleading; one message per slide or frame in
a logical order; on-image text short, legible, phone-appropriate; caption,
narration and visual complementary with nothing essential dropped; claims,
volatile facts, sources, limitations and warnings correct; content
problem-centred rather than promotional; subtitles, contrast, element placement
and chart explanations handled; the deliverable separated from internal notes.

**Both:** run the text through `scripts/persian_cleanup.py --edit` and
`scripts/fa_lint.py --check` before delivery — هکسره errors and broken
نیم‌فاصله are the fastest way for a professional channel to look amateur
(orthography.md §5.1).
