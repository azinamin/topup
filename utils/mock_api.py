"""شبیه‌سازی پاسخ API با page.route: درخواست به سرور واقعی نمی‌رسد، پس تراکنش واقعی ساخته نمی‌شود."""
import json
import time


class Spy:
    """تعداد درخواست‌هایی که به آدرس مورد نظر رفته را می‌شمارد."""

    def __init__(self):
        self.urls = []

    @property
    def count(self):
        return len(self.urls)


def mock_api(page, url_glob, status=500, delay_ms=0, abort=False, methods=("POST", "PUT")):
    spy = Spy()

    def handler(route, request):
        if request.method not in methods:
            return route.fallback()            
        spy.urls.append(request.url)
        if delay_ms:
            time.sleep(delay_ms / 1000)        # پاسخ را عمداً دیر بده
        if abort:
            return route.abort("failed")       # قطع شبکه
        body = json.dumps({"message": "خطا در انجام عملیات", "status": status})
        route.fulfill(status=status, content_type="application/json", body=body)

    page.route(url_glob, handler)
    return spy
