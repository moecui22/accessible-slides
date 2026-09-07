#!/usr/bin/env bash
# Mirror the canonical skill into every packaging target so they never drift.
set -e
cd "$(dirname "$0")"
for DEST in plugins/accessible-slides/skills/accessible-slides .cursor/skills/accessible-slides; do
  mkdir -p "$DEST/references" "$DEST/scripts"
  cp SKILL.md "$DEST/"
  cp references/*.md "$DEST/references/"
  cp scripts/*.py "$DEST/scripts/"
  echo "synced -> $DEST"
done
