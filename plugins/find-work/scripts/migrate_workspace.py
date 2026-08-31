#!/usr/bin/env python3
"""Apply versioned, non-destructive Find Work workspace migrations."""

from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import sys
from pathlib import Path


ROLES_V1_FIELDS = [
    "company", "role", "official_url", "requisition_id", "date_found",
    "date_verified", "status", "recommendation", "location", "compensation",
    "fit_summary", "gaps", "last_checked", "notes",
]
ROLES_V2_FIELDS = [
    "company", "role", "official_url", "requisition_id", "date_found",
    "date_verified", "posting_date_or_age", "status", "recommendation",
    "target_relevance", "job_location", "work_arrangement",
    "corporate_headquarters", "compensation", "compensation_source", "travel",
    "company_size", "ownership", "fit_summary", "gaps", "application_status",
    "last_checked", "notes",
]
APPLICATIONS_V2_FIELDS = [
    "company", "role", "official_url", "status", "date_files_produced",
    "folder", "notes",
]
APPLICATIONS_V3_FIELDS = [
    "company", "role", "official_url", "date_verified",
    "corporate_headquarters", "status", "applied_date", "resume_status",
    "cover_letter_status", "date_files_produced", "follow_up_date", "folder",
    "notes",
]


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


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def migrate_evidence_v0(path: Path) -> bool:
    if not path.is_file():
        return True
    fields, rows = read_csv(path)
    current = [
        "claim_id", "organization", "claim", "evidence_status", "source",
        "disclosure_status", "notes",
    ]
    legacy = [
        "claim_id", "organization", "claim", "evidence_level", "source",
        "external_use", "notes",
    ]
    if fields == current:
        return True
    if fields != legacy:
        print(f"Cannot migrate unsupported evidence-ledger header: {fields}", file=sys.stderr)
        return False

    backup = path.with_name("evidence_ledger.v0.backup.csv")
    if not backup.exists():
        shutil.copy2(path, backup)
    evidence_values = {
        "user_attested", "document_supported", "publicly_corroborated",
        "needs_clarification",
    }
    disclosure_values = {
        "approved_external", "approval_required", "confidential", "do_not_use",
    }
    migrated = []
    for row in rows:
        old_evidence = (row.get("evidence_level") or "").strip()
        old_disclosure = (row.get("external_use") or "").strip()
        migrated.append({
            "claim_id": row.get("claim_id", ""),
            "organization": row.get("organization", ""),
            "claim": row.get("claim", ""),
            "evidence_status": old_evidence if old_evidence in evidence_values else "needs_clarification",
            "source": row.get("source", ""),
            "disclosure_status": (
                old_disclosure if old_disclosure in disclosure_values
                else old_evidence if old_evidence in disclosure_values
                else "approval_required"
            ),
            "notes": row.get("notes", ""),
        })
    write_csv(path, current, migrated)
    return True


def application_move_plan(target: Path) -> list[tuple[Path, Path]] | None:
    applications = target / "applications"
    plan: list[tuple[Path, Path]] = []
    destinations: set[Path] = set()
    for status_name in ("in_progress", "files_produced"):
        source_root = applications / status_name
        if not source_root.is_dir():
            continue
        unexpected = [
            item for item in source_root.iterdir()
            if item.is_file() and item.name != ".gitkeep"
        ]
        if unexpected:
            print(f"Cannot migrate unexpected files in {source_root}:", file=sys.stderr)
            for item in unexpected:
                print(f"  {item.name}", file=sys.stderr)
            return None
        for source in sorted(
            (item for item in source_root.iterdir() if item.is_dir()),
            key=lambda item: item.name.lower(),
        ):
            destination = applications / source.name
            if destination.exists() or destination in destinations:
                print(
                    f"Cannot migrate application folder because the destination is ambiguous: {destination}",
                    file=sys.stderr,
                )
                return None
            destinations.add(destination)
            plan.append((source, destination))
    return plan


def migrate_roles_v1_to_v2(path: Path) -> bool:
    if not path.is_file():
        return True
    fields, rows = read_csv(path)
    if fields == ROLES_V2_FIELDS:
        return True
    if fields != ROLES_V1_FIELDS:
        print(f"Cannot migrate unsupported roles header: {fields}", file=sys.stderr)
        return False
    backup = path.with_name("roles.v1.backup.csv")
    if not backup.exists():
        shutil.copy2(path, backup)
    migrated = []
    for row in rows:
        migrated.append({
            **row,
            "posting_date_or_age": "",
            "target_relevance": "",
            "job_location": row.get("location", ""),
            "work_arrangement": "",
            "corporate_headquarters": "",
            "compensation_source": "",
            "travel": "",
            "company_size": "",
            "ownership": "",
            "application_status": "",
        })
    write_csv(path, ROLES_V2_FIELDS, migrated)
    return True


def migrate_applications_v1_to_v2(target: Path) -> bool:
    plan = application_move_plan(target)
    if plan is None:
        return False
    applications_csv = target / "applications.csv"
    fields: list[str] = []
    rows: list[dict[str, str]] = []
    if applications_csv.is_file():
        fields, rows = read_csv(applications_csv)
        if fields != APPLICATIONS_V2_FIELDS:
            print(f"Cannot migrate unsupported applications header: {fields}", file=sys.stderr)
            return False
    if not migrate_roles_v1_to_v2(target / "job_search" / "roles.csv"):
        return False
    if applications_csv.is_file():
        backup = applications_csv.with_name("applications.v1.backup.csv")
        if not backup.exists():
            shutil.copy2(applications_csv, backup)
        for row in rows:
            folder = (row.get("folder") or "").replace("\\", "/")
            for prefix in ("applications/in_progress/", "applications/files_produced/"):
                if folder.startswith(prefix):
                    row["folder"] = f"applications/{folder[len(prefix):]}"
                    break
    for source, destination in plan:
        shutil.move(str(source), str(destination))
    if applications_csv.is_file():
        write_csv(applications_csv, fields, rows)
    for status_name in ("in_progress", "files_produced"):
        legacy_root = target / "applications" / status_name
        marker = legacy_root / ".gitkeep"
        if marker.is_file():
            marker.unlink()
        if legacy_root.is_dir() and not any(legacy_root.iterdir()):
            legacy_root.rmdir()
    return True


def migrate_applications_v2_to_v3(path: Path) -> bool:
    if not path.is_file():
        return True
    fields, rows = read_csv(path)
    if fields == APPLICATIONS_V3_FIELDS:
        return True
    if fields != APPLICATIONS_V2_FIELDS:
        print(f"Cannot migrate unsupported applications header: {fields}", file=sys.stderr)
        return False
    backup = path.with_name("applications.v2.backup.csv")
    if not backup.exists():
        shutil.copy2(path, backup)
    migrated = []
    for row in rows:
        old_status = (row.get("status") or "").strip()
        new_status = {
            "Reviewing": "Not started",
            "Files produced": "Ready to apply",
        }.get(old_status, old_status)
        notes = row.get("notes", "")
        if old_status == "Files produced":
            migration_note = "Migrated from Files produced; confirm each document status."
            notes = f"{notes} {migration_note}".strip()
        migrated.append({
            "company": row.get("company", ""),
            "role": row.get("role", ""),
            "official_url": row.get("official_url", ""),
            "date_verified": "",
            "corporate_headquarters": "",
            "status": new_status,
            "applied_date": "",
            "resume_status": "",
            "cover_letter_status": "",
            "date_files_produced": row.get("date_files_produced", ""),
            "follow_up_date": "",
            "folder": row.get("folder", ""),
            "notes": notes,
        })
    write_csv(path, APPLICATIONS_V3_FIELDS, migrated)
    return True


def migrate_role_application_status_v2_to_v3(path: Path) -> bool:
    if not path.is_file():
        return True
    fields, rows = read_csv(path)
    if fields != ROLES_V2_FIELDS:
        print(f"Cannot migrate unsupported roles header: {fields}", file=sys.stderr)
        return False
    changed = False
    for row in rows:
        old_status = (row.get("application_status") or "").strip()
        new_status = {
            "Reviewing": "Not started",
            "Files produced": "Ready to apply",
        }.get(old_status, old_status)
        if new_status != old_status:
            row["application_status"] = new_status
            changed = True
    if changed:
        backup = path.with_name("roles.v2.backup.csv")
        if not backup.exists():
            shutil.copy2(path, backup)
        write_csv(path, ROLES_V2_FIELDS, rows)
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
        current = 1
    if current < 2:
        if not migrate_applications_v1_to_v2(target):
            return 1
        current = 2
    if current < 3:
        if not migrate_applications_v2_to_v3(target / "applications.csv"):
            return 1
        if not migrate_role_application_status_v2_to_v3(target / "job_search" / "roles.csv"):
            return 1
        current = 3

    copy_missing_scaffold(source, target)
    validation = subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("validate_workspace.py")),
            str(target),
            "--allow-missing-version",
        ],
        check=False,
    )
    if validation.returncode != 0:
        print("Workspace migration did not validate. The version marker was not advanced.", file=sys.stderr)
        return 1
    version_file.write_text(f"{latest}\n", encoding="utf-8")
    print(f"Workspace is current at schema version {latest}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
