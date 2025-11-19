import pytest
from playwright.sync_api import Playwright, Browser, Page, BrowserContext
import datetime
import os

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action = "store", default = "chrome", choices = ["chrome", "firefox", "webkit"]
    )

@pytest.fixture
def playwright_setup(playwright: Playwright, request):
    browser_name = request.config.getoption("browser_name")

    if browser_name == "chrome":
        browser: Browser = playwright.chromium.launch(headless = False)
    elif browser_name == "firefox":
        browser: Browser = playwright.firefox.launch(headless = True)
    elif browser_name == "webkit":
        browser: Browser = playwright.webkit.launch(headless = True)

    context: BrowserContext = browser.new_context()
    context.tracing.start(screenshots = True, snapshots = True)

    page: Page = context.new_page()
    page.set_default_timeout(10000)
    page.set_default_navigation_timeout(20000)

    os.makedirs("traces", exist_ok = True)

    try:
        yield page
    finally:
        context.tracing.stop(path = f"traces/{request.node.name}.zip")
        context.close()
        browser.close()

def pytest_configure(config):
    timestamp: str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    config.option.htmlpath = f"test-reports/test_report_{timestamp}.html"