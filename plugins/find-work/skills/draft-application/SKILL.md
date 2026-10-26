---
name: draft-application
description: Tailor, draft, write, or revise complete in-chat wording for a resume, cover letter, application answer, statement, or job-specific application. Use before final DOCX or PDF production, including when a match map still needs completion.
---

# Draft Application

## Workflow

1. Use the already-loaded `AGENTS.md` without re-reading it. Read matching tracker rows using targeted lookup, the target application folder, the verified posting, the match map, relevant evidence and employer context using [targeted evidence reads](../review-job/references/evidence-retrieval.md), and approved writing preferences.
2. Treat an explicit request to draft or tailor application materials as confirmation that the user has personally checked the posting and wants to apply. Do not reverify solely because drafting begins.
3. Perform the applicable `$review-job` steps when the role has never been verified under the live verification policy, the target is ambiguous, the match map is missing or stale, the user asks for reverification, or there is concrete evidence the posting changed.
4. Before drafting or revising a resume opening, cover-letter opening, or substantive application answers, retrieve complete selected examples from the corresponding approved-writing library using [writing retrieval](references/writing-retrieval.md). Use it as voice, structure, and decision history, never as factual evidence or boilerplate.
5. Present one complete reviewable Markdown document in chat. Include concise decision context, every requested resume section and bullet, the complete cover letter when requested, requested application answers, and material excluded claims. Present the match map when first establishing the application argument or when it changes. Do not repeat an unchanged full evaluation or match map during every revision. Do not use placeholders or references to an unseen draft.
6. Use the existing application argument to prioritize evidence and apply [evidence-led bullets](references/evidence-led-bullets.md). Follow the candidate's approved structure and voice. For a new or substantively revised resume opening, apply [opening quality](references/opening-quality.md). Make it an outcome-centered invitation to keep reading rather than a generic philosophy or keyword list.
7. For a cover letter, follow [cover-letter craft](references/cover-letter-craft.md): choose the argument before the proof, pick an opening thesis before writing, use the problem, approach and one-proof shape, and run the read-aloud check and clarity script. Include the exact role-title line when the candidate's preferred format calls for it. Open with the candidate's genuine reason for wanting this role. Use company details as evidence for that interest, not as a company overview. Do not repeat resume bullets.
8. Check material unknowns using [experience-gap guidance](../review-job/references/experience-gaps.md) and summarize them outside employer-facing wording. Use only supported facts. Preserve direct versus transferable evidence. Identify gaps and unsupported claims, exclude them from the wording, and offer the strongest defensible alternative when useful. Apply every confidentiality and disclosure restriction.
9. Run a mandatory cross-application contamination check before presenting the initial draft, presenting final assembled wording, saving approval, or handing off to `$produce-files`.
   - Establish the exact target company and role.
   - Check likely foreign company names, roles, products, missions, transactions, customers, URLs, and employer-specific terms from structured trackers and relevant prior applications.
   - Review every company-specific assertion semantically, including assertions that do not name the employer.
   - Re-ground adapted passages in the current employer's verified sources.
   - If foreign or unsupported employer-specific material appears, correct the complete affected artifact and rerun literal and semantic checks. Do not ask the user to catch contamination.
10. Apply the candidate's punctuation and formatting preferences to the complete writing.
11. Do not save a working draft by default. During revision, show changed sections and a concise summary, keep the current version unambiguous, and present the complete assembled wording again immediately before approval. Save `working_application_draft.md` only when requested or needed for an exact handoff, and mark it unapproved.
12. When the user approves the complete wording or unambiguously requests final files from it, save the exact current review document as `approved_application_wording.md`, record approval separately for each requested document, and continue with `$produce-files` without another confirmation.
13. When the user explicitly approves a final resume opening, cover-letter opening, or complete set of substantive application answers, append it to the corresponding approved-writing library with date, company, role, exact wording, why it worked, evidence or confidentiality limits, and future adaptation guidance. Use the shared approved-writing-entry template for new entries without rewriting older records. Section approval does not imply approval of the complete application.

## Optional depth

The default uses a concise critique and reusable feedback, without a separate reviewer, decision card, or full learning record. Read [optional drafting depth](references/optional-depth.md) only when requested or a repeated material writing issue justifies discussing it. Use [deep letter review](references/deep-letter-review.md) only when the candidate has turned it on, because it needs separate agents and substantial plan usage.

## Boundaries

- Do not create, export, or save DOCX or PDF files.
- Do not modify authoritative master documents.
- Do not infer complete-document approval from approval of one section.
- Do not present, approve, save, or produce an artifact until the contamination check passes.
