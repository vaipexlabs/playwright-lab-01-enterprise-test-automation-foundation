#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
MODE="${1:-headless}"
REPORT_DIRECTORY="${REPOSITORY_ROOT}/reports"
ARTIFACT_DIRECTORY="${REPOSITORY_ROOT}/artifacts/playwright"
PYTEST_ARGUMENTS=(
  tests/e2e
  -m "not evidence_demo"
  --browser chromium
  --output "${ARTIFACT_DIRECTORY}"
  --tracing retain-on-failure
  --screenshot only-on-failure
  --video retain-on-failure
  --html "${REPORT_DIRECTORY}/playwright.html"
  --self-contained-html
  --junitxml "${REPORT_DIRECTORY}/junit.xml"
)

case "${MODE}" in
  headless)
    PYTEST_ARGUMENTS+=(--numprocesses "${PLAYWRIGHT_WORKERS:-2}")
    ;;
  --headed)
    PYTEST_ARGUMENTS+=(
      --headed
      --slowmo "${PLAYWRIGHT_SLOW_MO:-500}"
      --numprocesses "${PLAYWRIGHT_WORKERS:-1}"
    )
    ;;
  --debug)
    export PWDEBUG=1
    PYTEST_ARGUMENTS+=(-s --numprocesses 0)
    ;;
  *)
    echo "Usage: ./scripts/test-e2e.sh [--headed|--debug]" >&2
    exit 2
    ;;
esac

"${REPOSITORY_ROOT}/scripts/install-browsers.sh"
mkdir -p "${REPORT_DIRECTORY}" "${ARTIFACT_DIRECTORY}"

echo "Running the Vaipex Store browser journeys (${MODE#--})..."
cd "${REPOSITORY_ROOT}"
"${REPOSITORY_ROOT}/.venv/bin/pytest" "${PYTEST_ARGUMENTS[@]}"

echo
echo "Reports:"
echo "  HTML:  ${REPORT_DIRECTORY}/playwright.html"
echo "  JUnit: ${REPORT_DIRECTORY}/junit.xml"
echo "Failure artifacts: ${ARTIFACT_DIRECTORY}"
