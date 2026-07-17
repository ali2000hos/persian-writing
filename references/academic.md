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
> • کاهش زمان پردازش
> • کاهش هزینه
> • مقیاس‌پذیری بهتر
>
> ✅ این روش سه مزیت عملی داشت: زمان پردازش هر درخواست از ۸ ثانیه به ۲ ثانیه
> رسید، هزینه‌ی زیرساخت حدود ۳۰٪ کاهش یافت و معماری جدید بدون بازنویسی تا
> ده برابر بارِ فعلی را تحمل می‌کند.

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

## 10. Checklist before delivering academic text

1. Register: no می‌باشد/لازم به ذکر است; hedges single; تعارف zero.
2. No اولاً/ثانیاً skeletons; no bullet lists where prose belongs.
3. پیشینه synthesizes; every number claim has a number; no invented sources.
4. Terminology: one Persian term per concept + Latin on first use.
5. Statistics/formulas in LTR runs; Persian digits in prose.
6. Structure matches genre (conventional sections for papers/theses).
7. Run `scripts/persian_cleanup.py --edit` then `scripts/fa_lint.py --check`
   on the text; fix everything contextual (dashes, میشود forms).
8. If producing docx/PDF: all rules in docx-pdf.md apply (RTL, keepNext
   captions, footnote bidi, fonts installed before conversion).
