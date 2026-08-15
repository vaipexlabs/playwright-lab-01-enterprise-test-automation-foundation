#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"
RUN_ID="$(date -u +%Y%m%dT%H%M%SZ)"
ARTIFACT_DIRECTORY="${REPOSITORY_ROOT}/artifacts/failure-demo/${RUN_ID}"
REPORT_DIRECTORY="${REPOSITORY_ROOT}/reports/failure-demo/${RUN_ID}"

"${REPOSITORY_ROOT}/scripts/install-browsers.sh"
mkdir -p "${ARTIFACT_DIRECTORY}" "${REPORT_DIRECTORY}"

echo "Running an intentionally failing browser assertion..."
set +e
VAIPEX_RUN_FAILURE_DEMO=1 "${REPOSITORY_ROOT}/.venv/bin/pytest" \
  "${REPOSITORY_ROOT}/tests/e2e/test_failure_evidence_demo.py" \
  --browser chromium \
  --numprocesses 0 \
  --output "${ARTIFACT_DIRECTORY}" \
  --tracing retain-on-failure \
  --screenshot only-on-failure \
  --video retain-on-failure \
  --html "${REPORT_DIRECTORY}/failure.html" \
  --self-contained-html \
  --junitxml "${REPORT_DIRECTORY}/junit.xml"
test_exit_code=$?
set -e

if [[ ${test_exit_code} -eq 0 ]]; then
  echo "FAIL: the evidence demonstration was expected to fail." >&2
  exit 1
fi

for extension in png zip webm; do
  if ! find "${ARTIFACT_DIRECTORY}" -type f -name "*.${extension}" -print -quit | grep -q .; then
    echo "FAIL: expected .${extension} failure evidence was not captured." >&2
    exit 1
  fi
done

echo
echo "PASS: the expected failure produced screenshot, trace, video, HTML, and JUnit evidence."
echo "Artifacts: ${ARTIFACT_DIRECTORY}"
echo "Reports:   ${REPORT_DIRECTORY}"
