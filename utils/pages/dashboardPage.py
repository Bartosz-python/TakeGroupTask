from playwright.sync_api import Page, Locator
from utils.pages.moviePage import MoviePage
import re
from typing import Pattern

class DashboardPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self) -> None:
        self.page.goto("https://vod.film/")

    def terms_accept(self) -> None:
        agree_btn: Locator = self.page.get_by_role("button", name="Zgadzam się", exact=True)
        agree_btn.click()

    def search_for_title(self, title: str) -> None:
        search_mag_glass: Locator = self.page.get_by_role("img", name="search icon")
        search_mag_glass.click()

        search_input_field: Locator = self.page.locator("#search")
        search_input_field.fill(title)

    def choose_title(self, title: str | Pattern[str]) -> Locator:
        pattern: Pattern[str] = re.compile(re.escape(title), re.IGNORECASE)
        chosen_title: Locator = self.page.get_by_text(pattern)
        return chosen_title
    
    def enter_title(self, target_title: Locator) -> MoviePage:
        click_the_title: Locator = target_title
        click_the_title.click()

        return MoviePage(self.page)