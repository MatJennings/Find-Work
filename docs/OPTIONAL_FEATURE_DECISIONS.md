# Default workflow and optional features

Decision date 2026-10-02. The live Free-account setup will be performed separately. No independent quality or account-usage improvement has been established. Retain a small default workflow and use observed feedback to justify additions.

## Included now

Targeted role lookup, shared batch lookup, phase routing, review reuse, material gap questions, evidence-led drafting, intermediary tracing, guarded evidence retrieval and complete approved-example retrieval. Version 0.5.0 adds, on 2026-10-26, single-context writing quality guidance learned in the reference project: argument before proof, a one-pass opening-thesis choice, the problem, approach and one-proof letter shape, a read-aloud check, resume-opening tests for concrete payoff, one thread, cold-read clarity and banned openings, a deterministic letter clarity script, seniority judged by scope, hard-rule screens, linked job titles, no bullets split across pages, optional standing form-answer defaults, and not re-reading auto-loaded instructions. Each answers an observed problem there: a rejected letter, peer feedback asking for shorter letters about approach rather than history, generic or overloaded openings, and measured usage waste from re-reads and truncated long reads. None adds an agent, a required record or a review turn. Tests demonstrate these deterministic behaviors and preserved boundaries, not model-level efficiency or writing quality. Manual reads remain supported when Python or a structured layout is unavailable.

## Optional or deferred

| Feature | Default | When to reconsider |
|---|---|---|
| Deep letter review, with multi-agent thesis selection, independent review and audit | Off | Candidate turns it on, typically for highest-fit roles, on a plan with separate agents and enough usage. Measured in the reference project at eight agents and several million processed tokens per letter after cost fixes, so not expected to fit a free plan |
| Independent drafting reviewer | Off | User requests it or repeated material objections justify the additional review |
| Separate hook decision card | Off | User wants a decision audit beyond the concise existing application argument |
| Full first-to-final learning records | Off | Repeated revision problems need comparison beyond concise approved-example feedback |
| Exhaustive company research | Proportional to decision | A serious uncertainty materially changes recommendation or user requests depth |
| Fixed employer quotas and specialist queues | No universal quota or sector queue | Candidate target profile and repeated source yield justify a private configuration |
| Scheduled searches | Explicit opt-in, capability-dependent | User asks for recurring work and tools can perform it |
| AI visual QA | Requested only | User asks and all current pages can be inspected |
| Company-follow handoff or email integration | No automatic action | Separate explicit request and an available authorized capability |
| Persistent generated fact or wording cache | Not included | Reconsider only with demonstrated need and a design that preserves source authority and freshness |
| Mandatory model choice or paid tools | Not included | Never required for baseline interviewing, drafting or tracking |

Do not add a feature solely because the private reference project has it. Record any private preference in existing profile files. Do not copy candidate names, employer-specific evidence, salary floors, industry exclusions, signature phrasing, punctuation, or document layout rules into shared defaults.

## Acceptance before adding an optional feature

Identify a concrete observed problem, the smallest proposed change, evidence that it applies beyond one candidate's preference, and relevant capability limits. Add a focused test where feasible. Preserve truthful claims, disclosure, complete approval, role identity, and user-confirmed submission. Compare recovery effort and useful output during real use before claiming efficiency. Do not require new records or extra review turns unless they solve the observed problem.

## Upgrade boundaries

Shared plugin source version is 0.5.0. Workspace schema remains 3 because tracker schemas and required workspace paths are unchanged. New blank profile prompts apply to new workspaces. Existing workspaces receive the 0.5.0 skill guidance after updating the plugin, and can add the new preference fields by hand. Migration adds missing scaffold files and never replaces existing profiles or local instructions. Existing workspaces should review obsolete policy deliberately, rather than accept a silent rewrite. Retain original source history and candidate approval state.

Source updates do not reinstall the plugin or regenerate historical release archives. Refresh through the documented updater and start a new task before testing the new skills. Publishing commits is distinct from changing installation state.
