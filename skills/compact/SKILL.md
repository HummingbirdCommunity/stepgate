---
name: compact
description: "StepGate compact: Prepare for a context compaction - capture what only this conversation knows into the plan (decisions, deviations, in-flight state), then hand you the compaction step and the line that resumes the flow. Run it after a compaction too, to re-anchor."
disable-model-invocation: true
---

# StepGate compact

If the absolute path of this skill is unavailable, run `agy plugin list --json`. Use the `path` of the enabled `stepgate` entry as the installed plugin root. Resolve the links below from this skill folder under `skills/` in that root.

Read [Antigravity CLI host conventions](../../plugins/stepgate/references/agy.md), then [the canonical compact workflow](../../plugins/stepgate/commands/compact.md) in full. Run that workflow using the host conventions. Use the text after the slash command as its invocation arguments.
