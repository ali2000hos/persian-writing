import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.persian_cleanup import (
    ZWNJ,
    edit_persian,
    fix_arabic_chars,
    fix_ezafe,
    fix_persian_punctuation,
    fix_zwnj_compound_verbs,
    fix_zwnj_suffixes,
    remove_extra_spaces,
)


class TestPersianCleanup(unittest.TestCase):
    def test_ezafe_no_double_heh(self):
        """Converting ezafe marker 'ی' after silent heh must not duplicate the letter heh."""
        inp = "خانه" + ZWNJ + "ی من و نامه" + ZWNJ + "ی شما و جلوه" + ZWNJ + "ی ویژه"
        expected = "خانهٔ من و نامهٔ شما و جلوهٔ ویژه"
        out = fix_ezafe(inp)
        self.assertEqual(out, expected)
        # Verify single heh followed by combining hamza U+0654
        first_word = out.split()[0]
        self.assertEqual(
            [c for c in first_word],
            ["خ", "ا", "ن", "ه", "\u0654"],
            "Ezafe must attach combining hamza U+0654 to single heh, not duplicate it.",
        )
        # Non-heh words must not be affected
        self.assertEqual(fix_ezafe("دست" + ZWNJ + "یابی"), "دست" + ZWNJ + "یابی")
        # Idempotency
        self.assertEqual(fix_ezafe(expected), expected)

    def test_thousands_separator(self):
        """Commas between digits must convert to Persian thousands separator (٬ U+066C), not clause comma (،)."""
        sample = "مبلغ 4,750,000,000 ریال و 10,000 تومان"
        out = edit_persian(sample)
        self.assertIn("۴٬۷۵۰٬۰۰۰٬۰۰۰", out)
        self.assertIn("۱۰٬۰۰۰", out)
        # Grammatical comma outside digits must convert to Persian comma (،)
        sample_comma = "سلام, دنیا"
        out_comma = edit_persian(sample_comma)
        self.assertIn("سلام، دنیا", out_comma)

    def test_compound_prefixes(self):
        """Prepositions 'بی', 'در', 'بر' must not be merged with subsequent verbs."""
        self.assertEqual(fix_zwnj_compound_verbs("بی داشتن سرپناه"), "بی داشتن سرپناه")
        self.assertEqual(fix_zwnj_compound_verbs("در گفتن حقیقت"), "در گفتن حقیقت")
        self.assertEqual(fix_zwnj_compound_verbs("بر داشتن این کتاب"), "بر داشتن این کتاب")
        self.assertEqual(fix_zwnj_compound_verbs("در دید و بازدید"), "در دید و بازدید")
        # Legitimate preverbs ('فرا', 'باز', 'وا', 'فرورد') must still join correctly
        self.assertEqual(fix_zwnj_compound_verbs("فرا گرفتن"), "فراگرفتن")
        self.assertEqual(fix_zwnj_compound_verbs("باز گشتن"), "بازگشتن")

    def test_user_version_regression(self):
        """Standalone decimals in Persian prose must convert to Persian digits; named software and v-versions stay Latin."""
        # Decimal in prose -> converted to Persian digits
        self.assertEqual(edit_persian("قیمت 2.5 میلیون تومان است."), "قیمت ۲.۵ میلیون تومان است.")
        self.assertEqual(edit_persian("رشد 42.8 درصدی"), "رشد ۴۲.۸ درصدی")
        self.assertEqual(edit_persian("ضریب 3.5 برابری"), "ضریب ۳.۵ برابری")
        # Named software versions and v-prefixed versions -> preserved as Latin
        self.assertIn("Python 3.11.4", edit_persian("نسخه Python 3.11.4 منتشر شد."))
        self.assertIn("Ubuntu 22.04", edit_persian("سیستم عامل Ubuntu 22.04 LTS"))
        self.assertIn("CUDA 12.2", edit_persian("پلتفرم CUDA 12.2"))
        self.assertIn("v1.28.2", edit_persian("نسخه v1.28.2"))
        self.assertIn("Bluetooth 5.2", edit_persian("بلوتوث Bluetooth 5.2"))

    def test_signature_alignment(self):
        """Wide columnar spacing (5+ spaces) for signature lines must be preserved, while accidental 2-4 spaces collapse."""
        sample_signature = "امضای کارفرما:                                          امضای پیمانکار:"
        out_sig = edit_persian(sample_signature)
        self.assertEqual(out_sig, sample_signature, "Wide signature column spacing must be preserved.")

        sample_spaces = "این  یک   متن    با فاصله است."
        out_spaces = edit_persian(sample_spaces)
        self.assertEqual(out_spaces, "این یک متن با فاصله است.")

    def test_arabic_chars(self):
        """Hamza on alef (أ) and waw (ؤ) must be preserved in standard Persian orthography."""
        words = "مؤلف و سؤال و مؤسسه و تأکید و تأثیر و تأمین و تأیید و تأخیر و رأی"
        self.assertEqual(fix_arabic_chars(words), words)
        # Arabic yeh, kaf, ta marbuta, and alef-with-hamza-below must convert
        self.assertEqual(fix_arabic_chars("كتاب علي و إسلام و دورة"), "کتاب علی و اسلام و دوره")

    def test_protect_regions_coverage(self):
        """URLs, emails, phone numbers, IBANs, DOIs, hardware models, and variables must be protected."""
        sample = (
            "برای اطلاعات بیشتر به https://example.com/api/v2/user/102?lang=fa&page=2 مراجعه کنید.\n"
            "ایمیل: support24@service.ir و تلفن: +971-4-3901122 و شبا: IR820170000000201847520003\n"
            "نسخه جدید Python 3.11 و Docker 24.0.5 و تراشه H100 و B200 منتشر شد.\n"
            "مقاله: (Habermas, 1984: 86) و doi:10.1177/0196859919888902\n"
            "فرمول: Y = β0 + β1(X1)"
        )
        out = edit_persian(sample)
        self.assertIn("https://example.com/api/v2/user/102?lang=fa&page=2", out)
        self.assertIn("support24@service.ir", out)
        self.assertIn("+971-4-3901122", out)
        self.assertIn("IR820170000000201847520003", out)
        self.assertIn("Python 3.11", out)
        self.assertIn("Docker 24.0.5", out)
        self.assertIn("H100", out)
        self.assertIn("B200", out)
        self.assertIn("(Habermas, 1984: 86)", out)
        self.assertIn("doi:10.1177/0196859919888902", out)
        self.assertIn("β0", out)
        self.assertIn("X1", out)


class TestRefinedTarRule(unittest.TestCase):
    def test_coordinated_comparatives_cleanup(self):
        """Coordinated comparatives 'X تر و Y تر' must attach ZWNJ to both words."""
        self.assertEqual(
            fix_zwnj_suffixes("سخت تر و پیچیده تر شده"),
            "سخت" + ZWNJ + "تر و پیچیده" + ZWNJ + "تر شده",
        )
        self.assertEqual(
            fix_zwnj_suffixes("قوی تر و شجاع تر از همه"),
            "قوی" + ZWNJ + "تر و شجاع" + ZWNJ + "تر از همه",
        )
        self.assertEqual(
            fix_zwnj_suffixes("بزرگ تر و بهتر شد"),
            "بزرگ" + ZWNJ + "تر و بهتر شد",
        )
        self.assertEqual(
            fix_zwnj_suffixes("ساده تر و آسان تر بود"),
            "ساده" + ZWNJ + "تر و آسان" + ZWNJ + "تر بود",
        )
        # Already attached coordinated comparatives must stay attached
        attached = "سخت" + ZWNJ + "تر و پیچیده" + ZWNJ + "تر شده"
        self.assertEqual(fix_zwnj_suffixes(attached), attached)

    def test_non_comparative_idioms_cleanup(self):
        """17 real-world coordinated 'تر و Y' compounds must stay detached as independent 'تَر'."""
        compounds = [
            "تر و تمیز",
            "تر و تازه",
            "تر و فرز",
            "تر و خشک",
            "تر و خالی",
            "تر و چابک",
            "تر و کثیف",
            "تر و مرتب",
            "تر و شاداب",
            "تر و ترد",
            "تر و باریک",
            "تر و برشته",
            "تر و نرم",
            "تر و براق",
            "تر و شیرین",
            "تر و خنک",
            "تر و مرطوب",
        ]
        nouns = [
            "سایت",
            "سبزی",
            "بچه",
            "زمین",
            "کوزه",
            "آدم",
            "لباس",
            "اتاق",
            "گل",
            "شیرینی",
            "خیار",
            "نان",
            "پوست",
            "موی",
            "سیب",
            "نسیم",
            "هوا",
        ]
        for noun, comp in zip(nouns, compounds):
            orig = f"یک {noun} {comp}"
            # Must stay detached
            self.assertEqual(
                fix_zwnj_suffixes(orig),
                orig,
                f"Idiom {orig!r} must stay detached.",
            )
            # Mistakenly attached 'Xتر و Y' must be un-joined back to 'X تر و Y'
            mistaken = f"یک {noun}{ZWNJ}{comp}"
            self.assertEqual(
                fix_zwnj_suffixes(mistaken),
                orig,
                f"Mistaken attachment {mistaken!r} must be un-joined to {orig!r}.",
            )


if __name__ == "__main__":
    unittest.main()
