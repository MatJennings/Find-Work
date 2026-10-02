# Approved examples and feedback

Start with the employer's mandate, the candidate's supported contribution and the resulting payoff. Retrieve only relevant examples. Similar titles alone do not establish fit.

```text
python <plugin>/scripts/retrieve_writing.py --root <workspace> --library resume --query "relevant context"
python <plugin>/scripts/retrieve_writing.py --root <workspace> --library resume --entry "Exact entry heading"
```

Libraries are resume, cover, and answers. Queries search headings and labeled metadata, not candidate wording. Exact entry selection returns the whole entry and related versions with exact company and role metadata. Reconcile recorded status and approval scope rather than choosing by date. No-match requires broader queries or a relevant manual read. Empty libraries are normal during onboarding. Legacy unstructured text is returned for manual routing without rewriting it.

New entries use the shared approved-writing-entry template. Keep only explicitly approved exact wording, context, scope, rationale, evidence and disclosure limits, and reuse guidance. Prior examples are style and decision history, not independent candidate facts. They do not approve a new application or expand section approval into document approval.

Capture concise substantive feedback in reuse guidance or the existing private application record when it would prevent repeated mistakes. Full first-to-final learning records and separate reviewers are optional. Do not scan unrelated application histories. Re-ground claims and employer assertions in the current sources and run contamination checks. Production uses only approved_application_wording.md.

If the helper or entry layout is unsuitable, read complete selected examples manually. Do not require Python for drafting or convert older libraries merely to use the helper.
