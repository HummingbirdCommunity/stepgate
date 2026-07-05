# Stepgate

**A supervised, human-in-the-loop feature-authoring pipeline for [Claude Code](https://claude.com/claude-code).**

Break a change into small steps, review every file yourself before it is committed, and keep planning separate from execution. Nothing gets staged, committed, or pushed without you looking at it first.

## Why stepgate

I built stepgate after noticing a pattern: the more the agent did on its own, the less I could stand behind what shipped.

Hand an agent a whole feature and it hands one back in a single shot. The code might even be good - but now you have to review a result you never watched get built. You read file after file, reconstructing intent from the diff, and some of what you planned quietly never made it in. You sign off not because you are sure, but because you are tired. You can't really vouch for code you only met after it was done.

Stepgate flips the order. You are there for every step: the agent plans with you, then builds one small, reviewable piece at a time, and nothing is committed until you have read it and said yes. When it is done, there is nothing to discover - you already know it is right, because you watched it become right. You also come away understanding the code, not just owning it, which makes it a good way to work when you are new to the codebase, or still learning to code.

Staying in the loop costs more up front, but it is faster overall: the expensive part of AI was never the typing, it is the bug that surfaces three days later and eats an afternoon. Catch it as it is written and it costs minutes. Every commit is one you can stand behind.

## The loop

Three commands, run in a cycle - `plan` once, `step` after each piece you build, `ship` once.

**1. Plan.** Give it a ticket, a description, or both. Stepgate reads the ticket if you gave one, researches the code, settles the approach with you, then writes a small-step plan. Nothing is coded yet.

```
/stepgate:plan #42                               # a ticket
/stepgate:plan add rate limiting to login        # or just describe it
/stepgate:plan #42 also cover the signup route   # or a follow-up on shipped work
```

On a follow-up, stepgate checks the ticket against the current code, plans only what is left, and tells you if it is already done.

**2. Step.** You build one step; stepgate walks its files with you, one at a time, and commits it once you are satisfied. Run it after every step.

```
/stepgate:step
```

Confident in the plan, or it's a small change? `/stepgate:step auto` runs the remaining steps hands-off - stepgate builds, self-reviews, and commits each, and you review them together at ship. (For a small task, `plan` suggests this itself.)

**3. Ship.** When every step is done: a whole-branch review, end-to-end verification, then a single push and PR.

```
/stepgate:ship
```

You review every file before it is committed, and nothing is pushed until the very end.

**`/stepgate:init` sets up the config, once per project** - the working commands run it automatically if a project has no config yet, so you can just start with `/stepgate:plan`. For a team, one person runs it and commits `.stepgate/config.md`, so everyone shares the same setup.

## Design principles

- **Human-in-the-loop.** Staging a file is the signal "I reviewed this" - the agent never commits a file you haven't seen. (Hand it a small task on autopilot and it commits without pausing - but even then, nothing ships until you review the whole branch.)
- **Small steps.** One plan step = one review pass = one commit. Small diffs are reviewable diffs.
- **Plan before execution.** The approach is locked with you before any code is written.
- **Push once, at the end.** No half-finished branches pushed mid-stream.
- **Config over hard-coding.** Project specifics live in your repo's config, so the same commands fit any project.
- **Learns your conventions.** When you diverge from the flow, stepgate offers to remember it - updating a config field, or saving a free-form rule - so it fits your team a little better each time.

## Install

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

## Configuration

Stepgate adapts to your project rather than imposing its own conventions. `/stepgate:init` works out your tracker, branches, review guideline, commit style, checks, and PR rules - detecting what it can from the repo and asking you the rest - and saves them to **`.stepgate/config.md`** in your repo.

You don't fill it out as a form: init interviews you and pre-fills what it detects. The working commands read this file, and run init automatically if a project doesn't have one yet.

The file is yours - plain markdown you can read and edit:

- **Commit it** to share one setup with your whole team.
- **Edit it by hand** anytime - no plugin changes needed.
- **Plugin updates never touch it.**

## Updating

Stepgate uses semantic versioning. Updates are pull-based - never force-applied to your machine.

```
/plugin update stepgate
```

See [CHANGELOG.md](CHANGELOG.md) for what changed between versions. Your `.stepgate/config.md` is untouched by updates.

## License

MIT
