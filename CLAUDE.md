# Stepgate - project guide for Claude Code

Stepgate is a Claude Code plugin: a supervised, human-in-the-loop feature-authoring
loop (`plan -> step -> ship`, plus `init` for one-time project setup that the working
commands auto-run when there's no config). The plugin lives at the repo root
(`.claude-plugin/{plugin,marketplace}.json`, `commands/`); the command prompt files run
in *other people's* repos. **Stepgate is the umbrella for the whole methodology** - future
tracks (reviewing others' PRs, promoting between environments) are added as more
`/stepgate:*` commands in this one plugin, not as separate plugins.

## Commits

- Style: Conventional Commits (`type(scope): subject`), e.g. `feat:`, `fix:`, `docs:`, `chore:`.
- Never add a `Co-Authored-By` trailer.
- Hyphens, not em dashes. English only.
- On any release: bump `version` in `.claude-plugin/plugin.json` and add a `CHANGELOG.md` entry.

## Editing commands (`commands/*.md`)

- These are prompts for an AI, not docs for a reader. Every line must drive behavior;
  cut reader-facing rationale.
- **Host-neutral**: describe the goal, not a Claude-only feature. Don't hard-code other
  slash commands or tool names; mark Claude-specific mechanisms as optional.
- **Config over hard-coding**: project specifics come from the user's
  `.stepgate/config.md`, never baked into a command. Prefer referencing a user's
  existing doc over re-asking.
- Keep `README.md` and `CHANGELOG.md` in sync when behavior changes.

## Porting to another tool (future)

Stepgate ships Claude-only for now, but nothing about the methodology is Claude-specific - adding a tool (Cursor, Codex, ...) is mechanical:

- The canonical content is the command bodies in `commands/*.md`. Reuse them as-is.
- Only three things are Claude-specific: the frontmatter (`description`, `argument-hint`), the `$ARGUMENTS` token, and the `/stepgate:*` cross-references. Translate those to the target tool's command/prompt format.
- Add the tool's own packaging dir (e.g. `.cursor-plugin/`, `.codex-plugin/`) as a sibling. Keep one canonical source and thin per-tool wrappers.
- The config path (`.stepgate/config.md`) and format are already tool-neutral - every tool's stepgate reads the same file.
- Do this only when actually adding a tool. Don't build multi-tool machinery (sync scripts, per-tool dirs) before then.
