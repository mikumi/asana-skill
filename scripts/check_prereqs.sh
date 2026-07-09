#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if ! command -v uv >/dev/null 2>&1; then
  echo 'uv: NOT_INSTALLED'
  echo 'Install with: brew install uv'
  exit 1
fi

echo "uv: $(uv --version)"

uv run --script "$SCRIPT_DIR/execute_action.py" --runtime-check

if [[ -n "${ASANA_ACCESS_TOKEN:-}" ]]; then
  echo 'asana-token: SET'
else
  echo 'asana-token: NOT_SET'
  echo 'Set with: export ASANA_ACCESS_TOKEN="YOUR_TOKEN"'
  exit 1
fi

echo 'status: READY'
