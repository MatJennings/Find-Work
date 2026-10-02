#!/usr/bin/env python3
"""Scan a distributable tree for likely personal data and forbidden terms."""

from __future__ import annotations

import argparse
import io
import re
import subprocess
import sys
import zipfile
from pathlib import Path


TEXT_SUFFIXES = {".csv", ".json", ".md", ".ps1", ".py", ".sh", ".toml", ".txt", ".yaml", ".yml"}
OFFICE_SUFFIXES = {".docx", ".pptx", ".xlsx"}
BINARY_ARTIFACT_SUFFIXES = OFFICE_SUFFIXES | {".doc", ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".tif", ".tiff", ".webp"}
SKIP_PARTS = {".git", "__pycache__"}
PII_PATTERNS = {
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "US phone number": re.compile(r"(?<!\d)(?:\+?1[ .-]?)?(?:\(\d{3}\)|\d{3})[ .-]\d{3}[ .-]\d{4}(?!\d)"),
    "Windows user path": re.compile(r"[A-Z]:\\Users\\[A-Z0-9._-]+\\", re.I),
    "macOS user path": re.compile(r"/Users/[A-Z0-9._-]+/", re.I),
}


def forbidden_patterns(terms: list[str]) -> list[tuple[str, re.Pattern[str]]]:
    return [
        (term, re.compile(rf"(?<![A-Z0-9]){re.escape(term)}(?![A-Z0-9])", re.I))
        for term in terms
        if term.strip()
    ]


def scan_text(label: str, text: str, forbidden: list[tuple[str, re.Pattern[str]]], issues: list[str]) -> None:
    for line_number, line in enumerate(text.splitlines() or [text], start=1):
        for name, pattern in PII_PATTERNS.items():
            if pattern.search(line):
                issues.append(f"{label}:{line_number}: possible {name}")
        for term, pattern in forbidden:
            if pattern.search(line):
                issues.append(f"{label}:{line_number}: forbidden term {term!r}")


def scan_zip_bytes(
    label: str,
    raw: bytes,
    forbidden: list[tuple[str, re.Pattern[str]]],
    issues: list[str],
    allow_binary_artifacts: bool,
) -> None:
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as archive:
            for member in archive.infolist():
                if member.is_dir():
                    continue
                member_label = f"{label}:{member.filename}"
                scan_text(f"path {member_label}", member.filename, forbidden, issues)
                member_raw = archive.read(member)
                suffix = Path(member.filename).suffix.lower()
                if suffix in BINARY_ARTIFACT_SUFFIXES and not allow_binary_artifacts:
                    issues.append(f"{member_label}: binary document or image requires explicit release review")
                elif suffix in OFFICE_SUFFIXES:
                    scan_zip_bytes(member_label, member_raw, forbidden, issues, allow_binary_artifacts)
                else:
                    scan_text(member_label, member_raw.decode("latin-1", errors="ignore"), forbidden, issues)
    except zipfile.BadZipFile:
        issues.append(f"{label}: ZIP archive could not be unpacked")


def scan_history_text(text, forbidden, issues, allow_git_identity_metadata=False):
    if allow_git_identity_metadata:
        text = "\n".join(
            "" if re.match(r"^(Author|Commit):\s", line) else line
            for line in text.splitlines()
        )
    scan_text("git history", text, forbidden, issues)


def scan_git(
    root: Path,
    forbidden: list[tuple[str, re.Pattern[str]]],
    issues: list[str],
    allow_binary_artifacts: bool,
    allow_git_identity_metadata: bool = False,
) -> None:
    git_dir = root / ".git"
    if not git_dir.exists():
        return
    config = git_dir / "config"
    if config.is_file():
        scan_text(".git/config", config.read_text(encoding="utf-8", errors="replace"), forbidden, issues)
    result = subprocess.run(
        ["git", "-C", str(root), "log", "--all", "--format=fuller", "--name-status"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        issues.append(f"git history: could not inspect commit metadata ({result.stderr.strip()})")
        return
    scan_history_text(result.stdout, forbidden, issues, allow_git_identity_metadata)

    objects = subprocess.run(
        ["git", "-C", str(root), "rev-list", "--objects", "--all"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if objects.returncode != 0:
        issues.append(f"git history: could not enumerate historical objects ({objects.stderr.strip()})")
        return
    seen: set[str] = set()
    for line in objects.stdout.splitlines():
        object_id, _, historical_path = line.partition(" ")
        if not object_id or object_id in seen:
            continue
        seen.add(object_id)
        object_type = subprocess.run(
            ["git", "-C", str(root), "cat-file", "-t", object_id],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        if object_type.returncode != 0:
            issues.append(f"git object {object_id}: could not inspect type")
            continue
        if object_type.stdout.strip() != "blob":
            continue
        blob = subprocess.run(
            ["git", "-C", str(root), "cat-file", "-p", object_id],
            capture_output=True,
            check=False,
        )
        if blob.returncode != 0:
            issues.append(f"git blob {object_id}: could not inspect historical content")
            continue
        label = f"git blob {object_id} {historical_path}".strip()
        suffix = Path(historical_path).suffix.lower()
        if suffix in BINARY_ARTIFACT_SUFFIXES and not allow_binary_artifacts:
            issues.append(f"{label}: historical binary document or image requires explicit release review")
            continue
        if suffix in OFFICE_SUFFIXES:
            try:
                with zipfile.ZipFile(io.BytesIO(blob.stdout)) as archive:
                    for member in archive.infolist():
                        if member.filename.endswith((".xml", ".rels")):
                            text = archive.read(member).decode("utf-8", errors="replace")
                            scan_text(f"{label}:{member.filename}", text, forbidden, issues)
            except zipfile.BadZipFile:
                issues.append(f"{label}: historical Office artifact could not be unpacked")
        else:
            scan_text(label, blob.stdout.decode("latin-1", errors="ignore"), forbidden, issues)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--forbid", action="append", default=[])
    parser.add_argument("--allow-binary-artifacts", action="store_true")
    parser.add_argument("--check-git-history", action="store_true")
    parser.add_argument("--allow-git-identity-metadata", action="store_true", help="After reviewing public attribution, exempt only Git Author and Commit headers, never messages, paths or file contents")
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    issues: list[str] = []
    forbidden = forbidden_patterns(args.forbid)

    for path in root.rglob("*"):
        if any(part in SKIP_PARTS for part in path.relative_to(root).parts) or not path.is_file():
            continue
        relative = str(path.relative_to(root))
        scan_text(f"path {relative}", relative, forbidden, issues)
        suffix = path.suffix.lower()
        try:
            if suffix in TEXT_SUFFIXES:
                scan_text(relative, path.read_text(encoding="utf-8", errors="replace"), forbidden, issues)
            elif suffix == ".zip":
                scan_zip_bytes(relative, path.read_bytes(), forbidden, issues, args.allow_binary_artifacts)
            elif suffix in BINARY_ARTIFACT_SUFFIXES and not args.allow_binary_artifacts:
                issues.append(f"{relative}: binary document or image requires explicit release review")
            elif suffix in OFFICE_SUFFIXES:
                with zipfile.ZipFile(path) as archive:
                    for member in archive.infolist():
                        if member.filename.endswith((".xml", ".rels")):
                            text = archive.read(member).decode("utf-8", errors="replace")
                            scan_text(f"{relative}:{member.filename}", text, forbidden, issues)
            else:
                scan_text(relative, path.read_bytes().decode("latin-1", errors="ignore"), forbidden, issues)
        except (OSError, zipfile.BadZipFile) as exc:
            issues.append(f"{relative}: could not inspect ({exc})")

    if args.check_git_history:
        scan_git(root, forbidden, issues, args.allow_binary_artifacts, args.allow_git_identity_metadata)

    if issues:
        print("Privacy scan failed:", file=sys.stderr)
        for issue in sorted(set(issues)):
            print(f"  {issue}", file=sys.stderr)
        return 1
    print(f"Privacy scan passed: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
