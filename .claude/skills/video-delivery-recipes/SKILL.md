---
name: video-delivery-recipes
description: Map a plain video request (vertical cut for a platform, hold a still at the end, fit to a length, make a delivery-ready file, check it before reporting) onto the ffmpeg-skill tools in the right order, with the verification step each one needs — fit before export, color --to-sdr before an SDR delivery of an HDR source, look.py before reporting, check.py against a platform, never raw ffmpeg. Use when an agent is asked to produce or fix a video deliverable with this repository's scripts, or when writing a demo or example that chains them.
---

# Video Delivery Recipes

These are chains of existing tools, not new behaviour. Every tool takes `--dry-run`; run it first
when the arguments are new. The tools execute an explicit edit and never decide one (SKILL.md,
"What this skill does and does not decide"), so the choices below (which platform, which
aspect, which seconds) come from the request, not from you.

| Request | Chain |
|---|---|
| Vertical cut for a platform | `fit.py --aspect 9:16 --fit crop\|pad\|blur` → `export.py --preset reels\|tiktok\|shorts` → `check.py --platform ...` → `look.py` |
| Make it N seconds | `fit.py --duration N --method speed\|trim` (speed retimes picture and sound; trim keeps the first N s or a centred window) |
| End card / title card from a still | `insert.py IMAGE --duration S` (silent clip) → `join.py` with the footage |
| Hold the last frame | `freeze.py --hold S` (`--mode extend`) |
| HDR source, SDR destination | `color.py --to-sdr` first, then the rest; `export.py youtube-hdr` refuses an SDR source |
| Whole edit as data | `render.py project.json`: change a number, re-render |
| Hand the user a summary | `report.py --before raw --after final --platform ...` |

## Rules that keep a result honest

1. **Fit, then export.** `export.py` scales to the preset keeping the source aspect; fixing the
   aspect after it re-encodes twice.
2. **Read the result document, not the exit code.** Look at `verified`, `warnings` and `dropped`;
   a refusal with a hint can be a decided behaviour (`docs/design-decisions.md`).
3. **Look before you report.** `look.py out.mp4` writes a contact sheet; open the PNG. Caption
   placement, crop and logo position are only visible there. Use `--safe tiktok` to shade what a
   platform's own UI covers.
4. **Captions are data.** Burn the words you were given; never rewrite or shorten them.
5. **No raw `ffmpeg`.** If no tool exposes the feature, say so and name the closest option.
