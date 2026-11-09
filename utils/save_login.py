"""یک بار اجرا کن:  python -m utils.save_login
مرورگر باز می‌شود، شماره وارد می‌شود، تو کد پیامکی را می‌زنی، و لاگین در .auth/state.json ذخیره می‌شود.
بعد از آن همه‌ی تست‌ها بدون OTP با همین لاگین شروع می‌شوند (OTP پیامکی را نمی‌شود خودکار کرد)."""
from playwright.sync_api import sync_playwright

from components.notification_modal import NotificationModal
from pages.login_page import LoginPage
from utils import config


def main():
    config.STATE_FILE.parent.mkdir(exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            channel=config.browser_channel() or None,
            args=["--window-size=1000,760", "--window-position=0,0"],
        )
        context = browser.new_context(locale="fa-IR", viewport={"width": 1000, "height": 600})
        if config.token():
            context.add_init_script(f"localStorage.setItem({config.token_key()!r}, {config.token()!r});")
        page = context.new_page()
        NotificationModal(page).auto_close()
        LoginPage(page).login(config.login_mobile(), config.otp())
        context.storage_state(path=str(config.STATE_FILE))
        print(f"\nلاگین ذخیره شد: {config.STATE_FILE}")
        browser.close()


if __name__ == "__main__":
    main()
