# Find Work Plugin Development Instructions

This repository is the canonical shared workflow for the Find Work plugin. It must remain safe to distribute publicly.

## Rules

1. Never add real candidate names, contact details, work histories, resumes, applications, search trackers, screenshots, or document metadata.
2. Use only blank templates or clearly synthetic test data outside release artifacts.
3. Keep reusable behavior in `plugins/find-work/skills/` and blank workspace files in `plugins/find-work/assets/workspace/`.
4. Keep candidate-specific facts and preferences in each user's private workspace, never in this repository.
5. Preserve the terminal application state `Files produced`. Do not add external submission states to the shared workflow.
6. Maintain compatibility with limited environments. Local onboarding and drafting must not require paid browsing, Git, Word, LibreOffice, or an API key.
7. When live job verification is unavailable, require manual user evidence and retain status `uncertain` until supplied.
8. Run every skill validator, the plugin validator, a synthetic workspace creation test, workspace validation, and the privacy scanner before release.
9. Use ISO dates in durable records.
10. Do not publish, push, or change marketplace installation state without explicit authorization.

## One-source maintenance

Edit the shared plugin here. Do not copy its skills into candidate workspaces. Candidate workspaces customize behavior through their own `AGENTS.md` and profile files. After shared changes, refresh the plugin installation and use a new task so Codex loads the revised version.
