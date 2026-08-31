---
name: draft-application
description: Tailor, draft, write, or revise complete in-chat wording for a resume, cover letter, application answer, statement, or job-specific application. Use before final DOCX or PDF production, including when a match map still needs completion.
---

# Draft Application

## Workflow

1. Read `AGENTS.md`, matching tracker rows, the target application folder, the verified posting, the match map, relevant evidence and employer context, and approved writing preferences.
2. Treat an explicit request to draft or tailor application materials as confirmation that the user has personally checked the posting and wants to apply. Do not reverify solely because drafting begins.
3. Perform the applicable `$review-job` steps when the role has never been officially verified, the target is ambiguous, the match map is missing or stale, the user asks for reverification, or there is concrete evidence the posting changed.
4. Before drafting or revising a resume opening, cover-letter opening, or substantive application answers, read the corresponding approved-writing library under `sources/authoritative/`. Use it as voice, structure, evidence, and decision history, not boilerplate.
5. Present one complete reviewable Markdown document in chat. Include the concise evaluation, match map, every proposed resume section and bullet, the complete cover letter when requested, application answers, and intentionally excluded claims. Do not use placeholders or references to an unseen draft.
6. Follow the candidate's approved structure and voice. Make a resume opening an outcome-centered invitation to keep reading rather than a generic philosophy or keyword list. Reuse distinctive posting language only when it remains broadly authentic and does not make customization conspicuous.
7. For a cover letter, include the exact role-title line when the candidate's preferred format calls for it. Open with the candidate's genuine reason for wanting this role. Use company details as evidence for that interest, not as a company overview. Connect the interest to relevant supported experience without repeating resume bullets.
8. Use only supported facts. Preserve direct versus transferable evidence. Identify gaps and unsupported claims, exclude them from the wording, and offer the strongest defensible alternative when useful. Apply every confidentiality and disclosure restriction.
9. Run a mandatory cross-application contamination check before presenting the initial draft, presenting final assembled wording, saving approval, or handing off to `$produce-files`.
   - Establish the exact target company and role.
   - Check likely foreign company names, roles, products, missions, transactions, customers, URLs, and employer-specific terms from structured trackers and relevant prior applications.
   - Review every company-specific assertion semantically, including assertions that do not name the employer.
   - Re-ground adapted passages in the current employer's verified sources.
   - If foreign or unsupported employer-specific material appears, correct the complete affected artifact and rerun literal and semantic checks. Do not ask the user to catch contamination.
10. Apply the candidate's punctuation and formatting preferences to the complete writing.
11. Do not save a working draft by default. During revision, show changed sections and a concise summary, keep the current version unambiguous, and present the complete assembled wording again immediately before approval. Save `working_application_draft.md` only when requested or needed for an exact handoff, and mark it unapproved.
12. When the user approves the complete wording or unambiguously requests final files from it, save the exact current review document as `approved_application_wording.md`, record approval separately for each requested document, and continue with `$produce-files` without another confirmation.
13. When the user explicitly approves a final resume opening, cover-letter opening, or complete set of substantive application answers, append it to the corresponding approved-writing library with date, company, role, exact wording, why it worked, evidence or confidentiality limits, and future adaptation guidance. Section approval does not imply approval of the complete application.

## Boundaries

- Do not create, export, or save DOCX or PDF files.
- Do not modify authoritative master documents.
- Do not infer complete-document approval from approval of one section.
- Do not present, approve, save, or produce an artifact until the contamination check passes.
