# Stepgate - project guide

Stepgate is a Claude Code, Codex, and Kimi Code plugin: a feature-authoring
loop (`plan -> step -> ship`, plus `init` for one-time project setup that the working
commands auto-run when there's no config, and `compact` to carry state across a context
compaction). The plugin lives in `plugins/stepgate/`
(`.claude-plugin/plugin.json`, `commands/`), listed by the marketplace at the repo root
(`.claude-plugin/marketplace.json`); the command prompt files run
in *other people's* repos. **Stepgate is the umbrella for the whole methodology** - future
tracks (reviewing others' PRs, promoting between environments) are added as more
`/stepgate:*` commands in this one plugin, not as separate plugins.

## Commits

- Style: Conventional Commits (`type(scope): subject`), e.g. `feat:`, `fix:`, `docs:`, `chore:`.
- Never add a `Co-Authored-By` trailer.
- Hyphens, not em dashes. English only.
- On any release: bump `version` in `plugins/stepgate/.claude-plugin/plugin.json` and add a `CHANGELOG.md` entry.

## Editing commands (`plugins/stepgate/commands/*.md`)

- These are prompts for an AI, not docs for a reader. Every line must drive behavior;
  cut reader-facing rationale.
- **Host-neutral**: describe the goal, not a Claude-only feature. Don't hard-code other
  slash commands or tool names; mark Claude-specific mechanisms as optional.
- **Config over hard-coding**: project specifics come from the user's
  `.stepgate/config.md`, never baked into a command. Prefer referencing a user's
  existing doc over re-asking.
- Keep `README.md` and `CHANGELOG.md` in sync when behavior changes.
- Plan executable acceptance checks for every step; run the changed API/UI/consumer before committing. Unit tests or prompt-text assertions alone do not verify behavior.

## Host packaging and shared source

The canonical content is `plugins/stepgate/commands/*.md`. All hosts read those files; never copy their workflow bodies into a second maintained instruction set.

- Claude packaging is in `plugins/stepgate/.claude-plugin/` and the root `.claude-plugin/marketplace.json`.
- Codex packaging is in `plugins/stepgate/.codex-plugin/`, `skills/`, and the root `.agents/plugins/marketplace.json`. Its thin skills read the canonical command and `plugins/stepgate/references/codex.md` for host-specific conventions.
- Kimi packaging is the root `.kimi-plugin/plugin.json`, pointing to canonical commands and `plugins/stepgate/references/kimi.md`. Export committed plugin files for clean local installs; do not package `.git` or `.stepgate`.
- Run `python3 scripts/build-codex.py` when command metadata changes.
- Before a release, run `python3 scripts/build-codex.py --check` and `python3 -m unittest discover -s tests -v`.
- Keep all three host manifests and the Claude marketplace version in sync, and add one changelog entry describing the release. Existing project configs stay intact.
