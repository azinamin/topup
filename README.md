# تست خودکار خرید شارژ دیجی‌پی

Playwright (Python) + pytest-bdd (Given/When/Then) + Page Object Model، روی Chromium در حالت **headed**.

## هر لایه چه کاری می‌کند
```
features/   ← سناریوها به زبان ساده (Given/When/Then): چه چیزی تست می‌شود
steps/      ← هر جمله‌ی فیچر یک تابع کوتاه است که متد صفحه را صدا می‌زند
pages/      ← اینجا لوکیتورها و کلیک/تایپ هستند (Page Object Model)
components/ ← بخش‌های تکراری UI (مودال اعلان)
test_data/  ← داده‌ی تست (اپراتورها، انواع سیم‌کارت، حد مبلغ). شماره موبایل در آن نیست
utils/      ← تنظیمات (.env)، داده، توابع کمکی، mock، ذخیره‌ی لاگین
tests/      ← هر فایل یک خط است: scenarios("topup/<فایل>.feature")
conftest.py ← فیکسچرها: مرورگر، context تازه برای هر تست، Page Objectها
docs/       ← TEST_DESIGN.md و DESIGN_NOTES.md
```
مسیر یک جمله: `features/topup/e2e.feature` ← `steps/form_steps.py` ← `pages/topup_page.py` (لوکیتور + کلیک).

## پیش‌نیازها
Python 3.10+، یک حساب دیجی‌پی (کد تأیید پیامکی می‌آید). برای Docker/CI: Docker یا GitHub Actions.

## نصب
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium     # اگر دانلود بلاک بود: BROWSER_CHANNEL=chrome را در .env بگذار
cp .env.example .env            # و مقدارها را پر کن (.env هرگز commit نمی‌شود)
```

## متغیرهای محیطی (.env)
| متغیر | الزامی | معنی |
|---|---|---|
| `BASE_URL` | بله | مثلاً `https://app.mydigipay.com` |
| `DIGIPAY_MOBILE` | بله | شماره‌ی لاگین |
| `TOPUP_MOBILE` | نه | شماره‌ی دریافت‌کننده‌ی شارژ (پیش‌فرض: همان شماره‌ی لاگین) |
| `DIGIPAY_OTP` | نه | OTP ثابت برای حساب تستی. خالی = کد پیامکی را خودت در مرورگر می‌زنی |
| `DIGIPAY_TOKEN`, `DIGIPAY_TOKEN_KEY` | نه | توکن که قبل از لاگین در localStorage گذاشته می‌شود |
| `BROWSER_CHANNEL` | نه | `chrome` = استفاده از Google Chrome نصب‌شده به‌جای Chromium دانلودی (فقط لوکال) |
| `ORDER_API_GLOB` | برای `@mocked` | الگوی URL درخواست ساخت سفارش (DevTools > Network) |
| `RETURN_URL_REGEX` | نه | الگوی آدرس بعد از برگشت از بانک (پیش‌فرض `mydigipay`) |

## اجرای لوکال (headed)
```bash
python -m utils.save_login      # یک بار: شماره وارد می‌شود، کد پیامکی را در مرورگر بزن، لاگین ذخیره می‌شود
pytest                          # همه‌ی تست‌ها
pytest -m e2e                   # فقط سناریوی اصلی
pytest -m "real and not e2e"    # تست‌های واقعی دیگر
pytest -m mocked                # تست‌های mock
pytest -k "below_min"           # یک مورد
```
OTP پیامکی را نمی‌شود خودکار کرد؛ برای همین لاگین یک بار انجام و در `.auth/state.json` ذخیره می‌شود و هر تست یک context تازه از آن می‌سازد.
اگر زیاد OTP بخواهی، سرور خطای 429 می‌دهد.

## اجرا با Docker
```bash
docker build -t digipay-tests .
docker run --rm --env-file .env -v "$PWD/.auth:/app/.auth" -v "$PWD/reports:/app/reports" digipay-tests
```
مرورگر headed داخل `xvfb-run` اجرا می‌شود.

## اجرا در CI (GitHub Actions)
فایل `.github/workflows/ci.yml` روی push/PR و به‌صورت دستی اجرا می‌شود. secretها: `BASE_URL`, `DIGIPAY_MOBILE`, `TOPUP_MOBILE`,
`ORDER_API_GLOB` و برای لاگین `AUTH_STATE_B64` (خروجی `base64 -i .auth/state.json`). اجرا headed با `xvfb-run` است و پوشه‌ی `reports/`
(گزارش HTML، اسکرین‌شات، trace) به‌عنوان artifact منتشر می‌شود.

## گزارش‌ها
- `reports/index.html`: گزارش HTML تک‌فایله (اسکرین‌شات تست شکست‌خورده داخلش است)
- `reports/artifacts/`: اسکرین‌شات و trace تست‌های شکست‌خورده. باز کردن trace: `playwright show-trace reports/artifacts/<پوشه>/trace.zip`

## تست‌های واقعی و mock
| تست | حالت | توضیح |
|---|---|---|
| E2E سناریوی اصلی | **واقعی** | در دکمه‌ی انصراف بانک متوقف می‌شود؛ پولی جابه‌جا نمی‌شود |
| TC-01 تا TC-08 | **واقعی** | هیچ‌کدام پرداخت نمی‌کنند |
| TC-09 خطای ۴۰۰/۵۰۰/۵۰۳، TC-10 قطع شبکه، TC-11 دابل‌کلیک | **mock** با `page.route` | درخواست ساخت سفارش به سرور نمی‌رسد |

## تفاوت با ساختار پیشنهادی
پوشه‌ی `features/` اضافه شد (فایل‌های Gherkin کد پایتون نیستند). `components/` فقط یک جزء مشترک دارد. اسکریپت ذخیره‌ی لاگین در `utils/save_login.py` است.

## قبل از اولین اجرای کامل
سایت واقعی را ندیده‌ام که برای همه‌ی صفحات لوکیتور حدسی نباشد. لوکیتورهای ورود، `/top-up`، باتم‌شیت سیم‌کارت و فیلد مبلغ از DOM واقعی گرفته شده‌اند.
لوکیتورهای بعد از مبلغ (دکمه‌ی ادامه، صفحه‌ی تأیید، دکمه‌ی پرداخت، دکمه‌ی انصراف بانک، رسید)، حد واقعی مبلغ در `test_data/topup_data.json` و `ORDER_API_GLOB` باید با سایت تطبیق داده شوند.
