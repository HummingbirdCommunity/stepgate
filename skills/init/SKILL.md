---
name: init
description: "StepGate init: One-time project setup - interview you about your conventions (task tracker, branches, review guideline, commit rules, migrations, automated checks) and write .stepgate/config.md. plan/step/ship run it automatically if there's no config yet; run it yourself anytime to (re)configure."
disable-model-invocation: true
---

# StepGate init

If the absolute path of this skill is unavailable, run `agy plugin list --json`. Use the `path` of the enabled `stepgate` entry as the installed plugin root. Resolve the links below from this skill folder under `skills/` in that root.

Read [Antigravity CLI host conventions](../../plugins/stepgate/references/agy.md), then [the canonical init workflow](../../plugins/stepgate/commands/init.md) in full. Run that workflow using the host conventions. Use the text after the slash command as its invocation arguments.
