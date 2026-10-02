---
name: review-job
description: Verify, assess, compare, or analyze one specific job from a company and title, official posting, or URL. Use to create a company profile, role evaluation, match map, recommendation, tracker record, and application folder for any occupation.
---

# Review Job

1. Read `AGENTS.md`, the approved profile and relevant evidence using [targeted evidence reads](references/evidence-retrieval.md), matching tracker rows through `<plugin>/scripts/lookup_application.py --root <workspace>`, any matching serious review, and the target application folder. See [lookup and reuse](../find-jobs/references/retrieval.md). Resolve warnings and ambiguous role identities. Do not load unrelated application folders by default.
2. Resolve the exact role and use [live verification](../find-jobs/references/verification.md), including intermediary tracing when applicable. Preserve recorded decisions and reopen only changed review work.
3. Treat search results, cached text, aggregator copies, successful HTTP status alone, and generic applicant-tracking-system shells as discovery evidence, not active-role proof. Mark removed only from conclusive detail and application-path evidence, not a browser or fetch failure. Mark it `uncertain` when the result is inconclusive, and do not recommend or rank it as active.
4. Record the official URL, requisition ID when available, verification date and method, application-path evidence, posting freshness, status, responsibilities, required and preferred qualifications, terminology, compensation and source, location, work arrangement, time-zone limits, and travel.
5. Research the company from authoritative sources. Record business and customers, problem and mission, headquarters, size, ownership, stability or growth signals, and material ethical concerns. Label estimates and uncertainty.
6. Evaluate the actual role shape against the target profile. Distinguish direct ownership of the desired work from management, coordination, or adjacent responsibility that only sounds similar.
7. Use [experience-gap guidance](references/experience-gaps.md) before labeling material gaps. Build a match map with direct evidence, transferable evidence, unknowns, confirmed gaps and risks, and prohibited or unsupported claims. Cite evidence-ledger claim IDs and employer context where practical.
8. Recommend `Apply`, `Research Further`, `Maybe`, or `Reject`, explaining decisive tradeoffs rather than relying on an unexplained score.
9. Update the matching `roles.csv` record, serious-review summary, and a concise search-log entry. Update `applications.csv` only when an application record is created or changed. Never record `Applied` without user confirmation.
10. Create or update `applications/<Company>/` using the shared application and role-review templates. Preserve existing decisions and drafts. Do not use status-based parent folders.
11. Before drafting, establish the application argument: the employer's core need, up to three strongest supported proof points, the central concern or unknown, and resulting document priorities. Keep this concise in the existing review.
12. Continue with `$draft-application` only when the user requests application wording.

Do not create DOCX or PDF files. Do not use uncertain, confidential, or unsupported claims as qualifications.
