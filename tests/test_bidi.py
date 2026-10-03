import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from scripts.persian_cleanup import RLM, edit_persian, first_strong, fix_bidi
from scripts import fa_lint


class TestBidi(unittest.TestCase):
    """Issue #4: Persian lines that start with a Latin word render left-to-right."""

    def test_latin_led_persian_lines_get_rlm(self):
        for line in ("React یک کتابخانه‌ی جاوااسکریپت است.",
                     "- Docker برای اجرای سرویس لازم است.",
                     "## API چیست؟",
                     "> Python زبان محبوبی است.",
                     "1. Git را نصب کنید."):
            out = fix_bidi(line)
            self.assertIn(RLM, out, line)
            body = out.split(RLM, 1)[1]
            self.assertEqual(first_strong(RLM + body), "R")
            self.assertEqual(out.replace(RLM, ""), line, "text itself must not change")

    def test_markdown_marker_stays_first(self):
        self.assertEqual(fix_bidi("- Docker لازم است."), "- " + RLM + "Docker لازم است.")
        self.assertEqual(fix_bidi("## API چیست؟"), "## " + RLM + "API چیست؟")

    def test_left_alone(self):
        for line in ("کتابخانه‌ی React را نصب کنید.",   # already Persian-led
                     "This is an English line.",          # English
                     "۲۰۲۶ سال خوبی بود.",                # digits are neutral
                     ""):
            self.assertEqual(fix_bidi(line), line)

    def test_code_fence_untouched(self):
        text = "```bash\nnpm install برای نصب\n```"
        self.assertEqual(fix_bidi(text), text)

    def test_table_cells(self):
        row = "| Git | Git برای کنترل نسخه است |"
        out = fix_bidi(row)
        self.assertEqual(out, "| Git | " + RLM + "Git برای کنترل نسخه است |")

    def test_idempotent(self):
        text = "React یک کتابخانه است.\n- Docker لازم است."
        once = fix_bidi(text)
        self.assertEqual(fix_bidi(once), once)

    def test_not_in_default_edit(self):
        """Invisible marks are opt-in: --edit alone must never insert them."""
        self.assertNotIn(RLM, edit_persian("React یک کتابخانه است."))

    def test_linter_reports_and_clears(self):
        fa_lint.ISSUES.clear()
        fa_lint.check_remaining("React یک کتابخانه‌ی جاوااسکریپت است.")
        self.assertTrue(any(i[0] == "bidi-start" for i in fa_lint.ISSUES))
        fa_lint.ISSUES.clear()
        fa_lint.check_remaining(fix_bidi("React یک کتابخانه‌ی جاوااسکریپت است."))
        self.assertFalse(any(i[0] == "bidi-start" for i in fa_lint.ISSUES))


if __name__ == "__main__":
    unittest.main()
