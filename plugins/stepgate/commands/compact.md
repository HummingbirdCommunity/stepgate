---
description: Prepare for a context compaction - capture what only this conversation knows into the plan (decisions, deviations, in-flight state), then hand you the compaction step and the line that resumes the flow. Run it after a compaction too, to re-anchor.
argument-hint: "[optional: a plan/step reference, or anything you specifically want preserved]"
---

# /stepgate:compact - save the thread state before the context is compacted

Move this session's live state out of the conversation and into the plan file, then hand the developer the compaction step and the line that picks the flow back up. **You never compact anything yourself** - compaction is the developer's action in their tool.

**This command runs because context is tight, and everything below is subordinate to that**: read the plan, read the repo state, write the delta, hand off. Don't re-investigate the codebase, don't re-review code, don't run the project's checks, don't re-read files you already know. If a step here would cost more context than it saves, say so and skip it.

**Recovery mode.** If the compaction **already happened** - the developer ran it, or their tool auto-compacted, and they're invoking this to get their bearings back - **skip Phases 2 and 3**: read the plan and the repo state, restate in a few lines where the flow stands, and give the resume line from Phase 4. There is nothing left to harvest; the thread is already gone.

**Load your project config.** Read `.stepgate/config.md` for the plans directory, base branch, and conventions. Skip the read when you still hold it from earlier in the session and it has not been edited since. **If it doesn't exist, do not run the init interview here** - it would burn the context this command exists to protect. Degrade instead: use the repo's default branch as the base, look for an obvious plans/notes directory (or ask the developer, in one question, where the note should go), save the state, and mention that `/stepgate:init` is worth running after the compaction.

**Language** (per your config's Language section; defaults: Local = match the user, Published = English): the plan file and our conversation in your **Local language**; any commit message in your **Published language**.

**Conventions & learning.** Follow any rules in the config's `## Conventions` section. If the developer states a standing **process/convention** rule here (what they always want preserved, a note format), offer to persist it - to an existing config field if one maps, otherwise under `## Conventions`. Always offer, never auto-write.

## Phase 1 - Locate the flow

1. Read the plan for this work from the plans directory (per config). **`$ARGUMENTS`**: a plan or step reference selects what to read; anything else is content the developer wants preserved (Phase 2). If there is no plan, see **No plan** below.
2. **Establish state from the repo, not from memory** - it is the part that survives: current branch, `git status`, and `git log --oneline <base>..HEAD`. Read a commit body only if you actually need one, and skim the uncommitted changes with `--stat` rather than in full.
3. Work out where the flow stands: which plan steps are committed, which step is in flight, and the immediate next action.

## Phase 2 - Harvest what only the conversation knows

The test for every candidate: **if it is already in the repo, it does not need saving.** Committed code, commit messages, the plan as written, and the config all survive the compaction - do not copy them. Save only what lives nowhere but this thread:

- **Decisions and reversals** - approach changes agreed mid-implementation, options considered and rejected, and *why* - so they are not re-litigated after the reset.
- **Discoveries about the codebase** - constraints found the hard way, a dependency that behaves unexpectedly, an area that turned out to be already implemented.
- **Plan deviations** - steps merged, split, reordered, added, or dropped; files that differ from what the step listed.
- **Review findings the developer waived** - what they chose not to fix and why, or you will raise it again at ship.
- **Open questions** - blocking ones still out with a product owner, and answers already received.
- **Verification done** - test cases run and their outcomes, manual checks performed; `/stepgate:ship` needs these.
- **In-flight state** - what the uncommitted work is meant to be, what is done, what is left, and the next concrete edit.
- **Anything the developer named in `$ARGUMENTS`**.

**Skip every empty category** - no heading per bullet, and never pad the plan to look thorough; padding is exactly the context you are trying to save. **If nothing qualifies** - the plan is already current, which is the normal case right after a step commit or a recent compaction - say so in one line and go straight to Phase 4.

## Phase 3 - Write it down, first

Securing the state is the cheapest thing you can do here, so do it before anything that might exhaust the budget. **Write the plan file directly - do not print the notes for approval first**: that spends the same content twice, and a local plan file is uncommitted and editable, so a wrong line costs nothing to fix.

- Reconcile step statuses with what the repo actually shows (done / in flight / not started).
- **Fold each item into where it belongs** - the step entry it concerns, the approach summary, the open questions, the test cases. The plan stays a living document, not a session transcript; never paste conversation into it.
- Add a **`## Resume here`** block directly under the approach summary: current branch, the commit it is being written at, the step in flight and its state, and the next concrete action (the commit lets recovery see what has been committed since). It is **transient** - overwrite it on every later run of this command (there is only ever one), and `/stepgate:ship` drops it when the plan becomes the final record.

Then report back a **terse bullet list of what you recorded** - the headings, not the prose - plus the file path, and invite corrections.

**No plan** (ad-hoc use): write the same content as a short state file in the plans directory, named after the branch or a slug - what is being built, what is committed, what is in flight, the decisions, the next action. That file becomes the resume anchor. If the developer would rather not have a file, give the notes in the chat and tell them to carry the state in the compaction instruction themselves.

## Phase 4 - Hand over

1. Confirm what was saved and **where**.
2. **The in-flight work.** If it is a complete step, **default to leaving it for after the compaction**: the file-by-file review and the pre-flight checks are exactly what will not fit, and they work just as well afterwards, because the diff lives in the working tree rather than in the conversation. Recommend committing it first - `/stepgate:step`, since a commit is better memory than a note - **only when the developer says there is room**, or when they came here with no warning having fired. If it is half a step, leave it, and make sure Phase 3 described it well enough to resume mid-file. (On Claude Code you can invoke `/stepgate:step`; elsewhere run the same flow inline.)
3. Tell the developer to **run their tool's context-compaction command now** - on Claude Code that is `/compact`, which takes a focus instruction. Hand them one, copy-pasteable and specific to this session:
   `/compact keep the current step's approach and the remaining plan steps; full state is in <plan path>`
4. Give the **resume line for after the compaction** - name one, from actual state:
   - A step is built and waiting to be reviewed: **`/stepgate:step`**.
   - All steps are done and committed: **`/stepgate:ship`** (**`/stepgate:ship stage`** when more stages of the ticket are to come).
   - A step is half-implemented: a copy-pasteable prose line, e.g. `Read <plan path>, then continue step <n> (<title>) from the "Resume here" block.`
   - The steps aren't settled yet: **`/stepgate:plan`** to finish planning.
5. **End the turn here. Do not start the next step** - every further tool call spends exactly what this command just saved.

---

Save what would be lost, skip what would not, and end with the developer holding two lines: the compaction command, and the one that restarts the flow.
