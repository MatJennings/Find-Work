---
name: draft-application
description: Tailor, draft, write, or revise complete editable wording for a resume, cover letter, application answer, statement, or job-specific application. Use after a role review or whenever a user asks for application wording, but before final DOCX or PDF production.
---

# Draft Application

1. Read `AGENTS.md`, the verified role review, candidate profile, chronology, evidence ledger, relevant employer context, and writing preferences.
2. If the role or match map is missing or stale, perform the applicable `$review-job` steps first.
3. Draft one complete reviewable Markdown document in chat. Include the concise role recommendation, match map, every proposed resume section and bullet, the complete cover letter when requested, application answers, and intentionally excluded claims.
4. Use only supported facts. Preserve the difference between direct evidence and transferable evidence. Never upgrade a claim's evidence level for rhetorical strength.
5. Follow the candidate's preferred tone, length, punctuation, formatting, and document structure. Use employer terminology naturally without keyword dumping. Do not volunteer missing qualifications or frame the candidate through what they have not done. Address a gap only when the application explicitly asks, an explanation is necessary to avoid misleading the reader, or the user directs it. Keep any explanation concise and pivot to the strongest relevant evidence.
6. Run a mandatory cross-application contamination check before presenting, saving, approving, or handing off any artifact.
   - Establish the exact target company and role from the verified posting.
   - Compare the complete draft with company names, roles, products, missions, transactions, customers, URLs, and employer-specific terms in `applications.csv`, `job_search/roles.csv`, and other application folders. Another application company may appear only when it is part of the candidate's supported work history and is clearly identified as such.
   - Check semantics as well as literal names. Confirm that every product, mission, market position, transaction, strategic challenge, and reason for interest belongs to the target employer and is supported by target-role or target-company sources.
   - Re-ground any adapted passage in current target sources. Do not reuse employer-specific cover-letter framing merely because two roles are similar.
   - If foreign or unsupported employer-specific material appears, stop, correct the complete artifact, and rerun both literal and semantic checks. Do not rely on the user to catch contamination.
7. Revise in chat until the current complete wording is unambiguous. Do not save a working file unless the user requests a snapshot or a handoff requires it.
8. When the user approves the complete wording or unambiguously requests final files, save the exact approved wording as `approved_application_wording.md` in the permanent application folder and continue with `$produce-files`.

Do not create, export, or save DOCX or PDF files in this workflow. Approval of one section does not imply approval of the complete application. Treat cross-application contamination as a blocking defect.
