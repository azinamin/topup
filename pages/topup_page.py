import re

from utils import config, data, helpers

# رنگ حاشیه و پس‌زمینه‌ی کارتی که دور متن اپراتور است را برمی‌گرداند (کارت انتخاب‌شده ظاهر متفاوتی دارد)
STYLE_JS = """el => {
  let n = el;
  for (let i = 0; i < 5 && n; i++) {
    const cs = getComputedStyle(n);
    if (parseFloat(cs.borderTopWidth) > 0 && cs.borderTopStyle !== 'none') {
      return cs.borderTopColor + '|' + cs.backgroundColor;
    }
    n = n.parentElement;
  }
  return '';
}"""


class TopupPage:
    """/top-up : شماره + اپراتور -> [خرید شارژ] -> انتخاب سیم‌کارت -> مبلغ -> ادامه"""

    def __init__(self, page):
        self.page = page
        # --- لوکیتورها ---
        # id فیلد شماره پویاست (dg-input-1234) پس از آن استفاده نمی‌کنیم
        self.mobile_field = page.locator("input[inputmode='numeric']").first
        self.buy_button = page.get_by_role("button", name="خرید شارژ").first
        self.amount_field = page.get_by_label("مبلغ دلخواه").or_(page.locator("input[id^='dg-amount-']")).first
        self.continue_button = page.get_by_role("button", name=re.compile("ادامه|تایید|تأیید")).first
        self.error_message = page.get_by_role("alert").or_(
            page.get_by_text(re.compile("نامعتبر|خطا|حداقل|حداکثر|مجاز نیست"))
        ).first

    # --- کارها ---
    def open(self):
        self.page.goto(f"{config.base_url()}/top-up", wait_until="domcontentloaded", timeout=90000)
        self.mobile_field.wait_for(state="visible", timeout=30000)

    def type_mobile(self, mobile):
        """اپ شماره‌ی لاگین را خودش در فیلد می‌گذارد؛ پس اول پاک می‌کنیم، تایپ می‌کنیم و چک می‌کنیم."""
        self.page.wait_for_timeout(1000)                     # صبر تا اپ شماره‌ی پیش‌فرض را بگذارد
        shown = ""
        for _ in range(3):
            self.mobile_field.click()
            self.mobile_field.press("ControlOrMeta+A")       # انتخاب همه
            self.mobile_field.press("Backspace")             # پاک کردن
            if mobile:
                self.mobile_field.press_sequentially(mobile, delay=40)
            self.page.wait_for_timeout(400)
            shown = helpers.normalize_digits(self.mobile_field.input_value()).replace(" ", "")
            if shown == mobile or not mobile.isdigit():      # حروف/خالی را نمی‌شود با عدد مقایسه کرد
                return
        raise AssertionError(f"فیلد شماره '{shown}' را نگه داشت، نه '{mobile}'")

    def wait_operator_selected(self, name):
        """هر ۴ کارت اپراتور همیشه دیده می‌شوند؛ کارت انتخاب‌شده فقط ظاهرش با بقیه فرق دارد."""
        styles = {}
        for _ in range(30):
            styles = {n: self.page.get_by_text(n, exact=True).first.evaluate(STYLE_JS, timeout=5000)
                      for n in data.operator_names()}
            others = [s for n, s in styles.items() if n != name]
            if styles[name] and all(styles[name] != s for s in others):
                return
            self.page.wait_for_timeout(300)
        raise AssertionError(f"اپراتور '{name}' انتخاب‌شده به نظر نمی‌رسد. ظاهر کارت‌ها: {styles}")

    def press_buy(self):
        self.buy_button.click()

    def choose_sim(self, label):
        self.page.get_by_text(label, exact=True).first.click()

    def sim_is_visible(self, label):
        return self.page.get_by_text(label, exact=True).first.is_visible()

    def type_amount(self, amount):
        """فیلد هنگام تایپ جداکننده‌ی هزارگان اضافه می‌کند؛ پس هر رقم را جدا می‌زنیم و نشانگر را به آخر می‌بریم."""
        self.amount_field.wait_for(state="visible", timeout=10000)
        self.amount_field.click()
        self.amount_field.press("ControlOrMeta+A")
        self.amount_field.press("Backspace")
        for digit in amount:
            self.amount_field.press(digit)
            self.amount_field.press("End")

    def press_continue(self):
        self.continue_button.click()

    def error_is_shown(self, timeout=8000):
        try:
            self.error_message.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False
