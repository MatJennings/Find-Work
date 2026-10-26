# Deep letter review (opt-in)

Off by default. Use this only when the candidate turns it on in `profile/cover_letter_preferences.md` or asks for it on a specific letter. A reasonable trigger is the candidate's highest-fit roles. It replaces the one-pass thesis step in [cover-letter craft](cover-letter-craft.md) with independent judgment, and keeps every shape, voice and truthfulness rule there.

## Cost and capability

This procedure needs separate clean-context agents and substantial usage. In the reference project it used eight agents and several million processed tokens per letter even after cost fixes, a meaningful share of a paid plan's weekly allowance. It is not expected to fit a free plan. Confirm the candidate's plan and that separate agents are available, record the choice in the capability record, and tell the candidate before starting. If separate agents are unavailable, say so and use the default procedure. A same-context review is never independent.

## Shared packet

Before spawning any agent, collect once: the verified posting, the current resume wording, the controlling evidence and its disclosure limits, the candidate's cover-letter preferences, relevant approved openings, and any letters the candidate has rated for quality. Withhold earlier letters for this application, their reviews, the candidate's criticism and the writer's rationale. Split the packet into numbered files of about 7K tokens or less, each ending with an `END OF PACKET FILE k OF n` line. Some tools silently cut the middle out of a larger read. Every agent reads each file once, confirms every end line with no truncation notice, and opens no other source file.

## Steps

1. **Anchor.** One agent names the role level, the single thing the employer most cares about with exact quotes, two runner-up anchors, and narrower traps. It writes no theses.
2. **Theses.** Two writers run in parallel. The first writes three different opening theses. The second writes one fresh thesis and one adapted from the approved openings or rated letters. Each card has the opening line, central idea, employer anchor with a quote, the question it makes a reader ask, one supported proof point with its source wording, and why this level.
3. **Judges.** Shuffle the five cards under neutral IDs without editing them. Two judges, the second with reversed order and fresh IDs, score each card 1 to 5 on boldness, pull, clarity, employer fit, provability and overall idea, rank them without ties, and flag any card the evidence cannot reach. The lowest summed rank wins. A card both judges flag cannot win.
4. **Letter.** A fresh writer drafts around the winning thesis and both judges' evidence cautions.
5. **Review.** A clean-context reviewer first records its own view of the strongest supported argument without seeing the letter, then reviews the letter. It leads with any materially better missed direction, then checks the substantive thought, the candidate's supported agency, the employer connection, a worthwhile interview question the letter earns with a quoted trigger, read-aloud flow and voice, and claim support.
6. **Audit.** A separate clean-context auditor repeats the independent argument step, then assesses both the letter and the review. Good-enough work passes when alternatives are only marginal. A material missed opportunity or unsupported claim returns the letter to the writer.

Allow at most two revisions, each with a fresh reviewer and auditor. If the letter still does not pass, hold it for the candidate with the unresolved findings. Never rotate agents until one agrees.

## Cost discipline

- Spawn each stage together and make one long blocking wait. Do not poll, list agents or send status messages while they work.
- The coordinator does not re-read instructions already loaded or source files the packet contains.
- Do not add agents for a step this procedure does not name.

## Records and boundaries

Save a compact `letter_review.json` in the application folder with the cards, scores, winner, review and audit verdicts, findings and the exact letter's SHA256. It is process evidence, never approved wording or candidate evidence. A reviewer or auditor pass is not the candidate's approval, does not expand disclosure, and never overrides the candidate's rejection. Do not add generated theses to the approved openings library.
