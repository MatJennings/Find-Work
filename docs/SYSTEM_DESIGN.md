# Find Work architecture

The shared plugin contains reusable behavior, blank assets, and read-only helpers. Each private workspace owns candidate facts, preferences, disclosure decisions, approved wording, and history. Do not transfer real candidate data into the plugin or release artifacts.

## Phase routing

| Phase | Read | Preserve |
|---|---|---|
| Setup and foundation | Capability record, current onboarding scope, relevant imported sources | Original sources, chronology, evidence and disclosure state |
| Search | Target profile, recent coverage, batch historical lookup | Separate new findings and known updates, source coverage and live verification |
| Review | Exact role lookup, relevant evidence, current employer details | Identity, match map, material unknowns, application argument |
| Draft and revise | Target review, relevant evidence, selected approved examples, current revision text | Candidate voice, contamination checks, complete wording and document approval |
| Produce | Exact approved wording, target records, preferences and masters | Exact text, file validation, Ready to apply only |
| Resume or submission | Matching records and latest user instruction | Outstanding questions and user-confirmed submission |

Lookup returns complete matching rows, diagnostics and provenance. It never decides verification, approval, disclosure, or submission. Batch discovery reads each tracker once. Reuse requires reconciled role identity and unchanged relevant work. New sessions and lost context require targeted reads. There is no generated duplicate fact cache. Evidence retrieval selects current controlling text with complete topic and disclosure guards, related claim rows, confidentiality policy, hashes and line spans. Writing retrieval returns complete selected examples and related versions without granting approval. Optional source checks establish byte freshness only. Helpers require an explicit workspace root and the Python standard library, with manual targeted-read fallbacks.

## Trust and capability boundaries

Employer detail and application paths are preferred. Complete live intermediary paths may qualify after employer tracing. Historical status is not a live check. Missing or blocked evidence remains uncertain. No-match retrieval does not prove lack of candidate experience.

Evidence and disclosure are independent. Approved examples supply style, not new career facts or approval for a new application. Production consumes only exact approved wording and never silently changes it. Successful file validation sets Ready to apply, while Applied requires user confirmation.

No browsing, API key, Git, Word, or LibreOffice is required for evidence interviews or in-chat drafting. Use available tools for exports and report unavailable checks honestly. Deterministic validation does not prove visual layout. AI visual QA is optional. Shared changes do not overwrite existing private instructions during migration.

## Validation

Run `python -m unittest discover -s tests`, `python evals/run_evals.py`, and `python plugins/find-work/scripts/validate_plugin.py`. Tests use synthetic fixtures to check helpers, workspace creation, migrations and workflow contracts. Privacy scans include the working tree and Git history before publishing. These checks do not measure autonomous agent quality, billed usage or Free-account completion. The live setup checklist records actual observations and leaves unexercised phases untested. No simulated end-to-end trial is required. Feedback drives subsequent generic revisions.
