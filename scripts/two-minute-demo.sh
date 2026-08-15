#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
JUNIT_REPORT="${REPOSITORY_ROOT}/reports/junit.xml"
HTML_REPORT="${REPOSITORY_ROOT}/reports/playwright.html"

echo "Vaipex Playwright Enterprise Test Automation Foundation"
echo "========================================================"
echo

echo "1/4 Reconcile and verify the pinned Python toolchain"
"${REPOSITORY_ROOT}/scripts/ensure-toolchain.sh"
"${REPOSITORY_ROOT}/.venv/bin/pip" check

echo
echo "2/4 Run formatting, linting, and fast application tests"
"${REPOSITORY_ROOT}/.venv/bin/ruff" format --check "${REPOSITORY_ROOT}"
"${REPOSITORY_ROOT}/.venv/bin/ruff" check "${REPOSITORY_ROOT}"
"${REPOSITORY_ROOT}/.venv/bin/pytest" "${REPOSITORY_ROOT}/tests/unit" -q

echo
echo "3/4 Run four isolated Playwright browser journeys"
"${REPOSITORY_ROOT}/scripts/test-e2e.sh"

echo
echo "4/4 Verify the human-readable and machine-readable evidence"
test -s "${HTML_REPORT}"
test -s "${JUNIT_REPORT}"
"${REPOSITORY_ROOT}/.venv/bin/python" - "${JUNIT_REPORT}" <<'PY'
import sys
import xml.etree.ElementTree as ET

root = ET.parse(sys.argv[1]).getroot()
suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))

def total(attribute: str) -> int:
    return sum(int(suite.get(attribute, "0")) for suite in suites)

print(
    "JUnit summary: "
    f"tests={total('tests')}, failures={total('failures')}, "
    f"errors={total('errors')}, skipped={total('skipped')}"
)
PY

echo
echo "PASS: the automation foundation produced an evidence-backed quality decision."
echo "HTML report: ${HTML_REPORT}"
echo "JUnit report: ${JUNIT_REPORT}"
