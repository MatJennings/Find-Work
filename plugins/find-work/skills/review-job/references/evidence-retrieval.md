# Targeted evidence reads

Use relevant claim IDs from the evidence ledger to route reads to controlling employer records. The ledger and its cited sources remain authoritative. There is no new generated evidence index or fact cache.

```text
python <plugin>/scripts/retrieve_evidence.py --root <workspace> --source experience/employers/example.md --catalog
python <plugin>/scripts/retrieve_evidence.py --root <workspace> --source experience/employers/example.md --section "Relevant work" --claim-id EXAMPLE-1
```

Select exact catalog headings. Child headings expand to complete level-two topics. Small files and sources without recognizable boundary headings stay whole. Larger structured records return selected topics, preamble, and scope, authority, approved-public-wording and disclosure guard sections. The current confidentiality policy and selected complete ledger rows accompany source text. Catalog output is routing only.

Inspect completeness, warnings, source hashes, inclusive line spans, ledger evidence and disclosure states, and all returned boundaries. Missing or duplicate headings, claim IDs, files, or disclosure policy need bounded fallback. No matching ledger row requires explicit relevant claim IDs or manual ledger inspection before external use. Imported binaries require normal extraction, not this text helper. Never treat a routing no-match as lack of experience.

Check semantic coverage of every material role requirement. Expand topics or read the full source when facts, scope, restrictions or cross-references span sections. Select only applicable claim IDs and reconcile their cited sources. A selected row is not proof the source substantiates it, and a supported fact is not disclosure approval. Existing gap questions and application approval remain unchanged.

Within the same session, reuse exact relevant retained context while current. When change is plausible, `check_retrieval_sources.py --root <workspace> --report <private-retrieval-report.json>` checks hashes without returning bodies. New sessions, lost text, compaction, or changed scope require targeted rereads even when hashes match. Byte freshness never proves semantic coverage, live verification, approval or submission. Keep transient reports private, not in shared releases.

If Python is unavailable or records use a legacy layout, read only the matching ledger rows and complete relevant sources manually. Helpers are optional and use the standard library only.
