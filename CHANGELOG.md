# Changelog

All notable changes to stepgate are documented here. This project follows [semantic versioning](https://semver.org/).

## 0.1.0

Initial release. The supervised author loop - `plan -> step -> ship` - plus optional setup:

- `/stepgate:plan` - requirement to a locked approach and a small-step, file-by-file-reviewable plan.
- `/stepgate:step` - review and commit one step; human-in-the-loop, one step = one local commit. Or `/stepgate:step auto` to run all the steps hands-off on a small task, reviewing the whole branch at ship.
- `/stepgate:ship` - whole-branch review, end-to-end verification, single push and PR.
- `/stepgate:init` - optional one-time project setup; writes `.claude/stepgate.config.md` (or the commands ask on demand).

Config-driven and stack-agnostic: task tracker, branches, review guideline, commit conventions, migrations, automated checks, and PR rules all come from your repo's config, not hard-coded defaults.

Learns as you go: a free-form `## Conventions` section that commands follow and offer to extend whenever you diverge from the flow.
