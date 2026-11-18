# Antigravity CLI host conventions

Apply these conventions while running StepGate or following its plan.

- Resolve the workflow and convention links from the installed `SKILL.md`. Resolve the workflow's own relative links from its file in `commands/`. Read each linked file you need in full.
- `/stepgate:plan`, `/stepgate:step`, `/stepgate:ship`, `/stepgate:init`, and `/stepgate:compact` are namespaced plugin skills. `$ARGUMENTS` is the text accompanying the skill invocation. For workflow handoffs, read the corresponding installed command and run it inline. Slash commands belong in the chat input.
- Apply [Configuration loading and updates](configuration.md) to the repository being worked on. Read its `.stepgate/config.md` and optional `.stepgate/config.local.md`, and resolve project paths from that repository's root.
- Use `ask_question` when available or ask in chat at human gates, then wait for the developer. AGY's execution mode governs tool permissions. Require the developer's explicit authorization for StepGate `auto`, and apply any active restrictions on staging, committing, and delivery in either StepGate mode.
- Use the available MCP and local tools. Resolve project commands from available skills or their source. Report missing prerequisites before claiming that a check passed. For a UI mockup, preview the saved local HTML with an available browser or preview tool. Publish only with the developer's authorization.
- When preparing a compaction with `/stepgate:compact`, save state and ask the developer to run bare `/compact`. Use `/stepgate:compact Recover after compaction from <plan path>` as the separate recovery line.
- In recovery mode, read the applicable installed workflow, both project configuration layers, and the plan's `Resume here` block from disk, even if a conversation summary already includes them. Report the restored execution mode, active restrictions, and the next action. Apply the developer's current instructions first.
