"""Retrieve controlling private evidence topics with disclosure and ledger context."""
import argparse
import csv
import io
import json
from pathlib import Path
from context_sources import read_source, headings, spans, exact_topic

GUARDS = ('purpose', 'authority', 'role overview', 'scope', 'boundar', 'confidential', 'disclosure', 'restriction', 'approved public', 'approved external', 'do not use')

def retrieve(root, source, sections=(), *, catalog=False, claim_ids=()):
    warnings, sources, claims = [], [], []
    result = {'version':1, 'complete':False, 'sources':sources, 'warnings':warnings, 'claims':claims, 'excerpts':[]}
    try:
        lines, metadata = read_source(root, source, ('experience/employers/', 'sources/authoritative/'), ('.md', '.txt'))
        if Path(metadata['path']).name in {'approved_resume_openings.md', 'approved_cover_letter_openings.md', 'approved_application_answers.md'}:
            raise ValueError('Approved writing libraries are style references, not factual evidence')
        sources.append(metadata)
    except (OSError, ValueError) as exc:
        warnings.append(str(exc))
        return result
    items = headings(lines)
    result['catalog'] = [{'heading':i['heading'], 'level':i['level'], 'start_line':i['start']+1} for i in items]
    if catalog:
        result['complete'] = True
        result['limitations'] = ['Catalog headings route reads and do not establish facts or gaps.']
        return result
    wanted = set(claim_ids)
    try:
        ledger_lines, ledger = read_source(root, 'experience/evidence_ledger.csv', ('experience/evidence_ledger.csv',))
        sources.append(ledger)
        reader = csv.DictReader(io.StringIO('\n'.join(ledger_lines)), strict=True)
        required = {'claim_id','source','evidence_status','disclosure_status','organization','claim','notes'}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError('Evidence ledger is missing required fields')
        seen = set()
        for row in reader:
            if None in row or any(value is None for value in row.values()):
                warnings.append('Malformed evidence ledger row at line ' + str(reader.line_num))
            claim_id = row.get('claim_id')
            if claim_id in seen:
                warnings.append('Duplicate evidence claim ID: ' + str(claim_id))
            seen.add(claim_id)
            linked = (row.get('source') or '').replace(chr(92), '/') == metadata['path']
            if claim_id in wanted or (not wanted and linked):
                claims.append({'end_line':reader.line_num, 'fields':row})
                if row.get('evidence_status') not in {'user_attested','document_supported','publicly_corroborated','needs_clarification'} or row.get('disclosure_status') not in {'approved_external','approval_required','confidential','do_not_use'}:
                    warnings.append('Unresolved evidence or disclosure state for claim ' + str(claim_id))
        found = {claim['fields'].get('claim_id') for claim in claims}
        if wanted - found:
            warnings.append('Claim IDs not found: ' + ', '.join(sorted(wanted-found)))
        if not claims:
            warnings.append('No ledger claims matched this source. Select relevant claim IDs or inspect the ledger before external use. No-match does not establish an experience gap.')
    except (OSError, ValueError, csv.Error) as exc:
        warnings.append(str(exc))
    try:
        policy, metadata = read_source(root, 'profile/confidentiality_preferences.md', ('profile/confidentiality_preferences.md',))
        sources.append(metadata)
        result['disclosure_policy'] = spans(policy, [(0,len(policy))])
    except (OSError, ValueError) as exc:
        warnings.append('Disclosure policy unavailable: ' + str(exc))
    intervals = []
    for section in sections:
        try:
            topic = exact_topic(items, section)
            intervals.append((topic['start'],topic['end']))
        except ValueError as exc:
            warnings.append(str(exc))
    guards = [i for i in items if any(term in i['heading'].casefold() for term in GUARDS)]
    # Small sources and unstructured boundaries stay whole, avoiding unsafe slicing.
    if not sections or sources[0]['bytes_read'] <= 16000 or not guards:
        intervals.append((0,len(lines)))
    elif intervals:
        intervals.append((0,next((i['start'] for i in items if i['level'] >= 2),len(lines))))
        intervals.extend((i['start'],i['end']) for i in guards)
    result['excerpts'] = spans(lines,intervals)
    result['complete'] = not warnings
    result['limitations'] = ['Selected source topics and claim rows remain distinct authorities. Claim selection is not proof of semantic coverage.', 'Read relevant scope and disclosure boundaries. Factual support does not approve disclosure or final wording.', 'No-match remains unknown. Broaden evidence before labeling a material gap.', 'No source text is changed or cached. This helper does not draft, approve, verify a job, or update application state.']
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--source', required=True)
    parser.add_argument('--section', action='append', default=[])
    parser.add_argument('--claim-id', action='append', default=[])
    parser.add_argument('--catalog', action='store_true')
    args = parser.parse_args()
    result = retrieve(args.root,args.source,args.section,catalog=args.catalog,claim_ids=args.claim_id)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['complete'] else 2

if __name__ == '__main__':
    raise SystemExit(main())
