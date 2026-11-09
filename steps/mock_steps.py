"""تست‌هایی که پاسخ API را با page.route جعل می‌کنند (تراکنش واقعی ساخته نمی‌شود)."""
from pytest_bdd import given, parsers, then, when

from utils import config
from utils.mock_api import mock_api


@given(parsers.parse('the order API fails with status "{status}"'))
def api_fails(page, mock_state, status):
    mock_state["spy"] = mock_api(page, config.order_api_glob(), status=int(status))


@given("the order API connection fails")
def api_connection_fails(page, mock_state):
    mock_state["spy"] = mock_api(page, config.order_api_glob(), abort=True)


@given(parsers.parse('the order API is slow and fails with status "{status}" after "{delay}" ms'))
def api_slow(page, mock_state, status, delay):
    mock_state["spy"] = mock_api(page, config.order_api_glob(), status=int(status), delay_ms=int(delay))


@when("I submit the order")
def submit_order(topup_page, confirm_page):
    topup_page.press_continue()
    if confirm_page.is_open(timeout=5000):
        confirm_page.choose_gateway_and_pay()


@when("I double-click the pay button")
def double_click_pay(topup_page, confirm_page):
    topup_page.press_continue()
    assert confirm_page.is_open(), "صفحه‌ی تأیید باز نشد"
    confirm_page.gateway_option.click()
    confirm_page.pay_button.dblclick()


@then("I should see an error message")
def see_error(topup_page):
    assert topup_page.error_is_shown(), "پیام خطایی نمایش داده نشد"


@then("I should not be on the bank page")
def not_on_bank(gateway_page):
    assert not gateway_page.is_open(), f"کاربر نباید به بانک برود: {gateway_page.page.url}"


@then(parsers.parse("the order API should be called at most {n} time"))
def call_count(page, mock_state, n):
    page.wait_for_timeout(4000)   # صبر تا پاسخ دیرِ جعلی تمام شود
    assert mock_state["spy"].count <= int(n), f"API {mock_state['spy'].count} بار صدا زده شد (ثبت دوباره‌ی سفارش)"
