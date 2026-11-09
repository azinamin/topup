# PR: Digipay top-up purchase automation (Playwright + pytest-bdd + POM)

## What was added
- Mandatory E2E scenario: login → buy top-up → confirm → gateway → cancel → failed receipt.
- 11 designed test cases (24 executable cases): positive, negative, boundary, and API errors with mocks.
- BDD (Given/When/Then) + Page Object Model, test data kept separate, each test independent.
- Dockerfile and a GitHub Actions workflow (headed run under xvfb; the report, screenshots, and traces are published).
- Docs: README, docs/TEST_DESIGN.md, docs/DESIGN_NOTES.md.

## How to review
```bash
cp .env.example .env          # fill in the values
python -m utils.save_login    # once: log in and save the session
pytest -m e2e                 # main scenario, Chromium headed
```

## Screenshots
_Add: (1) the terminal showing a successful run, (2) reports/index.html, (3) the browser on the failed receipt._

## Checklist
- [x] Chromium headed, with slowmo
- [x] Phone number, OTP, token, and URL come only from env; `.env` is gitignored
- [x] Real tests and mock tests are called out in the README
- [x] Feature branch and atomic commits
