---
name: build-career-foundation
description: Import, reconcile, verify, and expand a candidate's work history from resumes, profiles, portfolios, reviews, certificates, public sources, and conversation. Use for onboarding, career-history interviews, source conflicts, evidence review, target-profile creation, writing preferences, or baseline application materials.
---

# Build Career Foundation

## Context

1. Use the already-loaded `AGENTS.md` without re-reading it. Read `profile/onboarding_status.md`, and only the matching profile, employer, evidence-ledger and import-index records needed for the current onboarding step. Inventory filenames before loading source bodies.
2. Read only the sources relevant to the current employer, conflict, or profile decision. Preserve original imports unchanged.

## Build the evidence base

1. Inventory every imported source in `sources/imported/index.md`. Mark unreadable, password-protected, image-only, or OCR-dependent sources explicitly and request a usable export, pasted text, clearer scan, or manual transcription when needed.
2. Extract employers, roles, dates, responsibilities, accomplishments, metrics, products, methods, education, and credentials. Cite supporting filenames in `experience/evidence_ledger.csv`.
3. Present conflicts and missing dates. Do not silently reconcile them.
4. Interview the user about one employer or substantial engagement at a time. Ask a small set of useful questions covering the problem, the candidate's role, actions, collaborators, scope, outcome, evidence, confidentiality, and possible interview stories.
5. Use the shared employer-context template for new structured records, preserving original sources and existing records. Store durable employer context under `experience/employers/<employer-slug>.md`. Update chronology and the evidence ledger as facts are clarified.
6. Give every claim both an evidence status and a disclosure status. Never describe user attestation alone as independent verification.
7. For a high-value claim that is not approved for external use, identify the strongest defensible alternative and record whether public corroboration, user approval, or legal review is needed.

## Build preferences and approved history

1. Build `profile/job_target_profile.md` through a short conversation covering roles, seniority, work ownership, industries, company types, location, work arrangement, compensation, travel, management scope, practical constraints, ethics, and exclusions.
2. Build or revise resume and cover-letter preferences from the user's examples and feedback. Record filename, metadata, editable-file retention, punctuation, voice, and QA preferences explicitly rather than inferring them.
3. Use the blank approved-writing libraries under `sources/authoritative/` to preserve only wording the user explicitly approves. Treat these records as voice and decision history, not boilerplate or independent factual evidence.
4. Present a concise foundation audit. Ask the user to approve chronology, reusable claims, target profile, confidentiality limits, writing preferences, and prohibited claims. Record decisions in `profile/onboarding_status.md`.

## Baseline documents

If no authoritative master exists, draft complete baseline wording in chat first. Create an authoritative resume or cover-letter master only after the user approves the complete wording or explicitly requests production from that wording. Preserve supplied originals under `sources/imported/` and place approved authoritative copies under `sources/authoritative/` using the canonical paths recorded in the profile.

Do not invent missing facts. Do not expose confidential information merely because it appears in a source.
