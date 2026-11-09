# Test design

Each test is independent. It gets a fresh browser context (only the login cookies are shared, and they are read-only), reads its own data from `test_data/topup_data.json`, and does not depend on another test's result. Mobile numbers are absent from the data file; they are built from `.env`.

**R** = against the real server response | **M** = the API response is faked with `page.route` (no real transaction is created)

## Mandatory scenario

| ID | Scenario | Type | Goal | Technique | Expected result | Why it was chosen |
|---|---|---|---|---|---|---|
| E2E | Login → buy top-up → number/operator → SIM type and amount → confirm → internet gateway → **cancel at the bank** → return to the app → failed receipt | R | The full money path through a safe ending | End-to-end / state transition | The bank page is on another domain; after cancel, the app returns to mydigipay; the receipt shows «عملیات ناموفق» ("operation failed") with the amount and tracking code | Required by the task; cancelling at the bank is the only way to reach the gateway without moving real money |

## 12 designed test cases (22 executable cases)

| ID | Title / examples | Type | Goal | Technique | Expected result | Why |
|---|---|---|---|---|---|---|
| TC-01 | Operator detection: `0919`, `0935`, `0921` | R | The operator is selected from the prefix | Equivalence partitioning (one representative per operator) | The correct operator card is selected | A wrong operator means top-up for the wrong network; each operator is one partition |
| TC-02 | Invalid number: `short` (10 digits), `bad_prefix` (08...), `letters`, `empty` | R | A bad number does not open the flow | Equivalence partitioning of invalid classes + length boundary | The «خرید شارژ» ("buy top-up") button stays disabled | It is the first form field, and its validation protects the later steps |
| TC-03 | Valid number | R | The positive case for TC-02 | Equivalence partitioning (valid class) | The «خرید شارژ» button becomes enabled | Without the positive case, TC-02 can pass on a button that is always disabled |
| TC-04 | SIM bottom sheet | R | The three SIM types are shown | UI content check | «دائمی» (postpaid), «اعتباری» (prepaid), and «دیتا» (data) are visible | SIM type changes the product that is purchased |
| TC-05 | Invalid amount: `below_min`, `above_max` | R | An amount outside the range is rejected | Boundary value analysis (one below and one above the limit) | Continue stays disabled, or the confirmation page is never reached | Off-by-one errors happen right next to the limits. The custom field rejects `0` and letters, so those are not separate cases |
| TC-12 | Bonus charge («شارژ شورانگیز») | R | The 35% bonus can be switched on | State transition | The switch turns on, and the confirmation page shows the bonus | The amount sheet offers this option beside the preset amounts |
| TC-06 | Amount on the limit: `min`, `max` | R | The limits themselves are valid | Boundary value analysis (on the boundary) | The confirmation page opens | The pair of TC-05, so both sides of each boundary are covered |
| TC-07 | Confirmation for SIM types `credit` and `permanent` | R | The confirmation page shows what was selected | Decision table (SIM type → displayed label) | Number and amount are shown, and both SIM types display «مستقیم» | The user confirms this before going to the bank |
| TC-08 | User without a login | R | Access control | Negative / security test | The login page is shown | The app must keep the flow closed without a session |
| TC-09 | Order API error: `400`, `500`, `503` | M | A server error is handled | Equivalence partitioning of HTTP error classes | An error message is shown, and the app never goes to the bank | A server error cannot be forced on the real server, and the mock creates no real transaction |
| TC-10 | Network drop on the order API | M | A lost connection is handled | Fault injection (`route.abort`) | An error message is shown, and the app never goes to the bank | A different failure from an HTTP error: there is no response at all |
| TC-11 | Double-click on pay | M | The order is submitted once | Error guessing / concurrency (a fake delayed response plus a request count) | The API is called at most once | A duplicate order is the most expensive bug in the payment flow |

## Independence checklist
- Each test gets a fresh context; only `storage_state` is shared, and it is read-only.
- Each test starts from its own `Given` and does not depend on another test's result.
- Mocks are registered on that test's `page` and leave the other tests untouched.
- Proof: run each test alone with `pytest -k "<name>"`, or randomize the order with `pip install pytest-randomly`.
