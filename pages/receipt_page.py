import re

from playwright.sync_api import expect

from utils import config, helpers


class ReceiptPage:
    """رسید بعد از برگشت از بانک."""

    def __init__(self, page):
        self.page = page
        self.failed_text = page.get_by_text("عملیات ناموفق").first
        self.tracking_label = page.get_by_text(re.compile("کد رهگیری")).first

    def wait_until_back(self):
        self.page.wait_for_url(re.compile(config.return_url_regex()), timeout=45000)

    def is_in_app(self):
        return (config.app_domain() in self.page.url)

    def expect_failed(self):
        expect(self.failed_text).to_be_visible(timeout=30000)

    def shows_amount(self, amount):
        return helpers.text_has_number(self.page.locator("body").inner_text(), amount)

    def tracking_code(self):
        self.tracking_label.wait_for(state="visible", timeout=15000)
        for text in (self.tracking_label.inner_text(), self.tracking_label.locator("xpath=..").inner_text()):
            match = re.search(r"\d{5,}", helpers.normalize_digits(text))
            if match:
                return match.group()
        return ""
