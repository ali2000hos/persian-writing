#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
latex_to_omml.py — convert LaTeX math into native Word OMML (<m:oMath>).

Zero external dependencies (Python 3.8+ standard library only).

Why this exists
---------------
Writing raw ``$x^2 + y^2 = z^2$`` into a Word paragraph leaves literal dollar
signs in the document, and writing Unicode math ``x² + y² = z²`` into an RTL
Persian paragraph lets the bidi algorithm reverse operators and parentheses
(``z² = y² + x²``). Word's own editable equation format is Office Math Markup
Language (OMML: ``<m:oMath>`` inline, ``<m:oMathPara>`` for display blocks).

This module provides:
  1. ``latex_to_omml(latex, display=False)`` — LaTeX string → OMML XML string.
  2. ``add_inline_math(paragraph, latex)`` — append ``<m:oMath>`` to a
     ``python-docx`` paragraph while keeping surrounding Persian runs RTL.
  3. ``add_display_math(doc, latex, number=None, ...)`` — add a centered LTR
     display equation, or a 3-column borderless ``cantSplit`` RTL table when a
     Persian equation number such as ``"۱"`` or ``"۲-۱"`` is supplied.
  4. ``convert_docx_latex(in_path, out_path=None)`` — stdlib-only post-pass on
     any ``.docx`` (from ``docx-js``, templates, or ``python-docx``) that
     replaces ``$$...$$`` and ``$...$`` placeholders with native OMML equations.

CLI usage
---------
  python3 scripts/latex_to_omml.py "\\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}"
  python3 scripts/latex_to_omml.py --display "\\sum_{i=1}^{n} x_i"
  python3 scripts/latex_to_omml.py --docx draft.docx --out final.docx
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import sys
import xml.etree.ElementTree as ET
import zipfile
from typing import Dict, List, Optional, Sequence, Tuple, Union
from xml.sax.saxutils import escape as _xml_escape

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
M_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"

ET.register_namespace("w", W_NS)
ET.register_namespace("m", M_NS)

_FA_DIGITS = "۰۱۲۳۴۵۶۷۸۹"
_EN_TO_FA = str.maketrans("0123456789", _FA_DIGITS)
_PERSIAN_CHAR_RE = re.compile(r"[\u0600-\u06ff]")

# ---------------------------------------------------------------------------
# LaTeX symbol tables
# ---------------------------------------------------------------------------

GREEK_SYMBOLS: Dict[str, str] = {
    "alpha": "α", "beta": "β", "gamma": "γ", "delta": "δ",
    "epsilon": "ϵ", "varepsilon": "ε", "zeta": "ζ", "eta": "η",
    "theta": "θ", "vartheta": "ϑ", "iota": "ι", "kappa": "κ",
    "varkappa": "ϰ", "lambda": "λ", "mu": "μ", "nu": "ν",
    "xi": "ξ", "pi": "π", "varpi": "ϖ", "rho": "ρ",
    "varrho": "ϱ", "sigma": "σ", "varsigma": "ς", "tau": "τ",
    "upsilon": "υ", "phi": "ϕ", "varphi": "φ", "chi": "χ",
    "psi": "ψ", "omega": "ω",
    "Gamma": "Γ", "Delta": "Δ", "Theta": "Θ", "Lambda": "Λ",
    "Xi": "Ξ", "Pi": "Π", "Sigma": "Σ", "Upsilon": "ϒ",
    "Phi": "Φ", "Psi": "Ψ", "Omega": "Ω",
}

MATH_SYMBOLS: Dict[str, str] = {
    # Binary operators
    "pm": "±", "mp": "∓", "times": "×", "div": "÷", "cdot": "⋅",
    "ast": "∗", "star": "⋆", "circ": "∘", "bullet": "∙",
    "oplus": "⊕", "ominus": "⊖", "otimes": "⊗", "oslash": "⊘",
    "odot": "⊙", "dagger": "†", "ddagger": "‡", "amalg": "⨿",
    "cap": "∩", "cup": "∪", "uplus": "⊎", "sqcap": "⊓", "sqcup": "⊔",
    "vee": "∨", "lor": "∨", "wedge": "∧", "land": "∧",
    "setminus": "∖", "wr": "≀",
    # Relations
    "leq": "≤", "le": "≤", "geq": "≥", "ge": "≥",
    "neq": "≠", "ne": "≠", "approx": "≈", "equiv": "≡",
    "sim": "∼", "simeq": "≃", "asymp": "≍", "cong": "≅",
    "propto": "∝", "ll": "≪", "gg": "≫",
    "prec": "≺", "succ": "≻", "preceq": "⪯", "succeq": "⪰",
    "subset": "⊂", "supset": "⊃", "subseteq": "⊆", "supseteq": "⊇",
    "sqsubseteq": "⊑", "sqsupseteq": "⊒",
    "in": "∈", "notin": "∉", "ni": "∋", "owns": "∋",
    "vdash": "⊢", "dashv": "⊣", "models": "⊨", "perp": "⊥",
    "parallel": "∥", "mid": "∣", "nmid": "∤",
    # Arrows
    "to": "→", "rightarrow": "→", "gets": "←", "leftarrow": "←",
    "leftrightarrow": "↔", "Rightarrow": "⇒", "Leftarrow": "⇐",
    "Leftrightarrow": "⇔", "iff": "⇔", "implies": "⟹", "impliedby": "⟸",
    "mapsto": "↦", "longmapsto": "⟼",
    "longrightarrow": "⟶", "longleftarrow": "⟵", "longleftrightarrow": "⟷",
    "uparrow": "↑", "downarrow": "↓", "updownarrow": "↕",
    "Uparrow": "⇑", "Downarrow": "⇓", "Updownarrow": "⇕",
    "nearrow": "↗", "searrow": "↘", "swarrow": "↙", "nwarrow": "↖",
    "rightharpoonup": "⇀", "rightharpoondown": "⇁",
    "leftharpoonup": "↼", "leftharpoondown": "↽",
    "rightleftharpoons": "⇌",
    # Miscellaneous symbols
    "infty": "∞", "partial": "∂", "nabla": "∇",
    "forall": "∀", "exists": "∃", "nexists": "∄",
    "emptyset": "∅", "varnothing": "∅",
    "neg": "¬", "lnot": "¬",
    "aleph": "ℵ", "hbar": "ℏ", "ell": "ℓ", "wp": "℘",
    "Re": "ℜ", "Im": "ℑ",
    "prime": "′", "angle": "∠", "triangle": "△", "Box": "□", "square": "□",
    "diamond": "⋄", "Diamond": "◇", "degree": "°",
    "dots": "…", "ldots": "…", "cdots": "⋯", "vdots": "⋮", "ddots": "⋱",
    "colon": ":", "backslash": "\\",
    # Delimiter names (when used standalone or with \left / \right)
    "langle": "⟨", "rangle": "⟩",
    "lceil": "⌈", "rceil": "⌉",
    "lfloor": "⌊", "rfloor": "⌋",
    "vert": "|", "Vert": "‖", "|": "‖",
}

ESCAPED_LITERALS: Dict[str, str] = {
    "{": "{", "}": "}", "%": "%", "&": "&",
    "_": "_", "#": "#", "$": "$",
}

SPACING_COMMANDS: Dict[str, str] = {
    ",": "\u2009",   # thin space
    ":": "\u2005",   # medium math space
    ";": "\u2004",   # thick math space
    " ": " ",
    "quad": "\u2003",
    "qquad": "\u2003\u2003",
    "!": "",         # negative thin space (no-op in OMML)
}

# N-ary operators: command -> (glyph, default limLoc in display mode)
NARY_OPERATORS: Dict[str, Tuple[str, str]] = {
    "sum": ("∑", "undOvr"),
    "prod": ("∏", "undOvr"),
    "coprod": ("∐", "undOvr"),
    "bigcap": ("⋂", "undOvr"),
    "bigcup": ("⋃", "undOvr"),
    "bigsqcup": ("⨆", "undOvr"),
    "bigvee": ("⋁", "undOvr"),
    "bigwedge": ("⋀", "undOvr"),
    "bigoplus": ("⨁", "undOvr"),
    "bigotimes": ("⨂", "undOvr"),
    "bigodot": ("⨀", "undOvr"),
    "biguplus": ("⨄", "undOvr"),
    "int": ("∫", "subSup"),
    "iint": ("∬", "subSup"),
    "iiint": ("∭", "subSup"),
    "oint": ("∮", "subSup"),
}

# Upright function names; ones in LIMIT_FUNCTIONS place subscripts underneath in display mode
LIMIT_FUNCTIONS = {"lim", "limsup", "liminf", "max", "min", "sup", "inf", "argmax", "argmin"}
UPRIGHT_FUNCTIONS = LIMIT_FUNCTIONS | {
    "sin", "cos", "tan", "cot", "sec", "csc",
    "arcsin", "arccos", "arctan",
    "sinh", "cosh", "tanh", "coth",
    "log", "ln", "lg", "exp",
    "det", "dim", "ker", "hom", "arg", "deg", "gcd", "Pr", "cov", "var", "tr", "rank",
    "mod", "bmod", "pmod",
}

FUNCTION_LABELS: Dict[str, str] = {
    "limsup": "lim sup",
    "liminf": "lim inf",
    "argmax": "arg max",
    "argmin": "arg min",
}

# Combining accents for <m:acc>
ACCENTS: Dict[str, str] = {
    "hat": "\u0302", "widehat": "\u0302",
    "check": "\u030c",
    "tilde": "\u0303", "widetilde": "\u0303",
    "acute": "\u0301",
    "grave": "\u0300",
    "dot": "\u0307",
    "ddot": "\u0308",
    "dddot": "\u20db",
    "breve": "\u0306",
    "vec": "\u20d7", "overrightarrow": "\u20d7",
    "mathring": "\u030a",
}

BLACKBOARD_BOLD: Dict[str, str] = {
    "A": "𝔸", "B": "𝔹", "C": "ℂ", "D": "𝔻", "E": "𝔼", "F": "𝔽", "G": "𝔾",
    "H": "ℍ", "I": "𝕀", "J": "𝕁", "K": "𝕂", "L": "𝕃", "M": "𝕄", "N": "ℕ",
    "O": "𝕆", "P": "ℙ", "Q": "ℚ", "R": "ℝ", "S": "𝕊", "T": "𝕋", "U": "𝕌",
    "V": "𝕍", "W": "𝕎", "X": "𝕏", "Y": "𝕐", "Z": "ℤ", "1": "𝟙",
}

CALLIGRAPHIC: Dict[str, str] = {
    "A": "𝒜", "B": "ℬ", "C": "𝒞", "D": "𝒟", "E": "ℰ", "F": "ℱ", "G": "𝒢",
    "H": "ℋ", "I": "ℐ", "J": "𝒥", "K": "𝒦", "L": "ℒ", "M": "ℳ", "N": "𝒩",
    "O": "𝒪", "P": "𝒫", "Q": "𝒬", "R": "ℛ", "S": "𝒮", "T": "𝒯", "U": "𝒰",
    "V": "𝒱", "W": "𝒲", "X": "𝒳", "Y": "𝒴", "Z": "𝒵",
}

MATRIX_DELIMS: Dict[str, Tuple[str, str]] = {
    "matrix": ("", ""),
    "pmatrix": ("(", ")"),
    "bmatrix": ("[", "]"),
    "Bmatrix": ("{", "}"),
    "vmatrix": ("|", "|"),
    "Vmatrix": ("‖", "‖"),
    "smallmatrix": ("", ""),
}

BIG_SIZING_CMDS = {
    "big", "Big", "bigg", "Bigg",
    "bigl", "Bigl", "biggl", "Biggl",
    "bigr", "Bigr", "biggr", "Biggr",
    "bigm", "Bigm", "biggm", "Biggm",
}

STYLE_SWITCH_CMDS = {
    "displaystyle", "textstyle", "scriptstyle", "scriptscriptstyle",
    "limits", "nolimits", "noindent",
}


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

RAW_TEXT_ARG_CMDS = {
    "text", "textrm", "textup", "textnormal", "mbox", "hbox",
    "mathrm", "mathbf", "textbf", "boldsymbol", "bm", "mathit", "textit",
    "mathbb", "mathcal", "operatorname", "begin", "end",
    "hspace", "vspace", "phantom", "hphantom", "vphantom", "label", "tag",
}


class Token:
    __slots__ = ("kind", "val")

    def __init__(self, kind: str, val: str):
        self.kind = kind  # 'CMD', 'TEXT_GROUP', 'LBRACE', 'RBRACE', 'LBRACK', 'RBRACK', 'SUP', 'SUB', 'AMP', 'NEWLINE', 'CHAR'
        self.val = val

    def __repr__(self) -> str:  # pragma: no cover
        return f"Token({self.kind!r}, {self.val!r})"


def tokenize(latex: str) -> List[Token]:
    tokens: List[Token] = []
    i = 0
    n = len(latex)
    while i < n:
        ch = latex[i]
        if ch in " \t\r\n":
            i += 1
            continue
        if ch == "%":
            # LaTeX comment to end of line
            while i < n and latex[i] != "\n":
                i += 1
            continue
        if ch == "\\":
            if i + 1 >= n:
                i += 1
                continue
            nxt = latex[i + 1]
            if nxt == "\\":
                tokens.append(Token("NEWLINE", "\\\\"))
                i += 2
                # Optional row-spacing spec like \\[4pt]
                while i < n and latex[i] in " \t":
                    i += 1
                if i < n and latex[i] == "[":
                    end_br = latex.find("]", i + 1)
                    if end_br != -1:
                        i = end_br + 1
                continue
            if nxt.isalpha():
                j = i + 1
                while j < n and latex[j].isalpha():
                    j += 1
                cmd = latex[i + 1:j]
                if j < n and latex[j] == "*" and cmd in ("operatorname", "tag"):
                    j += 1
                cmd_clean = cmd.rstrip("*")
                tokens.append(Token("CMD", cmd_clean))
                i = j
                # Preserve exact whitespace inside {...} for text-taking commands
                if cmd_clean in RAW_TEXT_ARG_CMDS:
                    k = i
                    while k < n and latex[k] in " \t\r\n":
                        k += 1
                    if k < n and latex[k] == "{":
                        depth = 1
                        m_idx = k + 1
                        buf: List[str] = []
                        while m_idx < n and depth > 0:
                            c = latex[m_idx]
                            if c == "\\" and m_idx + 1 < n and latex[m_idx + 1] in "{}":
                                buf.append(latex[m_idx + 1])
                                m_idx += 2
                                continue
                            if c == "{":
                                depth += 1
                                buf.append(c)
                            elif c == "}":
                                depth -= 1
                                if depth > 0:
                                    buf.append(c)
                            else:
                                buf.append(c)
                            m_idx += 1
                        tokens.append(Token("TEXT_GROUP", "".join(buf)))
                        i = m_idx
                continue
            # Single-character command: \, \; \{ \} \| \% \  etc.
            tokens.append(Token("CMD", nxt))
            i += 2
            continue
        if ch == "{":
            tokens.append(Token("LBRACE", ch))
        elif ch == "}":
            tokens.append(Token("RBRACE", ch))
        elif ch == "[":
            tokens.append(Token("LBRACK", ch))
        elif ch == "]":
            tokens.append(Token("RBRACK", ch))
        elif ch == "^":
            tokens.append(Token("SUP", ch))
        elif ch == "_":
            tokens.append(Token("SUB", ch))
        elif ch == "&":
            tokens.append(Token("AMP", ch))
        elif ch == "'":
            # Collapse consecutive primes '' -> ″, ''' -> ‴
            j = i
            while j < n and latex[j] == "'":
                j += 1
            count = j - i
            prime_str = {1: "′", 2: "″", 3: "‴"}.get(count, "′" * count)
            tokens.append(Token("CHAR", prime_str))
            i = j
            continue
        else:
            tokens.append(Token("CHAR", ch))
        i += 1
    return tokens


# ---------------------------------------------------------------------------
# OMML XML builders (string-based for deterministic namespace output)
# ---------------------------------------------------------------------------

def _m_run(text: str, style: Optional[str] = None, normal_text: bool = False,
           persian_font: str = "Vazirmatn") -> str:
    """Build a single <m:r> element.

    Explicitly sets Cambria Math (ascii/hAnsi only, never w:cs) and w:rtl=0 on
    math runs so that a Persian Normal style (Vazirmatn + <w:rtl/>) does not
    bleed into equations, while keeping w:cs clean for verify_docx.py.
    """
    if not text:
        return ""
    m_rpr_parts: List[str] = []
    if normal_text:
        m_rpr_parts.append("<m:nor/>")
    if style:
        m_rpr_parts.append(f'<m:sty m:val="{style}"/>')
    m_rpr = f"<m:rPr>{''.join(m_rpr_parts)}</m:rPr>" if m_rpr_parts else ""

    if normal_text and _PERSIAN_CHAR_RE.search(text):
        w_rpr = (
            f'<w:rPr>'
            f'<w:rFonts w:ascii="{_xml_escape(persian_font)}" '
            f'w:hAnsi="{_xml_escape(persian_font)}" '
            f'w:cs="{_xml_escape(persian_font)}"/>'
            f'<w:rtl/>'
            f'</w:rPr>'
        )
    else:
        w_rpr = (
            '<w:rPr>'
            '<w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/>'
            '<w:rtl w:val="0"/>'
            '</w:rPr>'
        )

    space_attr = ' xml:space="preserve"' if (text[:1] == " " or text[-1:] == " " or "  " in text) else ""
    return f"<m:r>{m_rpr}{w_rpr}<m:t{space_attr}>{_xml_escape(text)}</m:t></m:r>"


def _ensure_nonempty(inner_xml: str) -> str:
    return inner_xml if inner_xml else _m_run("\u200b")


def _m_frac(num_xml: str, den_xml: str, bar: bool = True) -> str:
    fpr = "" if bar else '<m:fPr><m:type m:val="noBar"/></m:fPr>'
    return f"<m:f>{fpr}<m:num>{num_xml}</m:num><m:den>{den_xml}</m:den></m:f>"


def _m_rad(radicand_xml: str, degree_xml: Optional[str] = None) -> str:
    if degree_xml is None:
        return (
            '<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr>'
            f"<m:deg/><m:e>{radicand_xml}</m:e></m:rad>"
        )
    return (
        '<m:rad><m:radPr><m:degHide m:val="0"/></m:radPr>'
        f"<m:deg>{degree_xml}</m:deg><m:e>{radicand_xml}</m:e></m:rad>"
    )


def _m_delim(inner_xml: str, beg: str = "(", end: str = ")", sep: str = "") -> str:
    sep_el = f'<m:sepChr m:val="{_xml_escape(sep)}"/>' if sep else ""
    return (
        f'<m:d><m:dPr>'
        f'<m:begChr m:val="{_xml_escape(beg)}"/>'
        f'{sep_el}'
        f'<m:endChr m:val="{_xml_escape(end)}"/>'
        f'</m:dPr><m:e>{inner_xml}</m:e></m:d>'
    )


def _m_scripts(base_xml: str, sub_xml: Optional[str], sup_xml: Optional[str]) -> str:
    if sub_xml is not None and sup_xml is not None:
        return f"<m:sSubSup><m:e>{base_xml}</m:e><m:sub>{sub_xml}</m:sub><m:sup>{sup_xml}</m:sup></m:sSubSup>"
    if sub_xml is not None:
        return f"<m:sSub><m:e>{base_xml}</m:e><m:sub>{sub_xml}</m:sub></m:sSub>"
    if sup_xml is not None:
        return f"<m:sSup><m:e>{base_xml}</m:e><m:sup>{sup_xml}</m:sup></m:sSup>"
    return base_xml


def _m_nary(glyph: str, lim_loc: str, sub_xml: Optional[str], sup_xml: Optional[str], body_xml: str) -> str:
    sub_hide = "0" if sub_xml is not None else "1"
    sup_hide = "0" if sup_xml is not None else "1"
    return (
        f"<m:nary><m:naryPr>"
        f'<m:chr m:val="{_xml_escape(glyph)}"/>'
        f'<m:limLoc m:val="{lim_loc}"/>'
        f'<m:subHide m:val="{sub_hide}"/>'
        f'<m:supHide m:val="{sup_hide}"/>'
        f"</m:naryPr>"
        f"<m:sub>{sub_xml or ''}</m:sub>"
        f"<m:sup>{sup_xml or ''}</m:sup>"
        f"<m:e>{_ensure_nonempty(body_xml)}</m:e>"
        f"</m:nary>"
    )


def _m_acc(chr_val: str, base_xml: str) -> str:
    return (
        f'<m:acc><m:accPr><m:chr m:val="{_xml_escape(chr_val)}"/></m:accPr>'
        f"<m:e>{base_xml}</m:e></m:acc>"
    )


def _m_bar(pos: str, base_xml: str) -> str:
    return (
        f'<m:bar><m:barPr><m:pos m:val="{pos}"/></m:barPr>'
        f"<m:e>{base_xml}</m:e></m:bar>"
    )


def _m_matrix(rows: Sequence[Sequence[str]]) -> str:
    row_els = []
    for row in rows:
        cells = "".join(f"<m:e>{cell}</m:e>" for cell in row)
        row_els.append(f"<m:mr>{cells}</m:mr>")
    return f"<m:m>{''.join(row_els)}</m:m>"


# ---------------------------------------------------------------------------
# Recursive-descent parser
# ---------------------------------------------------------------------------

class _Parser:
    def __init__(self, raw: str, tokens: List[Token], display: bool = False,
                 persian_font: str = "Vazirmatn"):
        self.raw = raw
        self.tokens = tokens
        self.pos = 0
        self.display = display
        self.persian_font = persian_font

    def peek(self, offset: int = 0) -> Optional[Token]:
        idx = self.pos + offset
        return self.tokens[idx] if 0 <= idx < len(self.tokens) else None

    def next(self) -> Optional[Token]:
        tok = self.peek()
        if tok is not None:
            self.pos += 1
        return tok

    def parse_expression(self, stop_kinds: Tuple[str, ...] = (),
                         stop_cmds: Tuple[str, ...] = ()) -> str:
        """Parse a sequence of atoms/operators until a stop token or infix \\over."""
        left_parts: List[str] = []
        over_seen = False
        right_parts: List[str] = []

        while self.pos < len(self.tokens):
            tok = self.peek()
            if tok is None:
                break
            if tok.kind in stop_kinds:
                break
            if tok.kind == "CMD" and tok.val in stop_cmds:
                break
            if tok.kind == "CMD" and tok.val == "over":
                self.next()
                over_seen = True
                continue
            item = self.parse_scripted_atom(stop_kinds=stop_kinds, stop_cmds=stop_cmds)
            if over_seen:
                right_parts.append(item)
            else:
                left_parts.append(item)

        if over_seen:
            return _m_frac("".join(left_parts), "".join(right_parts), bar=True)
        return "".join(left_parts)

    def _read_SubSup(self) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """Read optional \\limits/\\nolimits, _sub, and ^sup in any order."""
        lim_override: Optional[str] = None
        sub_xml: Optional[str] = None
        sup_xml: Optional[str] = None

        while self.pos < len(self.tokens):
            tok = self.peek()
            if tok is None:
                break
            if tok.kind == "CMD" and tok.val in ("limits", "nolimits"):
                self.next()
                lim_override = "undOvr" if tok.val == "limits" else "subSup"
                continue
            if tok.kind == "SUB" and sub_xml is None:
                self.next()
                sub_xml = self.parse_group_or_atom()
                continue
            if tok.kind == "SUP" and sup_xml is None:
                self.next()
                sup_xml = self.parse_group_or_atom()
                continue
            break
        return sub_xml, sup_xml, lim_override

    def parse_scripted_atom(self, stop_kinds: Tuple[str, ...] = (),
                            stop_cmds: Tuple[str, ...] = ()) -> str:
        tok = self.peek()
        if tok is None:
            return ""

        # N-ary operators (\sum, \int, \prod, ...) consume their scripts AND summand
        if tok.kind == "CMD" and tok.val in NARY_OPERATORS:
            self.next()
            glyph, default_loc = NARY_OPERATORS[tok.val]
            sub_xml, sup_xml, lim_override = self._read_SubSup()
            if lim_override:
                lim_loc = lim_override
            elif not self.display and default_loc == "undOvr":
                lim_loc = "subSup"
            else:
                lim_loc = default_loc
            # Summand: read atoms up to the next additive/relational separator or stop
            body_parts: List[str] = []
            while self.pos < len(self.tokens):
                nxt = self.peek()
                if nxt is None or nxt.kind in stop_kinds or nxt.kind in ("AMP", "NEWLINE", "RBRACE"):
                    break
                if nxt.kind == "CMD" and nxt.val in stop_cmds:
                    break
                if body_parts and self._is_nary_boundary(nxt):
                    break
                body_parts.append(self.parse_scripted_atom(stop_kinds=stop_kinds, stop_cmds=stop_cmds))
            return _m_nary(glyph, lim_loc, sub_xml, sup_xml, "".join(body_parts))

        # Limit-like functions (\lim_{x \to 0}, \max_{i}, ...)
        if tok.kind == "CMD" and tok.val in LIMIT_FUNCTIONS:
            self.next()
            label = FUNCTION_LABELS.get(tok.val, tok.val)
            fn_xml = _m_run(label, style="p", persian_font=self.persian_font)
            sub_xml, sup_xml, lim_override = self._read_SubSup()
            use_under = (lim_override == "undOvr") or (lim_override is None and self.display)
            if sub_xml is not None and sup_xml is None and use_under:
                return f"<m:limLow><m:e>{fn_xml}</m:e><m:lim>{sub_xml}</m:lim></m:limLow>"
            return _m_scripts(fn_xml, sub_xml, sup_xml)

        # Overbrace / underbrace take ^{label} or _{label} as upper/lower limits
        if tok.kind == "CMD" and tok.val in ("overbrace", "underbrace"):
            cmd = tok.val
            self.next()
            inner = self.parse_group_or_atom()
            brace_chr = "⏞" if cmd == "overbrace" else "⏟"
            pos_val = "top" if cmd == "overbrace" else "bot"
            grp = (
                f'<m:groupChr><m:groupChrPr>'
                f'<m:chr m:val="{brace_chr}"/><m:pos m:val="{pos_val}"/>'
                f'</m:groupChrPr><m:e>{inner}</m:e></m:groupChr>'
            )
            sub_xml, sup_xml, _ = self._read_SubSup()
            if cmd == "overbrace" and sup_xml is not None:
                return f"<m:limUpp><m:e>{grp}</m:e><m:lim>{sup_xml}</m:lim></m:limUpp>"
            if cmd == "underbrace" and sub_xml is not None:
                return f"<m:limLow><m:e>{grp}</m:e><m:lim>{sub_xml}</m:lim></m:limLow>"
            return _m_scripts(grp, sub_xml, sup_xml)

        base = self.parse_atom()
        sub_xml, sup_xml, _ = self._read_SubSup()
        if sub_xml is not None or sup_xml is not None:
            return _m_scripts(_ensure_nonempty(base), sub_xml, sup_xml)
        return base

    @staticmethod
    def _is_nary_boundary(tok: Token) -> bool:
        """Stop an N-ary summand before top-level +, -, =, or relational operators."""
        if tok.kind == "CHAR" and tok.val in "+-=<>":
            return True
        if tok.kind == "CMD" and tok.val in (
            "pm", "mp", "leq", "le", "geq", "ge", "neq", "ne", "approx",
            "equiv", "sim", "simeq", "cong", "propto", "to", "rightarrow",
            "Rightarrow", "Leftrightarrow", "iff", "implies", "in", "notin",
            "subset", "subseteq", "supset", "supseteq",
        ):
            return True
        return False

    def parse_group_or_atom(self) -> str:
        tok = self.peek()
        if tok is None:
            return ""
        if tok.kind == "LBRACE":
            self.next()
            inner = self.parse_expression(stop_kinds=("RBRACE",))
            if self.peek() and self.peek().kind == "RBRACE":
                self.next()
            return inner
        return self.parse_atom()

    def _read_plain_text_group(self) -> str:
        """Extract text inside {...} preserving spaces (via TEXT_GROUP token)."""
        tok = self.peek()
        if tok is None:
            return ""
        if tok.kind == "TEXT_GROUP":
            return self.next().val
        if tok.kind != "LBRACE":
            t = self.next()
            return t.val if t else ""
        self.next()
        parts: List[str] = []
        depth = 1
        while self.pos < len(self.tokens) and depth > 0:
            t = self.next()
            if t is None:
                break
            if t.kind == "LBRACE":
                depth += 1
                parts.append("{")
            elif t.kind == "RBRACE":
                depth -= 1
                if depth > 0:
                    parts.append("}")
            elif t.kind == "CMD":
                if t.val in ESCAPED_LITERALS:
                    parts.append(ESCAPED_LITERALS[t.val])
                elif t.val in SPACING_COMMANDS:
                    parts.append(SPACING_COMMANDS[t.val] or " ")
                elif t.val in GREEK_SYMBOLS:
                    parts.append(GREEK_SYMBOLS[t.val])
                elif t.val in MATH_SYMBOLS:
                    parts.append(MATH_SYMBOLS[t.val])
                else:
                    parts.append(t.val)
            else:
                parts.append(t.val)
        return "".join(parts)

    def _read_optional_bracket(self) -> Optional[str]:
        if self.peek() and self.peek().kind == "LBRACK":
            self.next()
            inner = self.parse_expression(stop_kinds=("RBRACK",))
            if self.peek() and self.peek().kind == "RBRACK":
                self.next()
            return inner
        return None

    def _read_delimiter_char(self) -> str:
        tok = self.next()
        if tok is None:
            return ""
        if tok.kind in ("CHAR", "LBRACK", "RBRACK"):
            return "" if tok.val == "." else tok.val
        if tok.kind == "CMD":
            if tok.val in ("{", "lbrace"):
                return "{"
            if tok.val in ("}", "rbrace"):
                return "}"
            if tok.val in MATH_SYMBOLS:
                return MATH_SYMBOLS[tok.val]
            if tok.val == ".":
                return ""
            return tok.val
        return tok.val

    def parse_atom(self) -> str:
        tok = self.peek()
        if tok is None:
            return ""

        if tok.kind == "LBRACE":
            return self.parse_group_or_atom()

        if tok.kind in ("CHAR", "LBRACK", "RBRACK"):
            self.next()
            # Merge adjacent plain characters/digits into a single <m:r>
            buf = [tok.val]
            while self.peek() and self.peek().kind == "CHAR":
                # Do not merge if the next char has its own subscript/superscript!
                nxt_after = self.peek(1)
                if nxt_after and nxt_after.kind in ("SUB", "SUP"):
                    break
                buf.append(self.next().val)
            return _m_run("".join(buf), persian_font=self.persian_font)

        if tok.kind in ("AMP", "NEWLINE", "RBRACE"):
            self.next()
            return ""

        if tok.kind in ("SUB", "SUP"):
            # Orphan script with no base (e.g. {}^{14}\text{C})
            return _m_run("\u200b", persian_font=self.persian_font)

        # tok.kind == "CMD"
        self.next()
        cmd = tok.val

        if cmd in STYLE_SWITCH_CMDS:
            return ""

        if cmd in BIG_SIZING_CMDS:
            d = self._read_delimiter_char()
            return _m_run(d, persian_font=self.persian_font) if d else ""

        if cmd in ESCAPED_LITERALS:
            return _m_run(ESCAPED_LITERALS[cmd], persian_font=self.persian_font)

        if cmd in SPACING_COMMANDS:
            sp = SPACING_COMMANDS[cmd]
            return _m_run(sp, normal_text=True, persian_font=self.persian_font) if sp else ""

        if cmd in GREEK_SYMBOLS:
            return _m_run(GREEK_SYMBOLS[cmd], persian_font=self.persian_font)

        if cmd in MATH_SYMBOLS:
            return _m_run(MATH_SYMBOLS[cmd], persian_font=self.persian_font)

        if cmd in UPRIGHT_FUNCTIONS:
            label = FUNCTION_LABELS.get(cmd, cmd)
            return _m_run(label, style="p", persian_font=self.persian_font)

        if cmd == "operatorname":
            name = self._read_plain_text_group()
            return _m_run(name, style="p", persian_font=self.persian_font)

        if cmd in ("frac", "dfrac", "tfrac", "cfrac"):
            num = self.parse_group_or_atom()
            den = self.parse_group_or_atom()
            return _m_frac(num, den, bar=True)

        if cmd in ("binom", "dbinom", "tbinom"):
            num = self.parse_group_or_atom()
            den = self.parse_group_or_atom()
            return _m_delim(_m_frac(num, den, bar=False), "(", ")")

        if cmd == "sqrt":
            deg = self._read_optional_bracket()
            rad = self.parse_group_or_atom()
            return _m_rad(rad, deg)

        if cmd == "left":
            beg = self._read_delimiter_char()
            inner = self.parse_expression(stop_cmds=("right",))
            end = ""
            if self.peek() and self.peek().kind == "CMD" and self.peek().val == "right":
                self.next()
                end = self._read_delimiter_char()
            return _m_delim(inner, beg, end)

        if cmd in ACCENTS:
            base = self.parse_group_or_atom()
            return _m_acc(ACCENTS[cmd], base)

        if cmd in ("bar", "overline"):
            base = self.parse_group_or_atom()
            return _m_bar("top", base)

        if cmd == "underline":
            base = self.parse_group_or_atom()
            return _m_bar("bot", base)

        if cmd in ("text", "textrm", "textup", "textnormal", "mbox", "hbox"):
            txt = self._read_plain_text_group()
            return _m_run(txt, normal_text=True, persian_font=self.persian_font)

        if cmd == "mathrm":
            txt = self._read_plain_text_group()
            return _m_run(txt, style="p", persian_font=self.persian_font)

        if cmd in ("mathbf", "textbf"):
            txt = self._read_plain_text_group()
            return _m_run(txt, style="b", persian_font=self.persian_font)

        if cmd in ("boldsymbol", "bm"):
            txt = self._read_plain_text_group()
            return _m_run(txt, style="bi", persian_font=self.persian_font)

        if cmd in ("mathit", "textit"):
            txt = self._read_plain_text_group()
            return _m_run(txt, style="i", persian_font=self.persian_font)

        if cmd == "mathbb":
            txt = self._read_plain_text_group()
            mapped = "".join(BLACKBOARD_BOLD.get(c, c) for c in txt)
            return _m_run(mapped, persian_font=self.persian_font)

        if cmd == "mathcal":
            txt = self._read_plain_text_group()
            mapped = "".join(CALLIGRAPHIC.get(c, c) for c in txt)
            return _m_run(mapped, persian_font=self.persian_font)

        if cmd == "begin":
            env = self._read_plain_text_group().strip()
            return self._parse_environment(env)

        if cmd in ("not",):
            nxt = self.peek()
            if nxt and nxt.kind == "CHAR" and nxt.val == "=":
                self.next()
                return _m_run("≠", persian_font=self.persian_font)
            if nxt and nxt.kind == "CMD" and nxt.val == "in":
                self.next()
                return _m_run("∉", persian_font=self.persian_font)
            inner = self.parse_group_or_atom()
            return inner

        if cmd in ("hspace", "vspace", "phantom", "hphantom", "vphantom", "label", "tag"):
            _ = self._read_plain_text_group()
            return ""

        # Unknown command: if followed immediately by {...}, format its argument;
        # otherwise render the command name upright so the document never crashes.
        if self.peek() and self.peek().kind == "LBRACE":
            return self.parse_group_or_atom()
        return _m_run(cmd, style="p", persian_font=self.persian_font)

    def _parse_environment(self, env: str) -> str:
        env_clean = env.rstrip("*")
        # Optional column alignment argument e.g. \begin{array}{cc}
        if env_clean == "array" and self.peek() and self.peek().kind == "LBRACE":
            _ = self._read_plain_text_group()

        rows: List[List[str]] = []
        current_row: List[str] = []

        while self.pos < len(self.tokens):
            tok = self.peek()
            if tok is None:
                break
            if tok.kind == "CMD" and tok.val == "end":
                self.next()
                end_env = self._read_plain_text_group().strip()
                if end_env == env or end_env.rstrip("*") == env_clean:
                    break
            cell_xml = self.parse_expression(
                stop_kinds=("AMP", "NEWLINE"),
                stop_cmds=("end",),
            )
            current_row.append(cell_xml)
            sep = self.peek()
            if sep and sep.kind == "AMP":
                self.next()
                continue
            if sep and sep.kind == "NEWLINE":
                self.next()
                rows.append(current_row)
                current_row = []
                continue
            if sep and sep.kind == "CMD" and sep.val == "end":
                continue

        if current_row and any(c for c in current_row):
            rows.append(current_row)
        if not rows:
            rows = [[""]]

        # Normalize rectangular column count for matrices / cases
        max_cols = max(len(r) for r in rows)
        norm_rows = [r + [""] * (max_cols - len(r)) for r in rows]

        if env_clean in MATRIX_DELIMS or env_clean == "array":
            beg, end = MATRIX_DELIMS.get(env_clean, ("", ""))
            mat_xml = _m_matrix(norm_rows)
            return _m_delim(mat_xml, beg, end) if (beg or end) else mat_xml

        if env_clean == "cases":
            return _m_delim(_m_matrix(norm_rows), "{", "")

        if env_clean in ("aligned", "align", "gather", "split", "eqnarray", "multline"):
            lines = ["".join(r) for r in rows]
            eq_items = "".join(f"<m:e>{_ensure_nonempty(ln)}</m:e>" for ln in lines)
            return f"<m:eqArr>{eq_items}</m:eqArr>"

        # Fallback: join rows
        return "".join("".join(r) for r in rows)


# ---------------------------------------------------------------------------
# Public conversion API
# ---------------------------------------------------------------------------

def _strip_math_delimiters(latex: str) -> str:
    s = latex.strip()
    if s.startswith("$$") and s.endswith("$$") and len(s) >= 4:
        return s[2:-2].strip()
    if s.startswith(r"\[") and s.endswith(r"\]") and len(s) >= 4:
        return s[2:-2].strip()
    if s.startswith(r"\(") and s.endswith(r"\)") and len(s) >= 4:
        return s[2:-2].strip()
    if s.startswith("$") and s.endswith("$") and len(s) >= 2:
        return s[1:-1].strip()
    return s


def latex_to_omml(latex: str, display: bool = False,
                  include_ns: bool = True,
                  persian_font: str = "Vazirmatn") -> str:
    """Convert a LaTeX math expression into an OOXML ``<m:oMath>`` or ``<m:oMathPara>`` string.

    Args:
        latex: LaTeX formula (with or without ``$...$`` / ``$$...$$`` delimiters).
        display: If True, wraps in ``<m:oMathPara>`` (centered display equation).
        include_ns: Declare ``xmlns:m`` and ``xmlns:w`` on the root element so
            the string can be parsed standalone by ``docx.oxml.parse_xml`` or
            ``xml.etree.ElementTree.fromstring``.
        persian_font: Complex-script font used only if ``\\text{...}`` contains Persian.
    """
    clean_latex = _strip_math_delimiters(latex)
    tokens = tokenize(clean_latex)
    parser = _Parser(clean_latex, tokens, display=display, persian_font=persian_font)
    inner_xml = parser.parse_expression()
    if not inner_xml:
        inner_xml = _m_run("\u200b", persian_font=persian_font)

    ns = f' xmlns:m="{M_NS}" xmlns:w="{W_NS}"' if include_ns else ""
    if display:
        return (
            f"<m:oMathPara{ns}>"
            f'<m:oMathParaPr><m:jc m:val="center"/></m:oMathParaPr>'
            f"<m:oMath>{inner_xml}</m:oMath>"
            f"</m:oMathPara>"
        )
    return f"<m:oMath{ns}>{inner_xml}</m:oMath>"


_TAG_RE = re.compile(r"\\tag\*?\s*\{([^{}]*)\}")


def _extract_tag(latex: str) -> Tuple[str, Optional[str]]:
    """Strip ``\\tag{...}`` from a LaTeX expression and return ``(cleaned_latex, tag_value)``."""
    m = _TAG_RE.search(latex)
    if not m:
        return latex, None
    cleaned = (latex[:m.start()] + latex[m.end():]).strip()
    return cleaned, m.group(1).strip()


def format_persian_eq_number(number: Union[str, int]) -> str:
    """Format an equation label with Persian digits inside parentheses: ``1`` -> ``(۱)``."""
    s = str(number).strip().translate(_EN_TO_FA)
    if not (s.startswith("(") and s.endswith(")")):
        s = f"({s})"
    return s


def _build_numbered_eq_table_xml(latex: str, number: Union[str, int],
                                 font: str = "Vazirmatn",
                                 size: float = 11) -> str:
    """Build a 3-column borderless ``cantSplit`` RTL ``<w:tbl>`` for a numbered display equation.

    Layout (with ``<w:bidiVisual/>``, so cell 0 is visual right):
      * Cell 0 (15%, visual right): empty RTL balancing cell
      * Cell 1 (70%, center): LTR ``<m:oMathPara>`` (``<w:bidi w:val="0"/>``)
      * Cell 2 (15%, visual left): RTL Persian equation label e.g. ``(۱)``
    """
    omml_para = latex_to_omml(latex, display=True, include_ns=False, persian_font=font)
    label = _xml_escape(format_persian_eq_number(number))
    esc_font = _xml_escape(font)
    half_pts = str(int(round(size * 2)))

    def _tc_pr(w_pct: str) -> str:
        return (
            f"<w:tcPr>"
            f'<w:tcW w:w="{w_pct}" w:type="pct"/>'
            f'<w:vAlign w:val="center"/>'
            f"</w:tcPr>"
        )

    return (
        f'<w:tbl xmlns:w="{W_NS}" xmlns:m="{M_NS}">'
        f"<w:tblPr>"
        f'<w:tblW w:w="5000" w:type="pct"/>'
        f"<w:bidiVisual/>"
        f"<w:tblBorders>"
        f'<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f'<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        f"</w:tblBorders>"
        f"</w:tblPr>"
        f"<w:tr>"
        f"<w:trPr><w:cantSplit/></w:trPr>"
        f"<w:tc>{_tc_pr('750')}<w:p><w:pPr><w:bidi/></w:pPr></w:p></w:tc>"
        f'<w:tc>{_tc_pr("3500")}<w:p><w:pPr><w:bidi w:val="0"/><w:jc w:val="center"/></w:pPr>{omml_para}</w:p></w:tc>'
        f"<w:tc>{_tc_pr('750')}"
        f'<w:p><w:pPr><w:bidi/><w:jc w:val="center"/></w:pPr>'
        f"<w:r><w:rPr>"
        f'<w:rFonts w:ascii="{esc_font}" w:hAnsi="{esc_font}" w:cs="{esc_font}"/>'
        f"<w:rtl/>"
        f'<w:sz w:val="{half_pts}"/><w:szCs w:val="{half_pts}"/>'
        f"</w:rPr><w:t>{label}</w:t></w:r>"
        f"</w:p></w:tc>"
        f"</w:tr>"
        f"</w:tbl>"
    )


# ---------------------------------------------------------------------------
# python-docx integration helpers (lazy import — python-docx stays optional)
# ---------------------------------------------------------------------------

def add_inline_math(paragraph, latex: str, persian_font: str = "Vazirmatn"):
    """Append an inline ``<m:oMath>`` equation to a ``python-docx`` paragraph.

    Surrounding Persian runs keep their RTL properties; the equation itself
    renders strictly left-to-right in Cambria Math.
    """
    from docx.oxml import parse_xml
    omml = parse_xml(latex_to_omml(latex, display=False, include_ns=True, persian_font=persian_font))
    paragraph._p.append(omml)
    return omml


def add_display_math(doc, latex: str,
                     number: Optional[Union[str, int]] = None,
                     font: str = "Vazirmatn",
                     size: float = 11):
    """Add a display equation to a ``python-docx`` Document.

    * Without ``number`` (and no ``\\tag{...}`` in ``latex``): adds a centered LTR
      paragraph (``<w:bidi w:val="0"/>``) containing ``<m:oMathPara>``, overriding
      any inherited RTL style so the formula never mirrors.
    * With ``number`` (e.g. ``1``, ``"۱"``, ``"۲-۱"``) or ``\\tag{...}`` inside
      ``latex``: inserts a 3-column borderless ``cantSplit`` RTL table (15% empty
      right | 70% centered LTR equation | 15% Persian equation number ``(۱)`` on
      the visual left).
    """
    from docx.oxml import OxmlElement, parse_xml
    from docx.oxml.ns import qn
    from docx.table import Table

    cleaned_latex, extracted_tag = _extract_tag(_strip_math_delimiters(latex))
    eff_number = number if number is not None else extracted_tag

    if eff_number is None:
        omml_para = parse_xml(latex_to_omml(cleaned_latex, display=True, include_ns=True, persian_font=font))
        p = doc.add_paragraph()
        pPr = p._p.get_or_add_pPr()
        bidi = OxmlElement("w:bidi")
        bidi.set(qn("w:val"), "0")
        pPr.append(bidi)
        jc = OxmlElement("w:jc")
        jc.set(qn("w:val"), "center")
        pPr.append(jc)
        p._p.append(omml_para)
        return p

    tbl_el = parse_xml(_build_numbered_eq_table_xml(cleaned_latex, eff_number, font=font, size=size))
    body = doc._body._body
    sectPr = body.find(qn("w:sectPr"))
    if sectPr is not None:
        sectPr.addprevious(tbl_el)
    else:
        body.append(tbl_el)
    return Table(tbl_el, doc._body)


# ---------------------------------------------------------------------------
# Stdlib-only .docx post-processor (works on docx-js / template outputs too)
# ---------------------------------------------------------------------------

_DISPLAY_MATH_FULL_RE = re.compile(
    r"^\s*(?:\$\$([\s\S]+?)\$\$|\\\[([\s\S]+?)\\\])\s*$"
)
_INLINE_MATH_SPLIT_RE = re.compile(
    r"(\$\$[\s\S]+?\$\$|\\\[[\s\S]+?\\\]|\\\([^\n]+?\\\)"
    r"|(?<![\\$])\$(?![ \t\n$])(?:\\.|\\text\{[^}\n]*\}|[^$\n\u0600-\u06ff])+?(?<![ \t\n\\$])\$(?![0-9$]))"
)


def _clone_el(el: ET.Element) -> ET.Element:
    return ET.fromstring(ET.tostring(el, encoding="utf-8"))


def _convert_xml_part_math(xml_bytes: bytes, persian_font: str = "Vazirmatn") -> Tuple[bytes, int]:
    """Convert ``$$...$$`` and ``$...$`` inside an OOXML part to ``<m:oMathPara>`` / ``<m:oMath>``."""
    text_probe = xml_bytes.decode("utf-8", errors="ignore")
    if "$" not in text_probe and "\\[" not in text_probe and "\\(" not in text_probe:
        return xml_bytes, 0

    # Register every namespace prefix declared in the original XML so ElementTree
    # never invents ns0/ns1 prefixes or breaks mc:Ignorable prefix references.
    for pfx, uri in re.findall(r'xmlns:([A-Za-z0-9_.-]+)="([^"]+)"', text_probe):
        if pfx != "xml":
            ET.register_namespace(pfx, uri)
    ET.register_namespace("w", W_NS)
    ET.register_namespace("m", M_NS)

    orig_open_match = re.search(r"<([A-Za-z0-9_]+:[A-Za-z0-9_]+)\b[^>]*>", text_probe)
    orig_open_tag = orig_open_match.group(0) if orig_open_match else None

    root = ET.fromstring(xml_bytes)
    parent_map = {c: parent for parent in root.iter() for c in parent}
    converted = 0

    w_p_tag = f"{{{W_NS}}}p"
    w_pPr_tag = f"{{{W_NS}}}pPr"
    w_r_tag = f"{{{W_NS}}}r"
    w_rPr_tag = f"{{{W_NS}}}rPr"
    w_t_tag = f"{{{W_NS}}}t"
    w_bidi_tag = f"{{{W_NS}}}bidi"
    w_jc_tag = f"{{{W_NS}}}jc"

    for p in list(root.iter(w_p_tag)):
        children = list(p)
        # Gather full paragraph text when it consists solely of runs (and optional pPr)
        only_runs = all(c.tag in (w_pPr_tag, w_r_tag) for c in children)
        if only_runs:
            full_text = "".join(
                (t.text or "")
                for r in children if r.tag == w_r_tag
                for t in r.findall(w_t_tag)
            )
            m_disp = _DISPLAY_MATH_FULL_RE.match(full_text)
            if m_disp:
                raw_formula = m_disp.group(1) if m_disp.group(1) is not None else m_disp.group(2)
                formula, tag_num = _extract_tag(raw_formula)
                parent = parent_map.get(p)
                if tag_num is not None and parent is not None:
                    p_index = list(parent).index(p)
                    tbl_el = ET.fromstring(
                        _build_numbered_eq_table_xml(formula, tag_num, font=persian_font)
                    )
                    parent.remove(p)
                    parent.insert(p_index, tbl_el)
                    converted += 1
                    continue
                for c in list(p):
                    if c.tag != w_pPr_tag:
                        p.remove(c)
                pPr = p.find(w_pPr_tag)
                if pPr is None:
                    pPr = ET.Element(w_pPr_tag)
                    p.insert(0, pPr)
                bidi = pPr.find(w_bidi_tag)
                if bidi is None:
                    bidi = ET.SubElement(pPr, w_bidi_tag)
                bidi.set(f"{{{W_NS}}}val", "0")
                jc = pPr.find(w_jc_tag)
                if jc is None:
                    jc = ET.SubElement(pPr, w_jc_tag)
                jc.set(f"{{{W_NS}}}val", "center")
                omml_el = ET.fromstring(latex_to_omml(formula, display=True, include_ns=True, persian_font=persian_font))
                p.append(omml_el)
                converted += 1
                continue

        # Inline replacement inside individual <w:r> elements
        idx = 0
        while idx < len(p):
            child = p[idx]
            if child.tag != w_r_tag:
                idx += 1
                continue
            t_els = child.findall(w_t_tag)
            if len(t_els) != 1 or not t_els[0].text:
                idx += 1
                continue
            run_text = t_els[0].text
            if not _INLINE_MATH_SPLIT_RE.search(run_text):
                idx += 1
                continue

            parts = _INLINE_MATH_SPLIT_RE.split(run_text)
            rPr = child.find(w_rPr_tag)
            new_nodes: List[ET.Element] = []
            for part_idx, part in enumerate(parts):
                if not part:
                    continue
                if part_idx % 2 == 1:
                    omml_el = ET.fromstring(
                        latex_to_omml(part, display=False, include_ns=True, persian_font=persian_font)
                    )
                    new_nodes.append(omml_el)
                    converted += 1
                else:
                    new_r = ET.Element(w_r_tag)
                    if rPr is not None:
                        new_r.append(_clone_el(rPr))
                    new_t = ET.SubElement(new_r, w_t_tag)
                    if part[:1] == " " or part[-1:] == " " or "  " in part:
                        new_t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve")
                    new_t.text = part
                    new_nodes.append(new_r)

            p.remove(child)
            for offset, node in enumerate(new_nodes):
                p.insert(idx + offset, node)
            idx += len(new_nodes)

    if not converted:
        return xml_bytes, 0

    serialized_str = ET.tostring(root, encoding="unicode")
    if orig_open_tag and not orig_open_tag.endswith("/>"):
        patched_open = orig_open_tag
        if 'xmlns:m=' not in patched_open:
            patched_open = patched_open[:-1] + f' xmlns:m="{M_NS}">'
        serialized_str = re.sub(r"^<[A-Za-z0-9_]+:[A-Za-z0-9_]+\b[^>]*>", patched_open, serialized_str, count=1)

    header = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
    return (header + serialized_str).encode("utf-8"), converted


def convert_docx_latex(in_path: str, out_path: Optional[str] = None,
                       persian_font: str = "Vazirmatn") -> int:
    """Replace ``$$...$$`` and ``$...$`` inside a ``.docx`` with native OMML equations.

    Preserves ``[Content_Types].xml`` as the first ZIP entry and writes via a
    temporary file so a failure never damages the input package.
    Returns the total number of equations converted.
    """
    target = out_path or in_path
    with zipfile.ZipFile(in_path, "r") as zin:
        items = {n: zin.read(n) for n in zin.namelist()}

    total = 0
    for name in list(items):
        if re.match(r"word/(document|header\d*|footer\d*|footnotes|endnotes)\.xml$", name):
            updated, count = _convert_xml_part_math(items[name], persian_font=persian_font)
            if count:
                items[name] = updated
                total += count

    if total == 0 and target == in_path:
        return 0

    tmp = target + ".tmp"
    names = list(items)
    names.sort(key=lambda n: n != "[Content_Types].xml")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in names:
            zout.writestr(n, items[n])

    with zipfile.ZipFile(tmp, "r") as check:
        if check.testzip() is not None:
            os.remove(tmp)
            raise IOError("rewritten .docx failed CRC check")
        if check.namelist()[0] != "[Content_Types].xml":
            os.remove(tmp)
            raise IOError("[Content_Types].xml is not first entry")
    shutil.move(tmp, target)
    return total


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(
        description="Convert LaTeX math to native Word OMML (<m:oMath>) or patch .docx equations."
    )
    ap.add_argument("latex", nargs="?", help="LaTeX math string to convert to OMML XML.")
    ap.add_argument("--display", action="store_true",
                    help="Wrap output in <m:oMathPara> (centered display equation).")
    ap.add_argument("--docx", dest="docx_path",
                    help="Convert $...$ and $$...$$ placeholders inside a .docx file to OMML.")
    ap.add_argument("--out", dest="out_path",
                    help="Output .docx path when using --docx (default: overwrite in place).")
    ap.add_argument("--font", default="Vazirmatn",
                    help="Persian complex-script font for \\text{...} or equation labels (default: Vazirmatn).")
    args = ap.parse_args(argv)

    if args.docx_path:
        n = convert_docx_latex(args.docx_path, args.out_path, persian_font=args.font)
        dest = args.out_path or args.docx_path
        print(f"converted {n} LaTeX equation(s) to OMML in {dest}")
        return 0

    expr = args.latex
    if expr is None:
        if not sys.stdin.isatty():
            expr = sys.stdin.read().strip()
        else:
            ap.print_help()
            return 1
    print(latex_to_omml(expr, display=args.display, include_ns=True, persian_font=args.font))
    return 0


if __name__ == "__main__":
    sys.exit(main())
