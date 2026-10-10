---
description: Take a requirement (a ticket and/or a description) to a locked approach and a small-step implementation plan sized for file-by-file review. Surfaces the open decisions (and forwardable questions if you need a product owner's sign-off); does not start coding until you say the approach is settled.
argument-hint: "[ticket ref and/or a description of the work]"
---

# /stepgate:plan - requirement to a reviewable plan

You are taking the developer from a raw requirement to a settled approach and a concrete, small-step implementation plan. Size each step so it maps to **one `/stepgate:step` pass and one commit** (roughly 1-2 files).

This is **interactive**: the developer stays in the discussion until *they* say the approach is locked. Do not jump to writing the plan early.

**Load your project config.** Read `.stepgate/config.md`. It defines this project's task tracker, base branch, review guideline, commit rules, migration setup, and where plans are stored; everything below that says "per your config" comes from it. **If the file doesn't exist, set it up first, then continue** - don't stop or make the developer run a separate command. Briefly say you'll set stepgate up for this project, run the `/stepgate:init` setup inline (it interviews them and writes the config), then pick this command back up. (On Claude Code you can invoke `/stepgate:init`; elsewhere run the same setup flow inline.)

**Language** (per your config's Language section; defaults: Local = match the user, Published = English): use your **Local language** for our conversation, analysis, recommendations, and the plan file; use your **Published language** for anything that lands in the repo or goes to people - per-step commit stubs and any reviewer / product-owner-facing text (the forwardable questions in Phase 3).

**Conventions & learning.** Follow any rules in the config's `## Conventions` section. When the developer diverges from the flow on a **process/convention** matter (not the substance of a specific change) - a different base branch, a naming rule, a code-area to avoid - offer to persist it: if it maps to an **existing config field**, offer to update that field; otherwise offer to add it under `## Conventions`. Also honor an explicit "remember this". Always offer, never auto-write; the developer decides standing-rule vs one-off. These rules take priority over stepgate's built-in defaults; the developer's explicit instruction in the moment always wins.

## Phase 1 - Get the requirement

The input is in `$ARGUMENTS`: a ticket reference, a free-text description, or both.

- **If a ticket reference is present** and your config defines a tracker, fetch the ticket using the "How to fetch a ticket" method from config (e.g. `gh issue view <n>`, a tracker MCP, or ask the developer to paste it). **If that method needs a tool that isn't available** (an MCP not connected, `gh` not installed), say what to enable and offer manual paste - don't skip. Echo back a tight summary (title, body, acceptance criteria). If the ticket is thin or ambiguous, say so - that feeds Phase 3.
- **If it reads as a follow-up or feedback** on already-shipped work (not a fresh full scope), treat the **args as the real requirement** and any linked ticket as background; plan only the **delta**.
- **If there's no ticket at all**, work straight from the description. If your config requires a ticket, note that one will be needed before shipping and offer to help open one.

## Phase 2 - Requirement & feasibility analysis

1. **Understand the real ask** in product terms: who it's for, what changes for them, what "done" looks like.
2. **Ground it in the codebase.** Investigate the actual files, data flow, and constraints (use broad search in parallel - spawn subagents if your tool supports them). Identify: where it plugs in and which existing patterns to reuse (follow any file-placement rules in your review guideline); what it touches (DB/migrations, APIs, UI, jobs, external providers); **risks & unknowns** (data migration/backfill, auth, multi-path rules, fire-and-forget pitfalls); rough effort; and any cheaper alternative worth weighing.
   - **Check what is already there.** Compare the ticket or requirement against the current code. If it is already implemented, say so and stop - there is nothing to plan. If it is only partially done (common for a follow-up), plan only the remaining delta.
   - If this is a follow-up, confirm the code it builds on actually exists on the intended base branch (per config). If not, flag that the branch must base off the original feature branch, not a fresh base cut.
3. Present a clear analysis with a **recommended approach** - not a survey. Where there's a real fork, lay out the trade-off and your pick.
4. **Scope check**: if the work is too large for one reviewable PR, propose splitting it into smaller shippable slices rather than forcing an oversized plan through.

## Phase 3 - Surface the open decisions

Surface the open questions to the **developer first**, split into two buckets:
- **Needs a decision (blocking)** - scope/UX/edge-case choices you should not invent.
- **I can default this (non-blocking)** - state the sensible default you'd take unless told otherwise.

**Ask the blocking ones as interactive questions** - one at a time, each with 2-4 concrete options and your recommendation marked first - so the developer picks, rather than you presenting a wall of prose with a default you would take. Don't settle a blocking decision for them. They may answer some immediately. **Don't assume a product owner exists**: if the developer is the decision-maker, just resolve the questions together. **Only for the ones the developer decides need a product owner's sign-off**, write those up as a short, copy-pasteable list in plain English (no jargon) they can forward verbatim. Cover corner cases explicitly.

If any escalated answers are async, it's fine to **stop here**: save a partial plan (approach so far + open questions) to the plans directory and resume once answers are in. Don't block the session waiting.

## Phase 4 - Discuss until locked

Work through the developer's answers - and any product-owner answers that came back - together; iterate on the approach. **Do not proceed to Phase 5 until the developer explicitly says the approach is settled.** Keep it concrete and decision-oriented.

**A change to UI gets a mockup before the approach locks**, unless its look follows plainly from the description (a one-line copy fix). Draw every screen it touches as one HTML page built from the project's real components - their actual markup and classes, or as close an imitation as HTML allows when the UI is not a web page - and show the page around the change as it really is, not an approximation. Mark what is new and which existing components each piece reuses; where a choice is open, draw the options side by side for the developer to pick. Save it in the plans directory as `<ticket-or-slug>-ui.html`. If your tool can host a page for viewing (on Claude Code, an artifact), publish that same file and republish it to the same address after every revision; edit only the local file, which is the record. Iterate until the developer signs it off, then trim it to the chosen design.

## Phase 5 - Write the step-by-step plan

Once locked, write the plan as **small, ordered, individually-reviewable steps**. Each step is a coherent unit (~one commit / 1-2 files) that lines up with one `/stepgate:step` pass. For **each step** give:
- **What & why** - one line on the change and its reason.
- **Files** - the specific files created/edited.
- **How to verify** - the quick check that this step works (test, manual action, query).
- **Commit** - a suggested commit message stub following your commit conventions (style, scope, ticket reference).
- **Mockup** - for a UI step, the part of the signed-off mockup it builds.

Ordering: types/schema/migrations first, then core lib, then API, then UI, then tests/docs. Leave the tree working after each step where possible; call out any steps that must land together. **When several steps touch the schema, settle its final shape here, before splitting them**: no step undoes another's schema change unless that is the point - an expand, backfill and contract migration says so in the plan - because otherwise the branch reads as a sequence nobody can hold in their head, a policy created in step 2 and dropped in step 5. How the branch divides that into files is a project convention, so follow your config's migration rules.

**Mark the seams.** Where the plan crosses from one layer or surface to another - schema to API, backend to frontend, feature to tests - note it in the plan between those two steps: the point after which nothing ahead builds on the *detail* of what came before. These are the natural break points: `/stepgate:step` tops the plan up at each one, and points at them if the context ever does need compacting.

**Save the plan** to the plans directory from config, filename `<ticket-or-slug>.md`. Start the file with a one-paragraph **summary of the locked approach**, then the outstanding product questions (if any), then the steps. This is a **living document**: `/stepgate:step` updates it as implementation evolves, and `/stepgate:ship` appends the test cases and a plain-language summary - so it always reflects reality and ends as a complete record of the work. If your config says plans are not committed, leave it untracked and tell later commands to exclude it from staging.

End with:
- **Get explicit approval of the step breakdown** - locking the approach is not the same as approving the steps; the developer may want them merged, split, or reordered.
- Only after approval, **ensure the work is on a feature branch off the base branch** (per config; fetch it fresh first), **named per your config's feature-branch-naming convention**. If a ticket is set, include its short reference (e.g. its number) in the name for traceability, unless the convention says otherwise. Never start on a protected branch. For a follow-up whose base code hasn't merged yet, branch off the original feature branch instead. Then offer to **start implementing step 1**.
- Remind the developer of the rhythm: **implement a step -> `/stepgate:step` -> implement the next -> ...**, then **`/stepgate:ship`** once all steps are done.
- **Assess the size and risk of this plan. If it is small and low-risk, actively suggest autopilot**: `/stepgate:step auto` builds, self-reviews, and commits all the steps hands-off, and they review it together at ship. For anything larger or riskier, recommend stepping through supervised (default). Either way it is the developer's call.

---

Throughout: recommend, don't survey. Gate on the developer's input at the approach-lock step. Keep steps small enough that each is easy to review on its own - that is the whole point of pairing this with `/stepgate:step`.
