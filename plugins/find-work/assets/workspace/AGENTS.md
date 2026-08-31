# Private Find Work Workspace

This folder contains one candidate's private facts, preferences, source documents, searches, application records, and approved writing history. Use the installed Find Work plugin for shared workflows. Keep candidate-specific instructions here or in `profile/`, not in copied skill files.

## Durable local rules

1. Never invent, inflate, or imply experience, results, scope, credentials, customers, technical depth, or expertise.
2. Preserve imported sources unchanged and flag unresolved conflicts instead of guessing.
3. Protect personal, contractual, and confidential information.
4. Separate direct evidence, transferable evidence, gaps, and unsupported claims.
5. Verify plausible roles on the official employer role-detail page before recommending or ranking them. Require visible role details and a current Apply control, application link, or functional form. The title does not also need to appear on an openings index.
6. Present complete editable wording for review before creating DOCX or PDF files. A clear request to produce files from the current complete wording is approval.
7. Make no substantive wording changes during file production without returning the revision for approval.
8. Preserve searches, reviews, decisions, URLs, dates, warnings, approvals, and application history.
9. Use ISO dates: `YYYY-MM-DD`.
10. Do not publish this workspace or add a Git remote without explicit approval.

## Source order

Use sources in this order and flag unresolved conflicts:

1. The user's current explicit correction or instruction
2. Approved facts and restrictions in `profile/` and `experience/evidence_ledger.csv`
3. `experience/chronology.csv` and employer context files
4. Approved files in `sources/authoritative/`
5. Original files in `sources/imported/`
6. Public sources that directly corroborate a claim

Writing examples and approved-writing libraries are style and decision-history references, not factual sources or boilerplate.

## Evidence and disclosure

Record two independent values for each claim:

- Evidence status: `user_attested`, `document_supported`, `publicly_corroborated`, or `needs_clarification`
- Disclosure status: `approved_external`, `approval_required`, `confidential`, or `do_not_use`

Never describe user attestation alone as independent employment verification. Never use a confidential or prohibited claim externally.

## Candidate preferences

Read the approved files in `profile/` before applying preferences. Do not infer target roles, compensation, location, industries, formatting, punctuation, voice, filename conventions, or exclusions.

## Search and verification

- Treat boards, aggregators, indexed text, cached pages, and search results as discovery only.
- Classify a role `active` when the official role-detail page contains the role details and a current application path. A generic applicant-tracking-system shell is insufficient.
- Mark a role `removed` when the detail page is gone, redirects to an error or openings index, states that the role is unavailable, or lacks a current application path. Use `uncertain` when the result is inconclusive.
- A ranking of only new findings does not require a full portfolio refresh. A complete current ranking requires same-day reverification of every included active role.
- An explicit request to draft, tailor, or produce application materials confirms that the user has personally checked the posting and wants to apply. Do not reverify solely because drafting or production begins. Reverify when the user asks, the role has never been officially verified, the target is ambiguous, or there is concrete evidence its status changed.

## Application state

Store each application permanently at `applications/<Company>/`. Record workflow state in `applications.csv`, `job_search/roles.csv`, and the company record, never in parent-directory names.

- Successful file production sets status `Ready to apply`.
- Record `Applied` only after the user confirms submission. Use the confirmed submission date. If the date is unknown, leave it blank and record that uncertainty in notes.
- File production never proves submission.

## Application records and files

- Keep the exact approved review document in `approved_application_wording.md`.
- Save a working Markdown snapshot only when the user requests it or a task handoff needs exact wording. Mark it unapproved.
- Use the candidate's full application name plus document type for final filenames by default, such as `<Candidate Name> Resume.pdf` and `<Candidate Name> Cover Letter.pdf`. Keep company and role in the containing folder and records, not in filenames or metadata, unless the candidate explicitly chooses another convention.
- Retain editable DOCX files with final PDFs by default. Remove them only when the candidate explicitly chooses another retention policy.
- Use personal-only metadata. Do not embed the target company, role, another application, tool name, or stale template metadata.

## Production and QA

Use this handoff:

1. Duplicate authoritative masters when available and create only approved wording.
2. Export and normalize final files, including metadata and live contact links.
3. Run deterministic, nonvisual validation and resolve errors. Report every warning or incomplete check.
4. Do not rasterize pages or claim AI visual QA unless the user requests it. When requested, inspect every page produced from the current working files.
5. Provide the actual final files for the user's visual review, plus the official application link and permanent folder.

Deterministic validation does not prove the absence of clipping, overlap, spacing, alignment, pagination, or font-substitution defects.

## Local customization

Add candidate-specific durable rules below this heading. Do not copy or rewrite shared plugin workflows here.
