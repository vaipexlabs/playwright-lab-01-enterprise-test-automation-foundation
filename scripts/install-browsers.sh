#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"

"${REPOSITORY_ROOT}/scripts/ensure-toolchain.sh"

echo "Installing the Playwright Chromium browser..."
install_arguments=(install chromium)
if [[ "${PLAYWRIGHT_WITH_DEPS:-0}" == "1" ]]; then
  install_arguments=(install --with-deps chromium)
fi
"${REPOSITORY_ROOT}/.venv/bin/playwright" "${install_arguments[@]}"
echo "Chromium is ready."
