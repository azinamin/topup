"""مودال «فعال‌سازی اعلان‌ها» که بعد از لاگین روی صفحه می‌آید و جلوی کلیک‌ها را می‌گیرد."""
import re

from playwright.sync_api import TimeoutError as PWTimeout


class NotificationModal:
    def __init__(self, page):
        self.page = page
        self.title = page.get_by_text(re.compile("فعال.?سازی اعلان")).first   # .? یعنی نیم‌فاصله هم باشد اشکالی ندارد
        self.close_button = page.get_by_text("بستن", exact=True).last          # مودال آخر صفحه اضافه می‌شود

    def auto_close(self):
        """هر وقت مودال وسط کار ظاهر شد، خودکار بسته شود."""
        self.page.add_locator_handler(self.title, lambda: self.close_button.click())

    def close_if_shown(self, timeout=4000):
        try:
            self.title.wait_for(state="visible", timeout=timeout)
        except PWTimeout:
            return
        self.close_button.click()
