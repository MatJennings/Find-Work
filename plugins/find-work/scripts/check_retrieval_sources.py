"""Check source freshness for retained retrieval context, without deciding reuse."""
import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path.cwd()


def allowed_path(root, relative):
    path = Path(relative)
    if path.is_absolute() or '..' in path.parts:
        raise ValueError('Source path must be workspace-relative without traversal')
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root):
        raise ValueError('Source path escapes workspace')
    normalized = resolved.relative_to(root).as_posix()
    allowed = normalized in {'applications.csv', 'job_search/roles.csv'}
    allowed = allowed or (normalized.startswith('sources/authoritative/') and resolved.suffix in {'.md', '.txt'})
    allowed = allowed or normalized == 'experience/evidence_ledger.csv'
    allowed = allowed or (normalized.startswith('experience/employers/') and resolved.suffix in {'.md', '.txt'})
    allowed = allowed or normalized == 'profile/confidentiality_preferences.md'
    allowed = allowed or (normalized.startswith('applications/') and resolved.suffix == '.md')
    if not allowed:
        raise ValueError('Path is outside supported retrieval sources')
    return resolved


def check(root: Path, reports: list):
    root = root.resolve()
    if not isinstance(reports, list) or not reports:
        raise ValueError('Provide at least one retrieval report or provenance manifest')
    warnings, expected = [], {}
    for number, report in enumerate(reports, 1):
        if not isinstance(report, dict) or report.get('version') != 1:
            warnings.append({'type': 'invalid_report', 'report_number': number})
            continue
        complete = report.get('lookup_complete', report.get('complete'))
        if complete is not True or report.get('warnings'):
            warnings.append({'type': 'original_retrieval_incomplete', 'report_number': number,
                             'original_warnings': report.get('warnings', [])})
        sources = report.get('sources')
        if not isinstance(sources, list) or not sources:
            warnings.append({'type': 'missing_source_metadata', 'report_number': number})
            continue
        sources = list(sources)
        # lookup_application optional README/review text has its own provenance.
        local_records = report.get('local_records', [])
        if not isinstance(local_records, list):
            warnings.append({'type': 'invalid_local_provenance', 'report_number': number})
            local_records = []
        for directory in local_records:
            if isinstance(directory, dict):
                files = directory.get('files', [])
                if not isinstance(files, list):
                    warnings.append({'type': 'invalid_local_provenance', 'report_number': number})
                else:
                    sources.extend(file for file in files if isinstance(file, dict) and 'sha256' in file)
        for source in sources:
            try:
                if not isinstance(source, dict) or not isinstance(source.get('path'), str):
                    raise ValueError('Invalid source metadata')
                digest = source.get('sha256')
                if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-fA-F]{64}', digest):
                    raise ValueError('Missing or invalid SHA-256')
                path = allowed_path(root, source['path'])
                expected.setdefault(path, set()).add(digest.lower())
            except ValueError as exc:
                warnings.append({'type': 'invalid_source', 'report_number': number, 'reason': str(exc)})
    observations = []
    for path, digests in sorted(expected.items()):
        observation = {'path': path.relative_to(root).as_posix(), 'expected_sha256': sorted(digests)}
        if len(digests) > 1:
            warnings.append({'type': 'conflicting_snapshots', 'path': observation['path']})
        try:
            raw = path.read_bytes()
            actual = hashlib.sha256(raw).hexdigest()
            observation.update(current_sha256=actual, bytes_scanned=len(raw),
                               status='unchanged' if digests == {actual} else 'changed')
        except OSError as exc:
            observation.update(status='unavailable', reason=str(exc))
            warnings.append({'type': 'source_unavailable', 'path': observation['path']})
        observations.append(observation)
    state = 'incomplete' if warnings or not observations else 'changed' if any(o['status'] == 'changed' for o in observations) else 'unchanged'
    return {'version': 1, 'source_state': state, 'observations': observations, 'warnings': warnings,
            'limitations': ['Byte freshness only. It does not establish relevance, complete context, live status, approval or submission.',
                            'Reuse requires the exact relevant source context to remain available in this session.',
                            'Changed scope, missing context or compaction requires targeted retrieval even when hashes match.',
                            'Original incomplete lookup and source conflicts remain unresolved. Do not bypass their fallback.',
                            'Read current AGENTS.md and the invoked skill. This check does not replace policy or required live verification.']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--report', action='append', type=Path, required=True)
    args = parser.parse_args()
    try:
        reports = [json.loads(path.read_text(encoding='utf-8-sig')) for path in args.report]
        result = check(args.root, reports)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['source_state'] == 'unchanged' else 2


if __name__ == '__main__':
    sys.exit(main())
