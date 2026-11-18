#!/usr/bin/env python3
"""Generate Codex and Antigravity CLI skills from the shared command metadata."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins' / 'stepgate'
HOSTS = {
    'codex': (
        PLUGIN / 'skills', '../..', 'Codex', '', '',
        'Text following the skill mention is its invocation arguments.',
    ),
    'agy': (
        ROOT / 'skills', '../../plugins/stepgate', 'Antigravity CLI',
        'disable-model-invocation: true\n',
        'If the absolute path of this skill is unavailable, run `agy plugin list --json`. '
        'Use the `path` of the enabled `stepgate` entry as the installed plugin root. '
        'Resolve the links below from this skill folder under `skills/` in that root.\n\n',
        'Use the text after the slash command as its invocation arguments.',
    ),
}


def generated_skills(host='codex'):
    directory, workflow_root, label, extra_metadata, locate_skill, arguments = HOSTS[host]
    for command in sorted((PLUGIN / 'commands').glob('*.md')):
        metadata, _ = command.read_text().removeprefix('---\n').split('\n---\n', 1)
        description = next(line.removeprefix('description: ') for line in metadata.splitlines()
                           if line.startswith('description: '))
        name = command.stem
        text = ('---\n'
                f'name: {name}\n'
                f'description: {json.dumps("StepGate " + name + ": " + description)}\n'
                f'{extra_metadata}'
                '---\n\n'
                f'# StepGate {name}\n\n'
                f'{locate_skill}'
                f'Read [{label} host conventions]({workflow_root}/references/{host}.md), then '
                f'[the canonical {name} workflow]({workflow_root}/commands/{name}.md) in full. '
                f'Run that workflow using the host conventions. {arguments}\n')
        yield directory / name / 'SKILL.md', text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if generated entrypoints are stale')
    args = parser.parse_args()
    stale = []
    for host in HOSTS:
        for path, text in generated_skills(host):
            if args.check:
                if not path.exists() or path.read_text() != text:
                    stale.append(str(path.relative_to(ROOT)))
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text)
    if stale:
        parser.exit(1, 'Run python3 scripts/build-codex.py to refresh:\n' + '\n'.join(stale) + '\n')


if __name__ == '__main__':
    main()
