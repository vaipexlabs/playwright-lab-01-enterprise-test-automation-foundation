#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"

"${REPOSITORY_ROOT}/scripts/ensure-toolchain.sh"

echo "1/3 Verify formatting and lint rules"
"${REPOSITORY_ROOT}/.venv/bin/ruff" format --check "${REPOSITORY_ROOT}"
"${REPOSITORY_ROOT}/.venv/bin/ruff" check "${REPOSITORY_ROOT}"

echo
echo "2/3 Run fast application and configuration tests"
"${REPOSITORY_ROOT}/.venv/bin/pytest" "${REPOSITORY_ROOT}/tests/unit"

echo
echo "3/3 Run parallel Playwright browser journeys"
"${REPOSITORY_ROOT}/scripts/test-e2e.sh"

echo
echo "PASS: all local quality gates succeeded."
