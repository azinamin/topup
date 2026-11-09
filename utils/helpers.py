"""توابع کمکی کوچک."""
import re

_PERSIAN = "۰۱۲۳۴۵۶۷۸۹"
_ARABIC = "٠١٢٣٤٥٦٧٨٩"
_TO_LATIN = str.maketrans(_PERSIAN + _ARABIC, "0123456789" * 2)


def normalize_digits(text):
    """ارقام فارسی/عربی را به انگلیسی تبدیل می‌کند: ۰۹۲۱ -> 0921"""
    return text.translate(_TO_LATIN)


def text_has_number(text, number):
    """آیا عدد (مثل 10000) در متن هست؟ جداکننده‌ی هزارگان و نوع رقم مهم نیست."""
    t = normalize_digits(text)
    t = re.sub(r"(?<=\d)[,٬،](?=\d{3}(?!\d))", "", t)
    return re.search(rf"(?<!\d){re.escape(str(number))}(?!\d)", t) is not None


def text_has_mobile(text, mobile):
    t = re.sub(r"[\s\-]", "", normalize_digits(text))
    return mobile in t or mobile[1:] in t   # 0912... یا +98912...
