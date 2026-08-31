---
name: find-jobs
description: Find, refresh, verify, deduplicate, and rank current job openings against an approved candidate target profile. Use for quick searches, recurring searches, comprehensive searches, portfolio refreshes, or job-search tracker updates across any profession or seniority.
---

# Find Jobs

## Context

1. Read `AGENTS.md`, the approved target profile, the evidence summary needed for screening, `job_search/roles.csv`, and `applications.csv`.
2. Read only recent relevant search-log entries and matching serious reviews unless a full audit or historical comparison requires more.

## Search modes

- **Quick search**, the default for an ordinary current search: check high-yield general, employer, applicant-tracking-system, and target-relevant specialist sources. Verify plausible new roles and rank only new findings. Do not reverify the entire portfolio.
- **Comprehensive search**: cover the general boards, direct employers, applicant-tracking systems, specialist communities, relevant portfolio boards or recruiters, and any recurring sources recorded in the target profile. Reverify the active shortlist before presenting a complete current ranking.
- **Portfolio refresh**: use for all-current-role requests, complete rankings, and tracker audits. Reverify every role that could appear in the ranking on the same date.

Record completed, partial, paywalled, unavailable, and blocked source passes in `search_log.md`. Preserve completed searches with no new matches.

## Screen, verify, rank, and record

1. Search broadly enough to include direct and plausible transferable fits. Apply approved exclusions without inventing preferences.
2. Screen role shape before deep research. Use the candidate's desired ownership, responsibility, seniority, work arrangement, compensation, and exclusion criteria.
3. Treat job boards, aggregators, cached pages, indexed text, and search results as discovery only.
4. Verify only plausible roles. Classify a role `active` when its official employer role-detail page contains the role details and a current Apply control, application link, or functional form. The exact title does not also need to appear on the openings index. A generic applicant-tracking-system shell is insufficient. Use a rendered browser when needed.
5. Mark a role `removed` when the detail page is gone, redirects to an error or openings index, states that the role is unavailable, or lacks a current application path. Mark inconclusive roles `uncertain`. Exclude uncertain roles from recommendations and rankings.
6. Deduplicate by company, title, requisition ID, and official URL.
7. Keep preliminary discovery records compact. For serious roles, capture the official URL, verification date and method, posting age, status, location and work arrangement, headquarters, compensation and source, travel, company size and ownership, business and customers, target relevance, fit, gaps, recommendation, and application status.
8. Label ranking scope. A new-findings ranking does not require reverifying unrelated roles. A complete current ranking requires same-day reverification of every included active role.
9. Update `job_search/roles.csv` as the canonical structured tracker and append a concise search-log entry. Update `reviewed_roles.md` only for a serious review or meaningful change.
10. For an automated run, notify the user only when at least one new plausible role is verified, unless the user chooses another notification policy. Always record the run.

Do not draft application materials, create document files, or change application state during discovery.
