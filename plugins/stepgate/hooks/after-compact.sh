#!/usr/bin/env bash
# After a compaction, point Claude back at the stepgate config and plan it can no longer see.
# Prints nothing outside a stepgate project, so other projects are unaffected.

input=$(cat)
cwd=$(printf '%s' "$input" | sed -n 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
[ -n "$cwd" ] || cwd=$PWD
root=$(git -C "$cwd" rev-parse --show-toplevel 2>/dev/null) || root=$cwd
config="$root/.stepgate/config.md"
[ -f "$config" ] || exit 0

plans_dir=$(sed -n 's/^- Plans directory:[[:space:]]*//p' "$config" | head -n 1 | sed 's/[[:space:]]*$//')
[ -n "$plans_dir" ] || plans_dir=.stepgate/plans
branch=$(git -C "$root" branch --show-current 2>/dev/null)

related=""
if [ -d "$root/$plans_dir" ]; then
	for plan in $(ls -t "$root/$plans_dir" 2>/dev/null | grep '\.md$'); do
		name=${plan%.md}
		case "$name" in *-ui) continue ;; esac
		if [ -n "$branch" ] && printf '%s' "$branch" | grep -qiF -- "$name"; then
			related="$plans_dir/$plan (matches the branch)"
			break
		fi
	done
	if [ -z "$related" ]; then
		latest=$(ls -t "$root/$plans_dir" 2>/dev/null | grep '\.md$' | grep -v -- '-ui\.md$' | head -n 1)
		[ -n "$latest" ] && related="$plans_dir/$latest (most recently edited)"
	fi
fi

echo "This project uses stepgate. If this session was using it - running a stepgate command or working through a stepgate plan - the compaction dropped what was read before it, so before your next action:"
echo "- re-read .stepgate/config.md in full, and any file it points to that the work in hand needs;"
echo "- re-read the plan - its \"Resume here\" block, the step in progress and the steps left - and carry on in that flow under the command's rules."
echo "If the session was not using stepgate, ignore this."
[ -n "$branch" ] && echo "Current branch: $branch."
[ -n "$related" ] && echo "Plan: $related."
exit 0
