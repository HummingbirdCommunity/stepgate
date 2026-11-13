import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/stepgate'
spec = importlib.util.spec_from_file_location('build_codex', ROOT / 'scripts/build-codex.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class PluginTests(unittest.TestCase):
    def test_both_hosts_ship_the_same_release(self):
        claude = json.loads((PLUGIN / '.claude-plugin/plugin.json').read_text())
        codex = json.loads((PLUGIN / '.codex-plugin/plugin.json').read_text())
        marketplace = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
        self.assertEqual(claude['version'], codex['version'])
        self.assertEqual(claude['version'], marketplace['plugins'][0]['version'])

    def test_codex_entrypoints_resolve_to_live_workflow_sources(self):
        generated = list(builder.generated_skills())
        self.assertEqual({path.parent.name for path, _ in generated},
                         {path.stem for path in (PLUGIN / 'commands').glob('*.md')})
        for path, text in generated:
            self.assertEqual(path.read_text(), text)
            source = path.parent / '../../commands' / (path.parent.name + '.md')
            self.assertTrue(source.resolve().is_file())
            self.assertTrue((path.parent / '../../references/codex.md').resolve().is_file())
            self.assertNotIn('## Phase 1', text)

    def test_compaction_reminder_resolves_project_config_and_branch_plan(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'repo with spaces'
            root.mkdir()
            subprocess.run(['git', 'init', '-q', '-b', 'feat/VH-1140-example', str(root)], check=True)
            script = PLUGIN / 'hooks/after-compact.sh'
            before = subprocess.run(['bash', str(script)], input=json.dumps({'cwd': str(root)}),
                                    text=True, capture_output=True, check=True)
            self.assertEqual(before.stdout, '')
            plans = root / '.stepgate/plans'
            plans.mkdir(parents=True)
            config = Path(directory) / 'config.md'
            config.write_text('- Plans directory: .stepgate/plans\n')
            (root / '.stepgate/config.md').symlink_to(config)
            (plans / 'VH-1140.md').write_text('# Work in progress\n')
            (plans / 'another-plan.md').write_text('# More recent, unrelated work\n')
            nested = root / 'src'
            nested.mkdir()
            after = subprocess.run(['bash', str(script)], input=json.dumps({'cwd': str(nested)}),
                                   text=True, capture_output=True, check=True)
            self.assertIn('VH-1140.md (matches the branch)', after.stdout)
            self.assertIn('re-read .stepgate/config.md in full', after.stdout)


if __name__ == '__main__':
    unittest.main()
