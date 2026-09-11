# Contributing

Thanks for looking. Bug reports and fixes are welcome — especially ones that
come from actually running the toolkit on real Persian text, because that is
where the interesting failures live.

Before opening a pull request, please read the design contract below. Most
rejected changes are not wrong; they simply assume a different kind of project
than this one is.

## The design contract

**1. Standard library only.** Scripts target Python 3.8+ and import nothing
outside the stdlib. A Persian writer on a locked-down work laptop, and an AI
agent in a sandbox with no network, both have to be able to run
`python3 scripts/persian_cleanup.py` and have it work. Every dependency is a
place that promise can break.

**2. No packaging layer.** There is no `pyproject.toml`, no `setup.py` and no
`src/` tree. The project is cloned and run in place, and it ships through four
channels that all expect exactly that:

| Channel | What it loads |
|---|---|
| Claude skill (`.skill`) | the directory, unpacked |
| Claude Code plugin | the git repo |
| Cursor / Windsurf / other agents | the cloned folder |
| ChatGPT / Gemini | `universal/persian-writing-universal.md` |

Adding `pip install` adds a fifth channel with its own release cadence,
its own version number and its own copy of every file. If you want it, open an
issue and make the case first — please do not bring it as a surprise in a PR.

**3. One copy of everything, especially the dictionary.**
`assets/persian_words.txt` is 6.9 MB and 453,157 lines. Exactly one copy lives
in the repository. If a script cannot find it, fix the *lookup*, not the file
count: `persian_cleanup.resolve_dictionary_path()` searches several locations
and both scripts call it. Two copies do not make the tool more robust; they
guarantee that one day they disagree and nobody can say which is right.

The same rule applies to code. If you find yourself copying a function so that
a second entry point can use it, import it instead.

**4. The version lives in four places and they must agree.**

```
SKILL.md · .claude-plugin/plugin.json · scripts/persian_cleanup.py · README.md
```

Never edit them by hand:

```bash
python3 scripts/check_version.py            # verify they match
python3 scripts/check_version.py --set 1.4.0
```

Add a `README.md` version-history entry in the same commit, written so a
reader can tell whether the release affects them.

**5. Regenerate the single-file edition.** After changing `SKILL.md` or
anything in `references/`:

```bash
python3 scripts/build_universal.py
```

`universal/persian-writing-universal.md` is generated. Do not hand-edit it.

## Writing rules for the documentation itself

**The skill must pass its own linter.**

```bash
python3 scripts/fa_lint.py --check references/your-file.md
```

**Documentation legitimately contains wrong Persian.** A table teaching
«کتابه من ✗ → کتابِ من ✓» has to contain the error. Mark it rather than
rewriting it:

```markdown
<!-- fa-lint-ignore-next-line -->
- Never Arabic-Indic variants (٤ ٥ ٦).

<!-- fa-lint-ignore-start -->

| Wrong | Right |
|---|---|
| میخواهم | می‌خواهم |

<!-- fa-lint-ignore-end -->
```

`--fix` restores suppressed lines afterwards, so it will not quietly repair
your examples.

**Do not degrade English prose to satisfy a Persian rule.** The docs are
bilingual. An em dash between two English words is correct English; the linter
only flags one sitting between two Persian words. If a rule fires on correct
English, that is a bug in the rule — report it, and we will scope the rule.

**No brands, no invented facts.** No company names, products, client counts,
prices, statistics or hashtags, and no vocabulary specific to one industry.
Colors in examples are placeholders. The skill styles nothing on its own.

**The authorship boundary.** This project helps people write better Persian.
It will not help disguise who or what wrote a text: no invisible characters,
homoglyph substitution, watermark stripping or deliberately injected errors.
Changes in that direction are declined regardless of quality.

## Before you open the PR

```bash
python3 scripts/check_version.py
python3 scripts/fa_lint.py --check references/*.md SKILL.md
python3 scripts/persian_cleanup.py --edit --in some-real-file.md --out /tmp/out.md
diff some-real-file.md /tmp/out.md     # inspect every change you did not intend
```

Keep unrelated changes in separate commits. A PR whose good fix rides along
with a large restructuring is slow to review and usually lands as a
cherry-pick, which is a worse outcome for everyone than two clean commits.

Describe the bug you hit, and include the input that triggered it. A failing
example is worth more than a paragraph of explanation.
