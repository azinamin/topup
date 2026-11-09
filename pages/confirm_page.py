import re

from playwright.sync_api import TimeoutError as PWTimeout

from utils import helpers


class ConfirmPage:
    """صفحه‌ی تأیید + انتخاب روش پرداخت."""

    def __init__(self, page):
        self.page = page
        self.gateway_option = page.get_by_text("درگاه پرداخت اینترنتی").first
        self.pay_button = page.get_by_role("button", name=re.compile("پرداخت|تایید|تأیید|ادامه")).last

    def is_open(self, timeout=10000):
        try:
            self.gateway_option.wait_for(state="visible", timeout=timeout)
            return True
        except PWTimeout:
            return False

    def _text(self):
        return self.page.locator("body").inner_text()

    def shows_mobile(self, mobile):
        return helpers.text_has_mobile(self._text(), mobile)

    def shows_amount(self, amount):
        return helpers.text_has_number(self._text(), amount)

    def shows_text(self, text):
        return self.page.get_by_text(text).first.is_visible()

    def choose_gateway_and_pay(self):
        self.gateway_option.click()
        self.pay_button.click()
