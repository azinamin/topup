# PR: اتوماسیون خرید شارژ دیجی‌پی (Playwright + pytest-bdd + POM)

## چه چیزی اضافه شد
- سناریوی اجباری E2E: لاگین ← خرید شارژ ← تأیید ← درگاه ← انصراف ← رسید ناموفق.
- ۱۱ تست‌کیس طراحی‌شده (۲۴ مورد اجرایی): مثبت، منفی، مرزی و خطای API با mock.
- BDD (Given/When/Then) + Page Object Model، داده‌ی تست جدا، هر تست مستقل.
- Dockerfile و workflow برای GitHub Actions (اجرای headed با xvfb، انتشار گزارش، اسکرین‌شات و trace).
- مستندات: README، docs/TEST_DESIGN.md، docs/DESIGN_NOTES.md.

## نحوه‌ی بررسی
```bash
cp .env.example .env          # مقدارها را پر کن
python -m utils.save_login    # یک بار: لاگین و ذخیره‌ی نشست
pytest -m e2e                 # سناریوی اصلی، Chromium headed
```

## اسکرین‌شات
_اضافه کن: (۱) ترمینال با اجرای موفق، (۲) reports/index.html، (۳) مرورگر روی رسید ناموفق._

## چک‌لیست
- [x] Chromium headed و slowmo
- [x] شماره، OTP، توکن و آدرس فقط از env؛ `.env` در gitignore
- [x] تست‌های واقعی و mock در README مشخص شده‌اند
- [x] branch فیچر و کامیت‌های اتمیک
