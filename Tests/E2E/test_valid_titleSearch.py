from playwright.sync_api import expect, Locator
from utils.pages.dashboardPage import DashboardPage
from utils.pages.moviePage import MoviePage
import re
from typing import Pattern
import pytest

@pytest.mark.test
def test_valid_title_search(playwright_setup):
    title_under_test: str = "the pickup"
    title_ignored_case: Pattern[str] = re.compile(re.escape(title_under_test), re.IGNORECASE)

    dashboardPage: DashboardPage = DashboardPage(playwright_setup)
    dashboardPage.navigate()
    dashboardPage.terms_accept()
    dashboardPage.search_for_title(title_under_test)
    
    valid_title: Locator = dashboardPage.choose_title(title_under_test)
    expect(valid_title, message = "Title should be visible for the user").to_be_visible()

    moviePage: MoviePage = dashboardPage.enter_title(valid_title)
    movie_header: Locator = moviePage.locate_header()

    expect(movie_header).to_contain_text(title_ignored_case)

    movie_player: Locator = moviePage.locate_player()
    expect(movie_player, message = "The movie player should be visible").to_be_visible()