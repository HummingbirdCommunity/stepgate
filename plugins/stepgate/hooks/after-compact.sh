#!/usr/bin/env bash
# After a compaction, point the agent back at the stepgate config and plan it can no longer see.
# Prints nothing outside a stepgate project, so other projects are unaffected.

input=$(cat)
cwd=$(printf '%s' "$input" | sed -n 's/.*"cwd"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
[ -n "$cwd" ] || cwd=$PWD
root=$(git -C "$cwd" rev-parse --show-toplevel 2>/dev/null) || root=$cwd
config="$root/.stepgate/config.md"
local_config="$root/.stepgate/config.local.md"
[ -e "$config" ] || [ -L "$config" ] || exit 0

plans_directory() {
	awk '
		/^## / { section = $0; sub(/[[:space:]]*$/, "", section) }
		(section == "" || section == "## Plan storage") && /^- Plans directory:/ {
			sub(/^- Plans directory:[[:space:]]*/, "")
			sub(/[[:space:]]*$/, "")
			print
			exit
		}
	' "$1"
}

problem=""
for file in "$config" "$local_config"; do
	if [ -e "$file" ] || [ -L "$file" ]; then
		if [ ! -f "$file" ] || [ ! -r "$file" ]; then
			problem="Configuration is unreadable or has a broken link: ${file#"$root/"}"
			break
		fi
	fi
done

plans_dir=.stepgate/plans
if [ -z "$problem" ]; then
	base_dir=$(plans_directory "$config")
	[ -z "$base_dir" ] || plans_dir=$base_dir
	if [ -f "$local_config" ]; then
		local_dir=$(plans_directory "$local_config")
		[ -z "$local_dir" ] || plans_dir=$local_dir
	fi
fi
case "$plans_dir" in
	/*) plans_path=$plans_dir ;;
	*) plans_path="$root/$plans_dir" ;;
esac
branch=$(git -C "$root" branch --show-current 2>/dev/null)

related=""
latest=""
if [ -z "$problem" ] && [ -d "$plans_path" ]; then
	while IFS= read -r plan; do
		case "$plan" in *-ui.md) continue ;; *.md) ;; *) continue ;; esac
		[ -f "$plans_path/$plan" ] || continue
		[ -n "$latest" ] || latest=$plan
		name=${plan%.md}
		if [ -n "$branch" ] && printf '%s' "$branch" | grep -qiF -- "$name"; then
			related="$plans_dir/$plan (matches the branch)"
			break
		fi
	done < <(ls -t -- "$plans_path" 2>/dev/null)
	if [ -z "$related" ] && [ -n "$latest" ]; then
		related="$plans_dir/$latest (most recently edited)"
	fi
fi

echo "This project uses stepgate. If this session was using it - running a stepgate command or working through a stepgate plan - the compaction dropped what was read before it, so before your next action:"
echo "- re-read .stepgate/config.md in full and .stepgate/config.local.md if present, applying local overrides, and any file they point to that the work in hand needs;"
echo "- re-read the plan - its \"Resume here\" block, the step in progress and the steps left - and carry on in that flow under the command's rules."
echo "If the session was not using stepgate, ignore this."
[ -z "$problem" ] || echo "$problem; resolve it before relying on configuration."
[ -n "$branch" ] && echo "Current branch: $branch."
[ -n "$related" ] && echo "Plan: $related."
exit 0
