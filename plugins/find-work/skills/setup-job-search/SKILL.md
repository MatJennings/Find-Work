---
name: setup-job-search
description: Initialize, bootstrap, set up, or audit a private Find Work workspace. Use for a first run, an empty job-search folder, a downloaded starter package, capability checks, or repair of missing standard folders and blank trackers.
---

# Set Up Job Search

1. Confirm the intended private workspace root. Explain that OneDrive, iCloud, Dropbox, and similar locations are cloud-synced, then ask whether that is acceptable. Never initialize inside the plugin source repository.
2. For a new or empty folder, run `../../scripts/create_workspace.py --target <workspace-root>`. For an existing Find Work workspace, run `../../scripts/migrate_workspace.py --target <workspace-root>`. If the default Python command is unavailable, use the Python runtime available to Codex.
3. Read the new `AGENTS.md` and `START_HERE.md`.
4. Inspect available capabilities without requiring them: local file access, DOCX and PDF text extraction, OCR, web search, a rendered browser, document creation, PDF rendering, Git, Word, and LibreOffice. Record the result in `profile/environment_capabilities.md`.
5. Explain that limited or free plans can still support source intake, career interviews, drafting, and local tracking. When live browsing is unavailable, require the user to provide or manually inspect official job pages before recording a role as verified.
6. Ask for the candidate's preferred name and minimum contact information needed for applications. Store it only in `profile/candidate_profile.md`.
7. Invite the user to place prior resumes and other career records in `sources/imported/`. Pause until the user confirms uploads are finished or explicitly chooses to continue without prior materials. Then continue with `$build-career-foundation`.

Do not create application documents during setup. Do not copy any example person's data into the workspace.
