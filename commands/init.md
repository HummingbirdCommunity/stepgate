---
description: One-time project setup - interview you about your conventions (task tracker, branches, review guideline, commit rules, migrations, automated checks) and write .stepgate/config.md. plan/step/ship run it automatically if there's no config yet; run it yourself anytime to (re)configure.
argument-hint: "[optional: a section to reconfigure, e.g. branches | commits | tracker]"
---

# /stepgate:init - configure stepgate for this project

You are setting up stepgate for the current repository. Your job: produce `.stepgate/config.md` at the project root - the config the other stepgate commands read to follow this project's conventions. **Write it in the user's project, not the plugin directory.**

This is the one-time setup - it interviews the developer and writes the config the working commands depend on. `plan`/`step`/`ship` **run it automatically** whenever a project has no config yet, then continue; the developer can also run it directly to (re)configure. For a team, commit the config so everyone shares one setup.

**Language**: run the **entire interview in the user's language** - every question, every option label, and the summary must match the language they are talking to you in (they write in Chinese, you ask in Chinese). This command runs before the config exists, so judge their language from the conversation, not from config. Only the **config file's values** stay in English (they mirror real branch names, paths, and commands).

**If `.stepgate/config.md` already exists**, read it first and switch to adjust mode: show what's set, change only the sections the user asks for (or the single section named in `$ARGUMENTS`), and preserve the rest. Otherwise, do a fresh setup:

## Phase 1 - Detect, don't just ask

Before asking anything, inspect the repo to propose sensible defaults:

- **Default branch**: `git symbolic-ref refs/remotes/origin/HEAD` or `git branch --show-current` on a fresh clone; fall back to asking.
- **Task tracker signals**: is there a GitHub remote (`git remote -v`)? A `.jira` / Linear reference in docs? Existing ticket-style prefixes in recent commit messages - **subject and body** (`git log -30 --format='%B'`), since a ticket ref often sits in the body, not the title (e.g. `ABC-123`, `#123`)?
- **Review guideline**: look for common locations - `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `.github/copilot-instructions.md`, `.cursor/rules/`, `.cursorrules`, `docs/CODE_REVIEW*.md`, `docs/STYLE*.md`, `STYLE_GUIDE.md`, `CODING_STANDARDS.md`. If none match, just ask.
- **Automated checks**: read `package.json` scripts (test / lint / typecheck / format), or the equivalent for the stack (`Makefile`, `pyproject.toml`, `cargo`, `go`).
- **Running it locally**: how the app starts (`package.json` scripts `dev`/`start`, a `Procfile`, `docker-compose.yml`, `Makefile` targets, `manage.py`, `bin/rails`, a `main.go`), the port that command uses, and whether the repo carries browser tooling (`playwright.config.*`, `cypress.config.*`, an `e2e/` directory). A library or CLI with nothing to serve has none of this.
- **Database schema changes**: look for a migrations directory (`migrations/`, `supabase/migrations/`, `db/migrate/`, `prisma/migrations/`) **or** a manually-maintained SQL changelog / schema file (`schema.sql`, `db/CHANGELOG*`, a `database/`/`sql/` dir, `*.sql` change logs). If you find neither but the project clearly talks to a database, **ask** rather than assuming there are none.
- **Commit style**: scan recent commit **messages - subjects and bodies** (`git log -20`) - to capture the full style: the subject format (`type(scope): ...`) and its language, **and whether commits carry a body, its structure, and where a ticket link goes**.
- **How ship ends**: a project with no remote, or a convention doc that says work is merged locally, does not end in a pull request. Otherwise default to one, and ask when it is unclear.
- **PR template**: look for `.github/PULL_REQUEST_TEMPLATE.md` (or `.github/pull_request_template.md`, a `PULL_REQUEST_TEMPLATE/` dir, or GitLab's `.gitlab/merge_request_templates/`).
- **Merge strategy**: for a GitHub repo, `gh api repos/{owner}/{repo} --jq '{squash: .allow_squash_merge, merge: .allow_merge_commit, rebase: .allow_rebase_merge}'` - if only one method is allowed, that's it. **For any non-GitHub host, or if detection fails, ask the developer** (squash / merge commit / rebase) - don't leave it "unsure" unless they genuinely don't know.
- **Plans directory**: check `.gitignore` for an already-ignored scratch/notes/plans/specs path (a strong hint the project keeps working notes untracked), and look for an existing `docs/plans`, `docs/specs`, `docs/rfcs`, `.plans`, or `notes/`. Whether the chosen directory is gitignored also answers "commit plans to git". Any **other** ignored-but-present working path - a `docs/spec`, a `scratch/`, `*.local.md`, but not the plans directory itself - is a never-stage path; collect those too.

**Read what you find, don't just note its path.** Convention docs (especially `CLAUDE.md` / `AGENTS.md` / `CONTRIBUTING.md`) often state the base branch, whether a ticket is required, the commit scopes, and the migration commands outright - extract those values and pre-fill them, rather than only recording which file holds them.

**Detect from this project only** - its own files (docs, config, git history). **Do not infer conventions from the user's global slash-commands, skills, or other personal tooling** (e.g. a global command that mentions some other repo's branch flow); those are the developer's personal setup, not this project's rules. When in doubt, ask rather than borrow a convention from outside the repo.

## Phase 2 - Pre-fill, then ask only the gaps

You already know most of this from Phase 1. **Don't interrogate the user section by section.**

1. **Pre-fill** every value you could detect or read out of the convention docs. **Only pre-fill what you actually determined** - if you can't tell (a non-GitHub merge strategy, whether the DB has schema changes, etc.), leave it as a gap to ask in step 3; don't fill a lazy `no` / `unsure` just to move on.
2. **Present the filled config as a short summary** and ask for a single confirm-or-correct pass - not one question per field.
3. **Actively ask, one at a time and as interactive questions (each with options and your recommendation), only about values you couldn't determine** - usually the two **Language** settings, whether a ticket is **required** (if the docs don't say), any **promotion path**, **which port or process is the developer's own**, **how ship ends** (if not detected), **PR marker** preference, and **whether to commit the config and plan files or keep them local**. Don't ask about anything you already detected with confidence.

The sections to end up with (detected or asked):

1. **Language** - the **Local language** for our conversation, review findings, plans, and working notes (default: match the user); and the **Published language** for anything that lands in the repo or goes to other people - commit messages, PRs, ticket/task updates, code comments and strings, reviewer/product-owner-facing text (default: English). **Detect Published from the existing code comments and commit history** (a project that comments and commits in another language wants that), then confirm. Note: code **identifiers** stay English regardless - as do file paths and the commit-message stubs written inside a Local-language plan.
2. **Task tracker** - none / GitHub Issues / Jira / Linear / Notion / other; the ticket reference format; a skip marker for ticketless changes; whether a ticket is required on commits and PRs; how to fetch a ticket's details; a link base URL for clickable references.
3. **Branches** - the base branch features branch from and PRs target; protected branches never to commit to directly; feature-branch naming; any promotion path (e.g. `dev -> staging -> main`).
4. **Code review guideline** - path(s) to the file(s) that define review criteria, or none (then reviews use general best practices).
5. **Commit conventions** - a reference to your commit-message guide if you have one (a doc/section covering style, scopes, and wording); otherwise the default style (conventional commits or free).
6. **Database migrations** - whether this project has DB schema changes; the migrations directory or schema-change file; the apply command; the rules (idempotency, timestamped filenames).
7. **Automated checks** - format, typecheck, lint, and test commands (exactly as run; tests can be one or more commands - whatever should pass before shipping), how to run the tests of just a few files (step runs those before each commit), plus any setup note (e.g. a required toolchain version).
8. **Verifying locally** - how to stand this project up and actually look at a change: the run command and port; any port, server, or process that belongs to the developer and must never be touched; how a check gets past a login when pages are behind one; where screenshots and recordings are written and where they are delivered; what teardown is needed. **Ask only the cheap parts now** - how it runs, and which port or process is theirs. The rest is learned the hard way, so seed the section and move on rather than interrogating them about a setup they have not needed yet: `/stepgate:ship` offers additions each time it verifies something. **Write what you do not know as `unknown yet`, not as `n/a`** - `n/a` tells ship the field does not apply, so it will never try to learn it. Skip the section entirely for a project with nothing to serve.
9. **Pull requests** - how ship ends: a pull request, a local merge into the target branch with no pull request, or the whole-branch gate only (the developer takes it from there); the PR target branch; a PR template/guide reference if the project has one (else `ship` writes a Summary + Test plan); the merge strategy (squash / merge commit / rebase); whether `ship` should manage a regenerated body section between markers.
10. **Plan storage** - **ask where step plans should live** (suggest a sensible default like `.stepgate/plans` or `docs/plans`, but let the developer choose). Whether to commit them or keep them local is handled under Committing below (and if the chosen directory is already gitignored, that answers it - local). Also record any **other** paths that must never be staged - local scratch the developer keeps in the tree on purpose - so the working commands stop offering them.

**Committing (ask this during the interview, not at the end).** Two things can land in the repo: `.stepgate/config.md` and the plan files. **Ask the developer explicitly, for each, whether to commit it** (shared with everyone who clones the repo) **or keep it local** (gitignored). These are preferences you cannot detect - **do not assume or default either one**; ask. For anything kept local, add it to `.gitignore` when you write the config.

The config also ends with a free-form `## Conventions` section. Seed it with any standing rules the developer already mentions; otherwise leave it empty - the working commands append to it over time.

## Phase 3 - Write the config

Write `.stepgate/config.md` using exactly this structure (other commands rely on these section headings). Fill each value from the confirmed answers; use `none` / `n/a` where a section doesn't apply.

**Keep each field to its own plain value.** If a workflow *overrides* a field's normal meaning - e.g. "PRs target `dev`, except hotfixes, which go to `main`" - record the exception in `## Conventions`, don't stuff it into the field (Target branch stays just `dev`). Never write the same rule in both a field and Conventions.

```markdown
# Stepgate configuration
<!-- Generated by /stepgate:init. Edit freely and commit to share with your team. Stepgate commands read this file; plugin updates never overwrite it. -->

## Language
- Local language (our conversation, review findings shown to you, plans, working notes - anything that stays on your machine; file paths, identifiers, and commit-message stubs inside them stay English): <auto (match you) | a language>
- Published language (commit messages, pull requests, ticket/task updates, code comments and strings, questions and updates for your reviewer or product owner - anything that lands in the repo or goes to other people; code identifiers stay English regardless): <English | a language>

## Task tracker
- Type: <none | github-issues | jira | linear | notion | other>
- Ticket reference format: <e.g. #123 | ABC-123 | none>
- Skip marker: <e.g. [skip ticket] | none>
- Ticket required on commits and PRs: <yes | no - this only sets whether a ticket is mandatory; a ticket you do provide is always included>
- How to fetch a ticket: <e.g. `gh issue view <n>` | Jira MCP | manual paste | n/a>
- Ticket link base URL: <e.g. https://github.com/OWNER/REPO/issues/ | none>

## Branches
- Base branch: <e.g. main>
- Protected branches (never commit directly): <e.g. main>
- Feature branch naming: <e.g. free | feat/<slug> | <ticket>-<slug>>
- Promotion path: <e.g. none | dev -> staging -> main>

## Code review guideline
- Guideline files: <e.g. CLAUDE.md, docs/CODE_REVIEW_SPEC.md | none>

## Commit conventions
- Commit message guide: <path(s)/section documenting your commit style, scopes, and wording, e.g. CONTRIBUTING.md, docs/COMMIT_GUIDE.md | none>
- Default style (used when there's no guide): <conventional commits (type(scope): subject) | free>
- Body style: <how this project writes the commit body, from recent commits - its structure and where a ticket link goes, e.g. "body: what + why in Chinese; ticket link on the last line" | title only>

## Database migrations
- Present in this project: <yes | no>
- Migrations directory or schema-change file: <path, e.g. migrations/ or db/changelog.sql | n/a>
- Apply command: <command, or "applied manually" | n/a>
- Rules: <e.g. idempotent, timestamped filename | n/a>

## Automated checks
- Setup note: <e.g. use Node 22 | none>
- Format: <command operating on given files | none>
- Typecheck: <command, e.g. tsc --noEmit / mypy / cargo check | none - untyped project has no typecheck>
- Lint: <command operating on given files | none>
- Tests: <automated test command(s) run as the pre-ship gate; one or more, e.g. npm test | npm run test:unit | pytest | none. Leave slow/CI-only suites out - those belong in end-to-end verification, not this gate.>
- Tests for given files: <how to run only some test files, which step runs before each commit, e.g. npx vitest run <files> | pytest <files> | same as Tests - the runner cannot narrow>

## Verifying locally
<!-- How to stand this project up and actually look at a change. Prompts, not a schema - an answer that needs a paragraph gets a paragraph. It starts as whatever is known now and grows: /stepgate:ship offers additions whenever it verifies something the hard way. Delete the section for a project with nothing to serve. -->
- Run it: <command and port, e.g. `npm run dev` on 3000 | unknown yet>
- Hands off: <any port, server, or process that belongs to the developer - never start on it, kill it, or restart it | none>
- Getting past auth: <how a check gets a signed-in session or a test account, when pages are behind a login | unknown yet | n/a - no login>
- Evidence: <where screenshots and recordings are written, and where they are delivered for the developer to look at | unknown yet | none - nothing visual>
- Teardown: <what to clean up afterwards - temp credentials, servers, worktrees, stray artifacts | unknown yet | none>

## Pull requests
- Ship ends with: <a pull request | a local merge into the target branch, no pull request | the whole-branch gate only - the developer pushes and merges>
- Target branch: <e.g. main>
- PR template / guide: <path, e.g. .github/PULL_REQUEST_TEMPLATE.md, CONTRIBUTING.md#pull-requests | none - ship writes a Summary + Test plan>
- Merge strategy: <squash | merge commit | rebase | unsure>
- Regenerated body markers: <e.g. <!-- stepgate:start --> / <!-- stepgate:end --> | none>

## Plan storage
- Plans directory: <where step plans live, e.g. .stepgate/plans | docs/plans | .plans>
- Commit plans to git: <yes | no - if the directory is gitignored, this is no>
- Never stage these paths: <local scratch that lives in the tree but must never be committed, e.g. docs/spec/, scratch/, *.local.md | none - the plans directory above is excluded anyway>

## Conventions
<!-- Standing rules you establish over time, in plain language. Commands follow these, and offer to add here when you diverge from the flow on something no field above covers. Starts empty. -->
```

## Phase 4 - Close out

Confirm the file path, and **apply the commit-vs-local choices from the interview** - add `.stepgate/` and/or the plans directory to `.gitignore` for whatever the developer chose to keep local. Tell them they can edit the config by hand anytime. **If a stepgate command triggered this setup, hand control back to it and continue** where it left off - don't tell them to run something. Otherwise point them at the next step: **`/stepgate:plan`** to turn a requirement into a reviewable step plan.
