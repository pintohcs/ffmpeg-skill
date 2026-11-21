---
name: automating-ffmpeg-skill-jobs
description: Run ffmpeg-skill unattended over many files without surprises — batch.py recipes with {in}/{out} substitution and its content-hash cache, --dry-run first, --force and --watch semantics, a render project as the per-file recipe, verify.py as a smoke test on real footage, and wiring the same commands into cron, a scheduled task or CI without raw ffmpeg or new dependencies. Use when asked to process a folder, watch a folder, schedule a recurring media job, or turn a one-off edit into a repeatable one.
---

# Automating ffmpeg-skill Jobs

## The recipe

`batch.py FOLDER --recipe batch.json` applies a list of script steps to every file matching
`glob`. `{in}` and `{out}` are substituted and each step's output feeds the next:

```json
{"glob": "*.mp4", "output_dir": "out", "suffix": "_final",
 "steps": [["silence.py", "{in}", "--threshold", "-38", "-o", "{out}"],
           ["loudness.py", "{in}", "-o", "{out}"],
           ["export.py", "{in}", "--preset", "youtube", "-o", "{out}"]]}
```

Or give a render project for every file: `{"project": "project.json", "clip_key": 0}`.

## Order of operations

1. **`--dry-run` first**, always, on a new recipe or a new folder. Read what it says it would do.
2. **Run once by hand** on one file and open the contact sheet (`look.py`) before pointing it at
   a hundred.
3. **Re-runs are cheap.** Each item is cached by a key over its content, the recipe and the files
   the recipe names (a LUT, a logo, a `--compare` reference), so editing any of them re-runs the
   affected items. The cache is `.ffskill_cache.json` in `output_dir`. `--force` ignores it;
   use it when a tool itself changed, or after an FFmpeg upgrade, not after a recipe edit.
4. **`--watch 30`** polls the folder every 30 s. The recipe is re-read on every pass, so an edit is picked up without a restart. It is a loop in one process: run it under
   whatever supervisor the machine has, and stop it before you move or delete the folder.
5. **Smoke test on real footage:** `python3 scripts/verify.py ~/Footage/*.mov --quick --report
   verify.md` runs the toolchain on your own files and prints pass/fail.

## Scheduling

Anything that can run a command can run this: cron, a scheduled task, or a CI job. Keep the
command line identical to the one you ran by hand and read the exit status and the result
document, not just the log. Run `python3 scripts/_contract.py doctor` on the machine first; it
lists what that machine can actually run (encoders, filters, FFmpeg version), and a recipe that
needs a missing encoder fails there, not at 3 a.m.

## Never

- Never put raw `ffmpeg` in a recipe; use a script from `scripts/`.
- Never let a recipe write into its own input folder with a glob that matches its output.
- Never add a cloud call or API key to a recipe; that belongs to a different skill.
