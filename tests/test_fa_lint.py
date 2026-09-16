import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.fa_lint import (
    ISSUES,
    ZWNJ,
    check_remaining,
    find_hekasre,
    fix_safe,
    rhythm_report,
)
from scripts.persian_cleanup import protect_regions, restore_regions


class TestFaLint(unittest.TestCase):
    def setUp(self):
        ISSUES.clear()

    def test_hekasre_ane(self):
        """Adverbs and adjectives ending in '-انه' must not trigger false positive hekasre."""
        self.assertEqual(find_hekasre("فرآیندی همکارانه از خود نشان داد"), [])
        self.assertEqual(find_hekasre("رفتاری دوستانه با ما داشت"), [])
        self.assertEqual(find_hekasre("قضاوتی عادلانه در دادگاه بود"), [])
        self.assertEqual(find_hekasre("دیدگاهی محترمانه به موضوع"), [])
        # True hekasre errors must still be detected
        res = find_hekasre("کتابه من کجاست")
        self.assertTrue(len(res) > 0)
        self.assertEqual(res[0][1], "کتابِ من")

    def test_en_dash_range(self):
        """En-dashes inside numerical/page/date ranges (e.g. ۱۲۰–۱۴۵) must not be flagged as editorial dashes."""
        check_remaining("صفحات ۱۲۰–۱۴۵ را بخوانید.")
        dash_issues = [i for i in ISSUES if i[0] == "dash"]
        self.assertEqual(len(dash_issues), 0, "Numerical range en-dash must not be flagged.")

        # En-dash or em-dash as sentence clause separator MUST be flagged
        ISSUES.clear()
        check_remaining("این موضوع – که بسیار مهم است – بررسی شد.")
        dash_issues = [i for i in ISSUES if i[0] == "dash"]
        self.assertGreaterEqual(len(dash_issues), 1, "Parenthetical sentence dash must be flagged.")

    def test_rhythm_technical_text(self):
        """Technical documentation containing code blocks and inline commands must not trigger 'no-long-sentence'."""
        tech_text = (
            "راهنمای نصب سرویس در لینوکس.\n"
            "ابتدا مخزن را کلون کنید.\n"
            "سپس محیط مجازی بسازید.\n"
            "دستور زیر را اجرا کنید:\n"
            "```bash\npip install mypackage\n```\n"
            "پورت `8080` را بررسی کنید.\n"
            "فایل `config.yaml` را باز نمایید.\n"
            "سرویس را راهاندازی کنید.\n"
            "وضعیت پادها را با `kubectl get pods` بررسی کنید.\n"
        )
        report = rhythm_report(tech_text)
        no_long = [item for item in report if item[0] == "no-long-sentence"]
        self.assertEqual(len(no_long), 0, "Technical text should not be penalized for short concise sentences.")

    def test_fa_lint_tar_behavior(self):
        """Linter must flag un-joined coordinated comparatives, while ignoring coordinated 'تر و Y' idioms."""
        # 1. Coordinated comparatives without ZWNJ must be reported
        ISSUES.clear()
        check_remaining("سخت تر و پیچیده تر شده")
        self.assertTrue(any(i[0] == "zwnj-tar" for i in ISSUES))

        # 2. Coordinated comparatives with ZWNJ must not be reported
        ISSUES.clear()
        check_remaining("سخت" + ZWNJ + "تر و پیچیده" + ZWNJ + "تر شده")
        self.assertFalse(any(i[0] == "zwnj-tar" for i in ISSUES))

        # 3. Non-comparative idioms must not be reported
        ISSUES.clear()
        check_remaining("یه سایت تر و تمیز")
        self.assertFalse(any(i[0] == "zwnj-tar" for i in ISSUES))

        ISSUES.clear()
        check_remaining("سبزی تر و تازه")
        self.assertFalse(any(i[0] == "zwnj-tar" for i in ISSUES))

    def test_protect_regions_in_lint(self):
        """Protected tables, code blocks, and URLs must not trigger spurious warnings in fa_lint."""
        sample_table = '| `app.server.host` | String | "0.0.0.0" | آدرس واسط |\n| `app.server.port` | Integer | 8080 | پورت وب |'
        masked, _ = protect_regions(sample_table)
        check_remaining(masked)
        table_issues = [i for i in ISSUES if i[0] in ("quotes", "latin-digits")]
        self.assertEqual(len(table_issues), 0, "Protected table cells must not trigger quotes or latin-digits warnings.")

        code_sample = "```bash\n# نصب وابستگی های پروژه\npip install -r req.txt\n```"
        masked, tokens = protect_regions(code_sample)
        fixed = fix_safe(masked)
        restored = restore_regions(fixed, tokens)
        self.assertEqual(restored, code_sample, "Comments inside code blocks must remain completely untouched.")


if __name__ == "__main__":
    unittest.main()
