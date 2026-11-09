# Design notes: selectors and avoiding flaky tests

## Selector strategy
1. **Prefer what the user sees:** `get_by_role`, `get_by_text`, `get_by_label`. These survive CSS and DOM structure changes.
   (Real example: the amount field is found with `get_by_label("مبلغ دلخواه")` ("custom amount") because the placeholder is empty and only the label is visible.)
2. **Stable attributes:** `inputmode='numeric'`, a fixed id prefix (`id^='dg-amount-'`), `autocomplete='one-time-code'`.
3. **Never** a full dynamic id (`dg-input-8082` changes on every load), generated class names, an index, or a long XPath.
4. **Every locator lives only in `pages/` and `components/`.** Step files contain no selectors, so a UI change is fixed in one file.
5. If the mini-app sits inside an iframe, locators are built with `page.frame_locator(...)` (not needed so far).

## Avoiding flakiness
- **No fixed `sleep` for waiting.** Playwright's smart waits are used (`wait_for`, `wait_for_url`, `expect`). The only `wait_for_timeout` calls are a short delay so the app can fill the default phone number, and a wait in the double-click test until the fake delayed response finishes.
- **Login once.** SMS OTP cannot be automated, and the server returns 429 after several SMS requests. Login is done once and saved (`python -m utils.save_login`); each test builds a fresh context from that state.
- **Notification modal.** After login, the "enable notifications" modal blocks clicks. `page.add_locator_handler` closes it automatically whenever it appears.
- **Typing in masked fields.** The amount field inserts thousand separators while typing and moves the caret into the middle (`10000` became `1٬000٬000`). Each digit is typed separately, then `End` is pressed.
- **Default phone number.** The app fills the login number into the field itself, so the field is cleared before typing, the value is checked after typing, and the attempt is retried up to 3 times if needed.
- **Tolerant comparison.** Persian and Arabic digits are converted to Latin and thousand separators are stripped, so `10000` is distinct from `100000`.
- **Operator card.** All 4 cards are always visible, so "selected" is judged by a visual difference (border or background color) relative to the others, and visibility is ignored.
- **Bank gateway.** The bank page is outside our control. The cancel button is found as a button, link, or input, and the confirm dialog is accepted. The return is checked by URL domain, and pixel position is ignored.
- **Mocked errors are deterministic.** Server errors are produced with `page.route`, and the suite does not wait for a real failure. The mock creates no real transaction.
- **Money safety.** The real test stops at the bank cancel button, and no test completes a payment.
- **Failure evidence.** Screenshots and traces are captured only for failed tests, and the screenshot is embedded in the HTML report.

## Known limitations
- SMS OTP cannot be automated: locally it is entered by hand; in CI a saved session (`AUTH_STATE_B64`) or a test account with a fixed OTP is used.
- Until a real run, locators after amount selection (continue, confirmation page, pay, bank, receipt) and `ORDER_API_GLOB` still need to be aligned with the live site.
