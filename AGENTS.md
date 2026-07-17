# AGENTS.md

Guidance for ANY AI agent (Claude, Codex, Cursor, Gemini-based agents, Warp,
OpenCode, custom LLM harnesses...) using or maintaining this package. Nothing
here is specific to one vendor: the skill is Markdown instructions + optional
Python scripts (stdlib only).

## What this package is

A complete toolkit for producing professional Persian (Farsi) output:
natural human-sounding prose in the correct register, correct orthography
(ZWNJ, Persian digits/punctuation), correct right-to-left documents
(Word/PDF/PowerPoint/HTML/Excel/images), Persian SEO writing and copywriting,
plus deterministic scripts for cleanup, spell-check, linting, and PDF
verification. Bundled Vazirmatn and Lalezar fonts (SIL OFL).

## How an agent should use it

1. Read `SKILL.md` first — it is the entry point and source of truth. Its
   routing table says which file in `references/` to read for the task at
   hand. Do not skip register detection (writing-style.md, Part 1).
2. If you can execute code: use the scripts —
   `scripts/persian_cleanup.py --edit` (fix), `scripts/fa_lint.py --check`
   (lint), `scripts/verify_pdf.py` (PDF QA), `scripts/install_fonts.sh`
   (before any PDF conversion). Python 3.8+, standard library only.
3. If you can NOT execute code (chat-only environment): every rule the
   scripts enforce is also stated in prose in `references/orthography.md`
   and `references/writing-style.md` — apply them manually. A fully inlined
   single-file version for paste/upload use is at
   `universal/persian-writing-universal.md` (regenerate with
   `scripts/build_universal.py`).
4. Fonts: reference by family name (`Vazirmatn`, `Lalezar`); files live in
   `assets/fonts/`. Install them into the OS/font cache before rendering
   PDFs or images, or output silently falls back to broken glyphs.

## Layout

- `SKILL.md` — entry point (YAML frontmatter + core rules + routing)
- `references/` — depth: writing-style, orthography, academic,
  seo-copywriting, fonts, docx-pdf, pptx, html-css, format-skills-fa,
  cleanup/ (paknevis+davat docs)
- `scripts/` — persian_cleanup.py, fa_lint.py, verify_pdf.py,
  install_fonts.sh, download_fonts.py, build_universal.py
- `assets/` — fonts/ (TTFs), persian_words.txt (453K-word frequency
  dictionary for spell-check)
- `universal/` — generated single-file edition for chat-only AIs
- `.claude-plugin/` — optional Claude Code plugin manifests
- `evals/` — test prompts for regression-testing the skill

## Maintenance contract

- `SKILL.md` and the references must not contradict each other; SKILL.md
  summarizes, references specify.
- After editing SKILL.md or any reference, regenerate the universal file:
  `python3 scripts/build_universal.py`.
- Bump `version:` in SKILL.md frontmatter and `.claude-plugin/plugin.json`
  together.
- Keep wording harness-neutral; name specific tools as examples, not limits.
- Keep the package brand-free: no company names, no real client stats,
  placeholder colors only.
- Run `python3 scripts/fa_lint.py --check` on any Persian example text you
  add to the docs — the skill must pass its own linter.
