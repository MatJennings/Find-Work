---
name: find-jobs
description: Find, refresh, verify, deduplicate, and rank current job openings against an approved candidate target profile. Use for a new search, today's jobs, recurring searches, role refreshes, or updates to job-search trackers across any profession or seniority.
---

# Find Jobs

1. Read `AGENTS.md`, `profile/job_target_profile.md`, `experience/chronology.csv`, `experience/evidence_ledger.csv`, `job_search/roles.csv`, and `applications.csv`.
2. Search broadly enough to include direct and plausible transferable fits. Apply the candidate's approved exclusions and constraints without inventing unstated preferences.
3. Treat job boards, aggregators, cached pages, and search results as discovery sources only.
4. Before recommending a role as active, confirm the exact title or requisition on the employer's currently rendered careers board and confirm a functional application path. Use a rendered browser when necessary. Mark a role `removed` when the live board omits it even if an old detail URL resolves.
5. If browsing is unavailable, ask the user to inspect the official board and application path. Record the role as `uncertain` until that evidence is supplied. Never convert discovery evidence into official verification.
6. Capture company, role, official URL, requisition ID, discovery and verification dates, posting age, status, recommendation, relevance to the target profile, job location, work arrangement, corporate headquarters, compensation and source, travel, company size, ownership, fit evidence, gaps, application status, and verification notes.
7. Deduplicate by company, title, requisition ID, and official URL.
8. Before presenting a current or all-role ranking, reverify every tracked role that is not already at terminal application status. Require `last_checked` to equal the search date. Exclude rejected, closed, removed, uncertain, unsuccessfully reverified, and `Files produced` roles before calculating counts and rank order.
9. Rank verified plausible roles with short tradeoff explanations. Separate direct evidence, transferable evidence, and gaps.
10. Update `job_search/roles.csv`, `job_search/reviewed_roles.md`, and `job_search/search_log.md` with ISO dates. Preserve prior decisions and search history, including completed searches with no new matches.

Do not draft application materials or create document files during discovery.
