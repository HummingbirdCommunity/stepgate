# Kimi Code host conventions

Apply these rules only while running StepGate or following its plan.

- Find the enabled `stepgate` record in `<KIMI_CODE_HOME>/plugins/installed.json` (default `~/.kimi-code`). Its `root` is the installed plugin root. Canonical workflows are in `<root>/plugins/stepgate/commands/`; resolve their relative references there, not in the user's project.
- `/stepgate:plan`, `step`, `ship`, `init`, and `compact` are native plugin commands. Kimi expands `$ARGUMENTS`. For workflow handoffs, read the corresponding installed command and run it inline; never send slash commands to a shell.
- Read `<root>/plugins/stepgate/references/configuration.md` and apply it to the current project's base and optional local configuration. Installation does not initialize or rewrite project configuration.
- Use available question tools or chat at human gates, and wait for answers. Preserve the developer's explicit execution mode and current restrictions; installation grants no commit or delivery authorization.
- Use available MCP/local tools. Resolve project commands from available skills or their source; report missing tools or credentials before claiming a gate passed.
- After compaction or lost context, re-read the active installed workflow, both project configuration layers, and the plan's resume block before acting. Restore its execution mode and restrictions; ignore this recovery rule outside StepGate work.
- `/stepgate:compact` saves state and supplies the resume line; the developer then runs native `/compact`. Do not compact or clear the session yourself. Do not rely on `PostCompact` stdout to inject recovery instructions.
