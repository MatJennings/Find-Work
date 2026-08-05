#!/usr/bin/env python3
"""Apply versioned, non-destructive Find Work workspace migrations."""

from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import sys
from pathlib import Path


def copy_missing_scaffold(source: Path, target: Path) -> None:
    for item in source.rglob("*"):
        relative = item.relative_to(source)
        if str(relative) == ".find-work-version":
            continue
        destination = target / relative
        if item.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        elif not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, destination)


def migrate_evidence_v0(path: Path) -> bool:
    if not path.is_file():
        return True
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        current = ["claim_id", "organization", "claim", "evidence_status", "source", "disclosure_status", "notes"]
        legacy = ["claim_id", "organization", "claim", "evidence_level", "source", "external_use", "notes"]
        if reader.fieldnames == current:
            return True
        if reader.fieldnames != legacy:
            print(f"Cannot migrate unsupported evidence-ledger header: {reader.fieldnames}", file=sys.stderr)
            return False
        rows = list(reader)

    backup = path.with_name("evidence_ledger.v0.backup.csv")
    if not backup.exists():
        shutil.copy2(path, backup)
    evidence_values = {"user_attested", "document_supported", "publicly_corroborated", "needs_clarification"}
    disclosure_values = {"approved_external", "approval_required", "confidential", "do_not_use"}
    fields = ["claim_id", "organization", "claim", "evidence_status", "source", "disclosure_status", "notes"]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            old_evidence = (row.get("evidence_level") or "").strip()
            old_disclosure = (row.get("external_use") or "").strip()
            writer.writerow({
                "claim_id": row.get("claim_id", ""),
                "organization": row.get("organization", ""),
                "claim": row.get("claim", ""),
                "evidence_status": old_evidence if old_evidence in evidence_values else "needs_clarification",
                "source": row.get("source", ""),
                "disclosure_status": old_disclosure if old_disclosure in disclosure_values else (old_evidence if old_evidence in disclosure_values else "approval_required"),
                "notes": row.get("notes", ""),
            })
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, type=Path)
    args = parser.parse_args()

    source = Path(__file__).resolve().parents[1] / "assets" / "workspace"
    target = args.target.expanduser().resolve()
    if not target.is_dir() or not (target / "AGENTS.md").is_file():
        print("Target does not appear to be an existing Find Work workspace.", file=sys.stderr)
        return 1

    latest = int((source / ".find-work-version").read_text(encoding="utf-8").strip())
    version_file = target / ".find-work-version"
    current = int(version_file.read_text(encoding="utf-8").strip()) if version_file.is_file() else 0
    if current > latest:
        print(f"Workspace version {current} is newer than plugin version {latest}.", file=sys.stderr)
        return 1

    if current < 1:
        if not migrate_evidence_v0(target / "experience" / "evidence_ledger.csv"):
            return 1
        copy_missing_scaffold(source, target)
        validation = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("validate_workspace.py")), str(target), "--allow-missing-version"],
            check=False,
        )
        if validation.returncode != 0:
            print("Workspace migration did not validate. The version marker was not advanced.", file=sys.stderr)
            return 1
        version_file.write_text("1\n", encoding="utf-8")
        current = 1

    print(f"Workspace is current at schema version {current}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
