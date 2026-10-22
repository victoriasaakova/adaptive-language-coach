"""Build one public Project source from the canonical skill and references."""
import argparse
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    'SKILL.md', 'references/lesson-protocol.md', 'references/assessment.md',
    'references/records.md', 'references/configuration.md',
    'references/limitations.md', 'references/notion-sync.md',
    'templates/lesson.md', 'templates/state.md', 'config/schema.json',
]

def render():
    sections = ['# Adaptive Language Coach — ChatGPT Project bundle\n\n'
                'Generated from the canonical SKILL.md and its supporting files. '
                'Do not edit this generated copy. Contains no learner data.\n\n'
                'References to repository paths below resolve to the named sections in this file. '
                'The learner does not need to upload those files separately. '
                'Private paths denote agent-owned state, not required existing uploads. '
                'If Python helpers are unavailable, apply the documented SRS rules manually.\n']
    for name in SOURCES:
        body = (ROOT / name).read_text(encoding='utf-8')
        if name == 'SKILL.md':
            body = re.sub(r'\A---\n.*?\n---\n', '', body, count=1, flags=re.S)
        if name.endswith('.md'):
            body = re.sub(r'\[([^\]]+)\]\((?!https?://)([^)]+)\)', r'\1 (`\2`)', body)
        else:
            body = '```json\n' + body + '```\n'
        sections.append('\n---\n\n## Source: ' + name + '\n\n' + body)
    return ''.join(sections)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    dest = ROOT / 'docs/chatgpt-skill.md'
    content = render()
    if args.check:
        if not dest.exists() or dest.read_text(encoding='utf-8') != content:
            raise SystemExit('Project bundle is stale; run scripts/build_chatgpt_bundle.py')
        print('Project bundle: current')
    else:
        dest.write_text(content, encoding='utf-8')
        print('Project bundle: generated')

if __name__ == '__main__':
    main()
