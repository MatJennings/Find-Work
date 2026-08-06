---
name: produce-files
description: Create, generate, export, or finalize approved resume, cover-letter, and application files. Use only after complete wording is approved or when the user unambiguously requests final file production from the current complete wording. The terminal project state is Files produced.
---

# Produce Files

## Approval gate

1. Read `AGENTS.md`, the application record, `approved_application_wording.md`, writing preferences, and authoritative document sources.
2. Confirm complete wording exists for every requested document. Treat an unambiguous request to produce final files from the current complete wording as approval. If the approved snapshot is missing but the current task contains the complete wording, save that exact wording as `approved_application_wording.md` before production. Stop if wording is missing, partial, conditional, or ambiguous.

## Production

1. If `sources/authoritative/master_resume.docx` exists, duplicate it to a temporary working file and preserve its visual system. If it does not exist, create the document from approved wording and the approved resume preferences.
2. Create only the requested file formats. Prefer PDF for final application delivery and retain DOCX only when requested or selected in the candidate profile.
3. Make no substantive wording changes. Return any layout-driven wording change to the user for approval.
4. Rerun the literal and semantic cross-application contamination check against the approved wording before production. Stop if the target company, role, or employer-specific facts do not match the verified application record.
5. Use available document and PDF tooling. Render and inspect every page when visual tools are available. If they are unavailable, state the limitation and do not claim visual verification.
6. Check filenames, candidate contact details, employer, role, dates, links, page count, text completeness, stale placeholders, stale employer references, and document metadata. Compare the rendered result with the authoritative master or approved preferences. Inspect font metadata when visual differences suggest substitution.
7. Store final files in the permanent `applications/<company>/` folder. Do not move the folder when status changes. Preserve every review and wording record. Use a filesystem-safe candidate name, company, role, and document type in filenames.
8. Update the application record and `applications.csv` to status `Files produced` with the production date, final filenames, and permanent folder path. Update related job-search records when they track application status.
9. Do not track Ready to apply, Submitted, or Applied as separate project states. Do not claim to have submitted the application.
10. Return clickable links to the files, permanent containing folder, and verified official application URL.

Do not overwrite authoritative source files. Do not create final files from unapproved wording.
