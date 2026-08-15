#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"

"${REPOSITORY_ROOT}/scripts/ensure-toolchain.sh"

echo "Installing the Playwright Chromium browser..."
"${REPOSITORY_ROOT}/.venv/bin/playwright" install chromium
echo "Chromium is ready."
