#!/usr/bin/env python3
"""Codex Stop hook: block stopping until the tests pass, at most 5 times per session.

Usage in .codex/hooks.json:  python3 ~/lala/_shared/codex_stop_gate.py "<test command>"
"""

import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

MAX_FAILURES = 5
COUNTERS = Path(tempfile.gettempdir()) / "codex_stop_gate"
TAIL = 20000  # shortcut: only the last 20k chars of test output reach Codex; raise if failures get cut off


def main() -> int:
    if len(sys.argv) != 2:
        print('usage: codex_stop_gate.py "<test command>"', file=sys.stderr)
        return 2
    event = json.load(sys.stdin)
    # session_id becomes a file name, so keep only safe characters.
    session = re.sub(r"[^A-Za-z0-9_-]", "_", str(event.get("session_id") or "unknown"))
    counter = COUNTERS / session
    cwd = event.get("cwd") or os.getcwd()

    root = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=cwd,
                          capture_output=True, text=True)
    if root.returncode != 0:
        output, passed = f"Not inside a Git repository: {cwd}\n{root.stderr}", False
    else:
        tests = subprocess.run(sys.argv[1], shell=True, cwd=root.stdout.strip(),
                               capture_output=True, text=True)
        output, passed = tests.stdout + tests.stderr, tests.returncode == 0

    if passed:
        counter.unlink(missing_ok=True)
        print("{}")
        return 0

    failures = int(counter.read_text()) + 1 if counter.is_file() else 1
    COUNTERS.mkdir(parents=True, exist_ok=True)
    counter.write_text(str(failures))
    if failures <= MAX_FAILURES:
        print(f"Tests failed ({failures}/{MAX_FAILURES}): {sys.argv[1]}\n{output[-TAIL:]}",
              file=sys.stderr)
        return 2
    print(json.dumps({"continue": False,
                      "stopReason": f"Tests still fail after {MAX_FAILURES} attempts: {sys.argv[1]}"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
