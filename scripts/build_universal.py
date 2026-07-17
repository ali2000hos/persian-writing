#!/usr/bin/env python3
"""
build_universal.py — compile the persian-writing skill into ONE self-contained
Markdown file for chat-only AIs (ChatGPT, Gemini, any LLM without file access).

Output: universal/persian-writing-universal.md
Run after ANY edit to SKILL.md or references/.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'universal' / 'persian-writing-universal.md'

# Order matters: always-apply layers first, then genres, then formats.
PARTS = [
    ('writing-style.md',    'Writing style: registers & de-AI-ing'),
    ('orthography.md',      'Orthography (نگارش و رسم‌الخط)'),
    ('academic.md',         'Academic writing (نگارش علمی)'),
    ('seo-copywriting.md',  'SEO writing & copywriting'),
    ('fonts.md',            'Fonts'),
    ('docx-pdf.md',         'Word/DOCX + PDF'),
    ('pptx.md',             'PowerPoint'),
    ('html-css.md',         'HTML / CSS / email'),
    ('format-skills-fa.md', 'Images, reportlab PDFs, Excel'),
]

HEADER = """\
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
"""


def strip_frontmatter(text: str) -> str:
    if text.startswith('---'):
        end = text.find('\n---', 3)
        if end != -1:
            return text[end + 4:].lstrip('\n')
    return text


def drop_files_section(text: str) -> str:
    """Remove the '## Files' tree from SKILL.md (paths are meaningless here)."""
    return re.sub(r'\n## Files\n.*?(?=\n## |\Z)', '\n', text, flags=re.S)


def rewire_paths(text: str) -> str:
    """Point file references at the parts of this document instead."""
    for fname, title in PARTS:
        text = text.replace(f'`references/{fname}`', f'the «{title}» part below')
        text = text.replace(f'references/{fname}', f'the «{title}» part below')
        text = text.replace(f'`{fname}`', f'the «{title}» part')
    text = text.replace('`references/cleanup/paknevis-rules.md` + `usage-patterns.md`',
                        'the Orthography part (script docs ship with the full package)')
    text = re.sub(r'`?scripts/(persian_cleanup|fa_lint|verify_pdf|install_fonts|download_fonts|build_universal)\.(py|sh)`?',
                  r'the \1 script (full package; chat-only AIs apply the equivalent rules manually)',
                  text)
    return text


def main():
    OUT.parent.mkdir(exist_ok=True)
    chunks = [HEADER]

    skill = strip_frontmatter((ROOT / 'SKILL.md').read_text(encoding='utf-8'))
    skill = rewire_paths(drop_files_section(skill))
    chunks.append('# PART 0 — Core rules and routing\n\n' + skill.strip() + '\n')

    for i, (fname, title) in enumerate(PARTS, 1):
        body = strip_frontmatter((ROOT / 'references' / fname).read_text(encoding='utf-8'))
        body = rewire_paths(body)
        chunks.append(f'\n\n---\n\n# PART {i} — {title}\n\n' + body.strip() + '\n')

    OUT.write_text('\n'.join(chunks), encoding='utf-8')
    n_lines = OUT.read_text(encoding='utf-8').count('\n')
    print(f'wrote {OUT} ({n_lines} lines, {OUT.stat().st_size/1024:.0f} KB)')


if __name__ == '__main__':
    main()
