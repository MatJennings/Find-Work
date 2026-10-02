---
name: setup-job-search
description: Initialize, bootstrap, migrate, or audit a private Find Work workspace. Use for a first run, an empty job-search folder, a downloaded starter package, capability checks, schema updates, or repair of missing standard folders and blank trackers.
---

# Set Up Job Search

1. Confirm the intended private workspace root. Explain that OneDrive, iCloud, Dropbox, and similar locations are cloud-synced, then ask whether that is acceptable. Never initialize inside the plugin source repository.
2. For a new or empty folder, run `../../scripts/create_workspace.py --target <workspace-root>`. For an existing Find Work workspace, run `../../scripts/migrate_workspace.py --target <workspace-root>`. Use the available Python runtime if the default command is unavailable. If no Python runtime exists, use available local file tools to copy missing blank scaffold files for a new workspace. Do not simulate a successful script run or automate an existing schema migration without its validator. Preserve records, report the incomplete migration, and continue only work compatible with the existing schema.
3. Read the workspace `AGENTS.md`, `START_HERE.md`, `.find-work-version`, and onboarding status after setup or migration.
4. Inspect capabilities without requiring them: local file access, DOCX and PDF extraction, OCR, live web search, a rendered browser, scheduled tasks, document creation, PDF export, deterministic validation, optional page rendering, Git, Word, and LibreOffice. Record results and limitations in `profile/environment_capabilities.md`, including observed app surface, account plan when known, Python or bundled runtime, plugin version, and workspace schema. Do not infer capabilities from plan alone or require paid features for onboarding and drafting.
5. Explain that limited environments can still support source intake, career interviews, drafting, and local tracking. When official pages cannot be inspected, keep roles `uncertain` until the user supplies evidence from the role-detail page and application path.
6. Ask for the preferred name and minimum application contact information. Store it only in `profile/candidate_profile.md`.
7. Review the blank profile choices that affect later production: authoritative master paths, final filename convention, personal-only metadata, editable DOCX retention, punctuation, and whether AI visual QA is normally requested. Do not force a preference when the user has not chosen one. Defer nonblocking formatting decisions until drafting or production needs them, and avoid turning optional review features into onboarding questions.
8. Invite the user to place prior career records in `sources/imported/`. Pause until the user confirms uploads are complete or explicitly continues without them. Then continue with `$build-career-foundation`.

Do not create application documents during setup. Do not copy example-person data into the workspace. Do not overwrite conflicting existing records during migration.
