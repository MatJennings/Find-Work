# Migrating an Existing Workspace

This is a one-time, reviewable migration. Do not apply it automatically.

1. Commit or otherwise back up the existing private workspace.
2. Install the shared `find-work` plugin from this repository.
3. Compare local skills with the plugin skills. Preserve intentional candidate-specific behavior in the workspace `AGENTS.md` or profile files.
4. Remove or rename local skills that duplicate plugin skill names. Codex does not merge duplicate skills reliably into one workflow.
5. Keep all candidate history, evidence, preferences, trackers, and applications in the private workspace.
6. Run `$setup-job-search` in the private workspace. Its migration moves legacy `applications/in_progress/<Company>/` and `applications/files_produced/<Company>/` folders to permanent `applications/<Company>/` locations, updates tracker paths, expands the role schema, and creates CSV backups. It stops rather than merge ambiguous duplicate company folders.
7. Start a new task and test setup auditing, job review, drafting, and file production against an existing application record.
8. After the migration, make reusable workflow changes only in the plugin repository. Make candidate-specific changes only in the private workspace.

Updating the plugin does not rewrite candidate data. Refresh the plugin installation after shared changes, then start a new task so the revised skills are loaded.
