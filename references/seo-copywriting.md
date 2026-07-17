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
