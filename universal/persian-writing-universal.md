# Persian Writing — universal single-file edition
# نگارش فارسی حرفه‌ای برای هر هوش مصنوعی

This is the complete persian-writing skill compiled into one file, for AI
systems without file access. Give it to the AI as a system prompt, project
knowledge, or an attached document, with an instruction like:

> Follow the persian-writing guide for every task that involves Persian
> (Farsi) text or documents.

Two adaptations for this edition:

1. **Scripts become checklists.** The full package ships Python scripts
   (`persian_cleanup.py`, `fa_lint.py`, `verify_pdf.py`). Where the text says
   to run them, an AI without code execution applies the same rules manually —
   they are all stated in prose in the Orthography and Writing-style parts.
   An AI WITH code execution should get the full package instead.
2. **Fonts can't be bundled in a text file.** Get Vazirmatn and Lalezar from
   Google Fonts or github.com/rastikerdar/vazirmatn; everything here refers
   to them by name.

The single most important rule, before any writing: detect the register
(رسمی / اداری / محاوره / علمی) using the procedure in Part 1 — classify the
DELIVERABLE, not the tone of the request, and when the text goes to a third
party and signals conflict, ask one short question instead of guessing.

---

# PART 0 — Core rules and routing

# Persian Writing & RTL Documents

Two failure modes make Persian output look machine-made, and they are independent:

1. **The prose sounds like AI.** Technically correct, but stiff, کتابی, inflated —
   no Iranian would write it that way.
2. **The layout betrays the text.** Persian rendered left-aligned, Arabic ي/ك glyphs,
   Latin digits breaking RTL flow, headings orphaned at page bottoms, fonts falling
   back to DejaVu.

Fixing one without the other still produces something a native reader screenshots
and laughs at. This skill fixes both. Work through the two checklists below, and
read the reference file for your output format before generating anything.

## Step 0: Route by task

| Task | Read |
|---|---|
| Any Persian prose (always) | the «Writing style: registers & de-AI-ing» part below |
| Mechanical correctness (always) | the «Orthography (نگارش و رسم‌الخط)» part below |
| Academic: paper, thesis, report, مقاله/پایان‌نامه | the «Academic writing (نگارش علمی)» part below |
| Educational/technical content, docs, product pages, how-to | the «Content craft: POV, structure, honesty» part below |
| Telegram, Instagram, captions, carousels, reels, stories | the «Social channels: Telegram & Instagram» part below |
| SEO content, blog for search, landing/ad copy, کپشن فروش | the «SEO writing & copywriting» part below |
| Cleanup/normalize/spell-check existing text (ویرایش، پاکسازی) | the Orthography part (script docs ship with the full package) |
| Choosing/embedding fonts | the «Fonts» part below |
| Word/.docx or docx→PDF | the «Word/DOCX + PDF» part below |
| PowerPoint/.pptx | the «PowerPoint» part below |
| HTML, email templates, HTML→PDF | the «HTML / CSS / email» part below |
| Images/posters (PIL), new PDFs (reportlab), Excel | the «Images, reportlab PDFs, Excel» part below |

**Visual neutrality — read before copying any code example.** This skill styles
NOTHING. It governs direction, spacing, fonts-for-shaping and text — never
colors, accent bars, card backgrounds, or a house look. Every hex, border, and
fill in the code examples is a stand-in written in plain grey/black; they exist
to show WHERE a property goes, not what value to use. Default output is black
text on default background, no accent color. Take colors and visual form ONLY
from: the user's explicit request, an attached brand/theme skill, or an input
template being matched. Absent those, do not invent a palette and do not carry
one over from example to example — unstyled is the correct default, and a
surprise purple heading is a bug.

This skill composes with the general docx/pptx/pdf skills: those handle file
mechanics; this one overrides and extends them for Persian. When both disagree
about RTL behavior, this skill wins — its rules come from debugging real Persian
documents. If another active skill or the user specifies particular fonts or
colors, those win on aesthetics; this skill still governs RTL mechanics and
orthography. This skill itself is brand-neutral: colors in the code examples are
placeholders, and Vazirmatn is just the default font, not a requirement.

## Writing: the five-second summary

Full guide in the «Writing style: registers & de-AI-ing» part below. The core moves:

1. **Detect register before writing a word — a register error is the costliest
   mistake this skill can make.** Follow the 6-step detection procedure in
   writing-style.md Part 1. The core rules: classify the DELIVERABLE, not the
   tone the user typed in (a casual «یه پروپوزال بنویس» still needs a formal
   proposal); when the text goes to a third party and signals conflict, ask
   ONE short question instead of guessing; no signal at all → formal-but-human.
   - Proposal, invoice, report, official email, website copy → **formal-but-human**:
     full written forms (می‌شود نه میشه), شما, zero slang — but است نه می‌باشد,
     short sentences, concrete claims. Human ≠ خودمونی: proposals/contracts keep
     formal vocabulary (no «جور است»-style idioms); warmth comes from clarity,
     numbers, and one warm closing line (writing-style.md, "warmth trap").
   - نامه اداری → formal + letter conventions (honorifics, «با سلام و احترام؛»
     — writing-style.md).
   - Instagram/Telegram, chat, friendly email → **colloquial written Persian**
     (محاوره‌نویسی): میشه، می‌خوام، رو، particles like دیگه/که/مگه.
   - Blog, newsletter → between: written forms, warm direct voice.
   - Paper, thesis, university report → **academic** (نگارش علمی): measured,
     hedged, passive acceptable, zero تعارف — read the «Academic writing (نگارش علمی)» part below.
   - SEO/sales copy → register per artifact as above, plus the «SEO writing & copywriting» part below.
2. **Ban the bureaucratic tells:** می‌باشد، لازم به ذکر است، در راستای،
   از اهمیت ویژه‌ای برخوردار است، نقش بسزایی ایفا می‌کند.
3. **Ban the AI tells:** em dashes (—), rule-of-three triads (سریع، آسان و مطمئن),
   نه تنها ... بلکه, tacked-on «که نشان‌دهنده‌ی ... است», vague «کارشناسان معتقدند»,
   generic «در دنیای امروز» openers, «در نهایت می‌توان گفت» closers.
4. **Hold one point of view.** Explain facts impersonally, address the reader
   directly (the verb carries it — don't repeat «شما»), and use «ما» only for
   what the organization actually did or is responsible for. Sliding between
   the three inside one section is the most common flaw in Persian brand
   content — content-structures.md §1.
5. **Separate teaching from selling.** The explanation must be worth reading
   without buying anything: state the problem before the product, never hide
   the main answer, tie each feature to a checkable result, and never delete
   limitations or prerequisites — they are what make the rest believable.
6. **Claim only what the source supports.** Distinguish واقعیت / نظر /
   پیش‌بینی / ادعا; never invent a statistic, version, price, or quote to fill
   a section; surface contradictions instead of silently resolving them; ask
   one question rather than guessing (content-structures.md §3).
7. **The native test:** would an Iranian screenshot this as «متن هوش مصنوعی»?
   If yes, rewrite before delivering. Two properties cause most of it:
   *predictability* (the expected collocation every time — اهمیتِ ویژه، نقشِ
   بسزا) and *uniformity* (every sentence 15–20 words, every paragraph the same
   weight). Real specifics create real variation; `fa_lint.py --check --rhythm`
   flags flat rhythm, but lexical tells matter far more — writing-style.md §3.5.
   The goal is prose that is genuinely better, not prose tuned to a detector:
   AI detectors are unreliable and falsely flag second-language writers at very
   high rates, and this skill never helps disguise authorship (§3.6).
8. **Numbers, punctuation, spacing** must be Persian — next section.

## Orthography: non-negotiables

Full rules in the «Orthography (نگارش و رسم‌الخط)» part below. These six apply to every deliverable:

1. **ZWNJ (نیم‌فاصله, U+200C)** — می‌شود نه می شود؛ کتاب‌ها نه کتاب ها؛
   بزرگ‌تر، خانه‌ام، به‌عنوان. In code: `‌` or HTML `&zwnj;`.
2. **Persian characters only:** ی (U+06CC) not ي، ک (U+06A9) not ك.
3. **Persian digits** ۰۱۲۳۴۵۶۷۸۹ inside Persian text. Latin digits stay in URLs,
   emails, codes, version numbers. Never Arabic-Indic ٤٥٦ forms.
4. **Persian punctuation:** ، ؛ ؟ and «گیومه» for quotes. No space before, one after.
4b. **هکسره** — never write the ezafe kasre as «ـه»: «کتابِ من»، not «کتابه من».
   The «ـه» ending is only the colloquial «است» («این کتابه» = این کتاب است).
   Test by substituting «است»; if the sentence breaks, you need a kasre.
   Iranians treat this error as a mark of carelessness — orthography.md §5.1.
5. **No em/en dashes** in Persian prose — use «،» or restructure.
6. **Never letter-space Persian** (it breaks letter joining), never fake bold/italic.

Two scripts enforce this mechanically — use both before delivering Persian text:

```bash
# 1. FIX: paknevis-style editorial pass (ZWNJ, chars, digits, punctuation, گیومه)
python3 the persian_cleanup script (full package; chat-only AIs apply the equivalent rules manually) --edit --in text.md --out text.md
# 2. LINT: report what still needs contextual judgment (dashes, میشود forms,
#    fake tanvin, register issues) — fix these by hand
python3 the fa_lint script (full package; chat-only AIs apply the equivalent rules manually) --check text.md
```

`--edit` is safe on structured files. Fenced code blocks, inline code and table
rows are lifted out before processing and restored byte-identical, and leading
indentation is never collapsed. This matters because Persian typography rules
are correct for prose and destructive in code: they would turn `"text"` into
`«text»`, rewrite ASCII digits as Persian, and flatten the spacing a table's
columns rely on. Pass `protect_code=False` (Python API) only if you truly want
those rules applied everywhere. Keep the file in version control either way —
the tool is careful, not omniscient.

`persian_cleanup.py` is a full toolkit (paknevis + davat merged): aggressive
cleaning for NLP (`--preset persian`), single functions (`--fn convert_digits`),
spell-check against the bundled 453K-word frequency dictionary
(`--edit --spellcheck`), custom pipelines. Persian «ویرایش» requests → `--edit`
(conservative, content preserved); «پاکسازی/نرمالایز» → `--preset persian`
(strips links/mentions/emojis). Details: `references/cleanup/`. Note: `--edit`
applies the خانهٔ ezafe style; drop `fix_ezafe` from `--steps` to keep خانه‌ی.

## Fonts

Bundled in `assets/fonts/` (SIL OFL — free for commercial use):

- **Vazirmatn** — the default for everything: body, UI, documents. 9 weights.
- **Lalezar** — display font for headlines, covers, posters. One weight; never body.

Other families (Shabnam, Sahel, Samim, Parastoo, Tanha, Gandom) and pairing advice:
the «Fonts» part below. In offline sandboxes only bundled fonts exist —
the download_fonts script (full package; chat-only AIs apply the equivalent rules manually) works only where GitHub is reachable.

**Before any docx→PDF or pptx→PDF conversion, install the fonts:**

```bash
bash the install_fonts script (full package; chat-only AIs apply the equivalent rules manually)   # copies assets/fonts → ~/.fonts, runs fc-cache
fc-list | grep -i vazir         # verify — else LibreOffice silently falls back
```

Skipping this is the #1 cause of broken Persian PDFs: conversion "succeeds" but
every glyph is DejaVu tofu or disconnected letters.

## Documents: the rules that always apply

Format-specific recipes live in the reference files. The universal ones:

1. **RTL means START, not RIGHT.** In OOXML, with `bidirectional: true`,
   `AlignmentType.RIGHT` renders at the *visual left*. Always align `START`.
2. Every Persian run: `rightToLeft: true` + font with `hint: "cs"` (Complex Script).
3. Every section: `bidi: true`. Tables that must flow right-to-left:
   `visuallyRightToLeft: true`.
4. **Persian digits in numbered content** — a Latin "1." flips the paragraph LTR.
   Corollary for docx: never use the built-in `List Number`/`List Bullet` styles.
   Their markers live in `numbering.xml`, which has no bidi and renders Latin
   `1.` on the wrong side plus an OpenSymbol bullet that breaks font embedding.
   Write markers as ordinary runs («۱.  », «•  ») — docx-pdf.md §6.1.
5. **Fix the document defaults before adding content.** python-docx starts from
   a Latin template: `styles.xml` has no Persian font and Word's Heading styles
   carry a blue color you never asked for. Run `persianize_styles(doc)` from
   docx-pdf.md §6.1 immediately after `Document()`. Headers/footers are separate
   XML parts and need the RTL treatment applied to them directly.
6. **Pagination:** headings get `keepNext + keepLines` (no orphan headings);
   cards/boxes go inside a single-cell table with `cantSplit: true` (never split
   across pages); no separator after the last list item; no stray `PageBreak`
   before a section break (blank pages).
7. **Symbols:** Persian fonts miss many glyphs. In bundled Vazirmatn/Lalezar
   only • and · are verified; ▪ ■ ✓ ✕ ● ◆ ⊙ fall back to DejaVu. For any other
   symbol/font, check the cmap first (fonts.md shows how).

## Verify before delivering

Two gates. Check the .docx BEFORE converting (catches what code review can't),
then check the PDF:

```bash
# 1. DOCX: package integrity FIRST (a file Word won't open can't be RTL-checked),
#    then section bidi, jc=right traps, cs fonts, list numbering, heading colors.
#    --fix repairs missing <w:bidi/>; --sanitize strips the Word-for-Mac template
#    artifacts python-docx inherits (the classic "file is corrupt" fingerprint).
python3 scripts/verify_docx.py output.docx --expect-font Vazirmatn --fix --sanitize

# 2. PDF: fallback fonts, blank pages, template leaks, Arabic chars
python3 the verify_pdf script (full package; chat-only AIs apply the equivalent rules manually) output.pdf --expect-font Vazirmatn
```

`verify_docx.py` exists because setting an RTL flag and that flag reaching the
XML are different things: libraries drop `bidi` from section properties, and
OOXML requires `<w:bidi/>` to be the FIRST child of `<w:sectPr>` — appended
anywhere else, renderers ignore it. Verify the artifact, never the source code.

It also guards the package itself: `[Content_Types].xml` must be the first ZIP
entry, every relationship Target must resolve, every XML part must be
well-formed and free of control characters. Repairs are written to a temp file
and validated before replacing anything, so a failed repair can't destroy the
document. Details and the already-corrupt-file procedure: docx-pdf.md §4.5.

It checks: near-empty pages, "undefined"/template leaks, non-embedded or fallback
fonts, Arabic ي/ك in extracted text, and page count. Fix every warning, regenerate,
re-verify. For prose, re-read your final text against the native test — one pass of
`persian_cleanup.py --edit` + `fa_lint.py --check` plus one honest read-aloud
catches most disasters.



---

# PART 1 — Writing style: registers & de-AI-ing

# Persian writing style: registers and de-AI-ing

AI Persian fails in a specific way: it is *too correct*. Too formal, too کتابی,
inflated with ceremony that no working Iranian writer uses. The fix is not
"be casual everywhere" — a slangy proposal is as wrong as a bureaucratic
Instagram caption. The fix is: pick the right register, then strip the tells.

## Part 1: Register detection

A register error is the most expensive mistake this skill can make: a خودمونی
proposal loses the client; a stiff Instagram caption loses the audience; a
casual نامه اداری can embarrass the sender in front of an organization. Decide
the register BEFORE writing, using the procedure below — never by feel.

| Context | Register | Markers |
|---|---|---|
| Proposal, invoice, contract, report, official/B2B email, website copy | **Formal-but-human** | Full written forms، شما، no slang — but direct and alive |
| نامه اداری / letter to an organization or authority | **Formal-اداری** | Formal + letter conventions (honorifics, opener/closer — see below) |
| Blog post, newsletter, product update, LinkedIn | **Semi-formal** | Written forms + warm voice، direct address، occasional colloquial word |
| Instagram, Telegram, chat replies, friendly email, story captions | **Colloquial written** (محاوره‌نویسی) | میشه، می‌خوام، رو، particles، fillers |
| Paper, thesis, university report, مقاله/پایان‌نامه | **Academic** (نگارش علمی) | Measured, hedged, passive OK, zero تعارف — full guide: the «Academic writing (نگارش علمی)» part |

### The detection procedure (apply in this order)

1. **Explicit instruction wins.** «رسمی بنویس»، «خودمونی باشه»، «لحن اداری» —
   obey it, whatever the document type.
2. **Deliverable type, not request tone.** Users type casually: «یه پروپوزال
   واسه مشتری بنویس» is a casual REQUEST for a formal DELIVERABLE. Classify
   the artifact, ignore the register the user typed in. This is the single
   most common detection mistake.
3. **Audience + destination.** Going to a client, organization, professor,
   or government office → formal side, even if the channel is a DM. Going to
   followers, friends, one's own team chat → casual side.
4. **One register per artifact, not per conversation.** A formal cover letter
   with casual Instagram captions attached = two artifacts, two registers.
5. **High stakes + ambiguity → ask.** If the text goes to a third party and
   signals conflict, ask ONE short question («لحن رسمی باشد یا صمیمی؟») —
   a question costs three seconds; a wrong register can cost the deal.
6. **No signal at all → formal-but-human.** It's the safe default in Persian
   professional contexts; casual by mistake is worse than formal by mistake.

Cues that flip toward casual: کپشن، استوری، پست اینستا، توییت، پیام دوستانه،
گروه دوستان، فان. Cues that flip toward formal: مشتری، سازمان، اداره، مدیر،
قرارداد، رسمی، مناقصه، دانشگاه، استاد، مقام.

### نامه اداری conventions (Formal-اداری)

Persian administrative letters have fixed furniture — using it correctly IS
the register:

- **Structure:** موضوع (one line) ← گیرنده با سمت ← «با سلام و احترام؛» ←
  body (short, one request per letter) ← closing formula ← نام، سمت، تاریخ.
- **Honorifics:** جناب آقای / سرکار خانم + [دکتر/مهندس] + surname;
  «مدیریت محترم ...»، «ریاست محترم ...». Never تو، never first names.
- **Openers:** «با سلام و احترام؛» or «احتراماً، به استحضار می‌رساند...» —
  one احتراماً maximum; stacking ceremony reads as parody.
- **Closers:** «با تشکر و احترام»، «پیشاپیش از همکاری شما سپاسگزارم».
- Body verbs stay است/می‌شود (NOT می‌باشد — even اداری doesn't excuse it;
  it only feels mandatory because bad letters normalized it).
- Requests: «خواهشمند است دستور فرمایید...» is the standard polite-request
  formula and is correct here, though it would be fossil anywhere else.

### Formal-but-human (the register AI gets most wrong)

Formal Persian does NOT mean bureaucratic Persian. The models default to اداری
ceremony; real professional writing is closer to a smart person talking carefully:

- **است، شد، کرد** — never می‌باشد، گردید، به عمل آورد. The می‌باشد register is
  a government-office fossil; in a proposal it reads as either lazy or machine.
- Short sentences. One idea per sentence. Persian tolerates long chains of
  که-clauses; readers don't.
- Address the reader: «شما» and second-person verbs, not «کاربران محترم می‌توانند».
- Concrete over ceremonial: «سایت شما در ۳ ثانیه باز می‌شود» beats
  «بهبود چشمگیر سرعت بارگذاری را تجربه خواهید کرد».
- Warmth is allowed. تعارف is allowed in openings/closings of letters
  (یک سطر، نه یک بند). Flattery-padding is not.

**The warmth trap — «انسانی» یعنی روان، نه خودمونی.** Over-correcting away from
کتابی lands in colloquial idiom, which in a proposal or contract reads as
unprofessional to exactly the client you're trying to win. In proposals,
contracts, invoices, official letters and reports, these do NOT belong:

- Colloquial idioms: «جور بودن» (→ مناسب بودن/هم‌راستا بودن)، «ردیفه/حله»،
  «رهایتان نمی‌کنیم» (→ همراهتان می‌مانیم)، «نه آخر کار» (→ و به پایان پروژه
  موکول نمی‌شود)، «پیش خودتان می‌ماند» (→ در اختیار خودتان باقی می‌ماند)
- Spoken sentence shapes: «همین هفته یک جلسه بگذاریم» → «پیشنهاد می‌کنیم همین
  هفته جلسه‌ای کوتاه برگزار شود» — the suggestion stays, the register rises.
- Where warmth in a formal document actually comes from: short clear sentences،
  concrete numbers، direct «شما»، and ONE warm line in the closing. Not chatty
  idioms scattered through the body.

Formality slider inside this register (most → least formal): contract/invoice →
proposal/official letter → report → website copy. Website copy may borrow a
warm idiom; a proposal should not. When unsure, write the sentence formally
first and only relax it if the document type allows.

### Colloquial written Persian (محاوره‌نویسی)

For social/chat contexts, written Persian mirrors speech:

- **Verb forms:** است → ـه (خوبه)، می‌خواهم → می‌خوام، می‌روم → میرم،
  می‌شود → میشه، بگذار → بذار
- **را → رو** (after the object): «اون فایل رو فرستادم»
- **آن/این → اون/این**، آن‌ها → اونا
- **Particles that carry the music:** دیگه (already/come on)، که (emphasis:
  «گفتم که»)، ها (attention: «بیا ها»)، مگه (surprise: «مگه میشه؟»)، خب، اصلاً
- **Fillers where a person would breathe:** راستش، یعنی، حالا، بعدش، چیز
- **Reactions:** جدی؟ واقعاً؟ وای! عجب! دمت گرم! آفرین! خخخ/هاهاها in chat
- **Expressive vocabulary, not safe vocabulary:** خوب → عالی، خفن، توپ؛
  بد → افتضاح، گند زد؛ خیلی → کلی، یه عالمه
- **تو vs شما:** تو for friends/peers/followers spoken to as one person;
  شما for strangers, elders, customers, and often mixed politeness online
  (شما + colloquial verbs: «شما بگید» is normal and warm). Overusing تو with
  strangers is rude; overusing formal شما forms with friends is cold.
- **تعارف:** exists even casually («قابلی نداره»، «مخلصیم») but one beat of it.
  Don't stack three politeness rituals in a DM.
- **هکسره — the error that undoes everything else.** Colloquial writing is
  exactly where the «ـه» clitic (= است) lives, so it is also where writers
  collide it with the ezafe kasre. «این کتابه» (this is a book) is right;
  «کتابه من» is wrong and should be «کتابِ من». One هکسره in an Instagram
  caption gets quoted back at the brand; it reads as carelessness, not casualness.
  Test each one by swapping in «است»: if the sentence survives, «ـه» is correct.
  Full rules and the wrong/right table: orthography.md §5.1.

Consistency rule: don't mix میشه and می‌شود in the same piece. Pick the register
and hold it. (Exception: quoting someone's speech inside formal text.)

Brand-fact rule (all registers, especially marketing copy): use only facts the
user or their brief actually provides. Never invent stats, years of experience,
client counts, partner names, or hashtags — an invented «۹۷٪ رضایت» or a brand
hashtag the user never asked for damages trust more than a plain sentence. No
facts available? Write generic-but-concrete claims and tell the user which
blanks to fill. The full discipline — separating واقعیت from نظر, پیش‌بینی and
ادعا, and what to do with contradictory sources — is in content-structures.md §3.

Point of view is a separate axis from register, and an easy one to get wrong:
impersonal for facts and mechanisms, second person for what the reader does
(the verb alone — repeating «شما» reads as translated English), «ما» only for
the organization's own actions and responsibilities. See content-structures.md
§1 for the full table; social-channels.md covers what changes per channel.

## Part 2: Persian AI tells — find and rewrite

These are the patterns that make Iranian readers say «اینو ربات نوشته». Scan for
every one; rewrite, don't delete — keep the meaning, lose the tell. Watch for
**clusters**: one «همچنین» is fine; همچنین + می‌باشد + «در دنیای امروز» is a confession.

### T1. می‌باشد disease (copula inflation)
The single loudest tell. Also: به شمار می‌رود، محسوب می‌شود، به حساب می‌آید،
قرار دارد (for است), گردیده است.

> ❌ وردپرس یکی از محبوب‌ترین سیستم‌های مدیریت محتوا می‌باشد و ابزاری قدرتمند محسوب می‌شود.
> ✅ وردپرس محبوب‌ترین سیستم مدیریت محتواست — قدرتش هم دقیقاً از همین‌جا می‌آید.

### T2. Ceremonial filler announcements
لازم به ذکر است که، شایان ذکر است، قابل توجه است که، همان‌طور که می‌دانید،
باید خاطرنشان کرد. Cut the announcement; say the thing.

> ❌ لازم به ذکر است که پشتیبانی به صورت ۲۴ ساعته ارائه می‌گردد.
> ✅ پشتیبانی ۲۴ ساعته است.

### T3. Significance inflation
نقش بسزایی ایفا می‌کند، از اهمیت ویژه‌ای برخوردار است، گامی مهم در راستای،
جایگاه ویژه‌ای دارد، تحولی شگرف. Replace with the concrete claim.

> ❌ سئو نقش بسزایی در موفقیت کسب‌وکار شما ایفا می‌کند.
> ✅ اگر در نتایج گوگل دیده نشوید، مشتری هم ندارید — سئو یعنی همین.

### T4. Generic openers and closers
Openers: در دنیای امروز، در عصر دیجیتال، امروزه با پیشرفت تکنولوژی، با گسترش
روزافزون اینترنت. Closers: در نهایت می‌توان گفت، به طور کلی، آینده‌ای روشن در
انتظار. Start with the actual point; end with a concrete fact or next step.

### T5. «در راستای» abuse
در راستای، در همین راستا، در جهت نیل به → usually just «برای».

### T6. Promotional emptiness
بی‌نظیر، فوق‌العاده، مثال‌زدنی، برترین، منحصربه‌فرد، تجربه‌ای متفاوت،
با کیفیتی بی‌رقیب. Specifics or silence.

> ❌ تیم ما با تجربه‌ای بی‌نظیر، خدماتی منحصربه‌فرد ارائه می‌دهد.
> ✅ در پنج سال گذشته ۴۰ پروژه تحویل داده‌ایم؛ سه‌تایشان الان روزی
> هزار سفارش دارند.

### T7. Rule of three
سریع، آسان و مطمئن؛ طراحی، توسعه و پشتیبانی — the triad rhythm is an AI
fingerprint in Persian exactly as in English. Two items, or four, or one
developed idea.

### T8. نه تنها ... بلکه (negative parallelism)
Overused. Also the clipped tail: «بدون هیچ دردسری»، «بدون نگرانی» stapled to
sentence ends. State the positive claim plainly.

### T9. Tacked-on analysis clauses (the -ing disease in Persian)
که نشان‌دهنده‌ی ... است، که بیانگر ... می‌باشد، که حاکی از ... است،
که گواهی است بر — fake depth suffixes. If the analysis matters, give it its
own sentence with evidence; usually, delete.

### T10. Vague authority
کارشناسان معتقدند، مطالعات نشان می‌دهد، تحقیقات ثابت کرده — with no named
source. Name it (طبق گزارش ۲۰۲۴ Semrush...) or drop the appeal.

### T11. False ranges
«از طراحی سایت گرفته تا سئو و تولید محتوا» when the items aren't on any scale —
just list the services.

### T12. Em dashes and English punctuation rhythm
Persian prose traditionally has no em dash; ChatGPT-style «متن — توضیح — ادامه»
is a hard tell. Use «،»، «؛»، parentheses، or a new sentence. (This file uses
one for contrast; your deliverables get zero.)

### T13. Calque phrases (translationese)
در پایان روز (at the end of the day) → آخرش، در نهایت؛
نگاهی بیندازیم به (let's take a look) → ببینیم؛
شایسته است بدانید → cut. If a phrase only exists as an English idiom's shadow,
an Iranian didn't write it.

### T14. همچنین pileup
همچنین، علاوه بر این، افزون بر آن opening consecutive sentences. Persian
connects naturally with و، هم، تازه (casual), or nothing.

### T15. Fake tanvin words
گاهاً، دوماً، ناچاراً — tanvin on Persian words is wrong (tanvin is Arabic
morphology). Use گاهی، دوم اینکه، به‌ناچار. (Real Arabic loans keep it:
واقعاً، حتماً، اصلاً، لطفاً.)

### T16. Bold-header bullet lists
The «**سرعت بالا:** توضیح» list format is ChatGPT furniture. In prose
deliverables, write paragraphs. Bullets only when the content is truly a list —
and then plain bullets, no bold-colon headers.

### T17. Sycophantic chat residue
سؤال بسیار خوبی است!، البته!، خوشحال می‌شوم کمک کنم، امیدوارم مفید بوده باشد —
chatbot correspondence pasted into content. Delete on sight.

### T18. Universal tells (from the English humanizer — they transfer)
Elegant variation (وب‌سایت/سایت/پلتفرم/پورتال cycling for one thing);
passive hiding the actor (تصمیم گرفته شد — by whom?); excessive hedging
(شاید بتوان گفت که احتمالاً); staccato manufactured drama; aphorism formulas
(«سئو زبانِ اعتماد است»); emojis decorating headings; Title Case in Latin
brand names mid-Persian is fine, but no ALL-CAPS shouting.

## Part 3: What NOT to flag

- **Correct formal Persian is not a tell.** A contract in proper formal register
  is supposed to be formal — just not می‌باشد-formal.
- **تعارف is human.** One line of «با احترام» or «قربان شما» in a letter is
  culture, not AI. Only flag stacked, empty ceremony.
- **Poetry and literary prose** play by their own rules — سعدی gets to use
  constructions a proposal can't. Don't "humanize" quoted poetry, آیات, titles,
  or proper names. Never edit inside quotations.
- **Loanwords are normal.** Iranians say آپدیت، پیج، استوری، دیجیتال مارکتینگ.
  Forcing pure-Persian coinages (تارنما for سایت) sounds weirder than the loan.
- **One همچنین, one خیلی, one exclamation** — isolated instances mean nothing.
  Look for clusters.

## Part 3.5: Why machine prose reads flat — the underlying mechanism

T1–T18 are symptoms. Two properties of how language models generate text
explain most of them, and knowing the cause lets you fix cases the list doesn't
name.

**Predictability (perplexity).** A model picks, at each step, a highly probable
next word. Do that thousands of times and every phrase becomes the expected
one. In Persian this surfaces as the safe collocation every single time:
«اهمیت» always arriving with «ویژه‌ای»، «نقش» with «بسزایی»، «تیم» with
«مجرب». Nothing is wrong with any one of them; the tell is that no phrase ever
surprises. A human writer, even a careful one, occasionally reaches for the
less obvious word — and that irregularity is what reads as a person thinking.

**Uniformity (burstiness).** Human writing varies: a 6-word sentence next to a
30-word one, a two-line paragraph after a dense one, a section that runs long
because the idea deserved it. Generated text clusters in a narrow band —
sentences mostly 15–20 words, paragraphs of equal weight, sections of equal
length, every list with the same number of items. The prose has no dynamics.

Measured on the samples shipped with this skill: an AI-written services page
scored 0.39 sentence-length variation with paragraphs all within 0.19 of each
other, while its rewrite reached 0.65 with sentences from 2 to 27 words. Check
your own draft with:

```bash
python3 the fa_lint script (full package; chat-only AIs apply the equivalent rules manually) --check --rhythm text.md
```

Read the output as an editor's nudge, not a verdict. Rhythm is a **secondary**
signal: in that same comparison, the count of lexical tells went from 11 to 0,
which is the change a reader actually feels. A text with perfect variance and
«می‌باشد» in every paragraph still reads as machine-written. Fix T1–T18 first;
use rhythm to catch what's left.

**What actually creates variation** is having something specific to say. Uneven
sentences are a *consequence* of real content — a precise number, a caveat, an
aside, a change of mind mid-paragraph. Padding a draft with artificially short
sentences produces staccato drama (T18), not humanity. Write the specifics and
the rhythm follows.

## Part 3.6: About AI detectors — what to tell a client, and what not to chase

Persian writers, and Iranians writing in English, get caught by these tools
disproportionately, so the facts matter:

- A 2023 evaluation of 14 detection tools found **all scored under 80% accuracy,
  and only 5 above 70%**; accuracy degrades further on paraphrased text.
- **Non-native English writers are falsely flagged at an average rate of 61.3%**
  in one study of seven detectors — a system that flags most second-language
  writing as machine-written is not measuring what it claims to.
- Reported false-positive rates run as high as 50% in journalistic testing, and
  differ by writer demographic (20% for Black students vs 7% for white students
  in one 2024 report).
- Cambridge and other Russell Group universities, and UT Austin, withdrew from
  Turnitin's AI detection over reliability concerns. Published authors have had
  their own books flagged.

Three practical consequences:

1. **Never treat a detector score as evidence** — of your text or anyone's.
   It is a probabilistic guess about style, not a finding about authorship.
2. **Don't rewrite good Persian to please a tool.** Chasing a score pushes
   writers toward deliberately clumsy prose, which is worse for the reader —
   the only audience that matters.
3. **If a client or institution raises a false flag**, the evidence above is the
   answer: point to the measured false-positive rates for second-language
   writers and to the institutions that abandoned these tools.

**The boundary this skill holds.** Everything here is aimed at prose that is
genuinely better — specific, varied, honest, in the right register. That is
also, incidentally, prose that reads as human, because it is written like one.
What this skill will not do is help misrepresent authorship: no invisible
characters, no homoglyph substitution, no watermark stripping, no injected
typos. Those tricks damage the text, help no reader, and in a context where
disclosure is required — a thesis, a journal submission, a client contract, an
employer's AI policy — the honest move is to follow that policy and say what
was AI-assisted. Improving writing and hiding its origin are different jobs;
this skill does the first.

## Part 4: Signs of human Persian (preserve these)

Specific numbers and names (پنج‌شنبه ساعت ۴، پروژه‌ی آقای کریمی). Mixed feelings
(«راستش هنوز مطمئن نیستم»). Asides in parentheses. Uneven sentence lengths.
A joke that only lands in Persian. Era-bound slang. If a draft has these,
protect them through the rewrite.

## Part 5: Process

1. Identify register from context (Part 1). Academic → also read the «Academic writing (نگارش علمی)» part.
2. Draft.
3. Audit against T1–T18 and orthography (the «Orthography (نگارش و رسم‌الخط)» part; fix with
   the persian_cleanup script (full package; chat-only AIs apply the equivalent rules manually) --edit`, then lint with the fa_lint script (full package; chat-only AIs apply the equivalent rules manually) --check`).
4. Ask: «اگه یه ایرانی اینو ببینه، اسکرین‌شات می‌گیره بنویسه "متن هوش مصنوعی"؟»
   Name the remaining tells honestly.
5. Rewrite into the final. Deliver only the final unless asked for the audit.

### Worked example (formal-but-human — **website copy**, the loosest end of
this register; a proposal would keep the same directness but formal vocabulary
throughout — see the warmth-trap list above)

**Before (AI):**
> در دنیای امروز، داشتن وب‌سایت از اهمیت ویژه‌ای برخوردار می‌باشد. وب‌سایت نه
> تنها ویترین کسب‌وکار شما محسوب می‌شود، بلکه نقش بسزایی در جذب مشتریان جدید
> ایفا می‌کند. لازم به ذکر است که تیم ما با تجربه‌ای بی‌نظیر، خدماتی سریع،
> باکیفیت و مقرون‌به‌صرفه ارائه می‌دهد — از طراحی گرفته تا سئو و پشتیبانی.
> در نهایت می‌توان گفت انتخاب ما، انتخابی هوشمندانه است.

**After:**
> مشتری قبل از این‌که به شما زنگ بزند، اسمتان را گوگل می‌کند. اگر چیزی پیدا
> نکند — یا بدتر، سایتی پیدا کند که در موبایل به‌هم‌ریخته است — سراغ رقیبتان
> می‌رود. کار ما همین است: سایتی که پیدا می‌شود و اعتماد می‌سازد. طراحی و سئو
> را ما انجام می‌دهیم؛ بعد از تحویل هم رهایتان نمی‌کنیم. نمونه‌کارها را ببینید
> و اگر سؤالی بود، همین امروز جواب می‌دهیم.

(Note: the After still failed one check — it uses an em dash twice. Final pass
replaces them: «اگر چیزی پیدا نکند، یا بدتر، سایتی پیدا کند که...». This is
exactly why the audit step exists.)



---

# PART 2 — Orthography (نگارش و رسم‌الخط)

# Persian orthography: the mechanical layer

Correct orthography is what separates a professional Persian document from a
typed-in-a-hurry one. Readers may not name the rule, but they feel it. All of
this is enforceable: the persian_cleanup script (full package; chat-only AIs apply the equivalent rules manually) --edit` fixes the mechanical
layer automatically; the fa_lint script (full package; chat-only AIs apply the equivalent rules manually) --check` reports what needs judgment.

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

the fa_lint script (full package; chat-only AIs apply the equivalent rules manually) --check` flags probable هکسره in both directions. It reports
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



---

# PART 3 — Content craft: POV, structure, honesty

# Persian content craft: point of view, structure, and honesty

Register (writing-style.md) decides *how formal* the text is. This file decides
*who is speaking*, *in what order the ideas arrive*, and *what you are allowed
to claim*. These are the disciplines that separate content a professional
editorial team would publish from content that merely reads smoothly.

Applies to educational articles, documentation, product and service pages,
internal reference docs, and the long-form half of social content — in any
field. The examples below use ordinary business situations on purpose: the
same rules govern a clinic's patient guide, a law firm's explainer, a
workshop's how-to, and a software company's release note.
Channel-specific mechanics live in social-channels.md.

## 1. Point of view — the most-broken rule in Persian content

Most Persian brand content slips between «ما»، «شما» and impersonal narration
inside a single paragraph. The result feels like a sales letter interrupting a
tutorial. One rule fixes it:

> **Explain the subject impersonally, teach the reader directly, and use "we"
> only for what the organization actually did or is responsible for.**

| Content type | Voice | Example |
|---|---|---|
| Fact, definition, cause, how a system behaves, advantage, limitation | Impersonal, subject-centred | «سفارش پس از تأیید پرداخت ثبت می‌شود.» |
| A step the reader performs | Second person; the verb alone carries it | «در صفحه‌ی سفارش‌ها، گزینه‌ی ویرایش را انتخاب کنید.» |
| The organization's own action, decision, policy, commitment, investigation | First person plural «ما» | «ما این محدودیت را در نسخه‌ی بعدی برطرف می‌کنیم.» |
| How people in general behave | «کاربر» / third person | «کاربر معمولاً پیش از خرید، نظرات را می‌خواند.» |

Supporting rules:

- **Don't repeat «شما».** Persian verb endings already encode the person.
  «شما می‌توانید فایل را حذف کنید» → «می‌توانید فایل را حذف کنید». Repetition
  reads as translated-from-English.
- **Don't switch POV inside a short section** without a reason. If a paragraph
  starts impersonal, finishing it with «ما» makes the reader re-parse it.
- **«شما باید» only for a real obligation with a real consequence.** Otherwise
  it sounds bossy for no reason. «باید» earns its place when skipping the step
  breaks something: «پیش از حذف، باید نسخه‌ی پشتیبان بگیرید؛ این عمل
  برگشت‌پذیر نیست.»
- A neutral explanation is not "cold". It is exactly what makes the reader
  trust the later paragraph where you do speak as the organization.

## 2. Education, product, and promotion

The fastest way to destroy the credibility of educational content is to bend it
toward a product halfway through. Keep the three separated:

- **The teaching must be worth reading even for someone who never buys.**
  If the article only works as a funnel, it is an ad wearing a tutorial's
  clothes, and readers notice.
- **Don't withhold the main answer.** Putting the actual answer behind a
  signup, or delaying it to the last paragraph, is the fastest way to lose both
  the reader and the ranking.
- **Present the problem before the solution**, and the solution before the
  product name.
- **Introduce a product only where it genuinely solves the problem** being
  discussed. Otherwise the mention is noise.
- **Tie every feature to a use case and a checkable result.** «امکان ثبت
  خودکار دارد» says nothing; «سفارش‌ها هر شب یک‌بار ثبت می‌شوند، پس در بدترین
  حالت یک روز تأخیر دارید» says something the reader can act on.
- **Never delete limitations, prerequisites, or conditions of use.** They are
  the part of the text that proves the rest is honest.
- **Don't present general industry knowledge as a proprietary advantage**, and
  don't attack competitors — describe your own trade-offs instead.
- **Don't repeat the brand or product name without reason.** Once the reader
  knows whose text this is, repetition only reads as insecurity.

## 3. Source fidelity and the four kinds of statement

Content built on sources (documentation, reports, a client brief, research)
must keep the distinction between what is known and what is guessed:

| | Definition | How to write it |
|---|---|---|
| **واقعیت** | verifiable, in the source | state plainly |
| **نظر** | someone's judgement | attribute it: «به گفته‌ی [نام یا نقش]...» |
| **پیش‌بینی** | about the future | mark it: «انتظار می‌رود»، «احتمالاً» — never as settled fact |
| **ادعا** | asserted, unverified | attribute and, where it matters, note it is unverified |

Working rules:

- **Never invent** a statistic, date, version number, price, company name,
  quote, command, output, or comparison to fill a structural slot. An empty
  section is honest; a fabricated one is a liability.
- **If data is incomplete**, either write the sentence cautiously or drop it.
- **If missing information blocks a correct answer**, ask one specific question
  before writing rather than guessing.
- **Don't hide contradictions between sources.** Either present the
  contradiction explicitly, or leave the disputed point out entirely — but
  never resolve it silently by picking the more convenient version.
- **Volatile facts** (versions, prices, compatibility, limits, commands) should
  not be stated as permanent without verification. Date them or hedge them.
- **Preserve names, numbers, dates and amounts exactly** as the source has
  them. Precision here is what earns the reader's trust everywhere else.

## 4. General structure for educational content

Use this order and delete any section that has nothing real to say:

1. **عنوان** — names the subject, problem, or result. No clickbait, no
   curiosity gaps.
2. **طرح مسئله** — one or two sentences: what this is about and why it matters.
   Cut the historical preamble and the «در دنیای امروز» opener entirely.
3. **زمینه لازم** — only the concept or prerequisite the reader needs in order
   to follow the solution. Not everything you know about the topic.
4. **بدنه** — the substance, in whichever pattern fits (§5).
5. **نتیجه‌ی مورد انتظار** — what changes if the reader does this, or what
   decision they can now make.
6. **محدودیت، استثنا، هشدار** — version, platform, condition, risk,
   irreversible effect. Placed *next to the relevant step*, not collected in a
   graveyard at the end.
7. **جمع‌بندی** — compresses the answer or the decision criterion. Introduces
   nothing new and does not restate the article.

For a comprehensive article, the internal progression that works is:
**تعریف → نحوه‌ی کار → کاربردها → اجزا یا ویژگی‌ها → مزایا و محدودیت‌ها →
مقایسه → مخاطب مناسب → آموزش عملی → جمع‌بندی → پرسش‌های متداول.**
General before specific; understanding before action.

Three questions carry almost any explanatory piece: **«چیست؟»،
«چگونه کار می‌کند؟»، «چه زمانی به کار می‌آید؟»** Answer a complex idea in one
plain sentence first, then add the technical detail.

## 5. Six body patterns

Pick the one that matches the content; don't force everything into steps.

**مرحله‌ای (procedure).** Prerequisites stated first. Steps numbered. One
action per step. Exact path and option names. The expected result of each step.
Warnings sit beside the step they concern, never at the end.

**نکته‌ای (tips).** Each tip gets a short heading and its own paragraph. Order
by importance, execution order, or logic — not randomly. Keep recommendations
visibly separate from requirements.

**مقایسه‌ای (comparison).** Define the options and the criteria first. Apply
*the same* criteria to every option — usually some of: use case, resources,
scalability, management effort, cost, stability, security, required expertise.
**Conclude conditionally**: which option suits which situation. Declaring an
absolute winner is almost always a sign the comparison was rigged. If two
options are complementary rather than rival, say so and explain when to use
both.

**تعریف مفهوم (concept).** تعریف ساده → نحوه‌ی کار → کاربرد → مزیت و محدودیت
→ مثال → زمان مناسب استفاده.

**مسئله و راه‌حل (troubleshooting).** نشانه → علت‌های محتمل → بررسی از
ساده‌ترین و کم‌ریسک‌ترین اقدام → راهکار → نتیجه‌ی مورد انتظار → نقطه‌ای که
باید سراغ پشتیبانی یا متخصص رفت. Ordering diagnostics from cheapest and safest
outward is what makes troubleshooting content actually usable.

**معرفی محصول یا قابلیت.** نیاز → راهکار → کاربرد → مخاطب مناسب → قابلیت
مرتبط → محدودیت و پیش‌نیاز → تفاوت با نزدیک‌ترین گزینه → مسیر بررسی بیشتر.
Never open with adjectives; open with the need.

## 6. Specialist terminology and proper names

Applies to any field with its own vocabulary — medicine, law, finance,
engineering, design, cooking — not just technology.

- **Keep the term the field actually uses.** If practitioners and readers say
  it in English (or in an established loanword), keep that form. Inventing an
  unfamiliar Persian equivalent hurts comprehension more than the loanword
  does; forcing a purist coinage nobody uses is a translation error, not
  linguistic care.
- **Explain on first use only**, with a plain Persian explanation in
  parentheses, then use one fixed form for the rest of the text. Consistency
  beats variety here — synonym-cycling a specialist term confuses readers and
  is an AI tell (writing-style.md T18).
- **Never translate official names**: product names, menu items, buttons,
  options, form fields, legal titles, drug names, standards. Whatever the
  reader will see in front of them is what the text must say, unchanged.
- Keep the boundary between the official name and your Persian explanation
  visible, so the reader knows which words to look for.
- Write names, figures, units, dates and any codes consistently throughout —
  mixed conventions make one text look like it had several authors.
- Where a field uses commands, formulas, references or identifiers, present
  them in a fixed format and keep them LTR when they're in Latin script
  (html-css.md, docx-pdf.md).

## 7. Clarity mechanics

- Short-to-medium sentences, active verbs. Avoid stacking several independent
  claims into one sentence.
- One idea per paragraph; typically 2–5 sentences.
- Keep chronological and logical order intact.
- Cut redundant phrases, heavy nominalisation (اسم‌سازی: «انجام بررسی را به عمل
  آورد» → «بررسی کرد»), ambiguous pronouns, and translationese.
- Replace a vague phrase with the precise word.
- Keep the text scannable on a phone — but scannable is not the same as
  fragmented; don't chop prose into disconnected lines.

## 8. Formatting discipline

- **Bold** is for a heading, a key concept, a warning, or a critical result.
  Bold as decoration destroys its own signal.
- **Numbered lists = sequence. Bulleted lists = independent items.** Using a
  numbered list for unordered things implies an order that doesn't exist.
- Keep list items grammatically parallel, and merge lists that overlap.
- Start each bullet with the concept name, then a colon and a short practical
  explanation — but avoid turning an entire article into bold-header bullets
  (writing-style.md T16). Prose carries argument; lists carry inventories.
- Avoid long, nested, or repetitive bullets.
- **Tables** for three or more options across fixed criteria. For two options,
  a paragraph or short list is usually clearer.
- Present advantages and limitations under separate, explicit labels.
- Anything meant to be copied or typed exactly — a code snippet, a reference
  number, a formula, an address — goes in code formatting and stays LTR when
  it's Latin script (html-css.md, docx-pdf.md).
- Keep heading hierarchy regular and headings self-explanatory: a reader
  skimming only the headings should still learn the outline of the argument.

## 9. Notes, warnings, and limits

- **نکته** = supplementary information. **هشدار** = risk. **محدودیت** =
  a condition or boundary on the result. Don't blur them.
- State the consequence precisely: not «مراقب باشید» but «اگر این گزینه را
  فعال کنید، آدرس‌های قبلی از کار می‌افتند».
- Put the warning **next to the action it concerns**. A warning discovered
  after the damage is decoration.
- Examples earn their place only when they improve understanding or the
  reader's decision. Keep them short, realistic, and matched to the audience.

## 10. Conclusion and call to action

- The conclusion states the answer, the decision criterion, or the next step.
  It is not a summary of the text and not a brand slogan.
- **One primary call to action**, only where it is the logical continuation of
  the content. Name the destination and what happens there. No pressure, no
  manufactured urgency.
- Link to the most specific relevant page — the exact documentation page, not
  the homepage — and say what the reader will find there.
- For statistics, standards, security reports, and consequential claims, cite a
  credible, primary, current source, and state the date, period, unit, and
  context of the data.

## 11. Pre-delivery checklist

- Does every claim come from the source material or the brief?
- Is the core definition clear near the beginning?
- Does the text move from understanding → evaluation → action?
- Is each term explained on first use, then used consistently?
- Does every feature appear with its practical effect?
- Are comparisons criteria-based and conclusions conditional?
- Are steps, commands and prerequisites complete and mutually consistent?
- Are repetition, exaggeration, unintended promotion, and invented detail gone?
- Is the point of view consistent and correct per §1?
- Is the deliverable the finished text only, with no internal labels
  («مقدمه»، «بدنه»، «نسخه‌ی بازنویسی‌شده») left in the published output?



---

# PART 4 — Academic writing (نگارش علمی)

# Persian academic writing (نگارش علمی فارسی)

For theses (پایان‌نامه), journal papers (مقاله علمی-پژوهشی), student reports,
technical analyses, research reviews (مرور پژوهش), and case studies
(مطالعه موردی). Academic Persian is a *fourth register* — more formal than
business writing, but the same enemies apply: bureaucratic fossils and AI
patterns make a paper feel machine-written, and reviewers notice.

## 1. Two genre families — decide first

**Journal/thesis format (ساختارمند):** section names are conventional and
expected — چکیده، مقدمه، پیشینه پژوهش، روش، یافته‌ها، بحث و نتیجه‌گیری، منابع.
Do NOT invent creative headings here; the convention IS the genre.

**Essay/report format (تحلیل، گزارش، مطالعه موردی):** descriptive headings
that preview content beat generic labels:
- Instead of «مقدمه» → «داکر و تغییر معنای استقرار نرم‌افزار»
- Instead of «نتیجه‌گیری» → «آنچه از مهاجرت پایگاه‌داده بدون توقف آموختیم»

## 2. The academic register

What it IS:
- Precise, measured, impersonal-leaning. Third person or «نگارنده/پژوهشگر»؛
  first-person plural («بررسی کردیم») is accepted in modern Persian papers.
- **Passive is legitimate here** («داده‌ها گردآوری شد»، «نشان داده شد») —
  the one register where the passive-voice warning in writing-style.md relaxes.
  Still prefer active when the agent matters.
- Hedged claims: «به نظر می‌رسد»، «شواهد نشان می‌دهد»، «احتمالاً» — one hedge
  per claim, not three (شاید بتوان گفت که احتمالاً... is AI stacking).
- Standard scholarly formulas are FINE and expected: «هدف این پژوهش... است»،
  «در این بخش... بررسی می‌شود». Formulaic ≠ AI in this genre.

What it is NOT (these stay banned even in the most formal paper):
- می‌باشد، می‌گردد for است/می‌شود — the Academy's style guidance and every
  serious آیین نگارش condemn them. «این روش کارآمد می‌باشد» marks the text
  as bureaucratic, not scholarly.
- لازم به ذکر است، شایان ذکر است — say the thing.
- Significance inflation: «نقش بسزایی»، «از اهمیت ویژه‌ای برخوردار» — state
  the finding and its measured effect instead.
- تعارف and reader-flattery. Academic Persian has zero تعارف.

## 3. AI tells specific to academic text

**A1. Mechanical enumeration.** اولاً... ثانیاً... در نهایت / نخست... دوم...
سرانجام as paragraph skeletons. Real papers connect by content: the result of
one paragraph raises the question the next answers.

**A2. Bullet-point substitution for prose.** Academic argument lives in
paragraphs. When information is genuinely a list, embed it:

> ❌ مزایای این روش عبارتند از:
> • کاهش زمان اجرا
> • کاهش هزینه
> • دقت بیشتر
>
> ✅ این روش سه مزیت عملی داشت: زمان اجرای هر آزمون از ۸ دقیقه به ۲ دقیقه
> رسید، هزینه‌ی هر نمونه حدود ۳۰٪ کاهش یافت و خطای اندازه‌گیری از ۵٪ به ۲٪
> رسید.

**A3. Source-listing instead of synthesis.** «اسمیت (۲۰۱۸) روشی ارائه کرد...
جانسون (۲۰۱۹) مدلی توسعه داد... براون (۲۰۲۰) بررسی کرد...» is an annotated
bibliography, not a پیشینه. Synthesize: group by idea, show the line of
development, name the disagreement, end at the gap your work fills.

**A4. Generic claims where numbers belong.** «دقت قابل توجهی حاصل شد» → «دقت
از ۸۴٪ به ۹۱٪ رسید (جدول ۲)». If you don't have the number, don't imply it.

**A5. The empty «چالش‌ها و چشم‌انداز آینده» section.** Limitations must be
specific to THIS study (sample size, single-domain data, unmeasured variables),
not boilerplate about «چالش‌های پیش رو».

**A6. Elegant variation on terminology.** In academic prose, terminology
consistency is a virtue: pick ONE term per concept (یادگیری ماشین, not
alternating with فراگیری ماشینی and ماشین لرنینگ) and repeat it. Synonym
cycling reads as AI *and* confuses reviewers.

## 4. Terminology and Latin material

- First use: Persian term + Latin in parentheses or footnote —
  «یادگیریِ انتقالی (Transfer Learning)». After that, Persian term alone.
- Use فرهنگستان equivalents where they're actually current (رایانه، داده،
  الگوریتم is fine as-is); don't force coinages nobody uses (تارنما) — the
  established loan is more scholarly than a strange purism.
- Latin abbreviations stay Latin and LTR: CNN، API، p-value. Wrap in LTR
  runs/`<bdi>` per the format references.
- Footnotes (پانویس) are the classic Persian-academic home for Latin
  equivalents and side notes. In docx they inherit RTL problems — each
  footnote paragraph needs the same bidi treatment (docx-pdf.md).

## 5. Citations and references

- In-text: (نویسنده، سال) for Persian sources — (کریمی، ۱۴۰۲)؛ Latin sources
  stay Latin — (Esteva et al., 2017). Page for direct quotes:
  (کریمی، ۱۴۰۲، ص. ۴۵). Direct quotes in «گیومه».
- Reference list (منابع): Persian sources first (alphabetical by surname),
  then Latin sources. Persian dates in هجری شمسی as published; don't convert.
- Never fabricate sources. If the user hasn't supplied references, write
  the citation slots as placeholders — «(منبع؟)» — and tell them; an invented
  DOI is fatal in this genre. Vague authority («کارشناسان معتقدند») is
  doubly banned in academic text.

## 6. Numbers, statistics, formulas

- Persian digits in prose: «۱۲۸ شرکت‌کننده»، «۹۱٪». Spell out small counts
  at sentence start.
- Statistical notation stays Latin and LTR: p < 0.05, F(2,45) = 3.71, R².
  Keep the whole expression in one LTR run so bidi doesn't scramble it.
- Formulas: LTR blocks (dir="ltr" / LTR paragraph), numbered «رابطه‌ی ۱».
- Tables: «جدول ۱: عنوان» ABOVE the table, «شکل ۱: عنوان» BELOW the figure.
  Caption paragraphs get keepNext (caption never strands on the wrong page) —
  see docx-pdf.md.

## 7. Structure conventions (journal/thesis format)

- **چکیده:** ۱۵۰–۳۰۰ words, one paragraph: مسئله ← روش ← یافته‌ی اصلی ←
  نتیجه. No citations, no abbreviations, findings in past tense.
- **واژگان کلیدی:** ۳–۶ terms, separated by «؛».
- **مقدمه:** funnel — the problem, what's known, the gap, «هدف این پژوهش».
- **روش:** replicable detail; passive natural here.
- **یافته‌ها:** report, don't interpret; every claim tied to a table/figure/test.
- **بحث:** interpret against the literature; limitations (specific);
  one-paragraph practical implication beats a «چشم‌انداز روشن» closer.

## 8. First-person calibration (by document type)

| Type | Voice |
|---|---|
| تحلیل فنی / گزارش آزمایش | Objective; «ما» sparingly for design decisions |
| مرور پژوهش | Moderate; evaluative stances hedged («به نظر می‌رسد شواهد...») |
| مطالعه موردی / گزارش تجربه | First person welcome for decisions and lessons: «اگر دوباره طراحی می‌کردیم...» |
| پایان‌نامه | Follow the university's شیوه‌نامه; default «نگارنده» or «ما» |

## 9. Worked example

**❌ AI-style:**
> در دنیای امروز، یادگیری ماشین نقش بسزایی در تشخیص پزشکی ایفا می‌نماید.
> مطالعات متعددی در این زمینه انجام شده است. اولاً، اسمیت و همکاران (۲۰۱۸)
> روشی مبتنی بر CNN ارائه کردند. ثانیاً، جانسون (۲۰۱۹) مدلی عمیق توسعه داد.
> نتایج این مطالعات نشان‌دهنده‌ی دقت بالا، سرعت مناسب و پتانسیل قابل توجه
> می‌باشد.

**✅ Scholarly Persian:**
> کاربرد یادگیری ماشین در تشخیص پزشکی از سامانه‌های قاعده‌محور آغاز شد و با
> ظهور شبکه‌های عمیق پس از ۲۰۱۲ مسیر تازه‌ای یافت. نقطه‌ی عطف، کار Esteva و
> همکاران (2017) بود که با آموزش شبکه‌ای پیچشی بر ۱۲۹٬۴۵۰ تصویر بالینی، به
> دقتی هم‌سنگ ۲۱ متخصص پوست رسید. پژوهش‌های بعدی همین الگو را به حوزه‌های
> دیگر بردند؛ اما هرچه دامنه گسترده‌تر شد، مسئله‌ی تعمیم‌پذیری پررنگ‌تر شد:
> Liu و همکاران (2020) نشان دادند عملکرد مدل روی داده‌ی بیمارستان‌هایی جز
> منبعِ آموزش، ۱۵ تا ۲۰ درصد افت می‌کند. همین شکاف، انگیزه‌ی اصلی پژوهش
> حاضر است.

Note what changed: synthesis with a through-line, real numbers, Latin names
left Latin, one hedge, no اولاً/ثانیاً, no می‌باشد, ends at the gap.

## 9.5 AI assistance, disclosure, and detector accusations

Academic work is where authorship claims carry the most weight, so two things
need saying plainly.

**Disclosure follows the institution's rule, not convenience.** Universities and
journals differ: some permit AI assistance for language editing, some require a
declaration, some prohibit it for substantive drafting. Find the actual policy
(شیوه‌نامه‌ی دانشگاه، راهنمای نویسندگان مجله) and follow it. Writing help that
is disclosed where disclosure is required stays honest; the same help concealed
does not. This skill improves the writing — it does not launder authorship, and
the techniques for disguising it (invisible characters, homoglyphs, injected
errors) are not here and should not be sought elsewhere.

**If a detector falsely flags a student's or researcher's work**, that is a
documented and common failure, not proof of anything. Persian-speaking authors
writing in English are hit hardest: one study of seven detectors measured a
**61.3% average false-positive rate for non-native English writers**, a 2023
evaluation of 14 tools found none reached 80% accuracy, and several major
universities withdrew from these tools over reliability concerns. A score is a
style guess, never evidence of authorship. Anyone facing such an accusation
should present drafts, notes, version history and sources — the ordinary
evidence of having done the work — rather than trying to satisfy the tool.

## 10. Checklist before delivering academic text

1. Register: no می‌باشد/لازم به ذکر است; hedges single; تعارف zero.
2. No اولاً/ثانیاً skeletons; no bullet lists where prose belongs.
3. پیشینه synthesizes; every number claim has a number; no invented sources.
4. Terminology: one Persian term per concept + Latin on first use.
5. Statistics/formulas in LTR runs; Persian digits in prose.
6. Structure matches genre (conventional sections for papers/theses).
7. Run the persian_cleanup script (full package; chat-only AIs apply the equivalent rules manually) --edit` then the fa_lint script (full package; chat-only AIs apply the equivalent rules manually) --check`
   on the text; fix everything contextual (dashes, میشود forms).
8. If producing docx/PDF: all rules in docx-pdf.md apply (RTL, keepNext
   captions, footnote bidi, fonts installed before conversion).



---

# PART 5 — Social channels: Telegram & Instagram

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

**Both:** run the text through the persian_cleanup script (full package; chat-only AIs apply the equivalent rules manually) --edit` and
the fa_lint script (full package; chat-only AIs apply the equivalent rules manually) --check` before delivery — هکسره errors and broken
نیم‌فاصله are the fastest way for a professional channel to look amateur
(orthography.md §5.1).



---

# PART 6 — SEO writing & copywriting

# Persian SEO writing & copywriting

Two crafts, one file, because in practice they overlap: SEO content that reads
like a robot doesn't rank long, and copy that ignores search never gets seen.
Everything in writing-style.md still applies — register detection first, AI
tells banned, brand-fact rule enforced. This file adds what's specific to
Persian search and Persian selling.

## Part A: SEO writing (سئو)

### A1. Search intent decides the content shape

| Intent | Persian query pattern | Content that wins |
|---|---|---|
| Informational (اطلاعاتی) | «چطور...»، «چیست»، «آموزش...» | Answer FIRST, then depth; step structure; FAQ block |
| Commercial (مقایسه‌ای) | «بهترین...»، «مقایسه...»، «کدام» | Honest comparison, criteria table, verdict |
| Transactional (تراکنشی) | «خرید...»، «قیمت...»، «سفارش» | Product/service page: price clarity, trust signals, CTA |
| Navigational | brand names, often misspelled | Correct brand spelling variants on-page |

Write for ONE intent per page. A «قیمت طراحی سایت» page that opens with the
history of the web serves no one — and Google measures that no one stayed.

### A2. Persian keyword variants — the part English SEO guides miss

Iranians type the same query many ways. The page should use the correct form
in prose but *acknowledge* variants (naturally, in different sentences or the
FAQ — never as a stuffed list):

- **ZWNJ variants:** وب‌سایت / وبسایت / وب سایت — searchers rarely type ZWNJ.
  Write the correct form; variants appear naturally in quotes/FAQ phrasing.
- **Loan vs Persian term:** سئو/SEO، دیجیتال مارکتینگ/بازاریابی دیجیتال —
  use the dominant form as primary, mention the other once early.
- **Digit scripts:** آیفون ۱۳ and آیفون 13 are different strings to a search
  engine; prices get searched with Latin digits. Keep prose digits Persian
  (orthography rule); let structured data / attributes carry Latin forms.
- **Spelling variants:** طهران/تهران era is gone, but ی/ي contamination from
  copy-paste still splits queries — publish only Persian ی/ک (the cleanup
  script guarantees this).
- Mine real variants from Search Console queries when the user has access;
  invented keyword lists are the SEO version of fabricated brand facts.

### A3. On-page checklist (writer's portion)

1. **Title (~60 chars):** keyword phrase at the START (rightmost, first-read
   position in RTL), brand at the end: «قیمت طراحی سایت فروشگاهی در ۱۴۰۴ | برند».
2. **Meta description (~150 chars):** the promise + one concrete detail + soft
   CTA. It's ad copy for the SERP, not a summary.
3. **H1:** one, contains the keyword naturally. H2s: the sub-questions people
   actually ask (they feed پرسش‌های مرتبط / PAA).
4. **First paragraph answers the query.** اول جواب، بعد توضیح — this wins
   featured snippets and respects the reader.
5. **FAQ section (سوالات متداول):** 3–6 real questions, one-paragraph answers.
   Mark up as FAQ schema when building the page (html-css.md).
6. **Internal links:** descriptive Persian anchors («راهنمای سئوی فروشگاهی»)،
   never «اینجا کلیک کنید».
7. **Alt text:** describe the image in Persian, keyword only when true.
8. **Slug:** short, hyphenated; Persian slugs are legitimate
   (`/قیمت-طراحی-سایت/`) — transliterated ones too; follow the site's
   existing convention.
9. **Length:** as long as the intent needs, not a word more. 300 thin words
   lose; 3000 padded words also lose.

### A4. What kills Persian SEO content

- Keyword-stuffed titles: «طراحی سایت | طراحی سایت ارزان | قیمت طراحی سایت» —
  a 2015 fossil that now marks spam.
- The «در دنیای امروز» intro (T4) — readers bounce, rankings follow.
- Generic listicles with no Iranian reality (prices in dollars, examples
  from Amazon when the reader uses دیجی‌کالا).
- AI-tell clusters (T1–T18) — helpful-content systems and human readers
  converge on the same judgment.
- Register mistakes: service pages are formal-but-human; blogs semi-formal.
  A خودمونی pricing page undermines purchase trust exactly at the decision
  moment.

## Part B: Copywriting (کپی‌رایتینگ)

### B1. The two questions before any copy

1. **Register** — from the detection procedure in writing-style.md. Casual
   copy in the wrong place is not "punchy", it's costly.
2. **The ONE promise.** Each page/post/ad makes one promise. If the draft
   makes three, it makes none.

### B2. Structures that work in Persian

**PAS (درد ← تشدید ← راه‌حل)** — the workhorse:
> مشتری اسمتان را گوگل می‌کند و چیزی پیدا نمی‌کند. (درد)
> رقیبتان را اما پیدا می‌کند — با سایتی که ساعت ۲ شب هم سفارش می‌گیرد. (تشدید)
> سایت فروشگاهی شما در ۴۵ روز آماده می‌شود؛ از طراحی تا اولین سفارش. (راه‌حل)

**AIDA** for longer landing pages: hook → مزیت‌های ملموس → اثبات → CTA.

**Headline patterns (تیتر):**
- عددی: «۷ اشتباهی که فروش سایتتان را می‌خورد»
- سوالی: «چرا سایتتان بازدید دارد ولی مشتری نه؟»
- منفعتی: «سایتی که خودش می‌فروشد»
- Avoid the manufactured-aphorism tell (T18): «سئو زبانِ اعتماد است» is
  perfume, not copy.

### B3. Feature → benefit, the Persian habit

State the feature, then translate it into the customer's life:

| ویژگی (feature) | مزیت (benefit) |
|---|---|
| درگاه پرداخت مستقیم | پول همان لحظه به حساب خودتان می‌نشیند |
| پنل مدیریت سفارش | آشپزخانه بدون تلفن‌بازی سفارش را می‌بیند |
| نسخه‌ی موبایل‌محور | مشتریِ توی تاکسی هم راحت سفارش می‌دهد |

(That last one is semi-formal register — fine for web copy, not for a
proposal. Benefits inherit the artifact's register.)

### B4. CTA by register

| Register | CTA examples |
|---|---|
| Formal (proposal, service page) | «درخواست مشاوره رایگان»، «دریافت پیش‌فاکتور»، «رزرو جلسه» |
| Semi-formal (blog, newsletter) | «راهنمای کامل را بخوانید»، «همین حالا شروع کنید» |
| Casual (Instagram, Telegram) | «دایرکت بده»، «کلمه‌ی X رو کامنت کن»، «لینک توی بایو» |

One primary CTA per artifact; repeat it, don't multiply it.

### B5. Money, honesty, and Persian-specific trust

- **Prices: always name the unit** — تومان vs ریال ambiguity has burned
  enough customers that unlabeled numbers read as a trick. Persian digits,
  thousands separator: «۸۵٬۰۰۰٬۰۰۰ تومان». Ranges honestly: «از ۳ میلیون
  تومان شروع می‌شود» only if something real costs ۳.
- **Brand-fact rule (writing-style.md) applies doubly:** no invented client
  counts, satisfaction percentages, awards, or «۱۰ سال تجربه». Ask the user
  for real numbers; real-but-small beats fake-but-big.
- **Urgency only when true:** «ظرفیت این ماه: ۴ پروژه» works if it's true and
  reads as spam if it repeats forever. Never !!!.
- **تعارف calibration:** warmth yes, ritual no. «قابل شما را ندارد» jokes
  belong in casual social copy at most; B2B copy earns trust with clarity.
- **Microcopy:** buttons = short verb phrases («افزودن به سبد خرید»،
  «ثبت سفارش»، «ادامه»). Error messages: polite, direct, actionable —
  «کد تخفیف معتبر نیست. دوباره بررسی کنید یا بدون کد ادامه دهید.»

### B6. Landing page skeleton (Persian)

1. هدلاین — the one promise, in the reader's words
2. زیرتیتر — how, in one sentence
3. ۳ مزیت — concrete, feature→benefit translated
4. اثبات — real نمونه‌کار / real numbers / real testimonial (with permission)
5. رفع اعتراض — سوالات متداول: قیمت، زمان، پشتیبانی، «اگر راضی نبودم؟»
6. CTA — repeated after each scroll-depth section, same verb each time

## Part C: Content quality standards (E-E-A-T for Persian sites)

Google evaluates experience/expertise/authoritativeness/trust on competitive
queries across the board — and its AI-content detection improves every update.
The writing-side signals, Persian-adapted:

- **Named authors with real bios** (نویسنده با نام، تخصص و عکس). Anonymous
  «تیم محتوا» posts rank worse and read worse. If the user has no author
  program, say so and suggest one.
- **First-hand evidence:** original screenshots, real numbers from real
  projects (with permission), process details only a practitioner would know
  («در پروژه‌های فروشگاهی معمولاً درگاه X این خطا را می‌دهد...»). This is the
  brand-fact rule's positive side: real specifics are the strongest SEO asset.
- **Trust furniture Iranian users actually check:** صفحه‌ی درباره‌ی ما with
  real people, تماس with address/phone, اینماد for e-commerce, شفافیت قیمت.
- **The AI-tell connection:** the T1–T18 patterns (writing-style.md) are
  exactly what quality systems flag as generic content. De-AI-ing IS an
  E-E-A-T intervention.

**Word-count floors by page type** (floors, not targets — depth follows intent):
homepage ~500، صفحه‌ی خدمات ~800، پست بلاگ ~1500، صفحه‌ی محصول ~400،
لندینگ ~600، سوالات متداول ~800. Below these, pages read thin to users and
crawlers alike; padding above them with fluff is equally fatal.

**The doorway-page trap — the classic Iranian agency mistake:** mass-produced
«طراحی سایت در تهران / کرج / شیراز / تبریز...» pages with only the city name
swapped. Google's doorway detection penalizes the whole site. A location page
is publishable only with genuinely local content: local projects/clients,
محله and landmark references, a local contact signal. Can't produce that for
30 cities? Then don't publish 30 pages — one strong «خدمات در سراسر ایران»
page outranks 30 thin clones after the penalty.

**بریف محتوا (content brief) template** — fill before writing any SEO piece:

```
کلیدواژه‌ی اصلی: ...        اینتنت: اطلاعاتی/مقایسه‌ای/تراکنشی
کلیدواژه‌های فرعی/واریانت‌ها: ...
مخاطب و رجیستر: ...
H2های پیشنهادی (سوالات واقعی کاربر): ...
سوالات متداول (۳–۶): ...
لینک‌های داخلی (انکر توصیفی): ...
CTA و مقصدش: ...
واقعیت‌های برند که اجازه‌ی استفاده داریم: ...
```

**Division of labor:** this skill owns the Persian *writing* layer. Full
technical SEO — site audits, schema validation, Core Web Vitals, backlinks,
maps/local packs — belongs to dedicated SEO tooling (e.g. an SEO plugin or
agency toolchain); write to their briefs and findings rather than guessing
technical facts.

### Verification for SEO/copy deliverables

Same pipeline as all Persian text: `persian_cleanup.py --edit` →
`fa_lint.py --check` → the native test — plus four genre checks:
does the title match ONE intent? is every factual claim sourced from the
user/brief? does the CTA verb match the register? does every page in a batch
carry genuinely unique content (no doorway clones)?



---

# PART 7 — Fonts

# Persian fonts: catalog, pairing, embedding

All fonts here are SIL OFL — free for commercial use, embedding allowed.
Bundled families live in `assets/fonts/`. The rest need
the download_fonts script (full package; chat-only AIs apply the equivalent rules manually) (requires GitHub access — will NOT work in
offline/allowlisted sandboxes; in that case use only what's bundled, or ask
the user to drop TTFs into the project folder).

## Catalog

| Font | Personality | Use for | Avoid for | Weights |
|---|---|---|---|---|
| **Vazirmatn** ★bundled | Neutral, clean, contemporary; the Persian Inter | Body text, UI, documents, anything | — (the safe default) | 9 (Thin–Black) |
| **Lalezar** ★bundled | Loud, friendly, poster/tabloid display | Headlines, covers, banners, campaign titles | Body text, long headings | 1 |
| **Shabnam** | Softer, rounder Vazir sibling | Body alternative, friendly docs | — | 5 + FD variants |
| **Sahel** | Modern, slightly condensed | Headings, dashboards, UI labels | Dense long-form body | 3 + FD |
| **Samim** | Sober text face tuned for reading | Long reports, articles, books | Display sizes | 3 + FD |
| **Parastoo** | Bookish, literary, mild serif flavor | Formal letters, literary/academic docs | Modern tech branding | 2 + FD |
| **Tanha** | Thin, elegant, airy display | Pull quotes, elegant covers, invitations | Body text (too light) | 1 |
| **Gandom** | Warm, rounded, approachable | Casual brochures, kids/food/lifestyle content | Corporate formal docs | 2 + FD |

("FD" variants ship with built-in Farsi digit glyphs mapped to ASCII digits —
prefer real Persian digit characters instead; see orthography.md.)

Sources (for `download_fonts.py` or manual download):
- Vazirmatn: github.com/rastikerdar/vazirmatn (also on Google Fonts)
- Lalezar: fonts.google.com/specimen/Lalezar (github.com/BornaIz/Lalezar)
- Others: github.com/rastikerdar/{shabnam,sahel,samim,parastoo,tanha,gandom}-font

## Pairings that work

| Deliverable | Headings | Body |
|---|---|---|
| Business proposal / invoice | Vazirmatn Bold/Black | Vazirmatn Regular |
| Marketing one-pager, poster | Lalezar | Vazirmatn |
| Long report / whitepaper | Vazirmatn Bold | Samim or Vazirmatn |
| Product docs / dashboard | Sahel Bold | Shabnam or Vazirmatn |
| Literary / formal letter | Parastoo Bold | Parastoo |
| Elegant cover + quote | Tanha (display) | Vazirmatn |

One display font per document, maximum. When in doubt: Vazirmatn everywhere,
weights for hierarchy.

## Typography rules for Persian

- **Line height:** Persian needs more leading than Latin — 1.6–2.0 in CSS,
  `line: 312+` (≥1.3) in docx, more for headings. Tight leading clips
  ascenders and dots.
- **Size:** Persian x-height runs small; bump body ~1pt/10% over the Latin
  equivalent (11–12pt docx body, 16–18px web).
- **Never letter-space** (`letter-spacing`/character spacing) — Persian letters
  join; tracking tears the joins apart. Not even for headings. Use size/weight/
  color for emphasis instead.
- **Never fake bold/italic.** Use real weights. Italic barely exists in Persian
  type; for emphasis use bold, color, or «گیومه».
- **Kashida (کشیده):** justification by stretching connections. Word processors
  do it automatically with justify; don't insert manual ـ characters.
- **Justified text** is traditional for print Persian body; START-aligned
  (ragged left) is fine for web and modern docs. Headings: never justify.

## Embedding per format

### docx (docx-js / python-docx)
Font name exactly as the family name: `"Vazirmatn"`, `"Lalezar"`.
Always with `hint: "cs"` (docx-js) or `w:rFonts w:cs=` (python-docx) — see
docx-pdf.md. The font must be installed on the converting machine
(`bash the install_fonts script (full package; chat-only AIs apply the equivalent rules manually)) or LibreOffice substitutes DejaVu.

### HTML / CSS
```css
@font-face {
  font-family: "Vazirmatn";
  src: url("fonts/Vazirmatn-Regular.woff2") format("woff2"),
       url("fonts/Vazirmatn-Regular.ttf") format("truetype");
  font-weight: 400; font-display: swap;
}
body {
  font-family: "Vazirmatn", "Segoe UI", Tahoma, sans-serif; /* Tahoma = classic Persian-safe fallback */
  line-height: 1.8;
}
```
Online pages can use Google Fonts (`family=Vazirmatn:wght@100..900` or
`family=Lalezar`); offline/PDF-print pages must reference local files —
copy them from `assets/fonts/`.

### pptx
Set the font on both latin and cs typefaces of every run (see pptx.md).
PowerPoint font embedding is unreliable cross-platform; if the deck must
travel, export a PDF (with fonts installed) alongside it.

### Checking a glyph exists (before using any symbol)
```python
from fontTools.ttLib import TTFont
cmap = TTFont("assets/fonts/Vazirmatn-Regular.ttf").getBestCmap()
ok = all(ord(c) in cmap for c in "•·۱۲۳؟،؛«»٪٬")
```
Known result for the bundled fonts: • · and all Persian punctuation/digits are
present; ▪ ■ ✓ ● ◆ are NOT (they silently fall back to DejaVu in PDFs). Check
before using anything fancier than • — `verify_pdf.py` will catch the fallback
after the fact, but checking first is cheaper.



---

# PART 8 — Word/DOCX + PDF

# Persian DOCX + PDF: RTL and pagination recipes

Battle-tested fixes from real Persian proposal production. The docx-js (npm `docx`)
examples are the reference implementation; python-docx equivalents follow at the
end. Read the whole file before generating a Persian Word document — most of these
failures are invisible until you convert to PDF and look.

**Pick your library FIRST, in 10 seconds:** if `docx` (npm) is already importable,
use the docx-js recipes. If not — and in sandboxed environments npm installs are
often blocked — do NOT spend time fighting the package manager: go straight to
python-docx (§6), which ships in most sandboxes and sets the exact same OOXML
flags. The concepts in §1–§5 (START-not-RIGHT, bidi, cs fonts, keepNext,
cantSplit) apply identically to both libraries.

**Colors in this file are placeholders.** Where an example sets `color`, a
border, or a fill, it uses neutral grey/black purely to show the property's
position. Do NOT reproduce these values as a look. Default to unstyled (black
text, no accent). Pull real colors only from the user's request, an attached
brand skill, or a template you're matching. The RTL/pagination structure is the
reusable part; the styling is not.

## Table of contents

1. RTL: alignment, runs, tables, numbers, symbols, sections, styles
2. Divider/full-bleed pages (empty headers, titlePage, white-bar fix)
3. Pagination: orphan headings, unsplittable cards, blank pages, FAQ/tables
4. Fonts and PDF conversion workflow
5. Verification checklist (mandatory)
6. python-docx equivalents

---

## 1. RTL correctness

### 1.1 The core trap: RIGHT means visual LEFT in RTL

In OOXML, when `bidirectional: true` is set, `AlignmentType.RIGHT` is interpreted
as "end of text" — and in RTL, "end" is the **visual left**. Persian text aligned
RIGHT renders left-aligned. Use `START`, which in RTL always means visual right.

```javascript
// ❌ WRONG — left-aligns Persian in RTL
new Paragraph({
  alignment: AlignmentType.RIGHT,
  bidirectional: true,
  children: [new TextRun({ text: "متن فارسی", font: { name: "Vazirmatn" } })]
})

// ✅ RIGHT — visually right-aligned
new Paragraph({
  alignment: AlignmentType.START,
  bidirectional: true,
  children: [new TextRun({
    text: "متن فارسی",
    font: { name: "Vazirmatn", hint: "cs" },
    rightToLeft: true
  })]
})
```

`hint: "cs"` (Complex Script) tells Word this font applies to the Persian/Arabic
script run. Without it Word may pick a different font for Persian glyphs.
Audit rule: **grep your generator for `AlignmentType.RIGHT` — every hit is a bug**
(use `END` only when you deliberately want visual left, e.g. a Latin code block).

Define a helper once and use it for all Persian runs:

```javascript
const fa = (text, opts = {}) => new TextRun({
  text,
  rightToLeft: true,
  font: { name: "Vazirmatn", hint: "cs" },
  ...opts,
});
```

### 1.2 Tables must flow right→left

For any table where the first column belongs on the right (all Persian tables):

```javascript
new Table({
  width: { size: 100, type: WidthType.PERCENTAGE },
  visuallyRightToLeft: true,  // ← the key: first cell = visual right
  borders: allNoBorders,
  rows: [new TableRow({
    cantSplit: true,
    children: [
      new TableCell({ children: [/* first item — visual RIGHT */] }),
      new TableCell({ children: [/* second item — visual LEFT */] }),
    ]
  })]
})
```

Without `visuallyRightToLeft`, a two-column module list reads backwards.

### 1.3 Persian digits keep paragraphs RTL

A Latin digit at paragraph start flips the bidi direction of the line. Use
Persian digits in all Persian text, including list numbering:

```javascript
// ❌ Latin digit makes the paragraph LTR
fa((i + 1) + ".  ", { bold: true })

// ✅ Persian digit preserves RTL
const faDigits = "۰۱۲۳۴۵۶۷۸۹";
const toFa = (n) => String(n).replace(/[0-9]/g, d => faDigits[+d]);
fa(toFa(i + 1) + ".  ", { bold: true })
```

Prices too: «۲۵٬۰۰۰٬۰۰۰ تومان» (U+066C or ، as thousands separator — pick one
and be consistent).

### 1.4 Symbols: verify glyphs exist

Persian fonts miss many symbols; missing glyphs silently fall back to an ugly
substitute font in the PDF. Check before using:

```python
from fontTools.ttLib import TTFont
cmap = TTFont("Vazirmatn-Regular.ttf").getBestCmap()
print(0x2299 in cmap)  # ⊙ supported?
```

Verified safe in the bundled Vazirmatn and Lalezar: `•` (U+2022), `·` (U+00B7).
NOT in Vazirmatn/Lalezar (falls back to DejaVu): ▪ ■ ⊙ ◆ ✓ ✕ ● ○ and emoji.
Other Persian fonts have different coverage — run the check above before using
any symbol; a fallback shows up later as a DejaVu row in `pdffonts`.

### 1.5 Every section: bidi — and VERIFY it reached the XML

```javascript
sections.push({
  properties: {
    page: { size: { width: 11906, height: 16838 } },  // A4 portrait, twips
    bidi: true,  // ← required per section
  },
  children: [...]
})
```

**Setting it is not the same as it being written.** Some docx-js versions
silently drop `bidi` from section properties, and in python-docx it is easy to
append `<w:bidi/>` in the wrong position. `<w:bidi/>` must be the FIRST child
of `<w:sectPr>` (OOXML enforces child order — appended at the end, renderers
ignore it). Always check the produced file, not your source code:

```bash
unzip -p output.docx word/document.xml | grep -o '<w:sectPr[^>]*>.\{0,20\}'
# want: <w:sectPr ...><w:bidi/><w:pgSz .../>
# a sectPr going straight to <w:pgSz/> means the flag was dropped
```

**What section bidi actually controls** (measured, LibreOffice render):
it sets the section's BASE direction, which every element without its own
explicit direction inherits. A table with no `bidiVisual` renders its first
column on the LEFT without section bidi, and on the RIGHT with it — a silent
column-order reversal. Paragraphs and runs that DO carry their own
`bidirectional`/`rightToLeft` flags render correctly either way, so a
fully-flagged document may look fine and still be a trap: the first element
someone adds later without flags inherits the wrong direction.

Treat section bidi as the safety net, not the mechanism: set it, verify it in
the XML, AND set the per-paragraph/run/table flags. Belt and braces, because
each covers what the other misses.

**Patch it post-generation when the library drops it** — language-agnostic,
works on any .docx from any toolchain:

```python
import zipfile, re, shutil

def force_section_bidi(docx_path):
    """Insert <w:bidi/> as the first child of every <w:sectPr>. Idempotent."""
    tmp = docx_path + '.tmp'
    zin = zipfile.ZipFile(docx_path)
    items = {n: zin.read(n) for n in zin.namelist()}
    zin.close()
    xml = items['word/document.xml'].decode('utf-8')
    xml = re.sub(r'(<w:sectPr[^>]*>)(?!<w:bidi/>)', r'\1<w:bidi/>', xml)
    items['word/document.xml'] = xml.encode('utf-8')
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as zout:
        for n, d in items.items():
            zout.writestr(n, d)
    shutil.move(tmp, docx_path)
    return xml.count('<w:sectPr')
```

Node equivalent if you're in docx-js: same regex over `word/document.xml`
using `adm-zip` (`zip.readAsText` → replace → `zip.updateFile` → `writeZip`).
The `(?!<w:bidi/>)` guard keeps it safe to run twice.

### 1.6 Document default styles

```javascript
styles: {
  default: {
    document: {
      run: {
        font: { name: "Vazirmatn", hint: "cs" },
        size: 22,            // 11pt — half-points
        rightToLeft: true,
      },
      paragraph: {
        spacing: { line: 312 },   // ≈1.3 lines; Persian needs ≥1.3, tight leading clips
        bidirectional: true,
      },
    },
  },
}
```

---

## 2. Divider / full-bleed pages (OPTIONAL — only if the design calls for them)

This whole section is a technique, not a recommendation. Plain documents need
no divider pages. Build them only when the user's design or brand asks for
full-bleed color pages; otherwise skip §2 entirely.

Full-color divider pages must not show the running header/footer. Headers
inherit from the previous section unless you override with an *empty* header:

```javascript
const emptyPara = [new Paragraph({
  spacing: { before: 0, after: 0, line: 1, lineRule: "exact" },
  children: [new TextRun({ text: "", size: 1 })]
})];
const emptyHeader = {
  first: new Header({ children: emptyPara }),
  default: new Header({ children: emptyPara })
};
const emptyFooter = {
  first: new Footer({ children: emptyPara }),
  default: new Footer({ children: emptyPara })
};

sections.push({
  properties: {
    page: { margin: { top: 0, bottom: 0, left: 0, right: 0 } },
    bidi: true,
    titlePage: true,  // ← required for the empty first-page header to apply
  },
  headers: emptyHeader,
  footers: emptyFooter,
  children: buildDivider(...)
});
```

### White bars on dark pages (LibreOffice)

LibreOffice enforces a minimum header/footer margin, leaving white strips on
full-bleed dark pages. Fix in PDF post-processing with PyMuPDF — paint the
background color over the strips (set `BG` to the page's own color):

```python
import fitz  # PyMuPDF

BG = (r/255, g/255, b/255)  # set to the divider page's own background color

def fix_white_bars(pdf_path, is_dark_bg_page):
    doc = fitz.open(pdf_path)
    for page in doc:
        if is_dark_bg_page(page.get_text()):   # detect by known divider text
            r, over, bar, edge = page.rect, 5, 85, 5
            for box in [
                fitz.Rect(-over, -over, r.width + over, bar),                      # top
                fitz.Rect(-over, r.height - bar, r.width + over, r.height + over), # bottom
                fitz.Rect(-over, -over, edge, r.height + over),                    # left
                fitz.Rect(r.width - edge, -over, r.width + over, r.height + over), # right
            ]:
                page.draw_rect(box, color=BG, fill=BG, width=0)
    tmp = pdf_path + ".tmp"
    doc.save(tmp, deflate=True); doc.close()
    import os; os.replace(tmp, pdf_path)
```

---

## 3. Pagination

Four failure modes: orphan headings, split cards, blank pages, mid-sentence
breaks. All preventable at generation time.

### 3.1 No orphan headings

Every heading paragraph gets `keepNext` (stays with following content) and
`keepLines` (its own lines don't split):

```javascript
function sectionHeading(text) {
  return new Paragraph({
    alignment: AlignmentType.START,
    bidirectional: true,
    spacing: { before: 480, after: 280, line: 600, lineRule: "atLeast" },
    keepNext: true,
    keepLines: true,
    // border/color OPTIONAL and neutral — omit for plain output; set only
    // from the user's brief or brand. Structure is what matters here.
    children: [
      fa("•  ", { size: 32, bold: true }),   // • verified in Vazirmatn; ▪ is NOT
      fa(text, { size: 36, bold: true }),
    ],
  });
}
```

Apply to every heading level, FAQ questions (keep with their answer), and
workflow-step titles (keep with their description).

### 3.2 Unsplittable cards

Wrap each card/box in a single-cell table with `cantSplit` — if it doesn't fit,
the whole card moves to the next page instead of tearing in half:

```javascript
const cardChildren = [
  new Paragraph({ /* card title */ }),
  new Paragraph({ /* description */ }),
  new Paragraph({ /* price */ }),
  new Table({ /* module list */ }),
  new Paragraph({ /* delivery time */ }),
];

items.push(new Table({
  width: { size: 100, type: WidthType.PERCENTAGE },
  borders: allNoBorders,
  rows: [new TableRow({
    cantSplit: true,  // ← the whole card stays together
    children: [new TableCell({
      width: { size: 100, type: WidthType.PERCENTAGE },
      borders: allNoBorders,
      margins: { top: 0, bottom: 0, left: 0, right: 0 },
      children: cardChildren,
    })],
  })],
}));
```

Caveat: a card taller than one page will overflow — keep cards under ~¾ page.

### 3.3 No blank pages

Two causes. First, separators added after the *last* item:

```javascript
for (let i = 0; i < list.length; i++) {
  items.push(buildCard(list[i]));
  if (i < list.length - 1) {          // ← separator only BETWEEN items
    items.push(new Paragraph({
      spacing: { before: 100, after: 0 },
      // separator line optional; neutral grey placeholder if used at all
      border: { bottom: { style: BorderStyle.SINGLE, size: 3, color: "CCCCCC", space: 2 } },
      children: [new TextRun({ text: "" })],
    }));
  }
}
```

Second, manual `PageBreak` right before a section break:

```javascript
// ❌ empty paragraph + PageBreak at section end = blank page
items.push(new Paragraph({ children: [new TextRun({ text: "" })] }));
items.push(new Paragraph({ children: [new PageBreak()] }));

// ✅ a new section already starts a new page — no PageBreak needed
```

### 3.4 Paragraph integrity

```javascript
// Important/short paragraphs: don't strand them
new Paragraph({ keepNext: true, keepLines: true, /* ... */ });

// FAQ: question stays with answer
items.push(new Paragraph({
  keepNext: true, keepLines: true,
  children: [fa("۱. ", { bold: true }), fa(question, { bold: true })],
}));
items.push(new Paragraph({ children: [fa(answer)] }));
```

### 3.5 Multi-page data tables

```javascript
new TableRow({ tableHeader: true, cantSplit: true, children: headerCells }); // header repeats per page
new TableRow({ cantSplit: true, children: dataCells });                      // rows never split
```

---

## 4. Fonts and PDF conversion

1. Install fonts BEFORE converting (else LibreOffice substitutes silently):
   ```bash
   bash the install_fonts script (full package; chat-only AIs apply the equivalent rules manually) && fc-list | grep -i vazir
   ```
2. Convert: `soffice --headless --convert-to pdf output.docx`
3. Post-process white bars if you have full-bleed pages (§2).
4. Verify (§5).

Persian sizing guidance: body 11–12pt, line spacing ≥1.3 (`line: 312+`);
headings need `lineRule: "atLeast"` with generous values — Persian ascenders/
descenders clip in tight exact line heights.

---

## 4.5 Package integrity — "Word says the file is corrupt"

RTL correctness is worthless if Word refuses to open the file at all. A .docx is
a ZIP of XML parts, and a few structural rules decide whether Office accepts it:

| Requirement | Why it matters |
|---|---|
| `[Content_Types].xml` is the FIRST ZIP entry | Word may reject the package outright if it isn't |
| Every part's extension declared in `[Content_Types].xml` | undeclared part = "unreadable content" |
| Every `.rels` Target resolves to a real part | dangling relationship = repair prompt |
| Every XML part well-formed, no control chars (<0x20 except tab/LF/CR) | one stray byte kills the whole document |
| No duplicate part names | only the first wins; Word complains |

**python-docx ships a Word-for-Mac-2011 template — verified, not folklore.**
Every document created with `Document()` inherits these artifacts:

```
word/stylesWithEffects.xml            ← Mac-only part
docProps/thumbnail.jpeg               ← often malformed
xmlns:mo=... in document.xml          ← Mac namespace
<Application>Microsoft Macintosh Word</Application>, <AppVersion>14.0000
<?xml version='1.0' ...?>             ← single quotes, not Office's form
```

These usually open fine, but they are exactly the fingerprint found in files
that Word reports as corrupt on Windows. For anything you hand to a client,
clear them:

```bash
python3 scripts/verify_docx.py out.docx --fix --sanitize
```

`--sanitize` removes the stray parts, strips their references from
`[Content_Types].xml` and the `.rels` files (leaving them would create dangling
relationships — worse than the artifacts), and normalises the XML declarations.
It re-validates afterwards and refuses to hand back a package it just broke.
Measured on a real proposal: 17 parts → 15, content and RTL flags identical,
PDF conversion still clean.

**The nuclear option — LibreOffice round-trip.** LibreOffice parses leniently
and re-serialises into a clean, Office-compliant package, which fixes most
inherited corruption in one step:

```bash
soffice --headless --convert-to docx --outdir <OTHER_dir> input.docx
```

Input and output directories must differ, or soffice silently fails. Caveat:
a round-trip re-renders styles, so re-run the RTL checks afterwards — it can
also drop or alter formatting you set deliberately. Prefer `--sanitize` for
files you generated; keep the round-trip for files that arrive already broken.

**If a file is already corrupt**, work in this order: confirm it starts with the
bytes `PK\x03\x04`; run `verify_docx.py` to name the defective part; try the
LibreOffice round-trip; only then do manual surgery (rebuild the ZIP with
`[Content_Types].xml` first, dropping the offending part and every reference to
it). Never edit the user's original — always work on a copy.

## 5. Verification checklist (run every time)

`python3 the verify_pdf script (full package; chat-only AIs apply the equivalent rules manually) output.pdf --expect-font Vazirmatn` automates
these; the manual equivalents:

```bash
# 1. Near-empty pages (orphaned headings / stray breaks)
pdftotext -layout output.pdf check.txt
python3 - <<'EOF'
pages = open('check.txt').read().split('\x0c')
for i, p in enumerate(pages, 1):
    lines = [l.strip() for l in p.split('\n') if l.strip()]
    content = [l for l in lines if not l.isdigit()]   # drop bare page numbers
    if len(content) < 3 and i < len(pages):
        print(f'page {i}: possibly empty ({len(content)} content lines)')
EOF

# 2. Template leaks
grep -iE "undefined|NaN|null" check.txt

# 3. Fonts actually embedded (every row should say your font, emb=yes;
#    any DejaVu/Liberation row = fallback happened somewhere)
pdffonts output.pdf

# 4. Page count sanity
python3 -c "from pypdf import PdfReader; print(len(PdfReader('output.pdf').pages))"
```

Then open the PDF (or render pages to PNG with PyMuPDF and *look*): right
alignment on every page, no orphan headings, no split cards, digits Persian.

---

## 6. python-docx equivalents

python-docx has no first-class RTL API; set the OOXML elements directly.

```python
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

def _set(el, parent):
    parent.append(el); return el

def rtl_paragraph(p):
    """bidi paragraph; leave w:jc unset (bidi default start = visual right),
    or set start explicitly. NEVER set alignment RIGHT on a bidi paragraph."""
    pPr = p._p.get_or_add_pPr()
    if pPr.find(qn('w:bidi')) is None:
        bidi = OxmlElement('w:bidi'); bidi.set(qn('w:val'), '1'); pPr.append(bidi)
    jc = pPr.find(qn('w:jc'))
    if jc is None:
        jc = _set(OxmlElement('w:jc'), pPr)
    jc.set(qn('w:val'), 'start')

def fa_run(p, text, font='Vazirmatn', size=11, bold=False):
    run = p.add_run(text)
    run.bold = bold
    rPr = run._r.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts')) or _set(OxmlElement('w:rFonts'), rPr)
    for attr in ('w:ascii', 'w:hAnsi', 'w:cs'):
        rFonts.set(qn(attr), font)
    _set(OxmlElement('w:rtl'), rPr)                       # complex-script run
    szCs = _set(OxmlElement('w:szCs'), rPr)               # CS size (else tiny/huge)
    szCs.set(qn('w:val'), str(int(size * 2)))
    run.font.size = Pt(size)
    if bold:
        _set(OxmlElement('w:bCs'), rPr)                    # CS bold
    return run

def rtl_table(table):
    tblPr = table._tbl.tblPr
    if tblPr.find(qn('w:bidiVisual')) is None:
        tblPr.append(OxmlElement('w:bidiVisual'))          # first col = visual right

def rtl_section(section):
    sectPr = section._sectPr
    if sectPr.find(qn('w:bidi')) is None:
        sectPr.append(OxmlElement('w:bidi'))

def keep_with_next(p):
    pPr = p._p.get_or_add_pPr()
    pPr.append(OxmlElement('w:keepNext'))
    pPr.append(OxmlElement('w:keepLines'))

def cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:cantSplit'))

def repeat_header(row):
    trPr = row._tr.get_or_add_trPr()
    tblHeader = OxmlElement('w:tblHeader'); tblHeader.set(qn('w:val'), 'true')
    trPr.append(tblHeader)
```

Notes that bite in python-docx specifically:
- `w:szCs` matters: without it, complex-script text ignores your size.
- `w:bCs` matters: bold Persian needs it, or only Latin runs embolden.
- The unsplittable-card trick is identical: 1×1 table + `cant_split(row)`.
- Same digits/symbols/verification rules as above — they're format rules,
  not library rules.

### 6.1 Three failures the per-paragraph helpers do NOT fix

Setting bidi on every paragraph you create still leaves three holes, because
Word/LibreOffice pull from `styles.xml` and `numbering.xml`, which python-docx
generates from a Latin default template. All three are verified failures, not
theory: without the fix below, a test document rendered `.1` (Latin digit,
wrong side) for list items, a blue Heading nobody asked for, and pulled DejaVu +
OpenSymbol into the PDF. With it: Persian «۱.», black heading, Vazirmatn only.

**Run this once, right after `Document()`, before adding content:**

```python
from docx.shared import Pt, RGBColor

def persianize_styles(doc, font='Vazirmatn', size=11):
    """Fix the document-wide defaults python-docx inherits from its Latin template.
    Without this: Latin list numbers, Word's blue headings, DejaVu fallback."""
    st = doc.styles['Normal']
    st.font.name = font
    st.font.size = Pt(size)
    rPr = st.element.get_or_add_rPr()
    rF = rPr.find(qn('w:rFonts'))
    if rF is None:
        rF = _set(OxmlElement('w:rFonts'), rPr)
    for a in ('w:ascii', 'w:hAnsi', 'w:cs'):
        rF.set(qn(a), font)                       # cs = the Persian-shaping slot
    _set(OxmlElement('w:rtl'), rPr)
    _set(OxmlElement('w:szCs'), rPr).set(qn('w:val'), str(int(size * 2)))
    _set(OxmlElement('w:bidi'), st.element.get_or_add_pPr())

    # Built-in Heading styles: Persian font, bidi, and NO inherited color.
    # Word's Heading 1-4 default to blue — an accent the user never asked for.
    for i in range(1, 5):
        try:
            h = doc.styles[f'Heading {i}']
        except KeyError:
            continue
        h.font.name = font
        h.font.color.rgb = RGBColor(0, 0, 0)      # neutral; see SKILL.md visual neutrality
        hr = h.element.get_or_add_rPr()
        hf = hr.find(qn('w:rFonts'))
        if hf is None:
            hf = _set(OxmlElement('w:rFonts'), hr)
        for a in ('w:ascii', 'w:hAnsi', 'w:cs'):
            hf.set(qn(a), font)
        _set(OxmlElement('w:rtl'), hr)
        _set(OxmlElement('w:bidi'), h.element.get_or_add_pPr())
```

**Numbered and bulleted lists: do NOT use the built-in list styles.**
`doc.add_paragraph(style='List Number')` writes numbering into `numbering.xml`,
which carries no bidi and renders Latin `1.` on the wrong side; the `List
Bullet` glyph comes from OpenSymbol and drags a fallback font into the PDF.
Number manually instead — the marker becomes a normal Persian run you control:

```python
FA_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
to_fa = lambda n: str(n).translate(str.maketrans("0123456789", FA_DIGITS))

for i, item in enumerate(items, 1):
    p = rtl_paragraph(doc.add_paragraph())
    fa_run(p, f"{to_fa(i)}.  ")     # ۱.  ۲.  ۳. — stays RTL, right side
    fa_run(p, item)

for item in bullets:
    p = rtl_paragraph(doc.add_paragraph())
    fa_run(p, "•  ")                # • verified in Vazirmatn; ▪ is NOT
    fa_run(p, item)
```
Indent with `p.paragraph_format.right_indent` (RTL side), not `left_indent`.

**Headers and footers are separate XML parts** (`header1.xml`, `footer1.xml`)
and inherit nothing from the body — apply `rtl_paragraph` + `fa_run` to each:

```python
for section in doc.sections:
    for part in (section.header, section.footer):
        for p in part.paragraphs:
            rtl_paragraph(p)
            # rebuild text through fa_run so the cs font/rtl flags exist
```
Page numbers in footers: a Latin field digit flips the line — prefer a Persian
literal, or accept Latin numerals in the footer only.

**Confirm the fix in the output, not the code:** `pdffonts out.pdf` must list
your Persian font and nothing else. A `DejaVu` or `OpenSymbol` row means a
glyph fell back — usually a list bullet or a symbol from §1.4.
the verify_pdf script (full package; chat-only AIs apply the equivalent rules manually) flags this automatically.



---

# PART 9 — PowerPoint

# Persian PowerPoint: RTL slides with python-pptx

PowerPoint has no document-level RTL switch — direction is set per paragraph
and per run, which is why half-fixed Persian decks are so common. Every text
frame needs the treatment below.

## Core helpers (python-pptx)

```python
from pptx.util import Pt
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree

def rtl_paragraph(paragraph, align=PP_ALIGN.RIGHT):
    """RTL direction + visual-right alignment for a pptx paragraph.
    In DrawingML (unlike OOXML/docx!) algn='r' is PHYSICAL right — safe to use."""
    paragraph.alignment = align
    pPr = paragraph._p.get_or_add_pPr()
    pPr.set('rtl', '1')

def fa_run(run, font='Vazirmatn', size=18, bold=False, color=None):
    run.font.name = font          # sets latin typeface
    run.font.size = Pt(size)
    run.font.bold = bold
    if color: run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    rPr.set('lang', 'fa-IR')
    cs = rPr.find(qn('a:cs'))
    if cs is None:
        cs = etree.SubElement(rPr, qn('a:cs'))
    cs.set('typeface', font)      # complex-script typeface — REQUIRED for Persian

def fa_text_frame(tf, font='Vazirmatn', size=18):
    """Apply to every paragraph+run in a text frame."""
    for p in tf.paragraphs:
        rtl_paragraph(p)
        for r in p.runs:
            fa_run(r, font=font, size=size)
```

Key facts:
- `a:cs` typeface is what actually renders Persian glyphs. Setting only
  `run.font.name` leaves Persian on the theme's default CS font.
- DrawingML `algn="r"` is physical right (the docx START/RIGHT trap does
  NOT apply to pptx). `rtl="1"` controls word order/bidi, `algn` controls
  which edge. Persian body/title: `rtl='1'` + `PP_ALIGN.RIGHT`.
  Centered titles: `rtl='1'` + `PP_ALIGN.CENTER` is fine.

## Layout mirroring

Persian slides mirror LTR conventions:
- Title right-aligned (or centered), content starts at the top-right.
- Two-column "image + text": image LEFT, text RIGHT (reader enters from right).
- Process/timeline arrows flow right→left; flip arrow glyphs (→ becomes ←).
- Agenda/bullet columns: rightmost column is "first".
- Logos: keep brand corner conventions, but nav-like elements mirror.

## Bullets and numbering

```python
# Persian-safe bullet char (theme bullets often lack Persian-font glyphs).
# • is verified in Vazirmatn/Lalezar; ▪ is NOT (falls back to DejaVu).
pPr = paragraph._p.get_or_add_pPr()
buFont = etree.SubElement(pPr, qn('a:buFont')); buFont.set('typeface', 'Vazirmatn')
buChar = etree.SubElement(pPr, qn('a:buChar')); buChar.set('char', '•')
```

Numbered lists: `buAutoNum` renders Latin digits only. For Persian numbering,
disable auto bullets (`a:buNone`) and prefix runs manually: «۱. »، «۲. » —
Persian digits keep the line RTL (same rule as docx).

## Tables

`a:tbl` has no bidiVisual equivalent that survives PowerPoint round-trips.
Build RTL tables by **reversing column order yourself** (first data column =
rightmost cell) and applying `rtl_paragraph`/`fa_run` to every cell. Header
row: bold + fill; keep rows short — pptx tables don't paginate.

## Fonts and delivery

- Use bundled Vazirmatn (+ Lalezar for title slides) — see fonts.md pairings.
- PowerPoint font embedding is flaky cross-platform (and python-pptx can't do
  it). If the deck travels beyond machines with the fonts installed, ALWAYS
  ship a PDF export alongside: install fonts (`bash the install_fonts script (full package; chat-only AIs apply the equivalent rules manually)),
  then `soffice --headless --convert-to pdf deck.pptx`, then
  `python3 the verify_pdf script (full package; chat-only AIs apply the equivalent rules manually) deck.pdf --expect-font Vazirmatn`.
- No letter-spacing on Persian, real bold weights only, line spacing ≥1.3
  (`paragraph.line_spacing = 1.3`).

## If building via the pptx skill's HTML pipeline (html2pptx)

Apply html-css.md rules in the source HTML: `<html dir="rtl" lang="fa">`,
Vazirmatn @font-face, `text-align: right`, Persian digits, no letter-spacing.
Then visually verify a rendered screenshot of at least the first 3 slides —
bidi bugs in HTML pipelines show up as scrambled punctuation at line edges.

## Checklist

1. Every paragraph: `rtl='1'`; every run: `a:cs` typeface set.
2. Persian digits in all visible numbers (slide numbers can stay Latin).
3. Layout mirrored (text right, flow right→left).
4. Bullets use verified glyphs (• · in Vazirmatn), numbering manual Persian.
5. Tables column-reversed.
6. PDF exported with fonts installed + verify_pdf.py clean.



---

# PART 10 — HTML / CSS / email

# Persian HTML/CSS: RTL web pages, emails, and HTML→PDF

## The foundation

```html
<!DOCTYPE html>
<html dir="rtl" lang="fa">
```

`dir="rtl"` on `<html>` flips the whole layout: text flows right→left, flex/grid
main axes reverse, tables mirror, list markers move right. Most "RTL bugs" come
from fighting this with hard-coded `left`/`right` afterwards.

## CSS rules

### Use logical properties, not physical

| Physical (breaks RTL) | Logical (RTL-safe) |
|---|---|
| `margin-left` | `margin-inline-start` |
| `padding-right` | `padding-inline-end` |
| `text-align: left` | `text-align: start` |
| `border-left` | `border-inline-start` |
| `left: 0` | `inset-inline-start: 0` |

`text-align: right` is acceptable at the page level for Persian (it equals
`start` under `dir=rtl`), but inside components prefer `start`/`end` so the
component survives reuse.

### Typography

```css
body {
  font-family: "Vazirmatn", "Segoe UI", Tahoma, sans-serif;
  font-size: 17px;          /* Persian reads small — go one step larger */
  line-height: 1.8;         /* 1.6 minimum; Persian clips below that */
  letter-spacing: 0;        /* NEVER track Persian — it breaks letter joins */
}
h1, h2, h3 { line-height: 1.5; font-weight: 700; }  /* real weights, no faux bold */
```

Display headings: `font-family: "Lalezar"` — one display face per page, max.

### Mixed-direction content (the hard part)

Latin fragments (brand names, URLs, code, phone numbers) inside Persian text
disrupt bidi ordering. Tools:

```html
<!-- isolate an LTR fragment so surrounding punctuation doesn't scramble -->
<p>افزونه <bdi>WooCommerce 9.5</bdi> را نصب کنید.</p>

<!-- force a whole block LTR (code, addresses, phone) -->
<pre dir="ltr">npm install docx</pre>
<span dir="ltr">+98 912 345 6789</span>
```

CSS equivalent: `unicode-bidi: isolate` (default for `<bdi>`).
Fix stray punctuation jumping to the wrong side with `&lrm;`/`&rlm;` marks —
but if you need many of them, wrap the fragment in `<bdi>` instead.

Numbers: use Persian digits ۰-۹ in prose (they inherit RTL correctly).
Keep inputs like phone/URL fields `dir="ltr"` with `text-align: start`.

### Layout mirroring

- Flex/grid auto-mirror under `dir=rtl` — write `flex-direction: row` and let
  the browser flip it. Don't write `row-reverse` to "fix" RTL; that double-flips.
- Icons with direction (arrows, chevrons, back buttons): mirror with
  `[dir="rtl"] .icon-arrow { transform: scaleX(-1); }`. Symmetric icons stay.
- Shadows/border-radius asymmetries: use logical values or mirror per-dir.
- Carousels/sliders: reverse advance direction; "next" points left in RTL.

### Lists and tables

```css
ul, ol { padding-inline-start: 1.5em; }   /* not padding-left */
```
Ordered lists: browsers render Latin digits by default; for Persian numbering
use `list-style: arabic-indic` (`list-style-type: persian` where supported) or
generate markers manually with Persian digits.

Tables under `dir=rtl` mirror automatically: first `<th>` renders rightmost. ✓

## Persian web fonts

See fonts.md for the catalog. Online: Google Fonts serves Vazirmatn and Lalezar:

```html
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@100..900&family=Lalezar&display=swap" rel="stylesheet">
```

Offline / HTML→PDF / email: embed local files from `assets/fonts/` via
`@font-face`. Never rely on system fonts for Persian — Windows falls back to
Segoe UI (passable), macOS to Geeza Pro (wrong flavor), Linux to DejaVu (broken).

## HTML email

Email clients strip `<style>` unpredictably:
- `dir="rtl"` attribute on every structural `<table>`, `<td>`, `<div>` — not CSS.
- Inline styles only: `style="font-family:Tahoma,Arial; text-align:right; direction:rtl"`.
- Web fonts don't load in most clients → Tahoma is the classic Persian-safe
  email font stack.
- Test: Gmail web strips `<head>` styles; Outlook desktop ignores web fonts.

## HTML→PDF (weasyprint / headless Chrome)

The pagination principles from docx-pdf.md, in CSS:

```css
@page { size: A4; margin: 2cm; }
h1, h2, h3, h4 { break-after: avoid; }        /* no orphan headings */
.card, .price-box, figure { break-inside: avoid; }  /* no split cards */
p { orphans: 2; widows: 2; }                   /* no lonely lines */
.divider-page { break-before: page; break-after: page; }
```

- weasyprint honors `break-*` well and embeds @font-face fonts — good default.
- Headless Chrome (`--print-to-pdf`) also works; ensure fonts are installed
  (`bash the install_fonts script (full package; chat-only AIs apply the equivalent rules manually)) or referenced via @font-face with absolute
  paths.
- Verify the output exactly like a docx-derived PDF:
  `python3 the verify_pdf script (full package; chat-only AIs apply the equivalent rules manually) out.pdf --expect-font Vazirmatn`.

## Pre-delivery checklist

1. `<html dir="rtl" lang="fa">` present.
2. No physical left/right properties that fight RTL (grep for `margin-left`,
   `text-align: left`, `padding-right` and justify each hit).
3. `letter-spacing` nowhere on Persian text.
4. Latin fragments wrapped in `<bdi>`/`dir="ltr"`.
5. Persian digits in prose; `persian_cleanup.py --edit` + `fa_lint.py --check`
   on the text content.
6. Fonts load (DevTools → Network, or pdffonts on the exported PDF).
7. If printed/PDF: break rules applied, then verify_pdf.py.



---

# PART 11 — Images, reportlab PDFs, Excel

# Persian patches for format-skill toolchains

The general docx/pptx/pdf/xlsx/canvas skills assume Latin text. Their default
toolpaths silently mangle Persian: disconnected letters, reversed order,
left-aligned sheets. This file patches each toolchain. (docx → docx-pdf.md,
pptx → pptx.md; this file covers the rest.)

## 1. Images & posters (canvas-design skill, PIL/Pillow)

Naive `draw.text(..., 'سلام دنیا')` renders Persian LEFT-to-right with
DISCONNECTED letters — instantly, obviously broken to any reader.

**Check raqm first** (complex-script shaping engine in Pillow):

```python
from PIL import features
assert features.check('raqm')   # True in most modern Pillow builds
```

**With raqm (the normal case)** — pass direction and language, anchor right:

```python
from PIL import Image, ImageDraw, ImageFont
font = ImageFont.truetype('assets/fonts/Vazirmatn-Bold.ttf', 48)
draw.text(
    (width - margin, y),          # x = RIGHT edge of the text block
    'سلام دنیا ۱۲۳',
    font=font, fill='#111',
    direction='rtl', language='fa',
    anchor='ra',                   # right-aligned, ascender baseline
)
```

- Multi-line: draw each line separately (or `multiline_text` with
  `direction='rtl'` + `align='right'`), line height ≥ 1.6 × font size —
  Persian clips in tight leading.
- Mixed Persian/Latin in one line: raqm handles bidi correctly — do NOT
  reverse strings manually.
- Never letter-space; use Lalezar for display headlines, Vazirmatn otherwise
  (fonts.md pairings apply to posters too).
- Persian digits ۰-۹ in all visible numbers.

**Without raqm** (older Pillow, no libraqm): shaping needs
`arabic_reshaper` + `python-bidi`:

```python
import arabic_reshaper
from bidi.algorithm import get_display
shaped = get_display(arabic_reshaper.reshape('سلام دنیا'))
draw.text((x, y), shaped, font=font)   # per line; bidi already applied
```

These packages may not be installable in sandboxed environments — if neither
raqm nor reshaper is available, render the text via HTML→screenshot instead
of PIL.

**Verify visually, always:** render, then look at the image (or ask a
subagent to). Broken shaping is invisible in code and screaming in pixels.

## 2. Creating PDFs (pdf skill, reportlab)

**reportlab has no bidi and no Arabic shaping.** `drawString('متن فارسی')`
produces reversed, disconnected glyphs. Do not fight it. Route Persian PDF
creation through a pipeline that shapes text natively:

1. **python-docx → LibreOffice** (sandbox-proven, default):
   build the document with the docx-pdf.md recipes, install fonts
   (the install_fonts script (full package; chat-only AIs apply the equivalent rules manually)), then
   `soffice --headless --convert-to pdf file.docx`.
2. **HTML → PDF** (weasyprint or headless Chrome, where available): write
   RTL HTML per html-css.md with `@page` rules, convert.
3. reportlab ONLY if the environment has `arabic_reshaper` + `python-bidi`
   AND the layout truly needs canvas-level control:

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display

pdfmetrics.registerFont(TTFont('Vazirmatn', 'assets/fonts/Vazirmatn-Regular.ttf'))
c.setFont('Vazirmatn', 14)
line = get_display(arabic_reshaper.reshape('متن فارسی ۱۲۳'))
c.drawRightString(page_width - margin, y, line)   # right-anchored per line
```

Manipulating EXISTING Persian PDFs (merge/split/rotate/extract via pypdf,
form-filling) is safe — those operations never touch text shaping.
Always finish with the verify_pdf script (full package; chat-only AIs apply the equivalent rules manually) out.pdf --expect-font Vazirmatn`.

## 3. Excel (xlsx skill, openpyxl / pandas)

Three invisible-until-opened problems: sheets open left-to-right, cells
left-align, fonts fall back.

```python
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

wb = Workbook(); ws = wb.active
ws.title = 'گزارش فروش'

ws.sheet_view.rightToLeft = True          # ← THE critical line, per sheet

fa_font   = Font(name='Vazirmatn', size=11)
fa_header = Font(name='Vazirmatn', size=11, bold=True)
fa_align  = Alignment(horizontal='right', vertical='center',
                      readingOrder=2)     # 2 = right-to-left reading order

for cell in row:
    cell.font = fa_font
    cell.alignment = fa_align
```

- Set `rightToLeft` on EVERY worksheet (it's a per-sheet property).
- **Numbers stay real numbers** (Latin digits in numeric cells) so formulas,
  sorting and charts keep working; Persian digits belong in text/label cells.
  Give currency cells a format like `#,##0 "تومان"`.
- Headers, sheet names, chart titles: Persian, Vazirmatn, bold.
- pandas: `df.to_excel(...)` first, then reopen with openpyxl to apply
  rightToLeft + fonts + alignment (pandas can't set them).
- Column order: with rightToLeft the first column (A) displays rightmost —
  which is where Persian readers expect the first column. Write data in
  logical order and let the view mirror it.

## 4. Quick router

| Deliverable | Toolpath | Reference |
|---|---|---|
| Word/report/proposal | docx-js or python-docx → soffice PDF | docx-pdf.md |
| Slides | python-pptx (or html2pptx via RTL HTML) | pptx.md |
| Web page / email | RTL HTML/CSS | html-css.md |
| New PDF | docx or HTML pipeline, NOT raw reportlab | this file §2 |
| Poster/social image | PIL + raqm (direction='rtl') | this file §1 |
| Spreadsheet | openpyxl + rightToLeft + Vazirmatn | this file §3 |
