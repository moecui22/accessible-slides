#!/usr/bin/env bash
# Mirror the canonical skill into the plugin wrapper so the two never drift.
set -e
cd "$(dirname "$0")"
DEST=plugins/accessible-slides/skills/accessible-slides
mkdir -p "$DEST/references" "$DEST/scripts"
cp SKILL.md "$DEST/"
cp references/*.md "$DEST/references/"
cp scripts/*.py "$DEST/scripts/"
echo "synced -> $DEST"
