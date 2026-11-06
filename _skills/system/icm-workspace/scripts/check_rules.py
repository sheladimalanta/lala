#!/usr/bin/env python3
"""Catch a rule that changed in one file and not the others.

This is the generalized copy of the checker first written for
~/va-resume-v3. The incident that produced it: on 2026-08-08 the output
format was revised four times in ninety minutes, and a role playbook
carried a copy of the old format for nine hours. Nothing failed. Nothing
complained. It was found by accident. This script is the thing that would
have complained.

It is not clever. Each derived file declares what it derives from, and the
map records the hash of every dependency as of the last time a person
looked at the pair. If a dependency's content has changed since then, the
derived file is STALE until someone either updates it or blesses it with a
recorded reason.

Installed into a workspace as `_shared/check-rules.py`, next to the
`_shared/rule-map.json` it reads. What counts as the factory is declared in
that map under `_scan`, so this file is identical in every workspace.

  python3 _shared/check-rules.py
  python3 _shared/check-rules.py --bless <file> --reason "why no change was needed"
  python3 _shared/check-rules.py --register <file> --derives-from a.md,b.md
  python3 _shared/check-rules.py --register <file> --independent

Exit code is 1 when anything needs attention, so it can gate a commit.
"""

import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAP_PATH = ROOT / "_shared" / "rule-map.json"
SELF = "_shared/check-rules.py"

# Fallback only. The workspace declares its own factory under `_scan`.
DEFAULT_SCAN = {
    "dirs": ["_shared", "_templates"],
    "files": ["CONTEXT.md", "CLAUDE.md"],
    "ignore": [".git", ".obsidian", "_index"],
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def load_map() -> dict:
    if not MAP_PATH.exists():
        sys.exit(f"No rule map at {MAP_PATH}")
    return json.loads(MAP_PATH.read_text())


def save_map(m: dict) -> None:
    MAP_PATH.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")


def scan_config(m: dict) -> dict:
    cfg = dict(DEFAULT_SCAN)
    cfg.update(m.get("_scan", {}))
    return cfg


def discover(m: dict) -> set:
    """Every markdown file in the factory, so nothing hides by being unlisted.

    Records are deliberately out of scope. A delivered piece of work is a
    snapshot of the rules on its delivery date, not a derived file that
    should follow them forward.
    """
    cfg = scan_config(m)
    ignore = set(cfg["ignore"])
    found = set()
    for d in cfg["dirs"]:
        base = ROOT / d
        if not base.exists():
            continue
        for p in base.rglob("*.md"):
            if ignore & set(p.relative_to(ROOT).parts):
                continue
            found.add(str(p.relative_to(ROOT)))
    for f in cfg["files"]:
        if (ROOT / f).exists():
            found.add(f)
    return found


def audit(m: dict):
    files = m.get("files", {})
    independent = set(m.get("independent", []))

    stale, missing = [], []
    for rel, entry in sorted(files.items()):
        if not (ROOT / rel).exists():
            missing.append(f"{rel} (registered, but the file is gone)")
            continue
        for dep, recorded in sorted(entry.get("derives_from", {}).items()):
            dep_path = ROOT / dep
            if not dep_path.exists():
                missing.append(f"{rel} depends on {dep}, which is gone")
                continue
            current = digest(dep_path)
            if current != recorded:
                stale.append((rel, dep, recorded, current))

    for rel in sorted(independent):
        if not (ROOT / rel).exists():
            missing.append(f"{rel} (registered independent, but the file is gone)")

    unregistered = sorted(discover(m) - set(files) - independent)
    return stale, unregistered, missing


def report(stale, unregistered, missing) -> int:
    if not (stale or unregistered or missing):
        print("Rule map clean. Every derived file was checked against its "
              "current dependencies.")
        return 0

    if stale:
        print(f"\nSTALE — {len(stale)} file(s) derive from a rule that has "
              f"changed since they were last checked\n")
        by_file = {}
        for rel, dep, _, _ in stale:
            by_file.setdefault(rel, []).append(dep)
        for rel, deps in by_file.items():
            print(f"  {rel}")
            for dep in deps:
                print(f"      changed: {dep}")
        print("\n  Open each one. Update it, or bless it:")
        print(f'      python3 {SELF} --bless <file> --reason "why no change was needed"')

    if unregistered:
        print(f"\nUNREGISTERED — {len(unregistered)} factory file(s) are not "
              f"in the map, so nothing tracks whether they drift\n")
        for rel in unregistered:
            print(f"  {rel}")
        print("\n  Register each one:")
        print(f"      python3 {SELF} --register <file> --derives-from a.md,b.md")
        print(f"      python3 {SELF} --register <file> --independent")

    if missing:
        print(f"\nMISSING — {len(missing)} map entr(ies) point at files that "
              f"no longer exist\n")
        for line in missing:
            print(f"  {line}")

    print()
    return 1


def bless(m: dict, targets, reason: str) -> None:
    stale, _, _ = audit(m)
    if not stale:
        print("Nothing is stale.")
        return
    chosen = [s for s in stale if not targets or s[0] in targets]
    if not chosen:
        print(f"Nothing stale among: {', '.join(targets)}")
        return

    today = date.today().isoformat()
    for rel, dep, _, current in chosen:
        m["files"][rel]["derives_from"][dep] = current
        m.setdefault("blessings", []).append(
            {"date": today, "file": rel, "dependency": dep, "reason": reason}
        )
        print(f"blessed  {rel}  <-  {dep}")
    save_map(m)
    print(f"\nRecorded against: {reason}")


def register(m: dict, rel: str, deps, independent: bool) -> None:
    if not (ROOT / rel).exists():
        sys.exit(f"No such file: {rel}")
    m.setdefault("files", {})
    m.setdefault("independent", [])

    if independent:
        m["files"].pop(rel, None)
        if rel not in m["independent"]:
            m["independent"].append(rel)
            m["independent"].sort()
        print(f"registered  {rel}  (independent — derives from nothing)")
    else:
        if rel in m["independent"]:
            m["independent"].remove(rel)
        recorded = {}
        for dep in deps:
            dep_path = ROOT / dep
            if not dep_path.exists():
                sys.exit(f"Dependency does not exist: {dep}")
            recorded[dep] = digest(dep_path)
        entry = m["files"].get(rel, {})
        entry["derives_from"] = recorded
        m["files"][rel] = entry
        print(f"registered  {rel}  <-  {', '.join(deps)}")
    save_map(m)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bless", nargs="+", metavar="FILE",
                    help="accept the current dependency content for these files")
    ap.add_argument("--bless-all", action="store_true",
                    help="bless every stale file at once. Use only when one reason "
                         "honestly covers all of them; otherwise bless in groups.")
    ap.add_argument("--reason", help="required with --bless: why no change was needed")
    ap.add_argument("--register", metavar="FILE", help="add a file to the map")
    ap.add_argument("--derives-from", default="",
                    help="comma-separated dependency paths, used with --register")
    ap.add_argument("--independent", action="store_true",
                    help="used with --register: this file derives from nothing")
    args = ap.parse_args()

    m = load_map()

    if args.register:
        deps = [d.strip() for d in args.derives_from.split(",") if d.strip()]
        if not deps and not args.independent:
            sys.exit("--register needs either --derives-from or --independent")
        register(m, args.register, deps, args.independent)
        return 0

    if args.bless is not None or args.bless_all:
        if not args.reason:
            sys.exit("--bless requires --reason. A blessing without a recorded "
                     "reason is indistinguishable from a miss.")
        targets = args.bless or []
        if args.bless_all:
            stale, _, _ = audit(m)
            names = sorted({s[0] for s in stale})
            print("Blessing all of these against one reason:")
            for n in names:
                print(f"  {n}")
            print("If that reason does not honestly describe every file above, "
                  "stop and bless them in groups instead.\n")
            targets = []
        bless(m, targets, args.reason)
        return 0

    return report(*audit(m))


if __name__ == "__main__":
    sys.exit(main())
