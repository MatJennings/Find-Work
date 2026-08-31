from __future__ import annotations

import csv
import shutil
import subprocess
import sys
import unittest
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "find-work"
SCRIPTS = PLUGIN / "scripts"


class WorkspaceToolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.test_temp = ROOT / ".test-tmp"
        cls.test_temp.mkdir(exist_ok=True)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.test_temp, ignore_errors=True)

    def run_script(self, name: str, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPTS / name), *arguments],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_create_and_validate_current_workspace(self) -> None:
        temporary = self.test_temp / uuid.uuid4().hex
        temporary.mkdir()
        try:
            target = temporary / "workspace"
            created = self.run_script("create_workspace.py", "--target", str(target))
            self.assertEqual(0, created.returncode, created.stderr)
            validated = self.run_script("validate_workspace.py", str(target))
            self.assertEqual(0, validated.returncode, validated.stderr)
            self.assertEqual("3", (target / ".find-work-version").read_text(encoding="utf-8").strip())
        finally:
            shutil.rmtree(temporary, ignore_errors=True)

    def test_v2_files_produced_migrates_to_ready_to_apply(self) -> None:
        temporary = self.test_temp / uuid.uuid4().hex
        temporary.mkdir()
        try:
            target = temporary / "workspace"
            shutil.copytree(PLUGIN / "assets" / "workspace", target)
            (target / ".find-work-version").write_text("2\n", encoding="utf-8")
            for relative in (
                "sources/authoritative/approved_resume_openings.md",
                "sources/authoritative/approved_cover_letter_openings.md",
                "sources/authoritative/approved_application_answers.md",
            ):
                (target / relative).unlink()
            old_fields = [
                "company", "role", "official_url", "status", "date_files_produced",
                "folder", "notes",
            ]
            with (target / "applications.csv").open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=old_fields)
                writer.writeheader()
                writer.writerow({
                    "company": "Example Company",
                    "role": "Example Role",
                    "official_url": "https://example.invalid/job",
                    "status": "Files produced",
                    "date_files_produced": "2026-08-31",
                    "folder": "applications/Example_Company",
                    "notes": "Synthetic migration fixture",
                })
            roles_path = target / "job_search" / "roles.csv"
            with roles_path.open("r", encoding="utf-8", newline="") as handle:
                role_fields = list(csv.DictReader(handle).fieldnames or [])
            with roles_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=role_fields)
                writer.writeheader()
                writer.writerow({
                    "company": "Example Company",
                    "role": "Example Role",
                    "official_url": "https://example.invalid/job",
                    "status": "active",
                    "application_status": "Files produced",
                    "date_found": "2026-08-30",
                    "date_verified": "2026-08-31",
                    "last_checked": "2026-08-31",
                })
            (target / "applications" / "Example_Company").mkdir()

            migrated = self.run_script("migrate_workspace.py", "--target", str(target))
            self.assertEqual(0, migrated.returncode, migrated.stderr)
            with (target / "applications.csv").open("r", encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual("Ready to apply", rows[0]["status"])
            self.assertEqual("", rows[0]["resume_status"])
            self.assertEqual("", rows[0]["cover_letter_status"])
            self.assertIn("confirm each document status", rows[0]["notes"])
            self.assertTrue((target / "applications.v2.backup.csv").is_file())
            with roles_path.open("r", encoding="utf-8", newline="") as handle:
                role_rows = list(csv.DictReader(handle))
            self.assertEqual("Ready to apply", role_rows[0]["application_status"])
            self.assertTrue((target / "job_search" / "roles.v2.backup.csv").is_file())
            self.assertTrue((target / "sources/authoritative/approved_application_answers.md").is_file())
            self.assertEqual("3", (target / ".find-work-version").read_text(encoding="utf-8").strip())
        finally:
            shutil.rmtree(temporary, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
