# Vaipex Playwright Enterprise Test Automation Foundation

An open reference implementation for building reliable, maintainable, and
operable browser automation with Playwright and Python. It provides a supported
foundation that development and quality engineering teams can adopt, extend,
and run consistently from a workstation or continuous integration pipeline.

Developed by **Vaipex Labs** for the developer and quality engineering
communities.

![Focus](https://img.shields.io/badge/Focus-Test%20Automation-6D42E8)
![Playwright](https://img.shields.io/badge/Playwright-Python-2EAD33?logo=playwright&logoColor=white)
![Test Runner](https://img.shields.io/badge/Test%20Runner-pytest-0A9EDC?logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/License-Apache%202.0-blue)
[![Quality Gates](https://github.com/vaipexlabs/playwright-lab-01-enterprise-test-automation-foundation/actions/workflows/quality-gates.yaml/badge.svg)](https://github.com/vaipexlabs/playwright-lab-01-enterprise-test-automation-foundation/actions/workflows/quality-gates.yaml)

[Project Intent](#project-intent) ·
[Target Experience](#target-experience) ·
[Reference Application](#reference-application) ·
[Run Locally](#run-locally) ·
[Run the Browser Journey](#run-the-browser-journey) ·
[Test Architecture](#test-architecture) ·
[Failure Evidence](#failure-evidence) ·
[Continuous Integration](#continuous-integration) ·
[Delivery Roadmap](#delivery-roadmap) ·
[Toolchain](#toolchain) ·
[Contributing](#contributing)

## Project Intent

Browser tests often begin as isolated scripts and become difficult to operate
as the suite grows. This project demonstrates how to provide Playwright as an
engineering capability with consistent structure, configuration, execution,
evidence, and quality controls.

The completed reference implementation will demonstrate:

- A maintainable Python and Pytest project structure.
- Reusable browser, context, configuration, and test-data fixtures.
- Reliable locators and web-first assertions.
- Page and component abstractions that preserve test intent.
- Authentication-state reuse without committing credentials.
- Parallel-safe tests with deterministic setup and cleanup.
- Failure evidence through traces, screenshots, video, and reports.
- Consistent local and GitHub Actions execution.
- A concise two-minute demonstration for adopters.

## Target Experience

The intended developer journey is:

```text
Clone repository
      ↓
Install the supported toolchain
      ↓
Run one command
      ↓
Execute isolated browser journeys
      ↓
Inspect results and failure evidence
      ↓
Apply the same quality gate in CI
```

## Reference Application

The repository includes **Vaipex Store**, a compact FastAPI commerce
application designed specifically for deterministic automation. It provides:

- Demo authentication and session behavior.
- A searchable product catalog.
- Cart, checkout, and order-confirmation journeys.
- Validation and unauthorized-access scenarios.
- Health and catalog APIs.
- A test-only state-reset API that is disabled unless test mode is explicit.
- Accessible labels, semantic landmarks, and stable test attributes.

Owning the test target keeps this reference implementation independent of
external websites, rate limits, shared data, and unannounced UI changes.

## Run Locally

Python 3.12 is required. Start the complete application with:

```bash
./scripts/start-app.sh
```

The first run creates `.venv` and installs the complete dependency set pinned
in `requirements.lock`. Later commands automatically reconcile `.venv` whenever
that lock changes. Open [http://127.0.0.1:8000](http://127.0.0.1:8000) and use:

```text
Email:    demo@vaipex.io
Password: vaipex-demo
```

Stop the application with `Ctrl+C`. To validate the application without a
browser:

```bash
.venv/bin/pytest tests/unit
.venv/bin/ruff check .
```

## Run the Browser Journey

Execute the first complete Playwright journey with one command:

```bash
# Fast headless execution
./scripts/test-e2e.sh

# Watch the browser execute each step
./scripts/test-e2e.sh --headed

# Pause and inspect the journey with Playwright Inspector
./scripts/test-e2e.sh --debug
```

Headed mode uses a 500 ms delay between Playwright operations so the journey is
easy to follow. Override it when needed, for example:

```bash
PLAYWRIGHT_SLOW_MO=1000 ./scripts/test-e2e.sh --headed
```

The command installs the pinned Chromium build when necessary and runs four
independent scenarios across two parallel workers:

1. Invalid credentials are rejected with an actionable error.
2. A complete sign-in, cart, and Starter Kit checkout succeeds.
3. A previously authenticated customer can search the catalog.
4. A previously authenticated customer can purchase the Field Guide.

Each worker starts an isolated application, resets its own state, and stops the
application automatically. Change concurrency without editing code:

```bash
PLAYWRIGHT_WORKERS=4 ./scripts/test-e2e.sh
```

Every normal run writes:

- A self-contained report to `reports/playwright.html`.
- A machine-readable report to `reports/junit.xml`.
- Failure-only browser evidence beneath `artifacts/playwright/`.

## Test Architecture

The browser suite separates business intent from UI mechanics and environment
operation:

```text
Business-readable test
        ↓
Page objects and web-first assertions
        ↓
Configured Playwright page
        ↓
Environment and lifecycle fixtures
        ↓
Vaipex Store or a compatible target environment
```

| Layer | Responsibility |
| --- | --- |
| `tests/e2e/` | Describe the customer outcome being validated |
| `tests/e2e/conftest.py` | Start or connect to the application and reset test state |
| `tests/pages/` | Encapsulate locators, interactions, and page-level assertions |
| `tests/config.py` | Validate URLs, credentials, shipping data, and timeouts |
| `tests/data.py` | Generate deterministic, worker-specific scenario data |
| `tests/conftest.py` | Configure browser pages and reusable test-data fixtures |

Authentication is performed once per worker. Playwright saves the resulting
browser storage state in that worker's temporary directory, and authenticated
tests create fresh contexts from it. Storage state is never written into the
repository.

Test data is derived from the worker ID and scenario name. Repeated runs remain
predictable, while parallel workers receive distinct names, addresses, and
postal codes.

The defaults run entirely locally. A compatible environment can be selected
without changing test code:

```bash
VAIPEX_BASE_URL=https://store.example.test \
VAIPEX_DEMO_EMAIL=automation@example.test \
VAIPEX_DEMO_PASSWORD='replace-me' \
./scripts/test-e2e.sh
```

Supported configuration:

| Variable | Default | Purpose |
| --- | --- | --- |
| `VAIPEX_BASE_URL` | Dynamically started local app | Target environment |
| `VAIPEX_EXPECT_TIMEOUT_MS` | `5000` | Assertion and navigation timeout |
| `VAIPEX_DEMO_EMAIL` | `demo@vaipex.io` | Test-user identity |
| `VAIPEX_DEMO_PASSWORD` | `vaipex-demo` | Test-user credential |
| `VAIPEX_SHIPPING_NAME` | `Vaipex Developer` | Checkout recipient |
| `VAIPEX_SHIPPING_STREET` | `100 Platform Way` | Checkout street |
| `VAIPEX_SHIPPING_CITY` | `Cloud City` | Checkout city |
| `VAIPEX_SHIPPING_POSTAL_CODE` | `10001` | Checkout postal code |

## Failure Evidence

Playwright retains diagnostics only when a browser test fails:

| Evidence | Purpose |
| --- | --- |
| Screenshot (`.png`) | Show the browser's final visible state |
| Trace (`.zip`) | Replay actions, DOM snapshots, console, network, and timing |
| Video (`.webm`) | Show the complete failed browser journey |
| HTML report | Provide a human-readable suite result |
| JUnit XML | Integrate results with CI and quality systems |

Prove the behavior safely with:

```bash
./scripts/demonstrate-failure.sh
```

The script runs one intentionally incorrect assertion. It succeeds only when
the expected test failure produces all five forms of evidence, and stores that
run beneath timestamped `artifacts/failure-demo/` and
`reports/failure-demo/` directories.

Open the latest HTML report in a browser, or inspect a trace with:

```bash
.venv/bin/playwright show-trace path/to/trace.zip
```

Generated reports and browser evidence are ignored by Git.

## Continuous Integration

Run the complete local gate before submitting a change:

```bash
./scripts/quality-gate.sh
```

GitHub Actions applies the same contract on pushes to `main`, pull requests,
and manual workflow runs:

| Job | Gate |
| --- | --- |
| Fast Quality Gate | Locked setup, formatting, linting, and 10 fast tests |
| Browser Quality Gate | Chromium dependencies and four parallel Playwright journeys |
| Quality Gate | One stable required-check result across both execution jobs |

Fast-test JUnit results and browser HTML/JUnit reports are retained for 14
days. Screenshots, traces, and videos are uploaded when the browser job fails.
Workflow permissions are read-only, action dependencies are pinned to immutable
commit SHAs, and redundant runs on the same branch are cancelled.

The final `Quality Gate` check is ready to be selected as a required status
check in the repository's `main` branch protection settings.

Dependabot proposes grouped weekly updates for Python and GitHub Actions
dependencies. Every proposal must pass the same quality gates.

## Delivery Roadmap

- [x] Establish repository purpose, licensing, and contribution baseline.
- [x] Add the pinned Python and Playwright toolchain.
- [x] Deliver the deterministic Vaipex Store reference application.
- [x] Implement the first deterministic browser journey.
- [x] Introduce reusable configuration, fixtures, and page abstractions.
- [x] Add authentication, test-data, and parallel-execution patterns.
- [x] Produce reports, traces, screenshots, and failure evidence.
- [x] Add continuous integration and enforceable quality gates.
- [ ] Publish the two-minute demo and operating guidance.

Each milestone is intentionally small and independently reviewable.

## Toolchain

| Tool | Role |
| --- | --- |
| Python | Automation language |
| Playwright for Python | Browser automation across Chromium, Firefox, and WebKit |
| Pytest | Test runner, fixtures, markers, and assertions |
| pytest-xdist | Parallel test execution |
| Ruff | Python linting and formatting |
| pytest-html and JUnit XML | Human-readable and machine-readable test reporting |
| GitHub Actions | Repeatable continuous test execution |

Direct dependencies are declared in `pyproject.toml`; the complete transitive
environment is pinned in `requirements.lock`.

## Repository Structure

```text
src/vaipex_store/   FastAPI routes, templates, and application styling
scripts/            Reproducible setup and local startup commands
.github/             Quality-gate workflow and dependency automation
artifacts/          Generated failure screenshots, traces, and videos (ignored)
reports/            Generated HTML and JUnit reports (ignored)
tests/unit/         Fast application-contract tests
tests/e2e/          Business-readable Playwright browser journeys
tests/pages/        Reusable page interactions and UI assertions
tests/config.py     Validated environment and test-data configuration
tests/data.py       Deterministic, parallel-safe scenario data
tests/conftest.py   Shared browser and test-data fixtures
pyproject.toml      Python package, dependency, Pytest, and Ruff configuration
requirements.lock  Fully resolved runtime and test dependency versions
```

## Contributing

Community contributions are welcome. Keep changes portable, deterministic,
secure by default, and understandable to teams adopting the reference
implementation.

Licensed under the [Apache License 2.0](LICENSE).
