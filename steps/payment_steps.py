import re

from pytest_bdd import parsers, then, when

from utils import config, data


@when("I choose the internet gateway and pay")
def choose_gateway_and_pay(confirm_page):
    confirm_page.choose_gateway_and_pay()


@then("I should be on the bank page")
def on_bank_page(gateway_page):
    gateway_page.wait_until_open()
    assert gateway_page.is_open(), f"انتظار صفحه‌ی بانک را داشتم ولی {gateway_page.page.url} باز است"


@when("I cancel on the bank page")
def cancel_on_bank(gateway_page):
    gateway_page.cancel()


@then("I should be back in DigiPay")
def back_in_digipay(receipt_page, page):
    receipt_page.wait_until_back()
    assert re.search(config.return_url_regex(), page.url), f"آدرس بعد از برگشت اشتباه است: {page.url}"
    assert receipt_page.is_in_app(), f"به دیجی‌پی برنگشتیم: {page.url}"


@then(parsers.parse('I should see the failed receipt with the "{case}" amount and a tracking code'))
def failed_receipt(receipt_page, case):
    receipt_page.expect_failed()
    assert receipt_page.shows_amount(data.shown_amount(case)), "مبلغ رسید با مبلغ انتخابی فرق دارد"
    code = receipt_page.tracking_code()
    assert code, "کد رهگیری در رسید نیست"
    print(f"\nکد رهگیری رسید ناموفق: {code}")
