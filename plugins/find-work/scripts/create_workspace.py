#!/usr/bin/env python3
"""Create a private Find Work workspace from the bundled blank scaffold."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def same_bytes(left: Path, right: Path) -> bool:
    return left.stat().st_size == right.stat().st_size and left.read_bytes() == right.read_bytes()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--merge", action="store_true", help="Allow adding missing files to a nonempty target")
    args = parser.parse_args()

    source = Path(__file__).resolve().parents[1] / "assets" / "workspace"
    target = args.target.expanduser().resolve()
    if not source.is_dir():
        print(f"Workspace scaffold is missing: {source}", file=sys.stderr)
        return 2
    if source == target or source in target.parents or target in source.parents:
        print("Refusing to initialize in, above, or below the plugin source tree.", file=sys.stderr)
        return 2

    if target.exists() and any(target.iterdir()) and not args.merge:
        print("Target is not empty. Use --merge only after reviewing the existing workspace.", file=sys.stderr)
        return 1

    conflicts: list[str] = []
    created: list[str] = []

    for item in source.rglob("*"):
        relative = item.relative_to(source)
        destination = target / relative
        if item.is_dir():
            continue
        if destination.exists():
            if not destination.is_file() or not same_bytes(item, destination):
                conflicts.append(str(relative))
            continue
        created.append(str(relative))

    if conflicts:
        print("Workspace contains conflicting files. Nothing was overwritten:", file=sys.stderr)
        for path in conflicts:
            print(f"  {path}", file=sys.stderr)
        return 1

    target.mkdir(parents=True, exist_ok=True)
    for item in source.rglob("*"):
        relative = item.relative_to(source)
        destination = target / relative
        if item.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        elif not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, destination)

    print(f"Workspace ready: {target}")
    print(f"Created {len(created)} files; existing identical files were preserved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
