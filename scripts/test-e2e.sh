#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"

if [[ ! -x "${REPOSITORY_ROOT}/.venv/bin/pytest" ]]; then
  "${REPOSITORY_ROOT}/scripts/setup.sh"
fi

"${REPOSITORY_ROOT}/scripts/install-browsers.sh"

echo "Running the Vaipex Store browser journey..."
cd "${REPOSITORY_ROOT}"
"${REPOSITORY_ROOT}/.venv/bin/pytest" tests/e2e --browser chromium
