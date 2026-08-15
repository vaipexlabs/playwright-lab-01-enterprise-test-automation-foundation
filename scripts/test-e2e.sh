#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
MODE="${1:-headless}"
PYTEST_ARGUMENTS=(tests/e2e --browser chromium)

case "${MODE}" in
  headless)
    ;;
  --headed)
    PYTEST_ARGUMENTS+=(--headed --slowmo "${PLAYWRIGHT_SLOW_MO:-500}")
    ;;
  --debug)
    export PWDEBUG=1
    PYTEST_ARGUMENTS+=(-s)
    ;;
  *)
    echo "Usage: ./scripts/test-e2e.sh [--headed|--debug]" >&2
    exit 2
    ;;
esac

if [[ ! -x "${REPOSITORY_ROOT}/.venv/bin/pytest" ]]; then
  "${REPOSITORY_ROOT}/scripts/setup.sh"
fi

"${REPOSITORY_ROOT}/scripts/install-browsers.sh"

echo "Running the Vaipex Store browser journey (${MODE#--})..."
cd "${REPOSITORY_ROOT}"
"${REPOSITORY_ROOT}/.venv/bin/pytest" "${PYTEST_ARGUMENTS[@]}"
