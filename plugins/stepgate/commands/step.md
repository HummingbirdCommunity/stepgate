---
description: Review and commit ONE just-implemented step - file-by-file, human-in-the-loop, one step = one local commit. Run after each step; finish the feature with /stepgate:ship.
argument-hint: "[optional: 'auto' to run all remaining steps hands-off, or a step number/name/note]"
---

# /stepgate:step - review & commit one step

You are reviewing the **single step the developer just implemented** and committing it. **Human-in-the-loop**: the developer reviews every file themselves; **never auto-stage or auto-commit a file they have not personally looked at** - unless they choose auto mode (below).

**Auto mode.** If the developer invokes this with `auto` (`/stepgate:step auto`) or asks to run the rest automatically, they trust the plan and are deferring review to ship. Switch to autopilot: for **each remaining plan step**, implement it, run the checks and the guideline review, and commit it - **without pausing for their per-file review** - then update the plan and continue to the next. Hand off to **`/stepgate:ship`** when all steps are done (ship's whole-branch review is the human gate for auto mode). Auto means *unattended, not unchecked*: keep running every check and review, and **if a step turns out materially higher-risk than assessed, stop and explain the risk to the developer** before proceeding; size alone is not a reason to stop auto. They can switch back to supervised at any time.

**Load your project config.** Read and apply [Configuration loading and updates](../references/configuration.md), resolving that reference from this command file in the installed plugin. Everything below that says "per your config" uses the effective settings from `.stepgate/config.md` and optional `.stepgate/config.local.md`. **If the base file is missing, set it up first, then continue**: preserve and reuse local settings, run the `/stepgate:init` setup inline, reload the configuration, and pick this command back up. (On Claude Code you can invoke `/stepgate:init`; elsewhere run the same setup flow inline.)

**Language** (per your config's Language section; defaults: Local = match the user, Published = English): use your **Local language** for review findings, recommendations, and prompts; use your **Published language** for commit messages and code comments/strings (code identifiers stay English regardless).

**Conventions & learning.** Follow the effective `## Conventions` rules from both layers. When the developer diverges on a **process/convention** matter - a commit-scope rule, a waived review finding, a staging habit - or explicitly says "remember this", offer to persist it using the configuration reference's field and layer selection. Propose the text and destination; never auto-write.

## Phase 1 - Scope this step

1. The changes to review are the **currently uncommitted** working-tree changes (`git status` and `git diff`, staged + unstaged). **Do not** pull in already-committed work - earlier steps are done. If the uncommitted changes clearly span more than one plan step, say so and offer to review and commit them as **separate steps**.
2. Handle untracked files explicitly, but **don't dump the developer's whole untracked set**. When a plan exists, match untracked files against this step's expected file list; otherwise narrow to plausibly-relevant ones (recently created, in source dirs, matching the step). Ask only about those; never stage a file they didn't claim. **Always exclude `.stepgate/config.local.md` from staging; if already tracked, report it without changing the index.** **Never ask about anything under your config's never-stage paths** - that scratch lives in the tree on purpose - or about the plan file when your config keeps plans local.
3. If a plan exists in your plans directory, read this step's entry (`$ARGUMENTS` may name the step) for its intent, expected files, how-to-verify, and commit stub. Flag if the actual changes diverge from the planned step.

   **Execution mode.** After reading configuration and the plan, use the developer's current explicit choice, otherwise a choice explicitly recorded for this task. If neither exists, recommend auto unless there are material risks; explain high risks and recommend supervision. A recommendation, plan approval, or silence does not select a mode. Record an explicit choice in the plan as `Execution mode: <auto|supervised> (explicitly chosen by the developer)`, and update it when they switch. Do not repeatedly ask about a recorded choice. Current restrictions on staging, committing, or delivery still apply.

4. **Pre-flight** using the automated checks from config (skip any not set):
   - **Format** this step's changed files, so what you review is exactly what will be committed.
   - Run **lint** on those files, and **typecheck** (project-wide - types cross files). Only act on errors involving this step's files; unrelated pre-existing errors in the repo are out of scope (they would drown the signal).
   - Run the **tests that cover this step**: the tests for the changed files (beside them, or wherever this project keeps its tests) and any test this step added or changed, with the config's `Tests for given files` command. With no such field, work out how the test runner takes files and offer to record it; fall back to the full test command only when it cannot narrow. A failing test is fixed in this step, not left for ship.
   - Fix mechanical errors before the human review, so the developer reviews logic, not compile errors.
5. **A follow-up on a branch that already went out** (it has an open pull request): review it the same way, and record it in the plan - in the entry of the step it changes, or under a follow-ups list. It lands either folded into the step commit that introduced the code or as a commit of its own; follow your config's convention, and ask when it has none. Folding rewrites pushed history, which `/stepgate:ship` force-pushes only with the developer's OK.

## Phase 2 - File-by-file review

For each changed file in this step (sensible order; usually just 1-2 files), one at a time:

1. Read the file's diff yourself (just that file), and point the developer at it - they read it in their own tool (the editor's diff view, or `git diff -- <file>`). **Do not paste the diff into your reply** unless they ask: it is paid for as output and again on every later turn, and they already have it. In auto mode nobody reads it - review it and move on.
2. **Review against your guideline** (per config; if none, general best practices): correctness bugs, missing error handling, and violations of the project's documented conventions (typing, unawaited side-effects, layering rules, user-facing wording rules, etc.). **Before raising a "this is missing" finding, grep for how existing peers do it** - most such findings die on precedent. **A UI step with a mockup in the plan is checked against its part of the mockup** - layout, copy, controls and states; where the build has to differ from what was drawn, stop and ask rather than improvise. **When your config sets a Format command, raise no formatting findings on the files it covers** (indent, quote style, import order): Phase 1 already ran the formatter, so what is left is what it wants. Without one configured, they are fair game.
3. **Comment audit.** Flag every low-value comment: "what" comments that naming already covers, locator comments ("used by X", "added for Y", and **any reference to the plan file, a step number, or an acceptance-criteria id** - those point at local scratch nobody else has), and stale/obvious ones. A comment earns its place only when the WHY is genuinely non-obvious (a hidden invariant, a workaround for a specific bug). Propose deleting the rest. **Where doc comments sit above the definition, check that this step did not orphan one**: an inserted function silently inherits the comment written for the one it pushed down, and a deleted function leaves its comment behind on whatever follows. Read the comment above each insertion point and above each removed function, and ask whether it belongs with what moved; the fix is to move it, not to delete it. (If your guideline sets a different comment policy, follow it.)
4. Present findings as **must-fix** vs **nice-to-have** vs **looks good**. If clean, say so plainly.
5. **Pause for the developer.** They read the diff themselves. Apply any fix they want and say what changed (the changed lines, not the whole file again); do not move on until they confirm they're done with this file. (**Auto mode**: skip this pause - self-review against the guideline and move on.)
6. On their confirm, **`git add <that file>`** - staging is the signal "I've reviewed this." Next file.

## Phase 3 - Commit the step

**If a plan exists**, use its stub and verify step. If there's no plan (ad-hoc use), degrade gracefully: derive the commit message from the diff, ask the developer how to verify, and skip the plan update below.

Before committing, **run or walk through this step's how-to-verify** (the quick check that it works); if it fails, fix and re-review the touched files before proceeding. **A change with a visible or side-effecting surface is not verified by reading it** - format, lint, typecheck and a green suite can all pass while it is plainly broken on screen - so a step of that kind ends with you looking at the real thing - the developer only for what you cannot reach (your config's `## Verifying locally` says how to stand it up, if it has one). **If verifying it would delete or overwrite stored data, ask first**: that the deletion is the committed code's designed behaviour is not a reason to skip the ask, because running it by hand on a developer's machine is not the context it was designed for. Read-only queries and transactions that roll back need none.

**If this step adds or edits a DB migration** (and your config says migrations apply): apply it with the configured apply command and confirm it applies cleanly. Confirm it's idempotent and correctly ordered per your migration rules. A migration that only works on a fresh DB, or errors on re-apply, is a must-fix before commit.

If the current branch is a **protected branch** (per config - and, whether or not config lists any, always the repo's base/default branch), **stop and move the work to a feature branch first** (off the base branch, unless the developer specifies otherwise) - never commit straight to a protected/deploy branch.

Once it passes and all of this step's files are reviewed and staged, **suggest committing - one step, one commit** - using the plan's stub and your commit conventions (follow the commit-message guide from config if one is set, else the default style; **include the ticket reference whenever a ticket is available** - the config's "ticket required" setting only decides whether a ticket is mandatory, not whether to include one you have). **Write the commit the way this project actually writes them: follow the body style from your config's Commit conventions (whether commits carry a body, its structure, ticket-link placement). If the config doesn't capture that, skim recent commit messages (`git log -20`, full bodies) and mirror them. Don't hand back a bare subject if this project's commits have bodies.** Never add a Co-Authored-By trailer. Let the developer edit; commit only on their OK (**auto mode**: commit directly, no OK needed). **Local only - do not push.**

**That OK covers this commit and no other.** Implementing the next step ends at "the changes are ready" - stop there and wait, however small or mechanical the change is.

**Keep the plan live.** After committing, update the plan file to match reality: mark this step done, and reconcile its entry (files, what/why) with what was actually implemented. If steps were merged, split, reordered, added, or dropped, update the rest too - so later `/stepgate:step` passes and `/stepgate:ship`'s summary always read an accurate plan.

Then **recommend the next action based on actual state** (name the specific command, don't list both): check the plan and `git status`.
- If undone steps remain: say **which step is next** and to run `/stepgate:step` again after building it.
- If all steps are done, committed, and the tree is clean: recommend **`/stepgate:ship`** - or **`/stepgate:ship stage`** when the plan or the developer says more stages of this ticket are to come.
- If the branch already went out (an open pull request): once the follow-ups are committed, recommend **`/stepgate:ship`** to refresh it - the PR, its Test plan and the summary are now behind the branch.
- If there's no plan: say to run `/stepgate:step` again after the next change, or `/stepgate:ship` when the feature is complete.

**Compacting at seams, including auto.** After a step ends at a marked plan seam, first checkpoint decisions, explicit execution mode, active restrictions, verification, and the next action in the plan. Briefly recommend `/stepgate:compact` even without a context warning, then pause before the next step so the developer can compact or say continue. Preserve their execution mode. Record the reminder outcome; do not repeat it at the same seam after they decline or continue. If a real context warning occurs elsewhere, checkpoint at the next safe boundary rather than waiting for a seam. Never invoke native compaction yourself.

---

Gate on the developer's input at every file and at the commit. Keep it tight - this runs once per step.
