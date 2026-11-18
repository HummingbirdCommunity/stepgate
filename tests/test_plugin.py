import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/stepgate'
spec = importlib.util.spec_from_file_location('build_codex', ROOT / 'scripts/build-codex.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class PluginTests(unittest.TestCase):
    def test_all_hosts_ship_the_same_release(self):
        claude = json.loads((PLUGIN / '.claude-plugin/plugin.json').read_text())
        codex = json.loads((PLUGIN / '.codex-plugin/plugin.json').read_text())
        kimi = json.loads((ROOT / '.kimi-plugin/plugin.json').read_text())
        agy = json.loads((ROOT / '.antigravity-plugin/plugin.json').read_text())
        marketplace = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
        self.assertEqual(claude['version'], codex['version'])
        self.assertEqual(claude['version'], kimi['version'])
        self.assertEqual(claude['version'], agy['version'])
        self.assertEqual(claude['version'], marketplace['plugins'][0]['version'])

    def test_kimi_paths_resolve_in_a_clean_install(self):
        with tempfile.TemporaryDirectory() as directory:
            installed = (Path(directory) / 'installed plugin').resolve()
            shutil.copytree(ROOT / '.kimi-plugin', installed / '.kimi-plugin')
            shutil.copytree(PLUGIN, installed / 'plugins/stepgate')
            manifest = json.loads((installed / '.kimi-plugin/plugin.json').read_text())
            commands = (installed / manifest['commands']).resolve()
            conventions = (installed / manifest['systemPromptPath']).resolve()
            self.assertTrue(commands.is_relative_to(installed))
            self.assertTrue(conventions.is_relative_to(installed))
            self.assertEqual(commands, installed / 'plugins/stepgate/commands')
            self.assertTrue(conventions.is_file())
            self.assertEqual({path.stem for path in commands.glob('*.md')},
                             {path.stem for path in (PLUGIN / 'commands').glob('*.md')})
            self.assertTrue((commands / '../references/configuration.md').resolve().is_file())

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

    def test_agy_entrypoints_resolve_in_a_clean_install(self):
        with tempfile.TemporaryDirectory() as directory:
            installed = (Path(directory) / 'installed plugin').resolve()
            for path in ('.antigravity-plugin', 'skills', 'plugins/stepgate'):
                shutil.copytree(ROOT / path, installed / path)

            manifest = json.loads((installed / '.antigravity-plugin/plugin.json').read_text())
            self.assertEqual(manifest['name'], 'stepgate')
            self.assertNotIn('skills', manifest)
            shared = installed / 'plugins/stepgate'
            commands = {file.stem for file in (shared / 'commands').glob('*.md')}
            skills = {file.parent.name: file for file in installed.glob('skills/*/SKILL.md')}
            self.assertEqual(skills.keys(), commands)
            self.assertTrue((shared / 'references/configuration.md').is_file())

            for source, expected in builder.generated_skills('agy'):
                name = source.parent.name
                with self.subTest(skill=name):
                    skill = skills[name]
                    text = skill.read_text()
                    self.assertEqual(text, expected)
                    self.assertIn(f'\nname: {name}\n', text)
                    self.assertIn('\ndisable-model-invocation: true\n', text)
                    links = re.findall(r'\[[^\]]+\]\(([^)]+)\)', text)
                    targets = {(skill.parent / link).resolve() for link in links}
                    self.assertEqual(targets, {shared / 'references/agy.md',
                                               shared / 'commands' / f'{name}.md'})
                    for target in targets:
                        self.assertTrue(target.is_file())

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



class LayeredCompactionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name)
        self.root = self.directory / 'repo with spaces'
        self.root.mkdir()
        subprocess.run(['git', 'init', '-q', '-b', 'feat/VH-1140-example',
                        str(self.root)], check=True)
        (self.root / '.stepgate').mkdir()
        self.base = self.root / '.stepgate/config.md'
        self.local = self.root / '.stepgate/config.local.md'
        self.base.write_text('## Plan storage\n- Plans directory: shared plans\n')
        self.make_plan(self.root / 'shared plans')

    def make_plan(self, directory, name='VH-1140.md'):
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / name
        path.write_text('# Work in progress\n')
        return path

    def run_hook(self, cwd=None):
        return subprocess.run(
            ['bash', str(PLUGIN / 'hooks/after-compact.sh')],
            input=json.dumps({'cwd': str(cwd or self.root)}),
            text=True, capture_output=True, check=True).stdout

    def test_local_directory_overrides_base_from_subdirectory(self):
        self.local.write_text('## Plan storage\n- Plans directory: local plans\n')
        self.make_plan(self.root / 'local plans')
        nested = self.root / 'src'
        nested.mkdir()
        output = self.run_hook(nested)
        self.assertIn('Plan: local plans/VH-1140.md (matches the branch)', output)
        self.assertIn('.stepgate/config.local.md if present', output)
        self.assertNotIn('Plan: shared plans/', output)

    def test_missing_blank_or_unrelated_local_fields_inherit(self):
        for content in ('', '## Language\n- Local language: English\n',
                        '## Plan storage\n- Plans directory:   \n',
                        '## Plan storage\r\n- Plans directory: \t\r\n'):
            with self.subTest(content=content):
                self.local.write_text(content)
                self.assertIn('Plan: shared plans/VH-1140.md', self.run_hook())

    def test_absolute_directory(self):
        plans = self.directory / 'external plans'
        self.make_plan(plans)
        self.local.write_text('## Plan storage\n- Plans directory: ' + str(plans) + '\n')
        self.assertIn('Plan: ' + str(plans / 'VH-1140.md'), self.run_hook())

    def test_symlinked_configs_keep_paths_relative_to_repository(self):
        base_target = self.directory / 'base.md'
        local_target = self.directory / 'local.md'
        self.base.rename(base_target)
        self.base.symlink_to(base_target)
        local_target.write_text('## Plan storage\n- Plans directory: linked plans\n')
        self.local.symlink_to(local_target)
        self.make_plan(self.root / 'linked plans')
        self.assertIn('Plan: linked plans/VH-1140.md', self.run_hook())

    def test_removing_local_file_restores_base(self):
        self.local.write_text('- Plans directory: local plans\n')
        self.make_plan(self.root / 'local plans')
        self.assertIn('Plan: local plans/VH-1140.md', self.run_hook())
        self.local.unlink()
        self.assertIn('Plan: shared plans/VH-1140.md', self.run_hook())

    def test_blank_base_uses_default_directory(self):
        self.base.write_text('## Plan storage\n- Plans directory: \t\n')
        self.make_plan(self.root / '.stepgate/plans')
        self.assertIn('Plan: .stepgate/plans/VH-1140.md', self.run_hook())

    def test_configuration_values_are_not_executed_or_printed(self):
        sentinel = self.directory / 'executed'
        self.local.write_text(
            '- Plans directory: $(touch "' + str(sentinel) + '")\n'
            '- Private note: DO-NOT-PRINT-THIS\n')
        output = self.run_hook()
        self.assertFalse(sentinel.exists())
        self.assertNotIn('DO-NOT-PRINT-THIS', output)
        self.assertNotIn('Plan:', output)

    def test_broken_local_symlink_reports_problem_without_guessing_plan(self):
        self.local.symlink_to(self.directory / 'missing.md')
        output = self.run_hook()
        self.assertIn('unreadable or has a broken link', output)
        self.assertIn('.stepgate/config.local.md', output)
        self.assertNotIn('Plan:', output)

    def test_broken_base_symlink_still_reminds_to_resolve_configuration(self):
        self.base.unlink()
        self.base.symlink_to(self.directory / 'missing.md')
        output = self.run_hook()
        self.assertIn('unreadable or has a broken link', output)
        self.assertNotIn('Plan:', output)

    def test_local_only_does_not_mark_project_initialized(self):
        self.base.unlink()
        self.local.write_text('- Plans directory: local plans\n')
        self.assertEqual(self.run_hook(), '')

    def test_plan_field_in_another_section_does_not_override(self):
        self.local.write_text('## Other\n- Plans directory: wrong\n'
                              '## Plan storage\n- Plans directory: local plans\n')
        self.make_plan(self.root / 'local plans')
        self.assertIn('Plan: local plans/VH-1140.md', self.run_hook())

    def test_fallback_preserves_spaces_in_filenames_and_ignores_ui(self):
        (self.root / 'shared plans/VH-1140.md').unlink()
        self.make_plan(self.root / 'shared plans', 'review notes.md')
        self.make_plan(self.root / 'shared plans', 'new-ui.md')
        self.assertIn('Plan: shared plans/review notes.md (most recently edited)',
                      self.run_hook())

    def test_edited_symlink_target_is_read_again(self):
        target = self.directory / 'local.md'
        target.write_text('- Plans directory: first plans\n')
        self.local.symlink_to(target)
        self.make_plan(self.root / 'first plans')
        self.make_plan(self.root / 'second plans')
        self.assertIn('Plan: first plans/VH-1140.md', self.run_hook())
        target.write_text('- Plans directory: second plans\n')
        self.assertIn('Plan: second plans/VH-1140.md', self.run_hook())

if __name__ == '__main__':
    unittest.main()
