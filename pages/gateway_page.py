from urllib.parse import urlparse

from utils import config


def _is_bank(url):
    host = urlparse(url).hostname or ""
    return bool(host) and not host.endswith(config.app_domain())


class GatewayPage:
    """صفحه‌ی درگاه بانک (دامنه‌ی دیگر)."""

    def __init__(self, page):
        self.page = page
        self.cancel_button = page.locator(
            "button:has-text('انصراف'), a:has-text('انصراف'), input[value*='انصراف']"
        ).first

    def wait_until_open(self):
        self.page.wait_for_url(_is_bank, timeout=45000)

    def is_open(self):
        return _is_bank(self.page.url)

    def cancel(self):
        self.page.once("dialog", lambda d: d.accept())   # بعضی درگاه‌ها تأیید می‌خواهند
        self.cancel_button.click()
