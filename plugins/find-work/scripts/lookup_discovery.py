"""Read-only batch candidate lookup. Historical matches never establish live status."""
import argparse
import json
import sys
from pathlib import Path

try:
    from .lookup_application import ROOT, lookup, normalized, normalized_url, tracker_snapshot
except ImportError:
    from lookup_application import ROOT, lookup, normalized, normalized_url, tracker_snapshot


def ref(record):
    return f"{record['source']}:{record['record_number']}"


def lookup_discovery(root: Path, leads: list) -> dict:
    if not isinstance(leads, list) or not leads:
        raise ValueError("Provide a nonempty JSON list of leads")
    validated = []
    for lead in leads:
        if not isinstance(lead, dict) or set(lead) - {"company", "role", "requisition_id", "url"}:
            raise ValueError("Each lead accepts company, role, requisition_id and url only")
        if any(not isinstance(value, str) for value in lead.values()):
            raise ValueError("Lead values must be strings")
        lead = {key: value.strip() for key, value in lead.items() if value.strip()}
        if not lead.get("company") or not lead.get("role"):
            raise ValueError("Each lead needs company and role")
        if lead.get("url"):
            normalized_url(lead["url"])
        validated.append(lead)
    snapshot = tracker_snapshot(root.resolve())
    records, candidates, warnings = {}, [], []
    complete = True
    for number, lead in enumerate(validated, 1):
        queries = [{"company": lead["company"], "role": lead["role"]}]
        if lead.get("requisition_id"):
            queries.append({"company": lead["company"], "requisition_id": lead["requisition_id"]})
        if lead.get("url"):
            queries.append({"url": lead["url"]})
        selected, directories = {}, {}
        ambiguous = False
        for query in queries:
            result = lookup(root, query, _snapshot=snapshot)
            complete = complete and result["lookup_complete"]
            ambiguous = ambiguous or result["result"] == "ambiguous"
            for warning in result["warnings"]:
                if warning not in warnings:
                    warnings.append(warning)
            for record in result["records"]:
                clean = {key: value for key, value in record.items() if key != "match_type"}
                selected[ref(record)] = clean
            for directory in result["local_records"]:
                directories[directory["directory"]] = directory
        records.update(selected)
        flags = ["ambiguous_tracker_identity"] if ambiguous else []
        for record in selected.values():
            fields = record["fields"]
            for key in ("company", "role", "requisition_id"):
                if lead.get(key) and fields.get(key) and normalized(lead[key]) != normalized(fields[key]):
                    flag = f"different_{key}"
                    if flag not in flags:
                        flags.append(flag)
            if lead.get("url") and fields.get("official_url"):
                try:
                    if normalized_url(lead["url"]) != normalized_url(fields["official_url"]):
                        if "different_url" not in flags:
                            flags.append("different_url")
                except ValueError:
                    flags.append("invalid_stored_url")
        states = {normalized(r["fields"].get("application_status") or (r["fields"].get("status") if r["source"] == "applications.csv" else "") or "")
                  for r in selected.values()}
        if len(states - {""}) > 1:
            flags.append("different_recorded_states")
        candidates.append({"lead_number": number, "lead": lead,
                           "result": "historical_candidates" if selected else "no_match",
                           "record_refs": list(selected), "identity_flags": flags,
                           "local_records": list(directories.values())})
    return {"version": 1, "lookup_complete": complete, "candidates": candidates,
            "records": records, "sources": snapshot[1], "warnings": warnings,
            "limitations": ["Candidates require identity and decision reconciliation before review reuse.",
                            "No match with incomplete lookup is inconclusive. Check warning rows and relevant folders.",
                            "Different URLs may represent an employer/ATS pair. They are not automatically equivalent.",
                            "Stored verification is historical. Search coverage and required live checks remain unchanged.",
                            "This helper never skips, ranks, writes, approves or submits a role."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--leads", type=Path, required=True, help="JSON list of discovered lead identities")
    args = parser.parse_args()
    try:
        report = lookup_discovery(args.root, json.loads(args.leads.read_text(encoding="utf-8-sig")))
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["lookup_complete"] else 2


if __name__ == "__main__":
    sys.exit(main())
