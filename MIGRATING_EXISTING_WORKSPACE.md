# Migrating an Existing Workspace

This is a one-time, reviewable migration. Do not apply it automatically.

1. Commit or otherwise back up the existing private workspace.
2. Install the shared `find-work` plugin from this repository.
3. Compare local skills with plugin skills. Preserve intentional candidate-specific behavior in the workspace `AGENTS.md`, profile files, evidence records, and approved writing libraries.
4. Remove or rename local skills that duplicate plugin skill names. Codex does not reliably merge duplicate skills into one workflow.
5. Keep all candidate history, evidence, preferences, trackers, sources, applications, and approval records in the private workspace.
6. Run `$setup-job-search` in the private workspace. Its versioned migration:
   - moves legacy status-based application folders to permanent `applications/<Company>/` locations,
   - expands the role tracker with verification and company-context fields,
   - migrates `Files produced` to `Ready to apply`,
   - adds per-document, applied-date, production-date, follow-up, and folder fields,
   - creates blank approved resume-opening, cover-letter-opening, and application-answer libraries when missing,
   - preserves CSV backups before rewriting schemas,
   - stops rather than merging ambiguous company folders or unsupported tracker schemas.
7. Review local `AGENTS.md` and preferences after migration, especially official-only role verification, old source-loading rules, and local copies that shadow plugin skills. Migrations do not overwrite candidate-specific instructions, so copy in desired new generic policies deliberately.
8. Start a new task and test setup auditing, job search, role review, drafting, approval capture, file production, `Ready to apply`, and user-confirmed `Applied` against an existing application record.
9. After migration, make reusable workflow changes only in the plugin repository. Make candidate-specific changes only in the private workspace.

Updating the plugin does not rewrite candidate data. Refresh the plugin installation after shared changes, then start a new task so the revised skills are loaded.
