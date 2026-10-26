# Find Work Starter

Find Work is a private, evidence-based job-search workflow for ChatGPT and Codex. It helps any job seeker build a career foundation, define targets, find and verify roles, draft truthful application wording, produce validated files, and maintain an accurate application history.

The shared workflow lives in the `find-work` plugin. Each user creates a separate private workspace for personal history, target preferences, searches, approvals, and applications.

## Install

1. Download or clone this repository to a durable folder.
2. Open the ChatGPT desktop app and sign in.
3. Open this repository folder in the app, then open the integrated terminal with **Ctrl+`** on Windows or **Control+`** on macOS.
4. Install the local plugin:

   Windows PowerShell:

   ```powershell
   .\install_windows.ps1
   ```

   macOS Terminal:

   ```sh
   sh ./install_macos.sh
   ```

   A successful installation prints the plugin list with `find-work` present. If the `codex` command is unavailable, restart the desktop app, reopen this folder, and use its integrated terminal.
5. Create a separate private folder for the job search. A folder in OneDrive, iCloud, Dropbox, or a similar service is cloud-synced. Use a device-local folder if that is not acceptable.
6. Open the private folder in the desktop app, start a new task, and ask: `Use $setup-job-search to set up this folder.`
7. Follow the onboarding conversation. When invited, add previous resumes or other source files and explicitly confirm when uploads are finished.

No API key is required for local source intake, career interviews, drafting, and tracking. Live search, rendered browsing, scheduled tasks, file production, PDF export, and optional visual QA depend on the user's plan, operating system, installed software, and current product capabilities.

## Workflow

- `$setup-job-search` creates or migrates the private workspace and records available capabilities.
- `$build-career-foundation` reconciles chronology, evidence, disclosure limits, target preferences, and baseline writing preferences.
- `$find-jobs` runs scoped quick, comprehensive, recurring, or portfolio-refresh searches and verifies plausible roles on employer detail pages or qualifying live intermediary listings.
- `$review-job` evaluates one role, develops the company profile and match map, and updates durable records.
- `$draft-application` presents complete editable wording in chat, checks cross-application contamination, and preserves only explicitly approved writing.
- `$produce-files` creates approved files, runs deterministic nonvisual validation, sets `Ready to apply`, and waits for user confirmation before recording `Applied`.

The workflow does not require an employer openings index to repeat a role that has a live official detail page and current application path. It does not reverify a posting merely because drafting or production begins. It does reverify when requested, when verification under the live role policy never occurred, when the target is ambiguous, or when evidence suggests the posting changed.

## One-source updates

Reusable workflow changes belong in this repository's `plugins/find-work/` directory. Candidate workspaces contain personal data, local preferences, a minimal local `AGENTS.md`, approved writing history, and a schema version marker.

After updating this repository, refresh the local plugin and start a new task. Existing candidate data remains untouched.

Windows PowerShell:

```powershell
.\update_windows.ps1
```

macOS Terminal:

```sh
sh ./update_macos.sh
```

A customized workspace should override the plugin through local instructions and profile files, not copied skills. When an update changes workspace schemas, run `$setup-job-search` against the existing workspace. Migrations preserve backups and stop on unsupported schemas or ambiguous folder collisions.

Schema version 3 adds the complete `Ready to apply` and user-confirmed `Applied` lifecycle, per-document status, submission and follow-up dates, reusable approved-writing libraries, personal-only filename and metadata preferences, and deterministic nonvisual QA guidance. It migrates the former `Files produced` state to `Ready to apply` without claiming submission.

## Live setup and validation

The default target is the ChatGPT desktop app with a private local folder. Use the [live setup checklist](docs/LIVE_SETUP_CHECKLIST.md) during ordinary onboarding and record concrete feedback. Targeted helper and workflow tests are documented in [validation](docs/VALIDATION.md). Actual Free-account completion and usage savings have not yet been measured. See [default and optional-feature decisions](docs/OPTIONAL_FEATURE_DECISIONS.md) for what is included, deferred, and candidate-specific. Source version 0.5.0 adds single-context cover-letter and opening quality guidance, a letter clarity script and an opt-in deep letter review. It retains workspace schema 3 and does not rewrite private profiles or instructions.

## Privacy

Do not put real candidate data in this repository. Keep it in the separate private workspace. Before distributing a release, scan the working tree and Git history:

```powershell
python plugins/find-work/scripts/privacy_scan.py . --check-git-history
```

Release archives require explicit binary-artifact review.

## Repository map

- `.agents/plugins/marketplace.json`: local marketplace entry
- `plugins/find-work/.codex-plugin/plugin.json`: plugin manifest
- `plugins/find-work/skills/`: reusable workflows
- `plugins/find-work/assets/workspace/`: blank private-workspace scaffold
- `plugins/find-work/assets/templates/`: shared review, application, and approval templates
- `plugins/find-work/scripts/`: setup, migration, validation, versioning, and privacy tools
- `release/`: reviewed distributable archives

## License

MIT. See `LICENSE`.
