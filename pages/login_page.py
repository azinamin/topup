import re

from utils import config


class LoginPage:
    def __init__(self, page):
        self.page = page
        # --- لوکیتورها (آدرس المان‌ها) ---
        self.phone_field = page.locator("input[inputmode='numeric']").first
        self.continue_button = page.get_by_role("button", name="قبول شرایط و ادامه")
        self.otp_field = page.locator("input[autocomplete='one-time-code'], input[name*='otp' i]").first

    # --- کارها ---
    def open(self):
        """اگر لاگین نباشی اپ به /auth/login می‌رود و اگر باشی به /hub."""
        self.page.goto(config.base_url(), wait_until="domcontentloaded", timeout=90000)
        self.page.wait_for_url(re.compile(r"/(auth|hub)"), timeout=60000)

    def is_login_page(self):
        return "/auth/" in self.page.url

    def login(self, mobile, otp=""):
        self.open()
        if not self.is_login_page():
            return                                     # از قبل لاگین بوده
        self.phone_field.wait_for(state="visible", timeout=30000)
        self.phone_field.fill(mobile)
        self.continue_button.click()
        try:
            self.otp_field.wait_for(state="visible", timeout=30000)
        except Exception:
            raise RuntimeError(
                "صفحه‌ی کد پیامکی باز نشد. اگر ارسال پیامک خطای 429 (Too Many Requests) داد، "
                "چند ساعت صبر کن یا شبکه را عوض کن؛ مشکل از تست نیست."
            )
        if otp:
            self.otp_field.click()
            self.page.keyboard.type(otp, delay=80)
        else:
            print("\n>>> کد پیامکی را در همین مرورگر وارد کن (۲ دقیقه وقت داری)...")
        self.page.wait_for_url(lambda url: "/auth/" not in url, timeout=120000)
