#!/bin/bash
# Post-merge setup for the Geo-Arts Curriculum project.
# Runs automatically after a task is merged into the main app.
# Must be idempotent and non-interactive (stdin is closed).
set -e

echo "[post-merge] Syncing Python dependencies via uv..."
if command -v uv >/dev/null 2>&1; then
  uv sync --frozen 2>/dev/null || uv sync
else
  echo "[post-merge] uv not found on PATH; skipping dependency sync."
fi

echo "[post-merge] Done."
