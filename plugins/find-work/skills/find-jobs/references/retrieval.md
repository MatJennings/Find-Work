# Historical lookup and reuse

Run the installed plugin script with an explicit private workspace root. Paths below are relative to the plugin, not the candidate folder.

```text
python <plugin>/scripts/lookup_discovery.py --root <workspace> --leads <lead-identities.json>
python <plugin>/scripts/lookup_application.py --root <workspace> --company "Example Company" --role "Example Role" --include-context
```

The temporary leads file is a JSON list of company and role with optional requisition_id and url. Keep it private and outside release artifacts. Batch lookup scans each tracker once, preserves full matched rows and provenance, and shares rows across leads. It makes no stage, verification, or skip decisions. Single lookup accepts company, role, requisition-id, and url with AND matching. Contains matching is explicit. Context reads only matched README, application-record, and role-review files, not approved wording or historical drafts.

Inspect completeness, warnings, candidate identities, and conflicting states. Different requisitions remain separate. URLs may be an employer/ATS pair, but require reconciliation. An incomplete lookup, including missing trackers or malformed rows, makes no-match inconclusive. Use a bounded broader company or requisition lookup, warning-row inspection, or matching folder read. Never scan every application merely to resolve one role.

Reuse a matching unchanged review after reconciling identity, the user's decisions, and current requirements. Do not rereview unchanged known openings during quick discovery. Reopen changed qualifications, scope, or requisitions. Historical checks never replace required live verification. Approved wording and confirmed submission remain separate authorities.

In a new session or after exact context is lost, retrieve matching records again. In the same session, retain exact relevant text while it is current. Never reconstruct approval or candidate facts from memory or create a duplicate generated fact cache.

If Python is unavailable, use available local file tools to inspect matching tracker rows and target records manually. Keep the same identity, warning, verification and approval boundaries. Do not require an installation or paid tool merely to retrieve history.
