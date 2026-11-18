import os
import sys
import tempfile
import unittest
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    import docx
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
except ImportError:  # pragma: no cover
    docx = None

from scripts.latex_to_omml import (
    M_NS,
    add_display_math,
    add_inline_math,
    convert_docx_latex,
    format_persian_eq_number,
    latex_to_omml,
)
from scripts.persian_cleanup import edit_persian
from scripts.verify_docx import check, check_integrity


class TestLatexToOmml(unittest.TestCase):
    def _parse(self, xml_str: str) -> ET.Element:
        minidom.parseString(xml_str.encode("utf-8"))
        return ET.fromstring(xml_str)

    def test_quadratic_formula_fraction_and_sqrt(self):
        xml = latex_to_omml(r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}")
        root = self._parse(xml)
        self.assertEqual(root.tag, f"{{{M_NS}}}oMath")
        self.assertIsNotNone(root.find(f".//{{{M_NS}}}f"))
        self.assertIsNotNone(root.find(f".//{{{M_NS}}}rad"))
        self.assertIsNotNone(root.find(f".//{{{M_NS}}}sSup"))
        texts = "".join(t.text or "" for t in root.findall(f".//{{{M_NS}}}t"))
        self.assertIn("±", texts)
        self.assertIn("4ac", texts)

    def test_nth_root_and_binomial(self):
        xml = latex_to_omml(r"\sqrt[3]{x_i^2} + \binom{n}{k}")
        root = self._parse(xml)
        deg = root.find(f".//{{{M_NS}}}rad/{{{M_NS}}}deg")
        self.assertIsNotNone(deg)
        self.assertIn("3", "".join(t.text or "" for t in deg.findall(f".//{{{M_NS}}}t")))
        self.assertIsNotNone(root.find(f".//{{{M_NS}}}sSubSup"))
        nobar = root.find(f".//{{{M_NS}}}f/{{{M_NS}}}fPr/{{{M_NS}}}type")
        self.assertIsNotNone(nobar)
        self.assertEqual(nobar.get(f"{{{M_NS}}}val"), "noBar")

    def test_nary_sum_integral_and_limits(self):
        xml = latex_to_omml(
            r"\lim_{n \to \infty} \sum_{i=1}^{n} \frac{1}{i^2} = \int_0^\infty f(x)\,dx",
            display=True,
        )
        root = self._parse(xml)
        self.assertEqual(root.tag, f"{{{M_NS}}}oMathPara")
        self.assertIsNotNone(root.find(f".//{{{M_NS}}}limLow"))
        naries = root.findall(f".//{{{M_NS}}}nary")
        self.assertEqual(len(naries), 2)

    def test_matrices_cases_and_aligned(self):
        for expr in (
            r"A = \begin{pmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{pmatrix}",
            r"|x| = \begin{cases} x & x \geq 0 \\ -x & x < 0 \end{cases}",
            r"\begin{aligned} y &= ax + b \\ z &= cx + d \end{aligned}",
        ):
            root = self._parse(latex_to_omml(expr, display=True))
            self.assertEqual(root.tag, f"{{{M_NS}}}oMathPara")

    def test_accents_fonts_and_persian_text_in_math(self):
        xml = latex_to_omml(r"\hat{\beta}_1 \in \mathbb{R}, \quad \text{خطای استاندارد} = \bar{x}")
        root = self._parse(xml)
        self.assertIsNotNone(root.find(f".//{{{M_NS}}}acc"))
        self.assertIsNotNone(root.find(f".//{{{M_NS}}}bar"))
        texts = "".join(t.text or "" for t in root.findall(f".//{{{M_NS}}}t"))
        self.assertIn("ℝ", texts)
        self.assertIn("خطای استاندارد", texts)

    def test_persian_eq_number_formatting(self):
        self.assertEqual(format_persian_eq_number(1), "(۱)")
        self.assertEqual(format_persian_eq_number("2-14"), "(۲-۱۴)")
        self.assertEqual(format_persian_eq_number("(۳)"), "(۳)")

    def test_cleanup_protects_latex_math_but_converts_prose(self):
        src = (
            "در سال 1403 برای 25 نمونه، رابطه‌ی $\\bar{x} = \\frac{1}{25} \\sum_{i=1}^{25} x_i$ "
            "در سطح $p < 0.05$ بررسی می شود.\n\n"
            "$$\n\\sigma^2 = \\frac{1}{n - 1} \\sum_{i=1}^{n} (x_i - \\bar{x})^2\n$$"
        )
        out = edit_persian(src)
        self.assertIn("۱۴۰۳", out)
        self.assertIn("۲۵ نمونه", out)
        self.assertIn("می‌شود", out)
        # LaTeX math must stay exact ASCII so TeX commands/digits are never corrupted
        self.assertIn(r"$\bar{x} = \frac{1}{25} \sum_{i=1}^{25} x_i$", out)
        self.assertIn("$p < 0.05$", out)
        self.assertIn(r"\frac{1}{n - 1}", out)

    def test_cleanup_does_not_treat_currency_as_math(self):
        src = "قیمت سرویس از $100 به $200 می رسد."
        out = edit_persian(src)
        # Prose between $100 and $200 must STILL receive ZWNJ editing!
        self.assertIn("می‌رسد", out)

    @unittest.skipIf(docx is None, "python-docx not installed")
    def test_python_docx_helpers_pass_verify_docx(self):
        doc = docx.Document()
        st = doc.styles["Normal"]
        st.font.name = "Vazirmatn"
        rPr = st.element.get_or_add_rPr()
        rF = OxmlElement("w:rFonts")
        for attr in ("w:ascii", "w:hAnsi", "w:cs"):
            rF.set(qn(attr), "Vazirmatn")
        rPr.append(rF)
        rPr.append(OxmlElement("w:rtl"))
        szCs = OxmlElement("w:szCs")
        szCs.set(qn("w:val"), "22")
        rPr.append(szCs)
        st.element.get_or_add_pPr().append(OxmlElement("w:bidi"))
        doc.sections[0]._sectPr.insert(0, OxmlElement("w:bidi"))

        # Inline equation inside RTL Persian paragraph
        p = doc.add_paragraph()
        p._p.get_or_add_pPr().append(OxmlElement("w:bidi"))
        r1 = p.add_run("ضریب همبستگی برابر با ")
        r1._r.get_or_add_rPr().append(OxmlElement("w:rtl"))
        add_inline_math(p, r"r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2}}")
        r2 = p.add_run(" به دست آمد.")
        r2._r.get_or_add_rPr().append(OxmlElement("w:rtl"))

        # Unnumbered display equation + numbered display equation
        add_display_math(doc, r"E = mc^2")
        add_display_math(doc, r"\hat{y}_i = \beta_0 + \sum_{j=1}^{p} \beta_j x_{ij}", number="۲-۱")

        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "math_doc.docx")
            doc.save(path)
            ierr, _ = check_integrity(path)
            self.assertEqual(ierr, [])
            errors, warnings, notes = check(path, expect_fonts=["Vazirmatn"])
            self.assertEqual(errors, [], f"Unexpected errors: {errors}")
            self.assertEqual(warnings, [], f"Unexpected warnings: {warnings}")
            self.assertTrue(any("math zones (<m:oMath>): 3" in n for n in notes), f"Notes: {notes}")

    @unittest.skipIf(docx is None, "python-docx not installed")
    def test_convert_docx_latex_postprocessor(self):
        doc = docx.Document()
        st = doc.styles["Normal"]
        rPr = st.element.get_or_add_rPr()
        rF = OxmlElement("w:rFonts")
        rF.set(qn("w:cs"), "Vazirmatn")
        rPr.append(rF)
        rPr.append(OxmlElement("w:rtl"))
        rPr.append(OxmlElement("w:szCs"))
        st.element.get_or_add_pPr().append(OxmlElement("w:bidi"))
        doc.sections[0]._sectPr.insert(0, OxmlElement("w:bidi"))

        p1 = doc.add_paragraph()
        p1._p.get_or_add_pPr().append(OxmlElement("w:bidi"))
        p1.add_run("مقدار احتمال $p < 0.05$ و انرژی $E = mc^2$ است.")

        p2 = doc.add_paragraph()
        p2._p.get_or_add_pPr().append(OxmlElement("w:bidi"))
        p2.add_run(r"$$\int_0^\infty e^{-x^2}\,dx = \frac{\sqrt{\pi}}{2} \tag{1-2}$$")

        with tempfile.TemporaryDirectory() as tmpdir:
            raw_path = os.path.join(tmpdir, "raw.docx")
            out_path = os.path.join(tmpdir, "converted.docx")
            doc.save(raw_path)

            count = convert_docx_latex(raw_path, out_path)
            self.assertEqual(count, 3)

            ierr, _ = check_integrity(out_path)
            self.assertEqual(ierr, [], f"Integrity errors after --docx conversion: {ierr}")
            errors, warnings, notes = check(out_path, expect_fonts=["Vazirmatn"])
            self.assertEqual(errors, [], f"RTL errors: {errors}")
            self.assertEqual(warnings, [], f"RTL warnings: {warnings}")
            self.assertTrue(any("math zones (<m:oMath>): 3" in n for n in notes))

    def test_multiple_text_groups_preserve_spaces(self):
        xml = latex_to_omml(r"f(x) = \begin{cases} 1 & \text{if } x > 0 \\ 0 & \text{if } x \le 0 \end{cases}")
        root = self._parse(xml)
        t_vals = [t.text for t in root.findall(f".//{{{M_NS}}}t") if t.text]
        self.assertEqual(t_vals.count("if "), 2, f"Expected trailing spaces preserved in both \\text groups: {t_vals}")


if __name__ == "__main__":
    unittest.main()
