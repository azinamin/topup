import re

from utils import config


class HubPage:
    """صفحه‌ی اصلی بعد از لاگین (/hub)."""

    def __init__(self, page):
        self.page = page

    def open(self):
        self.page.goto(config.base_url(), wait_until="domcontentloaded", timeout=90000)
        self.page.wait_for_url(re.compile(r"/(auth|hub)"), timeout=60000)

    def expect_logged_in(self):
        assert "/auth/" not in self.page.url, (
            "لاگین ذخیره‌شده معتبر نیست. دوباره اجرا کن:  python -m utils.save_login"
        )
