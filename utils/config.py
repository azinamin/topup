"""همه‌ی تنظیمات فقط از متغیرهای محیطی (فایل .env) خوانده می‌شود. هیچ شماره یا آدرسی در کد نیست."""
import os
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

STATE_FILE = ROOT / ".auth" / "state.json"   # لاگین ذخیره‌شده (کوکی‌ها)


def _env(name, default=""):
    return (os.getenv(name) or default).strip()


def _required(name):
    value = _env(name)
    if not value:
        raise RuntimeError(f"متغیر {name} در فایل .env تنظیم نشده. .env.example را کپی کن به .env.")
    return value


def _mobile(name, value):
    if not (value.isdigit() and len(value) == 11 and value.startswith("09")):
        raise RuntimeError(f"{name} باید ۱۱ رقم باشد و با 09 شروع شود")
    return value


def base_url():
    return _required("BASE_URL").rstrip("/")


def app_domain():
    """app.mydigipay.com  ->  mydigipay.com"""
    host = urlparse(base_url()).hostname or ""
    return ".".join(host.split(".")[-2:])


def login_mobile():
    return _mobile("DIGIPAY_MOBILE", _required("DIGIPAY_MOBILE"))


def topup_mobile():
    return _mobile("TOPUP_MOBILE", _env("TOPUP_MOBILE") or login_mobile())


def otp():
    return _env("DIGIPAY_OTP")


def token():
    return _env("DIGIPAY_TOKEN")


def token_key():
    return _env("DIGIPAY_TOKEN_KEY", "token")


def browser_channel():
    return _env("BROWSER_CHANNEL")


def order_api_glob():
    return _env("ORDER_API_GLOB", "**/topup/**")


def return_url_regex():
    return _env("RETURN_URL_REGEX", "mydigipay")
