---
description: Finalize a feature whose steps are already reviewed & committed (via /stepgate:step) - whole-branch review (test gate + guideline review) to clean, end-to-end verification, then a single push, PR, and a plain-language summary. Human-in-the-loop.
argument-hint: "[optional: ticket ref, target branch]"
---

# /stepgate:ship - finalize: whole-branch review, push, PR

You are finalizing a feature. The per-step file-by-file review and the small commits already happened via **`/stepgate:step`** (one step = one commit). `/stepgate:ship` does **not** redo that per-step review - it runs the holistic pass, then ships. Stay **human-in-the-loop**: gate on the developer at the review-fix, push, and PR steps.

**Load your project config.** Read `.stepgate/config.md`. It defines this project's review guideline, automated checks, base/target branch, commit & PR conventions, and migration setup; everything below that says "per your config" comes from it. **If the file doesn't exist, set it up first, then continue** - don't stop or make the developer run a separate command. Briefly say you'll set stepgate up for this project, run the `/stepgate:init` setup inline (it interviews them and writes the config), then pick this command back up. (On Claude Code you can invoke `/stepgate:init`; elsewhere run the same setup flow inline.)

**Language** (per your config's Language section; defaults: Local = match the user, Published = English): use your **Local language** for our conversation and review findings; use your **Published language** for commit messages, PR title/body, the plain-language summary, and code comments/strings (code identifiers stay English regardless).

**Conventions & learning.** Follow any rules in the config's `## Conventions` section (e.g. requesting particular reviewers, moving a ticket's status on PR open) - carry them out with the tracker/platform tools, and if you can't, tell the developer to do it manually. When the developer diverges from the flow on a **process/convention** matter (not the substance of a specific change) - a reviewer, a ticket-status step, a merge habit - offer to persist it: if it maps to an **existing config field**, offer to update that field; otherwise offer to add it under `## Conventions`. Always offer, never auto-write; the developer decides standing-rule vs one-off. These rules take priority over stepgate's built-in defaults; the developer's explicit instruction in the moment always wins.

## Phase 1 - Pre-check branch state

1. Resolve the target branch (from config, or an override in `$ARGUMENTS`). `git fetch` it, then compute the diff base with `git merge-base HEAD origin/<target>`.
2. **Branch staleness**: `git rev-list --left-right --count origin/<target>...HEAD`. If the branch is **behind**, the review and PR would reflect a stale base and conflicts would only surface at merge. Offer to **rebase onto** (or merge in) the latest target now; resolve conflicts with the developer before continuing. If they decline, note the PR may conflict at merge and proceed.
3. Confirm the work is on a **feature branch**, not a protected branch (per config - and, whether or not config lists any, always the base/target branch). If it's on one, branch it off the base branch (unless specified otherwise) before going further.
4. Confirm **everything is committed**: if there are uncommitted or not-yet-reviewed changes (excluding unrelated untracked files, the plan file, and anything under your config's never-stage paths), **stop and tell the developer to run `/stepgate:step` first** - don't silently review-and-commit them here.
5. Resolve the ticket reference (per config): from `$ARGUMENTS`, else the branch name, else ask (or note the skip marker if your config allows ticketless changes).

## Phase 2 - Whole-branch review (loop to clean)

1. Run the **automated checks** from config: the test command(s) and typecheck across the project, plus lint **on the branch's changed files vs base** (not the whole repo). Tests must pass before the branch counts as clean - a failing or missing-but-needed test is a must-fix. Skip any command not configured.
2. Run a **holistic review** of the whole branch diff (`git diff <base>...HEAD`) against your guideline (per config; if none, general best practices). Report only real issues in the changed code - not pre-existing issues in unchanged lines. For each: file:line, which rule it violates, and a brief fix. **Same review discipline as `/stepgate:step`**: grep for how existing peers do it before raising a "this is missing" finding, and raise no formatting findings on files a configured formatter covers.
3. If anything is found (failing tests or review findings): present them as fix suggestions (**must-fix** vs **optional**). For fixes the developer approves, handle each with the **same review-and-commit flow as `/stepgate:step`** - file-by-file (show diff -> review -> comment audit -> wait for confirm -> `git add`), commit per your conventions (its own commit, or amend the affected step), **and update the plan** so the affected step's entry reflects the fix. (On Claude Code you can invoke `/stepgate:step`; elsewhere run the same flow inline.) Then **re-run Phase 2**.
4. Repeat until tests pass and the review comes back clean.

## Phase 3 - Verify it works end-to-end

After the branch is clean and **before pushing**, confirm the feature actually works - not just that checks pass. **Read your config's `## Verifying locally` section first, if it has one**: it holds this project's run command, the ports and processes that are off limits, how a check gets past a login, where evidence goes, and what teardown is needed. Scale this to the change:

- **Changes with a runtime / UX / integration surface** (UI, an endpoint, a job, external services - anything automated tests can't fully observe): write a short test plan and exercise it. Derive cases from the diff and the plan - especially the corner cases surfaced during planning - covering happy path(s), edge/boundary cases, error & failure handling, and regression-prone adjacent areas. Write each as **scenario -> steps -> expected result**. Ask whether the developer runs them or you **drive the app/flow** (use whatever run/verify tooling the setup has; if none is available - no Playwright/run tooling - the developer runs the cases manually; never skip verification silently). Record pass/fail; on any failure, fix and loop back to Phase 2.
- **Pure-logic changes already well covered by automated tests**: say so - the suite may be enough. Do a quick sanity check rather than a full manual plan.
- **If the branch includes DB migrations** (per config): add a case for applying them on a clean DB in commit order, and a post-deploy item to watch the migration apply after the push.

**When you drive it yourself:**

- **Start your own instance, and kill only what you started, by pid.** Never match processes by pattern - `pkill -f` also matches the shell running it - and never start on, kill, or restart anything the config hands off to the developer.
- **Point write-path checks at fixtures you created**, not at a corner of real data. A check that a request *should be refused* is destructive exactly when it finds the bug: the write that should have been blocked goes through.
- **Put a positive assertion beside every negative one.** "The control is absent" and "the page never rendered" look identical from the outside.

Record whatever cases you produce, and their pass/fail results, in the plan document (if one exists), and reuse them for the PR Test plan (Phase 4) and any capture step (Phase 5). **Then offer to write back what the setup taught you** - a port collision, a session that expires mid-run, a step needed before the app serves the change - into the config's `## Verifying locally`, so the next branch doesn't rediscover it - starting with any field still marked `unknown yet`. Propose the lines; never write them without the developer's OK.

## Phase 4 - Push & PR (only now, once)

Only after tests pass, the whole-branch review is clean, and the end-to-end verification passes - nothing has been pushed before this point.

**Pre-flight the tooling**: confirm the platform CLI is installed and authenticated (e.g. `gh auth status` for GitHub, `glab auth status` for GitLab). If it's missing or logged out, tell the developer how to fix it and stop before pushing.

1. Suggest pushing - a single push of the finished branch (`git push -u origin <branch>`).
2. **Create or refresh the PR** with the platform CLI (e.g. `gh`), targeting the configured target branch:
   - **Title**: follow your commit conventions (style, scope, ticket reference). **If a ticket is available, put its reference in the title**; if your config requires a ticket and there genuinely is none, use the skip marker.
   - **Body**: if your config points to a **PR template / guide**, read it and make the body satisfy its required sections and checklist - fill each from the final diff, and drop the Phase 3 test plan into its testing/verification section (append a Test plan only if it has none). If there's **no template**, fall back to stepgate's default: a **Summary** (3-6 bullets: what changed, why, how) and a **Test plan** (checkbox list from Phase 3). Either way, derive content from the **overall final diff** (`<base>...HEAD`), not by concatenating per-commit messages. If your config defines regenerated body markers, keep the regenerated section between them; if it wants a ticket-link line, add it at the top.
3. **Match the merge strategy from config.** If it **squashes**, the per-step commits collapse into one - **draft a single squash commit message** (title per conventions + a body summarizing the whole feature from the final diff) and hand it over to paste at merge time. If it uses **merge commits or rebase**, the per-step commits land as-is and are the record - no squash message; just confirm those commit messages read cleanly as the branch's history.

If a later pass reopens the loop, fix locally, re-run Phase 2, and hold the push/PR until it's clean again.

## Phase 5 - Plain-language summary & proof (no code)

Write a short **plain-language summary** of what shipped - the PR's own Summary is often too technical for a PM, PO, or other non-engineer, so produce one anyone can read. Don't ask first; just write it. Base it on the full change set (commits + the plan) so every shipped item and corner case is covered:
- Plain language, bullet points, lead with user/product impact - not implementation.
- No code, no file paths, no jargon.
- Cover everything shipped, including edge cases handled.

Save this summary to the plan document (if one exists), alongside the approach, steps, and test cases - so the plan is a complete record of the work. **Drop any transient `## Resume here` block** left there by `/stepgate:compact`: the work is done, so a stale resume pointer is noise in the final record.

**If the change has a visual surface** (UI, or output a reader can see), also propose **how to capture proof**: from the Phase 3 cases, the few screens to screenshot and flows to screen-record that best show the impact, with where to trigger each. **Record a flow rather than shoot a screen whenever what you are showing is a transition or a state over time** - a still proves the end state but not that it got there on its own. Ask whether the developer wants you to capture them (drive the app) or do it themselves. Skip this when there's nothing visual to show.

Whatever gets captured has to read on its own, and lands where your config's `## Verifying locally` says evidence goes:

- **Caption every shot and clip** with what it shows and what to look at in it. The reader is not the author and has none of the context; a bare image says nothing about what differs between two of them.
- **Show the product, not the harness.** Hide what only the development setup adds - dev badges, preview chrome, test controls - and let captions name production addresses rather than `localhost`; where the page prints its own host, make the frame agree with the caption.
- **Start a recording at the real entry point** the user would come through, and never film a screen they could not reach that way.
- **Pair each capture with the Phase 3 case it proves.** The image is for the reader; the recorded assertion is the measurement. A screenshot is not a check.

---

Throughout: be concise and opinionated, and gate on the developer's input at the review-fix, push, and PR steps. **When a needed tool or MCP is missing, never silently skip** - say what to enable and propose the best fallback: for a gate step (tests, PR, commit) stop rather than fake completion; for auxiliary closeout (reviewer, ticket status) note it and continue. Propose the fallback and let the developer confirm; don't act unilaterally.
