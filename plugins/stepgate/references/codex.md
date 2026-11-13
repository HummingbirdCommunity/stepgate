# Codex host conventions

The files in `../commands/` are the canonical workflows for both hosts. Apply these invocation and tooling translations when running them in Codex:

- `/stepgate:plan`, `/stepgate:step`, `/stepgate:ship`, `/stepgate:init`, and `/stepgate:compact` mean the corresponding `$stepgate:<name>` skill. Read the sibling skill and command when one workflow hands off to another. Do not send a Claude slash command to a shell or expect Claude to be installed.
- `$ARGUMENTS` means the text following the skill mention in the user's message. It is not an environment variable or an automatically expanded placeholder.
- Apply [Configuration loading and updates](configuration.md) to the current repository's base and optional local configuration. Both hosts use the same loading, precedence, paths, and update rules. Plugin installation and updates never initialize or rewrite project configuration.
- Use Codex's available question tools, or ask in chat and wait for a reply, at the workflow's human gates. Preserve existing authorization: the user's explicit `auto` choice enables the documented auto mode; installing a plugin does not authorize staging, committing, pushing, or posting tracker updates.
- Use connected MCP tools and local commands for the project's tracker and verification setup. A config referring to `/sync-pr` or another project command means its matching Codex skill when available. Otherwise read the command's source in the current repository's `.claude/commands/` and run its workflow inline. Report missing credentials or tools instead of claiming a gate passed.
- Preview a mockup from its saved local HTML file with an available browser or preview tool. Claude live artifacts are not required. Publish externally only when the user requests publication or explicitly invokes the publishing flow.
- `$stepgate:compact` saves state and hands control to the developer. In Codex CLI the developer then runs `/compact`, without a Claude focus argument. In an IDE with no compaction command, save the state first and provide the resume line for a fresh chat. Do not clear or compact the session yourself.
- The bundled `SessionStart` hook matches `compact` in Codex as well as Claude. Codex requires hook review and trust before running it; never bypass that review. Its reminder applies only when this session was using StepGate.
