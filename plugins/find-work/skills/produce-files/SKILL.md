---
name: produce-files
description: Create, export, produce, or finalize approved application PDFs and editable DOCX files. Use after complete wording is approved or when the user clearly requests production from the current complete wording. Validate files, set Ready to apply, and provide official and local links.
---

# Produce Files

## Approval gate

1. Use the already-loaded `AGENTS.md` without re-reading it. Read the target application record, writing and file preferences, authoritative document sources, and `approved_application_wording.md`. Use targeted tracker lookup when needed. Do not load historical writing libraries or unrelated evidence solely to export already-approved wording.
2. Confirm complete wording exists for every requested document. A clear request to produce final files from the current complete wording is approval. If the exact current wording is present in the task but the snapshot is missing, save it as `approved_application_wording.md` and record per-document approval before producing files. Stop when wording is missing, partial, conditional, or ambiguous.

## Production

1. Recheck the approved wording for literal and semantic cross-application contamination. Stop if target identity or employer-specific facts do not match the verified record.
2. Duplicate each available authoritative master to a temporary working file. Preserve fonts, colors, margins, headers, footers, hierarchy, alignment, hyperlinks, and visual language. Never overwrite a master. If no approved master exists, follow the candidate's approved document preferences and available document tooling.
3. Apply only approved wording using semantic document locations and employer blocks. Do not embed application prose in code, depend on brittle numeric paragraph positions, or create application-specific builders. Improve a reusable generator only when the approved structure genuinely requires it.
4. Make no substantive wording changes. Return any layout-driven wording revision for approval. Unless the candidate's preferences say otherwise, never let a bullet split across pages. When a split or excess length remains, propose the smallest fix for approval: first tighten bullets whose last line holds only a word or two, then remove the lowest-priority bullet.
5. Use the approved filename convention. By default, use the candidate's full application name plus document type, such as `<Candidate Name> Resume.pdf` and `<Candidate Name> Cover Letter.pdf`, with matching DOCX names. Keep company and role in the folder and records, not filenames or metadata.
6. Retain editable DOCX files with final PDFs unless the candidate explicitly selected another retention policy.
7. Normalize personal-only metadata and remove stale company, role, tool, author, manager, custom, PDF Info, and XMP properties that conflict with the approved metadata policy. Preserve visible email and professional-profile text as live links.
8. Export the requested files using available tooling. Keep diagnostic and temporary files outside permanent application folders when practical.
9. Run deterministic, nonvisual validation for integrity, exact filenames, expected page counts, extracted text, approved-text coverage, candidate-selected punctuation rules, role anchors, live links, standard bullet extraction, personal-only metadata, and obvious wrong-company terms. Resolve errors and report every warning or incomplete check.
10. Do not rasterize pages or claim AI visual QA unless the user requests it. When requested, render and inspect every page from the current working files. Deterministic validation does not prove visual quality.
11. Save final files in `applications/<Company>/`. After successful production and validation, set status `Ready to apply` and update the targeted application record, `applications.csv`, related role record, serious-review summary when applicable, and concise search log. Do not record `Applied` until the user confirms submission.
12. Use the recorded official application link. Do not reverify solely because production begins. Reverify only when the user asks, the role was never verified under the live verification policy, the target is ambiguous, or there is concrete evidence its status changed.
13. Return final file links, every warning or incomplete check, the official application link, and the permanent folder. Provide the actual files for the user's final visual review.

Do not draft new wording, use unapproved edits, overwrite authoritative sources, or infer submission from file production.
