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

[Project Intent](#project-intent) ·
[Target Experience](#target-experience) ·
[Reference Application](#reference-application) ·
[Run Locally](#run-locally) ·
[Run the Browser Journey](#run-the-browser-journey) ·
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
in `requirements.lock`. Open [http://127.0.0.1:8000](http://127.0.0.1:8000) and use:

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

The command installs the pinned Chromium build when necessary, starts Vaipex
Store on an available local port, resets deterministic state, and verifies:

1. The unauthenticated user is directed to sign in.
2. Valid credentials open the product catalog.
3. The Developer Starter Kit can be added to the cart.
4. Checkout captures the required shipping information.
5. The application confirms order `VPX-1001` with the expected total.

The application server is stopped automatically when the test session ends.

## Delivery Roadmap

- [x] Establish repository purpose, licensing, and contribution baseline.
- [x] Add the pinned Python and Playwright toolchain.
- [x] Deliver the deterministic Vaipex Store reference application.
- [x] Implement the first deterministic browser journey.
- [ ] Introduce reusable configuration, fixtures, and page abstractions.
- [ ] Add authentication, test-data, and parallel-execution patterns.
- [ ] Produce reports, traces, screenshots, and failure evidence.
- [ ] Add continuous integration and enforceable quality gates.
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
| Allure | Human-readable test reporting |
| GitHub Actions | Repeatable continuous test execution |

Direct dependencies are declared in `pyproject.toml`; the complete transitive
environment is pinned in `requirements.lock`.

## Repository Structure

```text
src/vaipex_store/   FastAPI routes, templates, and application styling
scripts/            Reproducible setup and local startup commands
tests/unit/         Fast application-contract tests
tests/e2e/          Playwright browser journeys and local server lifecycle
pyproject.toml      Python package, dependency, Pytest, and Ruff configuration
requirements.lock  Fully resolved runtime and test dependency versions
```

## Contributing

Community contributions are welcome. Keep changes portable, deterministic,
secure by default, and understandable to teams adopting the reference
implementation.

Licensed under the [Apache License 2.0](LICENSE).
