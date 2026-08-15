# Operating Guide

This guide covers the routine operation and extension of the Vaipex Playwright
Enterprise Test Automation Foundation.

## Prerequisites

- Python 3.12
- A supported macOS or Linux environment
- Network access on the first run to install pinned Python and Chromium builds

Run `./scripts/setup.sh` to create `.venv` and install the locked Python
environment. All other entry points reconcile the environment automatically
when `requirements.lock` changes.

## Execution Modes

| Command | Use case |
| --- | --- |
| `./scripts/two-minute-demo.sh` | Demonstrate the complete quality contract |
| `./scripts/quality-gate.sh` | Run the same complete gate used by delivery automation |
| `./scripts/test-e2e.sh` | Run four browser journeys headlessly across two workers |
| `./scripts/test-e2e.sh --headed` | Watch the journeys execute in Chromium |
| `./scripts/test-e2e.sh --debug` | Pause execution with Playwright Inspector |
| `./scripts/demonstrate-failure.sh` | Prove that failure evidence is captured |
| `./scripts/start-app.sh` | Explore Vaipex Store manually at `127.0.0.1:8000` |

Set `PLAYWRIGHT_WORKERS` to change headless concurrency and
`PLAYWRIGHT_SLOW_MO` to change the delay in headed mode.

## Test a Compatible Environment

The default fixtures start one isolated local application per worker. Point the
same journeys at a compatible deployed environment without changing test code:

```bash
VAIPEX_BASE_URL=https://store.example.test \
VAIPEX_DEMO_EMAIL=automation@example.test \
VAIPEX_DEMO_PASSWORD='replace-me' \
./scripts/test-e2e.sh
```

Use a dedicated test identity and supply credentials through local environment
variables or the CI secret store. Never commit production credentials or saved
browser storage state.

## Reports and Failure Evidence

A normal browser run writes:

- `reports/playwright.html` for human review.
- `reports/junit.xml` for CI and quality-system ingestion.
- Failure-only traces, screenshots, and videos under `artifacts/playwright/`.

Open an interactive failure trace with:

```bash
.venv/bin/playwright show-trace path/to/trace.zip
```

GitHub Actions retains fast-test results and browser reports for 14 days. A
failed browser job also uploads its diagnostic artifacts.

## Troubleshooting

### Pytest rejects a report argument

Run `./scripts/setup.sh`. The project now detects a stale `.venv` and
automatically reconciles it against `requirements.lock`, including
`pytest-html`.

### Chromium is missing

Run `./scripts/install-browsers.sh`. On Linux, the GitHub Actions workflow also
installs the required operating-system dependencies.

### The browser is not visible

Headless execution is the default. Use `./scripts/test-e2e.sh --headed` to
watch it or `--debug` to inspect each operation.

### A local port is already in use

The automated suite allocates dynamic ports for its worker-owned applications.
Only the manual `./scripts/start-app.sh` command uses port 8000.

### A test passes locally but fails in CI

Download the browser-test artifact from the failed workflow run. Inspect the
HTML report first, then use the screenshot, video, and trace to compare the UI,
network activity, and timing.

## Extend the Foundation

1. Add business outcomes to `tests/e2e/`.
2. Place UI mechanics and stable locators in `tests/pages/`.
3. Generate scenario data through `tests/data.py` so parallel workers remain
   independent.
4. Add environment settings to `tests/config.py` and validate them at startup.
5. Preserve web-first assertions and avoid fixed sleeps.
6. Run `./scripts/quality-gate.sh` before submitting the change.

The quality contract is complete only when fast checks, isolated browser
journeys, actionable evidence, and the stable CI gate remain green together.
