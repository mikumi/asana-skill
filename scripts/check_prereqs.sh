#!/usr/bin/env bash
set -euo pipefail

if ! command -v python3 >/dev/null 2>&1; then
  echo 'python3: NOT_INSTALLED'
  echo 'Install python3 first.'
  exit 1
fi

echo "python3: $(python3 --version 2>/dev/null)"

if python3 -c "import asana" >/dev/null 2>&1; then
  echo 'asana-python: INSTALLED'
else
  echo 'asana-python: NOT_INSTALLED'
  echo 'Install with: pip3 install asana'
  exit 1
fi

if [[ -n "${ASANA_ACCESS_TOKEN:-}" ]]; then
  echo 'asana-token: SET'
else
  echo 'asana-token: NOT_SET'
  echo 'Set with: export ASANA_ACCESS_TOKEN="YOUR_TOKEN"'
  exit 1
fi

echo 'status: READY'
