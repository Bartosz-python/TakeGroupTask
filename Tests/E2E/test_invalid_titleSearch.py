from playwright.sync_api import expect
import pytest
from utils.pages.dashboardPage import DashboardPage

@pytest.mark.test
def test_invalid_title_search(playwright_setup):

    dashboardPage: DashboardPage = DashboardPage(playwright_setup)
    dashboardPage.navigate()
    dashboardPage.terms_accept()
    dashboardPage.search_for_title("abcxyz123")

    expect(dashboardPage.choose_title("abcxyz123")).to_have_count(0, timeout = 5000)