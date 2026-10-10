# Changelog

All notable changes to stepgate are documented here. This project follows [semantic versioning](https://semver.org/).

## 0.3.1

- The plugin's files moved into `plugins/stepgate/`, the layout Claude Code's own marketplace uses, so the repository's development notes are no longer read as part of the plugin. The commands are unchanged; update as usual.

## 0.3.0

- **How ship ends is a config field**: a pull request, a local merge, or the gate alone. A convention that already says so keeps working; `/stepgate:init pull requests` moves it into the field.
- `/stepgate:ship stage` runs only the whole-branch gate, for a ticket built in stages on one branch.
- **Changes after the PR is open**: `step` reviews them like any step, and running `ship` again refreshes the PR.
- `/stepgate:step` runs the tests covering the step before committing (new field: `Tests for given files`).
- `/stepgate:plan` draws a UI change as an HTML mockup before the approach locks; `step` checks each UI step against it.
- `/stepgate:ship` drives the verification and captures proof itself, handing you only what it cannot reach.
- The PR's Test plan is the cases actually verified, ticked as they passed, with a reason for any not run.

## 0.2.0

- `/stepgate:compact` - prepare for a context compaction: harvests what only the conversation knows (decisions, plan deviations, waived review findings, verification done, in-flight state) into the plan, adds a transient `## Resume here` block, then hands you the compaction step and the one line that resumes the flow. Run it after a compaction too, to re-anchor.
- `/stepgate:plan` now marks the **seams** in a plan - where the work crosses layers or surfaces. `/stepgate:step` tops the plan up at each seam so an unannounced compaction loses nothing, and suggests compacting only when the tool actually warns about context - at a step boundary, at most once per seam, never in auto mode.
- `/stepgate:ship` now drops the `## Resume here` block when it writes the closing summary, so the finished plan reads as a clean record.

Rules promoted into the commands from three projects that had been carrying them as local conventions:

- `/stepgate:init` asks how the project is stood up and verified locally - the run command, the ports and processes that are off limits, how a check gets past a login, where evidence goes, what teardown is needed - and records the paths that must never be staged, which step and ship now honour. Every one of those projects had written both by hand.
- `/stepgate:step` scopes an approval to the one commit it was given for; requires a change with a visible or side-effecting surface to be looked at rather than read; asks before a check deletes or overwrites stored data, designed behaviour or not; checks repo precedent before raising a "this is missing" finding; stays off formatting where a formatter is configured; and catches doc comments orphaned by an inserted or deleted function.
- `/stepgate:ship` reads that local verification setup and offers back whatever the run taught it; guards the checks it drives itself (kill only what you started and by pid, point write-path checks at fixtures you created, pair every negative assertion with a positive one); and makes captured proof readable on its own - a caption on every shot, the product rather than the development harness, a recording wherever a still cannot show how it got there.
- `/stepgate:plan` settles a schema's final shape before splitting the steps that touch it, so no step undoes another's.

## 0.1.0

Initial release. The supervised author loop - `plan -> step -> ship` - plus optional setup:

- `/stepgate:plan` - requirement to a locked approach and a small-step, file-by-file-reviewable plan.
- `/stepgate:step` - review and commit one step; human-in-the-loop, one step = one local commit. Or `/stepgate:step auto` to run all the steps hands-off on a small task, reviewing the whole branch at ship.
- `/stepgate:ship` - whole-branch review, end-to-end verification, single push and PR.
- `/stepgate:init` - optional one-time project setup; writes `.claude/stepgate.config.md` (or the commands ask on demand).

Config-driven and stack-agnostic: task tracker, branches, review guideline, commit conventions, migrations, automated checks, and PR rules all come from your repo's config, not hard-coded defaults.

Learns as you go: a free-form `## Conventions` section that commands follow and offer to extend whenever you diverge from the flow.
