# Private Find Work Workspace

This folder contains one candidate's private facts, preferences, source documents, searches, and application records. Use the installed Find Work plugin for shared workflows. Keep candidate-specific instructions here or in `profile/`, not in copied skill files.

## Durable local rules

1. Never invent, inflate, or imply experience, results, scope, credentials, customers, or expertise.
2. Preserve imported sources unchanged.
3. Protect personal and confidential information.
4. Separate direct evidence, transferable evidence, gaps, and unsupported claims.
5. Present complete editable wording for review before creating final DOCX or PDF files.
6. Make no substantive wording changes during file production without approval.
7. Preserve searches, reviews, decisions, URLs, dates, and application history.
8. Use ISO dates: `YYYY-MM-DD`.
9. Do not publish this workspace or add a Git remote without explicit approval.

## Source order

Use sources in this order and flag unresolved conflicts:

1. The user's current explicit correction or instruction
2. Approved facts and restrictions in `profile/` and `experience/evidence_ledger.csv`
3. `experience/chronology.csv` and employer context files
4. Approved files in `sources/authoritative/`
5. Original files in `sources/imported/`
6. Public sources that directly corroborate a claim

Writing examples are style references, not factual sources.

## Evidence and disclosure

Record two independent values for each claim:

- Evidence status: `user_attested`, `document_supported`, `publicly_corroborated`, or `needs_clarification`
- Disclosure status: `approved_external`, `approval_required`, `confidential`, or `do_not_use`

Never describe user attestation alone as independent employment verification. Never use a confidential or prohibited claim externally.

## Candidate preferences

Read the approved files in `profile/` before applying preferences. Do not infer target roles, compensation, location, industries, formatting, punctuation, or exclusions.

## Application state

Store each application permanently at `applications/<Company>/`. Record workflow state in `applications.csv`, `job_search/roles.csv`, and the company record, never in parent-directory names. The terminal project state is `Files produced`. Do not track Ready to apply, Submitted, or Applied as separate states, and do not claim to have submitted an application.

## Local customization

Add candidate-specific durable rules below this heading. Do not copy or rewrite shared plugin workflows here.
