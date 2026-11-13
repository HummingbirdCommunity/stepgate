# Layered project configuration

## Read

- Use the current repository's .stepgate/config.md as the base and optional .stepgate/config.local.md for local differences. The base file remains the initialization signal; preserve and reuse local values when initialization is needed.
- Read both files once per session and after compaction. Re-read when either file or symlink target changes, including addition or removal. A missing local file is normal; report unreadable files or broken links before relying on affected settings.
- Preserve symlinks and existing single-file or private setups. Loading and plugin updates must not rewrite configuration or move plans. Read explicitly referenced documents only as needed.

## Merge

- Precedence: built-in defaults < base < local < the developer's current explicit instruction. Retain each setting's source. Configuration does not grant new commit, push, or external-write approval.
- Match fields by section and name. Local values override matching fields; omitted fields inherit. Merge free-form rules by matter: local wins clear conflicts, unrelated rules remain. Never replace a whole section or list unless explicitly requested; surface ambiguous conflicts.
- Briefly identify explicit conflicts and their winning local source, once per unchanged configuration.

## Paths

Resolve relative configuration paths from the current repository root, even through symlinks; keep absolute paths absolute.

Keep the plan directory as a literal, unquoted `- Plans directory: <path>` line. Missing or blank local values inherit the base; missing or blank base values use .stepgate/plans. Do not evaluate shell expressions or relocate existing plans.

## Update

- Prefer an existing field; otherwise use Conventions, or Verifying locally for verification setup.
- Identify the existing source and propose either editing it or creating a local override. Suggest base for team conventions and local for personal preferences or machine settings; honor the developer's chosen destination.
- Show the proposed text and file, including symlink targets, and obtain agreement before writing. Change only agreed content; keep local differences small. Keep credentials outside both files and personal machine details out of shared configuration.
- Respect separate sharing choices for the base and plans. Keep config.local.md ignored and excluded from staging. Only when the developer chooses to share config.md, ensure it is trackable; otherwise preserve its private setup. Report already-tracked local configuration instead of silently changing the index.
