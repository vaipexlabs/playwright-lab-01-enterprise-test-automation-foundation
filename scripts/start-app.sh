#!/usr/bin/env bash

set -euo pipefail

REPOSITORY_ROOT="$(CDPATH='' cd -- "$(dirname -- "$0")/.." && pwd)"

"${REPOSITORY_ROOT}/scripts/ensure-toolchain.sh"

export PYTHONPATH="${REPOSITORY_ROOT}/src"
export VAIPEX_TEST_MODE="${VAIPEX_TEST_MODE:-1}"
export VAIPEX_SESSION_SECRET="${VAIPEX_SESSION_SECRET:-local-vaipex-store-session-secret}"

echo "Starting Vaipex Store at http://127.0.0.1:8000"
echo "Demo user: demo@vaipex.io / vaipex-demo"
exec "${REPOSITORY_ROOT}/.venv/bin/uvicorn" vaipex_store.main:app \
  --host 127.0.0.1 \
  --port "${PORT:-8000}"
