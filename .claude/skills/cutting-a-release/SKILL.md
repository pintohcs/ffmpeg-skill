---
name: cutting-an-ffmpeg-skill-release
description: Prepare, check and recover a release of ffmpeg-skill without breaking its release machinery — what release.yml's label-driven auto-bump moves (version, docs/roadmap.md's version sentence, both server.json version fields), what a hand-written release PR must move in the same PR, the plugin branch that is never committed to by hand, and recovering a tag whose npm publish failed with the recover job instead of a local publish. Use when asked to release, bump a version, publish to npm or the MCP Registry, fix a half-finished release, or review a release PR in this repository.
---

# Cutting an ffmpeg-skill Release

The authority is CONTRIBUTING.md ("Pull requests", "Publishing the MCP listing") and the
comments in `.github/workflows/release.yml`. This skill is the order to read them in and the
mistakes that cost a release before.

## Normal release

1. Run `npm run release-check` (packaging, installer, MCP, doctor, full suite) on a clean tree.
2. Releases are label-driven: merged PRs carry a label and `release.yml` auto-bumps. The bump
   moves the version number and keeps the hand-written roadmap prose, marked with the version
   it describes (`.github/scripts/bump_roadmap_md.py`). It also moves both `version` fields in
   `server.json` (`bump_server_json.py`).
3. A **hand-written** release PR moves `docs/roadmap.md`'s "the released version today is ..."
   line in the same PR as the version bump, so the roadmap never describes a released version
   as planned.
4. `CHANGELOG.md` must mention every issue closed since the last tag (a test fails otherwise).
   Entries come from the merged PRs; do not invent a section for an unreleased version.
5. CI publishes to npm with provenance, then the MCP Registry (`server.json`, OIDC, no stored
   secret), then the `plugin` branch. `mcpName` in `package.json` must equal `server.json`'s
   `name` at that exact version, which is why npm comes first.

## Never

- Never commit to the `plugin` branch by hand or force-push it; hosts fast-forward it. To see
  the tree locally: `bash .github/scripts/publish_plugin_branch.sh --tree-only DIR`.
- Never `npm publish` locally: no provenance, and without `--tag` it moves `latest`.
- Never delete and re-tag to retry. A release whose npm publish failed keeps its tag.

## Recovering a failed publish

Dispatch the workflow on the tag:
`gh workflow run release.yml --ref vX.Y.Z -f version=X.Y.Z`. The `recover` job refuses a version
npm already has, a missing tag, and a run on any other commit. It publishes `latest` only when
the version is above every stable one on npm (else `backport`), and updates the plugin branch
and MCP Registry only when they are older, so a backport fills in neither. Tags up to v3.6.3
predate the job and cannot be recovered this way. If the Registry step alone failed and a
re-run does not fix it, the manual fallback is in CONTRIBUTING.md step 1 and needs the
repository owner's GitHub login.

## Before you report a release problem

Read the tag and workflow run at the commit in question, not a summary of it. An earlier review
reported committed media that was not in git; check `git ls-files` and the run logs first.
