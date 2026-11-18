# Stepgate

**A feature-authoring workflow for Claude Code, Codex, Kimi Code, and Antigravity CLI, with a human review before delivery.**

Plan together, build in small steps, and choose how review happens. In auto, the agent implements, self-reviews, checks, and commits each step; you review the whole branch at ship. In supervised mode, you also approve each file and commit.

## The loop

Three commands, run in a cycle - `plan` once, `step` after each piece you build, `ship` once.

**1. Plan.** Give it a ticket, a description, or both. Stepgate reads the ticket if you gave one, researches the code, settles the approach with you, then writes a small-step plan. A change to UI is drawn as a mockup first, so you pick the design before any code exists. Nothing is coded yet.

```
/stepgate:plan #42                               # a ticket
/stepgate:plan add rate limiting to login        # or just describe it
/stepgate:plan #42 also cover the signup route   # or a follow-up on shipped work
```

On a follow-up, stepgate checks the ticket against the current code, plans only what is left, and tells you if it is already done.

**2. Step.** For ordinary work, StepGate recommends auto: it implements the remaining steps, reviews each against your guideline, runs the checks, and commits each locally. For high-risk plans, it explains the concrete risk and recommends supervision.

```
/stepgate:step auto   # implement and check the remaining steps
/stepgate:step        # review one implemented step with you
```

Every step plans and executes a real acceptance check: call the running API, operate the UI, or exercise the actual consumer. Unit tests alone do not complete a step. Missing prerequisites stay pending unless you explicitly waive that check; auto uses the same gate.

Auto starts only when you explicitly choose it; approving a plan does not select a mode. You can choose supervision or switch modes anytime. File count alone is not a reason to discourage auto. If new material risks emerge, the agent stops and explains them. Your explicit choice is recorded in the plan and restored after compaction; current restrictions still apply.

**3. Ship.** When every step is done: a whole-branch review, end-to-end verification, then it goes out the way your project ends work - a pull request, a local merge, or just the gate, leaving the push to you. The PR's Test plan is the list of cases that were verified, ticked as they passed, with a reason beside any that could not be run.

```
/stepgate:ship
/stepgate:ship stage   # one stage of a ticket built in stages: the gate only, nothing goes out yet
```

Changes after the PR is open go through `step` like any other, then `ship` again refreshes the PR - re-running the cases they touch and updating the Test plan.

The agent reviews every step in either mode. Supervised mode adds your per-file approval; auto defers your review to ship. Nothing is delivered until the whole branch has been reviewed and verified.

**Long feature, context filling up?** Compaction blurs everything that was only ever said in the conversation - decisions, plan deviations, what the half-finished edit was supposed to be.

```
/stepgate:compact
```

Stepgate writes that state into the plan first, tells you to run `/compact`, and hands you the one line that picks the flow back up afterwards. The plan file is the memory that survives the reset.

At every marked **seam** - where the plan moves between layers or areas - StepGate saves the current state and suggests compacting, even without a context warning. This includes auto: it pauses so you can compact or say continue, keeping your chosen mode. It reminds once per seam; a real context warning elsewhere prompts a checkpoint at the next safe boundary. StepGate never runs native compaction itself. After compaction, it restores the plan, chosen mode, and active restrictions.

**`/stepgate:init` sets up the config, once per project** - the working commands run it automatically if a project has no config yet, so you can just start with `/stepgate:plan`. Keep `.stepgate/config.md` private or share it with a team; optional `.stepgate/config.local.md` keeps personal differences local.

## Design principles

- **Human-in-the-loop.** Choose auto for agent review and local commits, or supervision for your approval at each file and commit. Both keep the human review at ship.
- **Small steps.** One plan step = one review pass = one commit. Small diffs are reviewable diffs.
- **Plan before execution.** The approach is locked with you before any code is written.
- **Push at the end, never mid-stream.** A branch goes out only after the whole-branch review and verification - and so does every follow-up after it.
- **Config over hard-coding.** Project specifics live in your repo's config, so the same commands fit any project.
- **Learns your conventions.** When you diverge from the flow, stepgate offers to remember it - updating a config field, or saving a free-form rule - so it fits your team a little better each time.

## Install

### Claude Code

In Claude Code:

```
/plugin marketplace add HummingbirdCommunity/stepgate
/plugin install stepgate@stepgate
```

That enables it for you everywhere (user scope). To turn it on only in the current repo, install at project scope from your terminal:

```
claude plugin install stepgate@stepgate --scope project
```

`--scope project` records it in the repo's `.claude/settings.json`, so anyone who clones the repo gets it. Then just run `/stepgate:plan` in any repo - if the project has no config yet, it sets one up first (via `/stepgate:init`), then plans. You can also run `/stepgate:init` yourself first.

### Codex

After the Codex support release is published, install from the same repository:

```bash
codex plugin marketplace add HummingbirdCommunity/stepgate
codex plugin add stepgate@stepgate
```

For local development, replace the GitHub source with the path to your StepGate checkout. Reload the IDE extension or start a fresh Codex chat after installation. Type `$` and select `stepgate:plan`, `stepgate:step`, `stepgate:ship`, `stepgate:init`, or `stepgate:compact`:

```text
$stepgate:plan #42
$stepgate:step
$stepgate:ship
```

Codex uses the same base configuration, optional local differences, and plan files as Claude. Review and trust the compaction reminder in Codex's `/hooks` menu before it runs. To compact, use `$stepgate:compact` to save state, then run `/compact` in Codex CLI; in an IDE without that command, open a fresh chat with the supplied resume line.

### Kimi Code

Use the current Kimi Code CLI (`@moonshot-ai/kimi-code`), not the archived Python `kimi-cli`. After the Kimi support release is published, run inside Kimi Code:

```text
/plugins install https://github.com/HummingbirdCommunity/stepgate/tree/main
/reload
```

Use `/stepgate:plan`, `/stepgate:step`, `/stepgate:ship`, `/stepgate:init`, and `/stepgate:compact`. Installation is user-wide. Kimi reads the same workflows, configuration, and plans. After `/stepgate:compact` saves state, run native `/compact`; the plugin's host instructions restore the active workflow after compaction.

For local development, export committed plugin files from the repository root:

```bash
stepgate_install_dir="$(mktemp -d)"
git archive HEAD .kimi-plugin plugins/stepgate | tar -x -C "$stepgate_install_dir"
printf '/plugins install %s\n' "$stepgate_install_dir"
```

Run the printed command inside Kimi, then `/reload`. Re-export and reinstall after local commits. If you have hand-copied `stepgate-*` skills, move them outside scanned skill directories after installation so they cannot keep running older workflows.

### Antigravity CLI

Install once from a terminal, including your IDE's integrated terminal. The workflow was verified with `agy` 1.5.11.

```bash
agy plugin install https://github.com/HummingbirdCommunity/stepgate
```

Start `agy` in your project and enter a command in chat, for example `/stepgate:plan add a readiness endpoint`. Use `/stepgate:step` for per-file review, `/stepgate:step auto` to explicitly choose auto, and `/stepgate:ship` for the final review and verification. `/stepgate:init` sets up a new project's configuration. Existing StepGate configuration and plans also work in AGY.

To compact, run `/stepgate:compact` to save the plan state. Run AGY's `/compact`, then paste the separate StepGate recovery command it supplied.

For local development, export committed plugin files from the StepGate checkout and install the export.

```bash
stepgate_install_dir="$(mktemp -d)"
git archive HEAD .antigravity-plugin skills plugins/stepgate | tar -x -C "$stepgate_install_dir"
agy plugin install "$stepgate_install_dir"
```

MCP servers and project-specific commands are configured in the host separately. Installing StepGate does not install tracker credentials or browser automation.

## Configuration

`/stepgate:init` detects project conventions and asks only for missing choices. The base file, **`.stepgate/config.md`**, may stay entirely private or be committed to share with a team. Sharing is optional.

Put personal differences in optional **`.stepgate/config.local.md`**, which is always ignored and excluded from commits. All hosts use the same files:

| File | Purpose | Git |
|---|---|---|
| `.stepgate/config.md` | Base conventions | Private or shared, your choice |
| `.stepgate/config.local.md` | Personal preferences and machine settings | Always local |

For example, keep common checks in the base:

```markdown
## Automated checks
- Tests: npm test

## Language
- Local language: auto
```

Then set a personal language and evidence destination locally:

```markdown
## Language
- Local language: Chinese (Simplified)

## Verifying locally
- Evidence: /path/to/local/screenshots
```

Local fields override matching base fields; omitted fields inherit. Free-form rules about different matters combine. Clear conflicts identify the winning local source. Precedence is defaults, base, local, then your explicit instruction. When offering to remember a rule, StepGate shows the proposed text and destination before writing.

For a shared base with private plans, the relevant ignore rules are:

```gitignore
/.stepgate/config.local.md
/.stepgate/plans/
```

Leave config.md trackable only if you choose to share it, adjusting an existing parent ignore rule if necessary. If everything under .stepgate/ stays private, an existing `/.stepgate/` rule still works. Choose whether to share the base and plans separately; if their sharing choices differ, ignore individual private paths instead of the whole directory. Ignoring a file that is already tracked does not untrack it.

Existing single-file configurations keep working; no automatic split is required. To split one, move only the personal fields you choose into local configuration, preserving their section headings. Both files may be symlinks; relative working paths still resolve from the repository root. For a shared base, a symlink must be relative and resolve to a target shared within the repository; init explains other links and proposes a portable base only with your agreement. A plan directory may be absolute or relative, written as a plain `- Plans directory: <path>` line. Changing that value does not move old plans.

The base file remains the initialization signal. With only local configuration present, init preserves those answers while creating the missing base. Both files are yours to edit, and plugin updates never rewrite them. See [the shared configuration rules](plugins/stepgate/references/configuration.md) for the full loading and update behavior.

## Updating

Stepgate uses semantic versioning. Updates are pull-based - never force-applied to your machine. From your terminal:

```
claude plugin marketplace update stepgate
claude plugin update stepgate@stepgate
```

Or, inside a session, open `/plugin` (`/plugins` in VS Code), find stepgate on the **Installed** tab and select **Update now**. Restart the session to pick the new version up.

For a Git-backed Codex installation, refresh the marketplace and install its current plugin version, then reload the extension or start a fresh chat:

```bash
codex plugin marketplace upgrade stepgate
codex plugin add stepgate@stepgate
```

With a local marketplace source, update that checkout first, then run only `codex plugin add stepgate@stepgate`. `marketplace upgrade` applies to Git sources.

In Kimi Code, rerun `/plugins install https://github.com/HummingbirdCommunity/stepgate/tree/main`, then `/reload`. Local installations are managed copies: re-export current committed files using the local-development recipe above and reinstall the printed path.

For Antigravity CLI, rerun `agy plugin install https://github.com/HummingbirdCommunity/stepgate` and start a fresh `agy` session. For a local install, re-export the current commit and reinstall the new directory. Use `agy plugin list` to check the installed version and enabled status.

All hosts consume `plugins/stepgate/commands/*.md` as the canonical workflow content. Maintainers run `python3 scripts/build-codex.py` to regenerate the Codex and AGY skills after changing command metadata. Before a release, run `python3 scripts/build-codex.py --check`, `python3 -m unittest discover -s tests -v`, and `agy plugin validate --strict <exported-plugin-directory>`.

See [CHANGELOG.md](CHANGELOG.md) for what changed between versions. Your base and local configuration files are untouched by updates.

## License

MIT
