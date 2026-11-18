---
name: step
description: "StepGate step: Review and commit ONE just-implemented step - file-by-file, human-in-the-loop, one step = one local commit. Run after each step; finish the feature with /stepgate:ship."
disable-model-invocation: true
---

# StepGate step

If the absolute path of this skill is unavailable, run `agy plugin list --json`. Use the `path` of the enabled `stepgate` entry as the installed plugin root. Resolve the links below from this skill folder under `skills/` in that root.

Read [Antigravity CLI host conventions](../../plugins/stepgate/references/agy.md), then [the canonical step workflow](../../plugins/stepgate/commands/step.md) in full. Run that workflow using the host conventions. Use the text after the slash command as its invocation arguments.
