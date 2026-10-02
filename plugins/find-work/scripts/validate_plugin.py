"""Validate local manifests, all skill frontmatter, and bundled reference links."""
import json
import re
import sys
from pathlib import Path

def validate(root):
    errors = []
    try:
        manifest = json.loads((root/'.codex-plugin/plugin.json').read_text(encoding='utf-8'))
        if manifest.get('name') != 'find-work' or manifest.get('skills') != './skills/' or not manifest.get('version'):
            errors.append('Invalid plugin identity, skills path, or version')
        marketplace = json.loads((root.parents[1]/'.agents/plugins/marketplace.json').read_text(encoding='utf-8'))
        if not any(p.get('name') == 'find-work' and p.get('source', {}).get('path') == './plugins/find-work' for p in marketplace.get('plugins', [])):
            errors.append('Marketplace does not reference this plugin')
    except (OSError, ValueError, TypeError) as exc:
        errors.append(str(exc))
    skills = sorted((root/'skills').glob('*/SKILL.md'))
    if not skills:
        errors.append('No skills found')
    for path in skills:
        text = path.read_text(encoding='utf-8')
        front = re.match(r'^---\n(.*?)\n---\n', text, re.S)
        if not front:
            errors.append(f'{path.parent.name}: missing frontmatter')
            continue
        fields = dict(re.findall(r'^(name|description): (.+)$', front.group(1), re.M))
        if fields.get('name') != path.parent.name or not fields.get('description'):
            errors.append(f'{path.parent.name}: invalid skill name or description')
        if not (path.parent/'agents/openai.yaml').is_file():
            errors.append(f'{path.parent.name}: missing UI metadata')
    for path in (root/'skills').rglob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if '://' in link or link.startswith('#'):
                continue
            destination = (path.parent / link.split('#')[0]).resolve()
            if not destination.is_relative_to(root.resolve()) or not destination.is_file():
                errors.append(f'{path.relative_to(root)}: broken or escaped link {link}')
    return errors

if __name__ == '__main__':
    errors = validate(Path(__file__).resolve().parents[1])
    for error in errors:
        print(error, file=sys.stderr)
    print('Plugin and all skills validation ' + ('failed' if errors else 'passed'))
    raise SystemExit(bool(errors))
