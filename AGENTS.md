# Find Work Plugin Development Instructions

This repository is the canonical shared workflow for the Find Work plugin. It must remain generic, portable, and safe to distribute publicly.

## Rules

1. Never add real candidate names, contact details, work histories, resumes, applications, search trackers, screenshots, document metadata, or private employer facts.
2. Use only blank templates or clearly synthetic test data outside release artifacts.
3. Keep reusable behavior in `plugins/find-work/skills/`, blank workspace files in `plugins/find-work/assets/workspace/`, and shared record templates in `plugins/find-work/assets/templates/`.
4. Keep candidate facts, preferences, approved examples, target profiles, and confidentiality decisions in each user's private workspace.
5. Preserve the full application lifecycle: `Not started`, `Drafting`, `Approved`, `Ready to apply`, `Applied`, `Will not apply`, or `Removed`. File production ends at `Ready to apply`. Record `Applied` and an actual or explicitly unknown submission date only after the user confirms submission.
6. Maintain compatibility with limited environments. Source intake, career interviews, drafting, and local tracking must not require paid browsing, Git, Word, LibreOffice, or an API key.
7. Treat job boards and search results as discovery only. An active role requires a live official role-detail page with role details and a current application path. The role does not also need to appear on an openings index. When verification is inconclusive, keep status `uncertain`.
8. Preserve the approval boundary. Present complete editable wording before creating DOCX or PDF files. A clear request to produce files from the current complete wording is approval. Do not make substantive wording changes during production.
9. Make production claims narrowly. Deterministic validation does not prove visual quality. AI visual review is optional and requires inspection of every current page when requested.
10. Run every skill validator, the plugin validator, a synthetic workspace creation test, workspace validation, migration tests, and the privacy scanner before release.
11. Use ISO dates in durable records.
12. Do not publish, push, reinstall, or change marketplace installation state without explicit authorization.

## One-source maintenance

Edit the shared plugin here. Do not copy its skills into candidate workspaces. Candidate workspaces customize behavior through their own `AGENTS.md`, profile files, evidence records, and approved writing libraries. After shared changes, refresh the plugin installation and use a new task so Codex loads the revised version.
