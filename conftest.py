import base64

import pytest

from components.notification_modal import NotificationModal
from pages.confirm_page import ConfirmPage
from pages.gateway_page import GatewayPage
from pages.hub_page import HubPage
from pages.login_page import LoginPage
from pages.receipt_page import ReceiptPage
from pages.topup_page import TopupPage
from utils import config

pytest_plugins = [
    "steps.common_steps",
    "steps.form_steps",
    "steps.payment_steps",
    "steps.mock_steps",
]


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    args = {**browser_type_launch_args,
            "args": [*browser_type_launch_args.get("args", []), "--window-size=1000,760", "--window-position=0,0"]}
    if config.browser_channel():            # فقط وقتی BROWSER_CHANNEL=chrome در .env باشد
        args["channel"] = config.browser_channel()
    return args


@pytest.fixture
def browser_context_args(browser_context_args, request):
    args = {**browser_context_args, "locale": "fa-IR", "timezone_id": "Asia/Tehran",
            "viewport": {"width": 1000, "height": 600}}
    if request.node.get_closest_marker("no_auth") is None:       # تگ @no_auth = بدون لاگین
        if not config.STATE_FILE.exists():
            pytest.fail("لاگین ذخیره‌شده نیست. اول اجرا کن:  python -m utils.save_login")
        args["storage_state"] = str(config.STATE_FILE)           # کوکی‌های لاگین (فقط‌خواندنی)
    return args


@pytest.fixture
def mock_state():
    """یک دیکشنری تازه برای هر تست (نگه‌داشتن شمارنده‌ی درخواست‌های mock)."""
    return {}


@pytest.fixture
def login_page(page): return LoginPage(page)

@pytest.fixture
def hub_page(page): return HubPage(page)

@pytest.fixture
def topup_page(page): return TopupPage(page)

@pytest.fixture
def confirm_page(page): return ConfirmPage(page)

@pytest.fixture
def gateway_page(page): return GatewayPage(page)

@pytest.fixture
def receipt_page(page): return ReceiptPage(page)

@pytest.fixture
def notification_modal(page): return NotificationModal(page)


@pytest.fixture(autouse=True)
def _auto_close_notification(notification_modal):
    notification_modal.auto_close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            try:
                from pytest_html import extras
                png = base64.b64encode(page.screenshot()).decode()
                report.extras = getattr(report, "extras", []) + [extras.png(png)]
            except Exception:
                pass
