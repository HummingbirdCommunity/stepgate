#!/usr/bin/env python3
"""Generate Codex skill entrypoints from the canonical Claude command metadata."""

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins' / 'stepgate'


def generated_skills():
    for command in sorted((PLUGIN / 'commands').glob('*.md')):
        metadata, _ = command.read_text().removeprefix('---\n').split('\n---\n', 1)
        description = next(line.removeprefix('description: ') for line in metadata.splitlines()
                           if line.startswith('description: '))
        name = command.stem
        text = ('---\n'
                f'name: {name}\n'
                f'description: {json.dumps("StepGate " + name + ": " + description)}\n'
                '---\n\n'
                f'# StepGate {name}\n\n'
                'Read [Codex host conventions](../../references/codex.md), then '
                f'[the canonical {name} workflow](../../commands/{name}.md) in full. '
                'Run that workflow using the host conventions. Text following the skill mention '
                'is its invocation arguments.\n')
        yield PLUGIN / 'skills' / name / 'SKILL.md', text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Fail if generated entrypoints are stale')
    args = parser.parse_args()
    stale = []
    for path, text in generated_skills():
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
