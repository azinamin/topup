# Digipay top-up automation

Playwright (Python) + pytest-bdd (Given/When/Then) + Page Object Model, on Chromium in **headed** mode.

## What each layer does
```
features/   ← scenarios in plain language (Given/When/Then): what is tested
steps/      ← each feature sentence is a short function that calls a page method
pages/      ← locators, clicks, and typing live here (Page Object Model)
components/ ← shared UI pieces (the notification modal)
test_data/  ← test data (operators, SIM types, amount limits). Mobile numbers are absent
utils/      ← settings (.env), data, helpers, mocks, saved login
tests/      ← each file is one line: scenarios("topup/<file>.feature")
conftest.py ← fixtures: browser, a fresh context per test, Page Objects
docs/       ← TEST_DESIGN.md and DESIGN_NOTES.md
```
Path of one sentence: `features/topup/e2e.feature` ← `steps/form_steps.py` ← `pages/topup_page.py` (locator + click).

## Prerequisites
Python 3.10+, and a Digipay account (an SMS verification code is sent). For Docker/CI: Docker or GitHub Actions.

## Setup
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium     # if the download is blocked: set BROWSER_CHANNEL=chrome in .env
cp .env.example .env            # then fill in the values (.env is never committed)
```

## Environment variables (.env)
| Variable | Required | Meaning |
|---|---|---|
| `BASE_URL` | yes | for example `https://app.mydigipay.com` |
| `DIGIPAY_MOBILE` | yes | login phone number |
| `TOPUP_MOBILE` | no | phone number that receives the top-up (default: the login number) |
| `DIGIPAY_OTP` | no | fixed OTP for a test account. Empty = you type the SMS code in the browser |
| `DIGIPAY_TOKEN`, `DIGIPAY_TOKEN_KEY` | no | token written to localStorage before login |
| `BROWSER_CHANNEL` | no | `chrome` = use the installed Google Chrome in place of the downloaded Chromium (local only) |
| `ORDER_API_GLOB` | for `@mocked` | URL pattern of the create-order request (DevTools > Network) |
| `RETURN_URL_REGEX` | no | URL pattern after returning from the bank (default `mydigipay`) |

## Local run (headed)
```bash
python -m utils.save_login      # once: the number is entered, you type the SMS code in the browser, the login is saved
pytest                          # all tests
pytest -m e2e                   # the main scenario only
pytest -m "real and not e2e"    # the other real tests
pytest -m mocked                # the mock tests
pytest -k "below_min"           # one case
```
SMS OTP cannot be automated, so login is done once and saved in `.auth/state.json`, and each test builds a fresh context from it.
Asking for OTP too often makes the server return 429.

## Run with Docker
```bash
docker build -t digipay-tests .
docker run --rm --env-file .env -v "$PWD/.auth:/app/.auth" -v "$PWD/reports:/app/reports" digipay-tests
```
The headed browser runs inside `xvfb-run`.

## Run in CI (GitHub Actions)
`.github/workflows/ci.yml` runs on push, on pull request, and manually. Secrets: `BASE_URL`, `DIGIPAY_MOBILE`, `TOPUP_MOBILE`,
`ORDER_API_GLOB`, and for login `AUTH_STATE_B64` (the output of `base64 -i .auth/state.json`). The run is headed under `xvfb-run`, and the `reports/` folder
(HTML report, screenshots, traces) is published as an artifact.

## Reports
- `reports/index.html`: a single-file HTML report (the failed-test screenshot is embedded)
- `reports/artifacts/`: screenshots and traces of failed tests. Open a trace with `playwright show-trace reports/artifacts/<folder>/trace.zip`

## Real tests and mock tests
| Test | Mode | Notes |
|---|---|---|
| E2E, the main scenario | **real** | Stops at the bank cancel button; no money moves |
| TC-01 through TC-08 | **real** | None of them pay |
| TC-09 errors 400/500/503, TC-10 network drop, TC-11 double-click | **mock** via `page.route` | The create-order request never reaches the server |

## Difference from the suggested layout
The `features/` folder was added because Gherkin files sit outside the Python code. `components/` holds a single shared piece. The login-save script is `utils/save_login.py`.

## Before the first full run
The live site has not been seen well enough for every page's locator to be free of guesswork. Locators for login, `/top-up`, the SIM bottom sheet, and the amount field come from the real DOM.
Locators after the amount (the continue button, the confirmation page, the pay button, the bank cancel button, the receipt), the real amount limits in `test_data/topup_data.json`, and `ORDER_API_GLOB` still need to be aligned with the site.
