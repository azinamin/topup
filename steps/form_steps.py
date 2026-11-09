import pytest
from pytest_bdd import given, parsers, then, when

from utils import config, data


# ---------- ساخت فرم ----------
def _fill_until_amount(topup_page, sim):
    topup_page.type_mobile(data.mobile_for("valid"))
    topup_page.press_buy()
    topup_page.choose_sim(data.sim_label(sim))


@given("the form is filled up to the amount step")
def filled_until_amount(topup_page):
    _fill_until_amount(topup_page, "credit")


@given("a valid top-up form")
def valid_form(topup_page):
    _fill_until_amount(topup_page, "credit")
    topup_page.type_amount(data.shown_amount("default"))


@when(parsers.parse('I type the "{case}" mobile number'))
def type_mobile(topup_page, case):
    topup_page.type_mobile(data.mobile_for(case))


@when(parsers.parse('I type my number with prefix "{prefix}"'))
def type_mobile_with_prefix(topup_page, prefix):
    topup_page.type_mobile(data.mobile_with_prefix(prefix))


@when("I press the buy button")
def press_buy(topup_page):
    topup_page.press_buy()


@when(parsers.parse('I choose the "{sim}" sim type'))
def choose_sim(topup_page, sim):
    topup_page.choose_sim(data.sim_label(sim))


@when(parsers.parse('I type the "{case}" amount'))
def type_amount(topup_page, case):
    topup_page.type_amount(data.shown_amount(case))


@when("I turn on the bonus charge")
def turn_on_bonus_charge(topup_page):
    topup_page.turn_on_bonus_charge()


@when("I press continue")
def press_continue(topup_page):
    topup_page.press_continue()


# ---------- بررسی‌ها ----------
@then(parsers.parse('the operator "{key}" should be selected'))
def operator_selected(topup_page, key):
    topup_page.wait_operator_selected(data.operator_name(key))


@then("the operator of my number should be selected")
def my_operator_selected(topup_page):
    key = data.operator_key_for(config.topup_mobile())
    if key is None:
        pytest.skip("پیش‌شماره‌ی این شماره در test_data/topup_data.json نیست")
    topup_page.wait_operator_selected(data.operator_name(key))


@then("the buy button should be disabled")
def buy_disabled(topup_page):
    from playwright.sync_api import expect
    expect(topup_page.buy_button).to_be_disabled(timeout=5000)


@then("the buy button should be enabled")
def buy_enabled(topup_page):
    from playwright.sync_api import expect
    expect(topup_page.buy_button).to_be_enabled(timeout=10000)


@then("I should see the sim types")
def see_sim_types(topup_page):
    from playwright.sync_api import expect
    for label in data.sim_labels():
        expect(topup_page.page.get_by_text(label, exact=True).first).to_be_visible(timeout=10000)


@then("I should not be able to continue")
def cannot_continue(topup_page, confirm_page):
    button = topup_page.continue_button
    assert button.count() > 0, "دکمه‌ی ادامه پیدا نشد؛ لوکیتور continue_button را اصلاح کن"
    if button.is_disabled():
        return                                    # دکمه غیرفعال است: درست
    button.click()                                # فعال بود: نباید به صفحه‌ی تأیید برود
    assert not confirm_page.is_open(timeout=3000), "مبلغ نامعتبر نباید به صفحه‌ی تأیید برسد"


@then("I should reach the confirmation page")
def reach_confirmation(confirm_page):
    assert confirm_page.is_open(), "صفحه‌ی تأیید باز نشد"


@then(parsers.parse('the confirmation shows my mobile, the "{case}" amount and the "{sim}" sim type'))
def confirmation_details(confirm_page, case, sim):
    assert confirm_page.shows_mobile(config.topup_mobile()), "شماره‌ی موبایل در صفحه‌ی تأیید نیست"
    assert confirm_page.shows_amount(data.shown_amount(case)), "مبلغ در صفحه‌ی تأیید نیست یا اشتباه است"
    assert confirm_page.shows_text(data.sim_confirm_label(sim)), "نوع سیم‌کارت در صفحه‌ی تأیید نیست"


@then("the confirmation shows the bonus charge")
def confirmation_bonus(confirm_page):
    assert confirm_page.shows_bonus_charge(), "شارژ شورانگیز در صفحه‌ی تأیید نیست"
