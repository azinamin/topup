from pytest_bdd import given, parsers, then, when


@given("I am logged in")
def logged_in(hub_page):
    hub_page.open()
    hub_page.expect_logged_in()


@given("I have no session")
def no_session(context):
    assert context.cookies() == [], "این تست باید بدون لاگین شروع شود"


@given("I open the top-up page")
@when("I open the top-up page")
def open_topup(topup_page, notification_modal):
    topup_page.open()
    notification_modal.close_if_shown(timeout=2000)


@when("I open the DigiPay app")
def open_app(login_page):
    login_page.open()


@then("I should see the login page")
def see_login_page(login_page):
    login_page.phone_field.wait_for(state="visible", timeout=30000)
    assert login_page.is_login_page(), f"انتظار صفحه‌ی ورود را داشتم ولی {login_page.page.url} باز شد"
