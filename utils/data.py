"""داده‌های تست از test_data/topup_data.json. شماره موبایل‌ها از روی .env ساخته می‌شوند (نه ذخیره در فایل)."""
import json

from utils import config

_FILE = config.ROOT / "test_data" / "topup_data.json"


def _load():
    with open(_FILE, encoding="utf-8") as f:
        return json.load(f)


# ---------- شماره موبایل ----------
def mobile_for(case):
    valid = config.topup_mobile()
    cases = {
        "valid": valid,
        "short": valid[:-1],             # ۱۰ رقم
        "bad_prefix": "08" + valid[2:],  # با 09 شروع نمی‌شود
        "letters": "abcdefghijk",
        "empty": "",
    }
    return cases[case]


def mobile_with_prefix(prefix):
    return prefix + config.topup_mobile()[4:]


def operator_key_for(mobile):
    return _load()["operators"]["prefixes"].get(mobile[:4])


def operator_name(key):
    return _load()["operators"]["names"][key]


def operator_names():
    return list(_load()["operators"]["names"].values())


# ---------- نوع سیم‌کارت ----------
def sim_label(key):
    return _load()["sim_types"][key]


def sim_confirm_label(key):
    """برچسب نوع شارژ در صفحه‌ی تأیید. اعتباری و دائمی آنجا «مستقیم» دیده می‌شوند."""
    return _load().get("sim_confirm_labels", {}).get(key, sim_label(key))


def sim_labels():
    return list(_load()["sim_types"].values())


def amount_for(case):
    limits = _load()["amount_limits"]
    cases = {
        "default": limits["default"],
        "min": limits["min"],
        "max": limits["max"],
        "below_min": limits["min"] - 1,
        "above_max": limits["max"] + 1,
    }
    return str(cases[case])


def shown_amount(case):
    """مبلغ به ریال است. بازه‌ی واقعی صفحه: ۲۲۰٬۰۰۰ تا ۱٬۰۰۰٬۰۰۰."""
    return amount_for(case)
