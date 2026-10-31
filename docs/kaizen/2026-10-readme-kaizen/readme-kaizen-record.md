# README kaizen record: Chwezi SDLC Documentation

Date: 2026-10-31. Scope: the root `README.md` only, run as one micro-cycle of the portfolio kaizen steps. Starting point: branch `main` at `efec2c7`, clean working tree. Work branch: `kaizen/2026-10-readme-kaizen`. This is a scoped cycle, so it publishes no score. The latest published score stays 55.68 out of 100 (pass 2 final report).

## 1. Observe: baseline

Measured with the portfolio readability script on `README.md` at `efec2c7`, before any edit.

| Measure | Baseline | Reading |
|---|---:|---|
| `words` | 8,995 | A long document for a front page. |
| `h2` | 6 | Few sections, each very large. |
| `toc` | 0 | No contents list. |
| `first_cmd` | 34 | First fenced command at line 34. |
| `longest_sec` | 2,951 | The skill table section. |
| `long_lines` | 44 | Lines over 300 characters. |
| `max_line` | 1,240 | The opening paragraph. |
| `sent_len` | 15.5 | Mean words per sentence in prose paragraphs. |
| `fre` | 43 | Flesch reading ease: difficult. |

Other observations from the same read:

- The longest paragraph held 162 words and the longest table cell 47 words.
- The opening was one 1,240-character paragraph that listed every document type, then a second 1,009-character paragraph of standards.
- The 159-row skill table and the book, repository and website lists made up about 40 percent of the words.
- Each kept-change entry in "What the October 2026 kaizen improved" ran to 300 to 1,000 characters of process detail, in a single line.

## 2. Select: items applied and skipped

| Item | Decision | Reason or evidence |
|---|---|---|
| R1 Front door | Applied | Purpose, audience and when to use it, six measured facts, and three numbered start-here steps with exact commands. The first fenced block is at line 22. The step 3 result (exit 1, 22 blocking findings) was re-run in a scratch clone. |
| R2 Contents | Applied, with a placement note | A list of 12 in-page links follows Start here, under a bold "Contents" label rather than an H2. The readability script counts a contents list only when its links come before the third H2, and the skeleton puts At a glance and Start here first. All links resolve (preservation check). |
| R3 Structure | Applied, one preferred target missed | 14 H2 sections. The longest, "What the October 2026 kaizen improved", holds 1,445 words (target 1,500 met; preferred 1,200 missed). It keeps Scores, Measures and Kept changes as H3s because `docs/README.md` and the changelog point readers to that one section by name. |
| R4 Find the right skill | Applied | 12 rows. Every skill name was confirmed with `find` and each task paraphrases a routing fixture prompt. A note records the known near miss for the bare phrase "software requirements specification". |
| R5 No walls of text | Applied | Longest paragraph 51 words, longest table cell 27 words, longest list item 52 words. Lines over 300 characters fell from 44 to 5. Table cells that held lists became bullets or split rows. |
| R6 Plain English | Applied | Shorter sentences, active voice, terms defined at first use (PRD, SRS, BRD, ADR, NFR, CI). British English. No marketing language. |
| R7 Say it once | Applied | The standards paragraph became bullets under "Standards it follows" with a pointer to the full list. The score definition appears once and is cross-referenced. Process narrative sits in the linked evidence records. "What the October 2026 kaizen improved" is kept and tightened. |
| R8 Relocate bulk | Applied to two blocks | See section 3, commit 1. The standards list, the phase table with its total of 159 and every cited heading stay in the README. |
| Skeleton item 10 | Applied | A short "Contributing and licence" section. The licence (MIT, copyright 2026 Peter Bamuhigire) was read from `LICENSE`. |

R8 grep evidence. No script, test, manifest or workflow reads the README skill rows or the phase table. `scripts/validate_engine.py` requires only `projects/<ProjectName>/`, `docs/hybrid-operating-model.md` and `docs/regulated-evidence-model.md` in the README, and all three remain. Two documents did point at the README table: `AGENTS.md` (the "Full Skill Suite" section) and `skill_overview.md`. Both were updated in the same commit. The standards-citation ratchet counts lines in the live README, so the Standards and official sources list was not moved.

## 3. Experiment: what each commit changed

1. `84bd602` Relocation. The 159 skill rows moved to `docs/skill-catalogue.md`, grouped by phase, each name linking to its `SKILL.md`. Independent check: the 159 `SKILL.md` directories found on disk equal the 159 linked in the page, and every description is identical to the old README row. The Books, Repositories and Websites and articles lists moved to `docs/references.md`; every moved line is present, with two relative links rewritten for the new folder. `AGENTS.md` and `skill_overview.md` now point at the catalogue page. The README kept the phase table, the standards list and links to both pages.
2. `4488804` Restructure, front door and plain English. The new order and content are in section 2. The 15 kept-change entries were tightened to one to three sentences each, and their full original text moved unchanged to `kept-changes-detail.md` (links made relative, "today" written as 2026-10-31).
3. `5d44827` `docs/README.md` index rows for the new pages and a line in the 2026-10-31 changelog entry.
4. The commit that adds this record.

### Deliberate changes and removals

- The sentence "Generated from the `SKILL.md` frontmatter on disk" was removed. The repository holds no generator for the table, and `AGENTS.md` says the table is not the source of truth. The catalogue page says so instead.
- "Skill paths are relative to the category folder" was removed: each catalogue entry now links to its real path.
- The opening standards paragraph became bullets, and "superseded" was added to the IEEE Std 830-1998 layout statement, as the References list already says.
- The security standards line was split into three bullets with new labels. A word-count comparison of the old and new Standards section shows no entry added or removed.
- Commands that moved within the README: the `git clone`, `cd` and `pip install` lines and the `new-project` and `validate` lines are now in Start here. The `doctor` line stays under "Manual route".
- The pytest skip explanation and the routing detail moved from table cells to notes below the Validation table.
- The "Which checks need which tool" lead-in became a heading of that name, so the `AGENTS.md` reference resolves to a real heading. Its two long rows were split.

## 4. Check

### Preservation

`python3 -I readme-preserve-check.py <repo> main kaizen/2026-10-readme-kaizen`, run after the last README edit (`4488804`) and again at the final tip. Results, abbreviated:

- Links: old README 66 targets, new README 34, moved to docs 39, LOST 0.
- Commands: old README 49, kept in README 49, moved to docs 0, LOST 0.
- Anchors: 1 anchor link into the README from tracked files, BROKEN 0.
- In-page links: 16 anchors used, BROKEN 0.
- Result: OK (exit 0).

No deliberate replacement was flagged. The one anchor link into the README from tracked files is in `docs/references.md`, which points back at the standards heading. The commit-hash checker reports 36 cited hashes, all commits and ancestors of the branch (problems: 0).

### Metrics

| Measure | Before | After | Target | Result |
|---|---:|---:|---|---|
| `words` | 8,995 | 5,663 | at most 9,444; aim 8,096 | Met (-37%), by relocating and tightening |
| `h2` | 6 | 14 | none | Reported |
| `toc` | 0 | 1 | 1 | Met |
| `first_cmd` | 34 | 22 | 40 or less | Met |
| `longest_sec` | 2,951 | 1,445 | 1,500 or less; 1,200 preferred | Met; preferred figure missed |
| `long_lines` | 44 | 5 | 22 or less | Met |
| `max_line` | 1,240 | 374 | 700 or less | Met |
| `sent_len` | 15.5 | 11.6 | 16.5 or less | Met |
| `fre` | 43 | 53 | at least 43; aim 48 | Met (+10) |

The script measures sentence length on prose paragraphs only. Counting list items as well, the mean falls from 13.8 to 12.0 words.

### Validators

Run in throwaway clones outside the repository, with the pinned-package virtual environment and `PYTHONPATH=.` (the system `python3` has no `pytest` or `ruamel.yaml`). The "before" run is `efec2c7`; the "after" run is `4488804`. The exit codes are identical.

| Command | Before | After |
|---|---:|---:|
| `python3 -m pytest` (535 passed, 5 skipped, 96.19% coverage, both runs) | 0 | 0 |
| `scripts/validate_engine.py` | 0 | 0 |
| `scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json` | 0 | 0 |
| `scripts/routing_smoke_test.py --min-rank1 83 --lint-fixtures --min-covered 8` (72 of 72; 64 of 72) | 0 | 0 |
| `python3 -m pytest -o addopts= tests/test_routing_smoke_owned_negatives.py tests/test_validate_skill_engine_tier1.py` (19 passed) | 0 | 0 |
| `python3 -m engine validate-skills` | 0 | 0 |
| `scripts/validate_plugin_packages.py` | 0 | 0 |
| `scripts/check_portable_paths.py` | 0 | 0 |
| `scripts/check_cross_engine_refs.py` (category and URL paths `NOT_ASSESSED`, no dev-engine checkout) | 0 | 0 |
| `scripts/check_standards_currency.py` | 0 | 0 |
| `scripts/validate_source_register.py` (18 records, as of 2026-10-31) | 0 | 0 |
| `scripts/validate_traceability_evidence.py engine/tests/fixtures/traceability-evidence.json` | 0 | 0 |
| `scripts/validate_sdd_phase_boundaries.py --feature-dir engine/tests/fixtures/sdd_feature` | 0 | 0 |
| `scripts/validate_requirements_decision.py engine/tests/fixtures/requirements_decision/reuse.json` | 0 | 0 |
| `scripts/source_ingestion_guardrail.py` | 0 | 0 |
| `scripts/seed_demo_project.py`, then `python3 -m engine validate projects/_demo-hybrid-regulated` | 0 | 0 |
| The same validate with `--break-something` (built to fail) | 1 | 1 |
| `node hooks/test-destructive-bash-gate.js` | 0 | 0 |
| `node hooks/test-plugin-hook-config.js` | 0 | 0 |
| `python3 -m pytest -o addopts= tests` (33 passed) and the six Plan Canvas Node.js files | 0 | 0 |

Re-run at `b5a5c13` (the tip with the docs index, the changelog line and the first version of this record): the same 20 commands returned the same exit codes, and pytest again reported 535 passed, 5 skipped and 96.19% coverage. The commit after it edits only this record.

Standards-citation ratchet: the lines in the README that match the counted patterns are unchanged (IEEE 830: 3, 42010 2011: 1, 29119-3 2013: 1), and `scripts/check_standards_currency.py` exits 0.

`NOT_ASSESSED` on this host: `bash scripts/build-doc.sh` and Mermaid rendering (no Pandoc, renderer or browser), `install.ps1` and `scripts/setup-srs-project.ps1` (no PowerShell), and the four pytest skips that depend on them. A README edit does not touch these paths.

Read-only cross-engine check: the portfolio tour file for this engine (`docs/engine-tours/chwezi-sdlc-documentation.json` in `chwezi-engine-agents`) says "Start with README.md: it states what Chwezi SDLC Documentation is for and what it does not cover". The new opening still does, so no change is needed there.

## 5. Standardise: README conventions for a maintainer

- Order: title and purpose; At a glance (five or six measured facts, each dated); Start here (three numbered steps with exact commands, first fenced block within 40 lines); Contents; task-to-skill table (6 to 12 rows of real skills); how it works; what is inside; standards; requirements; installation; engine-specific sections; validation; quality and improvement; references; contributing and licence.
- Limits: no H2 section over 1,500 words (aim for 600); no paragraph over 90 words (51 now); no table cell over 35 words (27 now); no list item over about 55 words; no line over 700 characters; mean sentence length 16 words or fewer.
- Keep these headings, which other documents cite by name: "Which checks need which tool", "Validation", "Quality and improvement" and "What the October 2026 kaizen improved".
- Keep in the README: the nine-row phase table with its total, the Standards and official sources list (the ratchet counts its lines, and `AGENTS.md` tells agents to map requirements to it) and the three strings `scripts/validate_engine.py` requires. Do not add a line that mentions a counted superseded edition.
- Put bulk reference material in `docs/` and leave a summary and a link. Update every document that points at the moved text in the same commit.
- Re-measure every number you touch, and give its date.

## 6. Teach: three lines for the next editor

1. Run the preservation check and the readability script after the last edit, and fix the README rather than the validator.
2. Put long reference lists and per-change history in `docs/`, and keep the README to what a new reader needs in the first 40 lines.
3. Never add a mention of IEEE Std 830, ISO/IEC/IEEE 42010:2011 or 29119-3:2013 to a live line without lowering another, because the ratchet counts lines.

## 7. Re-measure and next cycle

Re-measured after the last README commit: every figure in section 4. No score is published for this cycle.

Open items for a later cycle:

- "What the October 2026 kaizen improved" is 1,445 words against the preferred 1,200. Splitting it into separate H2 sections would reach the figure, but it would break the pointers in `docs/README.md` and the changelog, which name it as one section.
- `AGENTS.md` (the router) was edited in one line to point at the catalogue page. Peter may prefer to revert that line; if so, the README still links the catalogue page.
- The catalogue page is a hand-maintained list. A generator that reads the `SKILL.md` frontmatter would keep it exact. That is a script change, so it was out of scope.
- Several existing README facts predate this cycle and were carried over unchanged (for example the Codex 0.165.0 result of 2026-10-29). They keep their dates and were not re-verified here.
