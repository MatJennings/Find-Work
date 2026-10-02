# Maintainer validation

This is targeted release validation, not a simulated application conversation or a live Free-account trial.

From the starter repository root, run commands separately and stop on a failure:

```text
python -m unittest discover -s tests -v
python evals/run_evals.py
python plugins/find-work/scripts/validate_plugin.py
python plugins/find-work/scripts/privacy_scan.py .
python plugins/find-work/scripts/privacy_scan.py . --check-git-history
git diff --check
```

The unittest suite creates and validates a synthetic workspace, checks versioned migration and preserved backups, runs read-only lookup and retrieval tests, and checks documented behavioral boundaries. This fixture use is targeted testing, not a full workflow run-through. The contract runner repeats only the workflow and retrieval contract subset for maintainers who changed policy.

The plugin validator checks manifest and marketplace linkage, every skill's required frontmatter and UI-file presence, and bundled relative Markdown links. When the Codex skill-creator validator is available, run its quick_validate.py against each skill as an additional frontmatter check. These do not establish successful runtime installation. Privacy scanning is heuristic and does not establish absence of all confidential information.

Do not weaken a failed test or a privacy check to make a release pass. Investigate the cause. Report warnings and incomplete checks. Keep generated fixtures out of releases. Existing reviewed release archives are historical packages, and do not automatically reflect source updates. Update instructions should obtain current source rather than imply an old archive is current.

The actual live setup and feedback checklist is [LIVE_SETUP_CHECKLIST.md](LIVE_SETUP_CHECKLIST.md). Record phases not exercised as not observed. Helper tests do not establish independent writing quality, account savings, optional export-tool availability or Free-account completion.
