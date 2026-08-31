#!/usr/bin/env python3
"""Validate the structure and core schemas of a Find Work workspace."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    ".find-work-version",
    "AGENTS.md",
    "START_HERE.md",
    "applications.csv",
    "profile/onboarding_status.md",
    "profile/environment_capabilities.md",
    "profile/candidate_profile.md",
    "profile/job_target_profile.md",
    "profile/resume_preferences.md",
    "profile/cover_letter_preferences.md",
    "profile/confidentiality_preferences.md",
    "experience/chronology.csv",
    "experience/evidence_ledger.csv",
    "experience/skills_and_methods.md",
    "experience/education_and_credentials.md",
    "sources/imported/index.md",
    "sources/authoritative/approved_resume_openings.md",
    "sources/authoritative/approved_cover_letter_openings.md",
    "sources/authoritative/approved_application_answers.md",
    "job_search/roles.csv",
    "job_search/reviewed_roles.md",
    "job_search/search_log.md",
]

REQUIRED_DIRS = [
    "experience/employers",
    "sources/imported",
    "sources/authoritative",
    "sources/style_examples",
    "applications",
]

CSV_HEADERS = {
    "applications.csv": [
        "company", "role", "official_url", "date_verified",
        "corporate_headquarters", "status", "applied_date", "resume_status",
        "cover_letter_status", "date_files_produced", "follow_up_date", "folder",
        "notes",
    ],
    "experience/chronology.csv": [
        "organization", "title", "start_date", "end_date", "location", "source",
        "status", "notes",
    ],
    "experience/evidence_ledger.csv": [
        "claim_id", "organization", "claim", "evidence_status", "source",
        "disclosure_status", "notes",
    ],
    "job_search/roles.csv": [
        "company", "role", "official_url", "requisition_id", "date_found",
        "date_verified", "posting_date_or_age", "status", "recommendation",
        "target_relevance", "job_location", "work_arrangement",
        "corporate_headquarters", "compensation", "compensation_source", "travel",
        "company_size", "ownership", "fit_summary", "gaps", "application_status",
        "last_checked", "notes",
    ],
}

EVIDENCE_VALUES = {
    "user_attested", "document_supported", "publicly_corroborated",
    "needs_clarification",
}
DISCLOSURE_VALUES = {
    "approved_external", "approval_required", "confidential", "do_not_use",
}
APPLICATION_VALUES = {
    "Not started", "Drafting", "Approved", "Ready to apply", "Applied",
    "Will not apply", "Removed",
}
ROLE_VALUES = {"active", "uncertain", "closed", "removed"}
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def read_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def valid_optional_date(value: str) -> bool:
    return not value.strip() or bool(ISO_DATE.fullmatch(value.strip()))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--allow-missing-version", action="store_true")
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    errors: list[str] = []

    for relative in REQUIRED_FILES:
        if relative == ".find-work-version" and args.allow_missing_version:
            continue
        if not (root / relative).is_file():
            errors.append(f"Missing file: {relative}")
    for relative in REQUIRED_DIRS:
        if not (root / relative).is_dir():
            errors.append(f"Missing directory: {relative}")

    data: dict[str, list[dict[str, str]]] = {}
    for relative, expected in CSV_HEADERS.items():
        path = root / relative
        if not path.is_file():
            continue
        actual, rows = read_rows(path)
        data[relative] = rows
        if actual != expected:
            errors.append(f"Unexpected CSV header in {relative}: {actual}")

    claims = data.get("experience/evidence_ledger.csv", [])
    claim_ids = [row.get("claim_id", "").strip() for row in claims if row.get("claim_id", "").strip()]
    if len(claim_ids) != len(set(claim_ids)):
        errors.append("Duplicate claim IDs in experience/evidence_ledger.csv")
    for number, row in enumerate(claims, start=2):
        if row.get("evidence_status") not in EVIDENCE_VALUES:
            errors.append(f"Invalid evidence_status at evidence ledger row {number}")
        if row.get("disclosure_status") not in DISCLOSURE_VALUES:
            errors.append(f"Invalid disclosure_status at evidence ledger row {number}")

    for number, row in enumerate(data.get("applications.csv", []), start=2):
        status = row.get("status", "")
        if status and status not in APPLICATION_VALUES:
            errors.append(f"Invalid application status at applications.csv row {number}: {status}")
        for field in ("date_verified", "applied_date", "date_files_produced", "follow_up_date"):
            if not valid_optional_date(row.get(field, "")):
                errors.append(f"Invalid {field} at applications.csv row {number}")
        folder = row.get("folder", "").replace("\\", "/").strip("/")
        if folder and (
            folder.startswith("applications/in_progress/")
            or folder.startswith("applications/files_produced/")
        ):
            errors.append(f"Application row {number} uses a status-based folder")
        if folder and (not folder.startswith("applications/") or folder.count("/") != 1):
            errors.append(f"Application row {number} does not point to applications/<Company>")
        if status in {"Ready to apply", "Applied"} and not folder:
            errors.append(f"{status} row {number} is missing its permanent application folder")
        if status == "Ready to apply" and not row.get("date_files_produced", "").strip():
            errors.append(f"Ready to apply row {number} is missing date_files_produced")
        if status == "Applied" and not row.get("applied_date", "").strip():
            notes = row.get("notes", "").lower()
            if "date unknown" not in notes and "date not confirmed" not in notes:
                errors.append(
                    f"Applied row {number} needs applied_date or an explicit unknown-date note"
                )

    for number, row in enumerate(data.get("job_search/roles.csv", []), start=2):
        status = row.get("status", "")
        if status and status not in ROLE_VALUES:
            errors.append(f"Invalid role status at job_search/roles.csv row {number}: {status}")
        application_status = row.get("application_status", "")
        if application_status and application_status not in APPLICATION_VALUES:
            errors.append(
                f"Invalid application_status at job_search/roles.csv row {number}: {application_status}"
            )

    for relative, date_fields in {
        "experience/chronology.csv": ["start_date", "end_date"],
        "job_search/roles.csv": ["date_found", "date_verified", "last_checked"],
    }.items():
        for number, row in enumerate(data.get(relative, []), start=2):
            for field in date_fields:
                if not valid_optional_date(row.get(field, "")):
                    errors.append(f"Invalid {field} at {relative} row {number}")

    if errors:
        print("Workspace validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1
    print(f"Workspace validation passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
