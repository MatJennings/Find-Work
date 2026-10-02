"""Read selected complete approved-writing entries without treating them as facts."""
import argparse
import json
import re
from pathlib import Path
from context_sources import read_source, headings, spans

LIBRARIES = {'resume':'approved_resume_openings.md', 'cover':'approved_cover_letter_openings.md', 'answers':'approved_application_answers.md'}

def metadata(lines,item):
    body = '\n'.join(lines[item['start']:item['end']])
    fields = {}
    allowed = {'company','role','context','reuse guidance','tags','approval date','status','approval scope','evidence and disclosure limits'}
    for key,value in re.findall(r'^- ([^:\n]+):\s*(.*)$',body,re.M):
        if key.casefold() in allowed:
            fields[key.casefold()] = value
    return fields

def retrieve(root, library, queries=(), entries=()):
    warnings = []
    result = {'version':1,'complete':False,'sources':[],'warnings':warnings,'catalog':[],'entries':[]}
    try:
        if library not in LIBRARIES:
            raise ValueError('Unknown writing library')
        lines, source = read_source(root,'sources/authoritative/'+LIBRARIES[library],('sources/authoritative/',))
        result['sources'].append(source)
    except (OSError,ValueError) as exc:
        warnings.append(str(exc))
        return result
    items = [item for item in headings(lines) if item['level'] == 2]
    result['policy'] = spans(lines,[(0,items[0]['start'] if items else len(lines))])
    if not items:
        # Blank libraries are valid. Legacy prose is returned in full for manual routing.
        if queries or entries:
            warnings.append('No structured entries. Read returned library text and do not infer that no useful example exists.')
        result['complete'] = not warnings
        result['limitations'] = ['Library text is a style reference, never factual evidence or approval for a new application.']
        return result
    duplicates = {i['heading'] for i in items if sum(j['heading']==i['heading'] for j in items)>1}
    if duplicates:
        warnings.append('Ambiguous duplicate entry headings: '+', '.join(sorted(duplicates)))
    selected = []
    for item in items:
        fields = metadata(lines,item)
        routing = item['heading']+' '+ ' '.join(fields.values())
        if not queries or any(query.casefold() in routing.casefold() for query in queries):
            result['catalog'].append({'entry_id':item['heading'], 'metadata':fields, 'start_line':item['start']+1})
        if item['heading'] in entries and item['heading'] not in duplicates:
            selected.append(item)
    for entry in entries:
        if not any(i['heading']==entry for i in items):
            warnings.append('Entry not found: '+entry)
    groups = set()
    for item in selected:
        fields = metadata(lines,item)
        if fields.get('company') and fields.get('role'):
            groups.add((fields['company'].casefold(),fields['role'].casefold()))
    for item in items:
        fields = metadata(lines,item)
        identity = (fields.get('company','').casefold(),fields.get('role','').casefold())
        if identity in groups and item not in selected:
            selected.append(item)
    for item in sorted(selected,key=lambda i:i['start']):
        result['entries'].append({'entry_id':item['heading'],'metadata':metadata(lines,item),'excerpts':spans(lines,[(item['start'],item['end'])])})
    result['complete'] = not warnings
    result['limitations'] = ['Metadata search is OR substring routing, not semantic ranking. No-match requires broader search or manual reading.', 'Complete related versions retain their explicit status. Do not choose an approved version solely by date.', 'Historical or section approval never approves new application wording. Re-ground facts in controlling evidence.', 'Only approved_application_wording.md supplies production wording. No generated wording cache or application-state changes.']
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--library',choices=LIBRARIES,required=True)
    parser.add_argument('--query',action='append',default=[])
    parser.add_argument('--entry',action='append',default=[])
    args = parser.parse_args()
    result = retrieve(args.root,args.library,args.query,args.entry)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['complete'] else 2

if __name__ == '__main__':
    raise SystemExit(main())
