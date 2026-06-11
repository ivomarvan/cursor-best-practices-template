#!/bin/bash
# Cursor sessionStart hook — ensure git commit-msg hook is active.
#
# Registers .cursor/hooks/git as git's hooks directory so the versioned
# commit-msg hook runs on every commit (strips Cursor auto-attribution).
# The submodule is always mounted at .cursor/, so the path is constant.

# Consume stdin (required by Cursor hook protocol)
input=$(cat)

# Only act inside a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo '{}'
    exit 0
fi

# Set core.hooksPath once; skip if already correct
current=$(git config --local --get core.hooksPath 2>/dev/null)
if [ "$current" != ".cursor/hooks/git" ]; then
    git config --local core.hooksPath .cursor/hooks/git
fi

echo '{}'
exit 0
