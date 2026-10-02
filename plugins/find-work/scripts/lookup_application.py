"""Read-only lookup of canonical role and application trackers and local records."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

ROOT = Path.cwd()
TRACKERS = ("job_search/roles.csv", "applications.csv")
RECORD_FILES = ("README.md", "role_review.md", "hook_decision_card.md",
                "draft_learning_record.md", "approved_application_wording.md")


def normalized(value: str) -> str:
    return " ".join(value.split()).casefold()


def folder_name(value: str) -> str:
    return normalized(value.replace("_", " "))


def normalized_url(value: str) -> str:
    parts = urlsplit(value.strip())
    if parts.scheme.lower() not in {"https", "http"} or not parts.hostname or parts.username or parts.password:
        raise ValueError("URL must be an HTTP(S) URL without credentials")
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if not k.casefold().startswith("utm_")]
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path.rstrip("/"),
                       urlencode(sorted(query)), parts.fragment))


def inside(root: Path, path: Path) -> Path:
    resolved = path.resolve()
    if not resolved.is_relative_to(root):
        raise ValueError(f"Path escapes workspace: {path.name}")
    return resolved


def load_tracker(root: Path, relative: str) -> tuple[list[dict], dict]:
    path = inside(root, root / relative)
    raw = path.read_bytes()
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")), strict=True)
    fields = reader.fieldnames or []
    if len(fields) != len(set(fields)) or not {"company", "role", "official_url"}.issubset(fields):
        raise ValueError(f"Invalid tracker header: {relative}")
    records = []
    warning_count = 0
    warning_refs = []
    for number, row in enumerate(reader, start=1):
        missing = [key for key in fields if row.get(key) is None]
        extra = row.pop(None, [])
        warnings = []
        if extra or missing:
            warning_count += 1
            warnings.append({"type": "irregular_row", "extra_fields_count": len(extra), "missing_fields": missing})
        if not row.get("company") or not row.get("role"):
            warnings.append({"type": "missing_identity"})
        if warnings:
            warning_refs.append({"record_number": number, "end_line": reader.line_num, "warnings": warnings})
        records.append({"source": relative, "record_number": number,
                        "end_line": reader.line_num, "fields": row,
                        "extra_fields": extra, "warnings": warnings})
    return records, {"path": relative, "sha256": hashlib.sha256(raw).hexdigest(),
                     "bytes_read": len(raw), "records_scanned": len(records),
                     "irregular_rows": warning_count, "warning_records": warning_refs}


def matches(record: dict, selectors: dict, contains: bool) -> bool:
    row = record["fields"]
    for key in ("company", "role", "requisition_id"):
        if selectors.get(key):
            wanted, actual = normalized(selectors[key]), normalized(row.get(key) or "")
            if (contains and key != "requisition_id" and wanted not in actual) or ((not contains or key == "requisition_id") and wanted != actual):
                return False
    if selectors.get("url"):
        try:
            if normalized_url(row.get("official_url") or "") != normalized_url(selectors["url"]):
                return False
        except ValueError:
            return False
    return True


def record_key(record: dict) -> tuple[str, str]:
    row = record["fields"]
    return normalized(row.get("company") or ""), normalized(row.get("role") or "")


def local_records(root: Path, identities: set[tuple[str, str]], include_context: bool) -> tuple[list[dict], list[dict]]:
    """Inspect directory names, then read only matching company and role records."""
    base = inside(root, root / "applications")
    if not base.exists():
        return [], [{"type": "applications_directory_missing"}]
    companies = {folder_name(company) for company, _ in identities}
    found, warnings = [], []
    for directory in sorted(base.iterdir()):
        if folder_name(directory.name) not in companies or not directory.is_dir():
            continue
        try:
            company_dir = inside(root, directory)
            role_names = {folder_name(role) for company, role in identities if folder_name(company) == folder_name(directory.name)}
            locations = [(company_dir, "company-level")]
            for child in sorted(company_dir.iterdir()):
                if folder_name(child.name) in role_names and child.is_dir():
                    locations.append((inside(root, child), "role-level"))
            for location, scope in locations:
                files = []
                for name in RECORD_FILES:
                    candidate = location / name
                    if candidate.is_file():
                        file = inside(root, candidate)
                        entry = {"path": file.relative_to(root).as_posix()}
                        if include_context and name in {"README.md", "role_review.md"}:
                            raw = file.read_bytes()
                            entry.update(text=raw.decode("utf-8-sig"), sha256=hashlib.sha256(raw).hexdigest(), bytes_read=len(raw))
                        files.append(entry)
                found.append({"directory": location.relative_to(root).as_posix(), "scope": scope, "files": files})
        except (OSError, ValueError) as exc:
            warnings.append({"type": "local_record_unavailable", "directory": directory.name, "reason": str(exc)})
    return found, warnings


def tracker_snapshot(root: Path) -> tuple:
    """Read both canonical trackers once, retaining diagnostics and raw fields."""
    records, sources, warnings = [], [], []
    for relative in TRACKERS:
        try:
            rows, metadata = load_tracker(root, relative)
            records.extend(rows)
            sources.append(metadata)
        except (OSError, ValueError, csv.Error) as exc:
            warnings.append({"type": "tracker_unavailable", "source": relative, "reason": str(exc)})
    return records, sources, warnings


def lookup(root: Path, selectors: dict, *, contains: bool = False, include_context: bool = False,
           _snapshot: tuple | None = None) -> dict:
    root = root.resolve()
    selectors = {key: value.strip() for key, value in selectors.items() if value and value.strip()}
    if not selectors or set(selectors) - {"company", "role", "requisition_id", "url"}:
        raise ValueError("Provide at least one supported nonempty selector")
    if "url" in selectors:
        normalized_url(selectors["url"])
    records, sources, source_warnings = tracker_snapshot(root) if _snapshot is None else _snapshot
    warnings = list(source_warnings)
    direct = [r for r in records if matches(r, selectors, contains)]
    identities = {record_key(r) for r in direct if all(record_key(r))}
    selected = []
    for record in records:
        if record in direct or record_key(record) in identities:
            selected.append({**record, "match_type": "direct" if record in direct else "company_role_candidate"})
    groups = []
    for company, role in sorted(identities):
        group = [r for r in selected if record_key(r) == (company, role)]
        requisitions = sorted({r["fields"].get("requisition_id") for r in group if r["fields"].get("requisition_id")})
        counts = {source: sum(r["source"] == source for r in group) for source in TRACKERS}
        identity_ambiguous = len(requisitions) > 1 or any(count > 1 for count in counts.values())
        groups.append({"company": group[0]["fields"]["company"], "role": group[0]["fields"]["role"],
                       "record_refs": [{"source": r["source"], "record_number": r["record_number"]} for r in group],
                       "requisition_ids": requisitions, "identity_ambiguous": identity_ambiguous})
    ambiguous = len(groups) > 1 or any(g["identity_ambiguous"] for g in groups)
    incomplete = bool(warnings) or any(r["warnings"] for r in records) or any(s["irregular_rows"] for s in sources)
    directories, path_warnings = local_records(root, identities, include_context) if identities else ([], [])
    warnings.extend(path_warnings)
    incomplete = incomplete or bool(path_warnings)
    if any(s["irregular_rows"] for s in sources):
        warnings.append({"type": "irregular_tracker_rows", "reason": "Malformed records can affect field alignment. Inspect source rows before a definitive no-match or decision."})
    return {
        "version": 1, "query": selectors, "match_mode": "contains" if contains else "exact",
        "result": "ambiguous" if ambiguous else "match" if direct else "no_match",
        "lookup_complete": not incomplete,
        "direct_match_count": len(direct), "records": selected, "role_groups": groups,
        "local_records": directories, "sources": sources, "warnings": warnings,
        "limitations": ["Stored verification is historical, not a live status check.",
                        "Company and title links are candidates, not proof that differing URLs or requisitions identify the same opening.",
                        "File existence is not wording approval, production validation, submission or a next-action decision.",
                        "Read the target records for outstanding questions and chronology. Returned notes are not parsed into new facts.",
                        "No matching tracker row does not prove no prior application exists. Untracked folders are not searched."]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--company")
    parser.add_argument("--role")
    parser.add_argument("--requisition-id")
    parser.add_argument("--url")
    parser.add_argument("--contains", action="store_true", help="Substring matching for company/title only")
    parser.add_argument("--include-context", action="store_true", help="Read matching README and role review text")
    args = parser.parse_args()
    try:
        report = lookup(args.root, {"company": args.company, "role": args.role, "requisition_id": args.requisition_id, "url": args.url},
                        contains=args.contains, include_context=args.include_context)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["lookup_complete"] else 2


if __name__ == "__main__":
    sys.exit(main())
