#!/usr/bin/env python3
"""PostToolUse hook: after an Edit/Write of SKILL.md, fail loudly if it is over its byte budget.

SKILL.md is loaded into every session, so tests/test_contract.py caps it at 30,000 bytes
(test_skill_md_stays_under_the_30kb_budget). This gives the same answer right after the edit
instead of minutes later. Exit 2 puts the message in front of the agent; anything unexpected
exits 0, because a broken guard must never block work.
"""
import json
import sys
from pathlib import Path

BUDGET = 30_000

try:
    path = Path(json.load(sys.stdin).get("tool_input", {}).get("file_path", ""))
    if path.name == "SKILL.md" and path.parent.name != "skills" and path.parent == Path.cwd():
        size = path.stat().st_size
        if size > BUDGET:
            print(f"SKILL.md is {size} bytes, {size - BUDGET} over its {BUDGET}-byte budget "
                  "(CONTRIBUTING.md): trim a line for every line you add.", file=sys.stderr)
            sys.exit(2)
except SystemExit:
    raise
except Exception:
    pass
