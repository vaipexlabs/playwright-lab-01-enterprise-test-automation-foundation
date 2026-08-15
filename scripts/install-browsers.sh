#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"

if [[ ! -x "${REPOSITORY_ROOT}/.venv/bin/playwright" ]]; then
  "${REPOSITORY_ROOT}/scripts/setup.sh"
fi

echo "Installing the Playwright Chromium browser..."
"${REPOSITORY_ROOT}/.venv/bin/playwright" install chromium
echo "Chromium is ready."
