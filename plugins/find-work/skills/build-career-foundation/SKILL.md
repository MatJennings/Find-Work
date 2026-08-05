---
name: build-career-foundation
description: Import, reconcile, verify, and expand a candidate's work history from prior resumes, LinkedIn exports, portfolios, reviews, certificates, and conversation. Use for onboarding, career-history interviews, source conflicts, accomplishment inventories, evidence review, target-profile creation, or baseline resume preparation.
---

# Build Career Foundation

1. Read `AGENTS.md`, `profile/onboarding_status.md`, and existing files under `profile/`, `experience/`, and `sources/imported/`.
2. Inventory every imported source in `sources/imported/index.md`. Preserve original files unchanged. Mark unreadable, password-protected, image-only, or OCR-dependent sources explicitly. Ask the user to export as text or DOCX, paste the relevant text, provide a clearer scan, or manually transcribe the needed facts when extraction is unavailable.
3. Extract chronology and claims. Record employers, roles, dates, responsibilities, accomplishments, metrics, products, methods, education, and credentials. Cite the supporting filename in `experience/evidence_ledger.csv`.
4. Present conflicts and missing dates to the user. Do not silently reconcile conflicting sources.
5. Interview the user about one employer or substantial engagement at a time. Ask only a small set of useful follow-up questions per turn. Cover the problem, the user's role, actions, collaborators, scope, outcome, evidence, confidentiality, and a potential interview story.
6. Store durable employer context under `experience/employers/<employer-slug>.md`. Update `experience/chronology.csv` and `experience/evidence_ledger.csv` as facts are clarified.
7. Give every claim both an evidence status and a disclosure status. Evidence status is `user_attested`, `document_supported`, `publicly_corroborated`, or `needs_clarification`. Disclosure status is `approved_external`, `approval_required`, `confidential`, or `do_not_use`. Never describe user attestation alone as independent verification.
8. Build `profile/job_target_profile.md` through a short conversation covering roles, seniority, industries, location, work arrangement, compensation, travel, management scope, practical constraints, and exclusions.
9. Build or revise `profile/resume_preferences.md` and `profile/cover_letter_preferences.md` from the user's examples and feedback.
10. Present a concise foundation audit. Ask the user to approve the chronology, reusable claims, target profile, and prohibited claims. Record approvals in `profile/onboarding_status.md`.
11. If no authoritative master resume exists, draft complete baseline wording in chat. Create `sources/authoritative/master_resume.docx` only after the user approves the complete wording. If the user supplies an existing master, preserve the original import and place the approved authoritative copy at that exact path so file production can find it.

Do not invent missing facts. Do not expose confidential information merely because it appears in an imported source.
