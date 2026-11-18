---
name: ship
description: "StepGate ship: Finalize a feature whose steps are already reviewed & committed (via /stepgate:step) - whole-branch review (test gate + guideline review) to clean, end-to-end verification, then hands it over the way the project ends its work (a pull request, a local merge, or the gate alone) with a plain-language summary. Run it again after follow-up commits to refresh what went out. Human-in-the-loop."
disable-model-invocation: true
---

# StepGate ship

If the absolute path of this skill is unavailable, run `agy plugin list --json`. Use the `path` of the enabled `stepgate` entry as the installed plugin root. Resolve the links below from this skill folder under `skills/` in that root.

Read [Antigravity CLI host conventions](../../plugins/stepgate/references/agy.md), then [the canonical ship workflow](../../plugins/stepgate/commands/ship.md) in full. Run that workflow using the host conventions. Use the text after the slash command as its invocation arguments.
