# Find Work Starter

Find Work is a private, evidence-based job-search workflow for ChatGPT and Codex. It helps any job seeker build a career foundation, define targets, find and verify roles, draft truthful application wording, and produce final files.

The shared workflow lives in the `find-work` plugin. Each user creates a separate private workspace for personal history, target preferences, searches, and applications.

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
7. Follow the short onboarding conversation. When invited, add previous resumes or other source files and explicitly confirm when uploads are finished.

No API key is required for the local workflow. Live search, rendered browsing, scheduled tasks, and document rendering depend on the user's plan, operating system, installed software, and current product availability.

## One-source updates

Reusable workflow changes belong in this repository's `plugins/find-work/` directory. Candidate workspaces contain personal data, local preferences, a minimal local `AGENTS.md`, and a schema version marker.

After updating this repository, refresh the local plugin and start a new task. Existing candidate data remains untouched.

Windows PowerShell:

```powershell
.\update_windows.ps1
```

macOS Terminal:

```sh
sh ./update_macos.sh
```

A customized workspace should override the plugin through its local `AGENTS.md` and profile files, not by copying and editing the shared skills.

When an update changes workspace schemas, run `$setup-job-search` against the existing workspace. It uses the versioned, non-destructive migration script before continuing.

An older standalone workspace can migrate later by installing this plugin and removing or renaming local skills with the same names. Review that migration before making it because local rules may intentionally differ.

## Privacy

Do not put real candidate data in this repository. Keep it in the separate private workspace created by the setup skill. Run the included privacy scanner, including Git history, before distributing a release:

```powershell
python plugins/find-work/scripts/privacy_scan.py . --check-git-history
```

## Repository map

- `.agents/plugins/marketplace.json`: local marketplace entry
- `plugins/find-work/.codex-plugin/plugin.json`: plugin manifest
- `plugins/find-work/skills/`: reusable workflows
- `plugins/find-work/assets/workspace/`: blank private-workspace scaffold
- `plugins/find-work/assets/templates/`: shared application templates
- `plugins/find-work/scripts/`: setup, validation, and privacy tools

## License

MIT. See `LICENSE`.
