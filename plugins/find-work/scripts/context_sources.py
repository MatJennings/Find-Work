"""Shared read-only source and Markdown section mechanics. No derived fact cache."""
import hashlib
import re
from pathlib import Path

def read_source(root, relative, prefixes, suffixes=('.md', '.txt', '.csv')):
    root = Path(root).resolve()
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts:
        raise ValueError('Use a workspace-relative source without traversal')
    path = (root/rel).resolve()
    if not path.is_relative_to(root):
        raise ValueError('Source escapes workspace')
    name = path.relative_to(root).as_posix()
    if not any(name == prefix.rstrip('/') or name.startswith(prefix) for prefix in prefixes) or path.suffix.lower() not in suffixes:
        raise ValueError('Source is outside allowed records')
    raw = path.read_bytes()
    text = raw.decode('utf-8-sig')
    return text.splitlines(), {'path': name, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes_read': len(raw)}

def headings(lines):
    result, fence = [], None
    for index, line in enumerate(lines):
        fenced = re.match(r'^\s*(`{3,}|~{3,})', line)
        if fenced:
            marker = fenced.group(1)[0]
            fence = None if fence == marker else marker if fence is None else fence
            continue
        if fence:
            continue
        match = re.match(r'^(#{1,6})\s+(.+?)\s*#*\s*$', line)
        if match:
            result.append({'start': index, 'level': len(match.group(1)), 'heading': match.group(2)})
    for index, item in enumerate(result):
        item['end'] = next((other['start'] for other in result[index+1:] if other['level'] <= item['level']), len(lines))
    return result

def spans(lines, intervals):
    merged = []
    for start,end in sorted(intervals):
        if start >= end:
            continue
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(end,merged[-1][1])
        else:
            merged.append([start,end])
    return [{'start_line': start+1, 'end_line': end, 'text': '\n'.join(lines[start:end])} for start,end in merged]

def exact_topic(items, heading):
    matches = [item for item in items if item['heading'] == heading]
    if len(matches) != 1:
        raise ValueError('Missing or ambiguous exact heading: ' + heading)
    item = matches[0]
    parents = [p for p in items if p['level'] == 2 and p['start'] <= item['start'] < p['end']]
    return parents[0] if parents else item
