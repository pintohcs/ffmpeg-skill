---
name: adding-an-ffmpeg-skill-tool
description: Add a new tool (a script under scripts/) to ffmpeg-skill so it lands on every surface at once — the contract entry in scripts/_contract.py, README tool and contract tables, SKILL.md (which has a 30,000-byte budget, so a line in means a line out), references/scripts.md, docs/contract.md, CHANGELOG.md, a before/after demo in demos/build.py (or an INSPECTION row), a tests/sweep.py TABLE or BY_HAND entry, and tests in the right group module. Use when asked to add a tool or a flag to this repository, or when reviewing a feat PR for a surface it forgot.
---

# Adding a Tool to ffmpeg-skill

A tool is public because a file named `scripts/<name>.py` exists (`public_tools()` globs
`scripts/*.py` and skips names starting with `_`). Everything else (MCP schemas, installer,
docs checks) is generated from or tested against the contract, so a new script that is missing
from one surface fails a test rather than shipping half done. Read the bar first: CONTRIBUTING.md
"Scope". New tools are a higher bar than fixes, and anything needing AI/LLM judgement, a cloud
call, a raw `ffmpeg` shell call outside `scripts/*.py`, or a new runtime dependency does not
belong here. Open an issue before writing code.

## Checklist

Work through these in order; each one has a test that fails if you skip it.

1. **The script.** Python 3.10+, standard library only, FFmpeg 6.1 as the oldest supported. Use
   `scripts/_common` (`add_common`, `apply_common`, `emit`, `die`, `probe`, `default_output`);
   do not hand-roll output documents, error kinds or `--dry-run`. Never modify an input. The
   module docstring carries an `Examples:` block (see `scripts/freeze.py`). The contract's per-tool
   `examples` are parsed from SKILL.md's "User says" / "Do" table, so the tool needs a row there.
2. **The contract entry** in `scripts/_contract.py`: role (one of `ROLES`), required
   capabilities (`encoder:`, `filter:`, `ffmpeg`/`ffprobe`), dry-run semantics, error reasons.
   Extend the generator; never hand-copy a schema into another file.
3. **Tests.** Behaviour goes in the group module that owns the topic (`test_analysis`,
   `test_editing`, `test_audio`, `test_picture`, `test_delivery`, `test_orchestration`,
   `test_accel`, `test_asr`, `test_cut_copy`). Contract, docs and dry-run guarantees go in
   `tests/test_contract.py`. Run the group alone while working:
   `python3 tests/test_editing.py EditingTests.test_name`.
4. **Sweep list.** A tool taking one media file gets a row in `tests/sweep.py` `TABLE`; one that
   needs a second file or a project goes in `BY_HAND`. `test_contract.py` fails when a script is
   in neither.
5. **Docs surfaces.** `README.md` (tool table, contract table, gotchas), `SKILL.md`,
   `references/scripts.md`, `docs/contract.md`, `CHANGELOG.md`. `SKILL.md` must stay under
   30,000 bytes (`test_skill_md_stays_under_the_30kb_budget`): check with `wc -c SKILL.md`
   and trim a line for every line you add; the PR body says which.
6. **A demo.** Add a before/after to the table in `demos/build.py`, then
   `python3 demos/build.py --docs` regenerates `docs/demos.md` (never hand-edit it). Every
   script must appear in some demo's command line. The one exception is a tool whose entire
   output is a table, JSON or HTML: add it to `INSPECTION` in `demos/build.py` instead.
7. **Drift check.** `python3 scripts/_contract.py --json` is the authority; diff what README and
   SKILL.md say against it for names, flags and error kinds.

## Before you push

- `npm run test:fast` (contract, docs, dry runs), then your group module, then `npm test` or
  `python3 tests/run_parallel.py --part 1/3` if the change touches shared code.
- Read `docs/design-decisions.md` before arguing with a refusal or a warning; it lists what
  looks like a bug and is a decision, with the test that pins it.
- The PR body explains why, lists the surfaces updated, and fills in the template's "Siblings"
  section if the PR also fixes a defect (see the `sibling-sweep` skill).
