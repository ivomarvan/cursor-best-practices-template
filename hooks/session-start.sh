#!/bin/bash
# Cursor sessionStart hook — ensure git commit-msg hook is active.
#
# Registers .cursor/hooks/git as git's hooks directory so the versioned
# commit-msg hook runs on every commit (strips Cursor auto-attribution).
# The template is always installed at .cursor/, so the path is constant.
#
# Never overrides a hooksPath the user set for another purpose (husky,
# pre-commit, ...) — in that case it only reports what to do by hand.

# Consume stdin (required by Cursor hook protocol)
input=$(cat)

# Only act inside a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo '{}'
    exit 0
fi

want=".cursor/hooks/git"
current=$(git config --local --get core.hooksPath 2>/dev/null)

if [ -z "$current" ]; then
    git config --local core.hooksPath "$want"
elif [ "$current" != "$want" ]; then
    # Respect the user's setup; stderr is shown by Cursor, stdout must stay JSON.
    echo "session-start: core.hooksPath is '$current' (not '$want')." >&2
    echo "  Keep both by chaining: copy or exec .cursor/hooks/git/commit-msg from your hook dir." >&2
fi

echo '{}'
exit 0
