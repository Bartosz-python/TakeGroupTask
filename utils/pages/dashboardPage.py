from playwright.sync_api import Page, Locator, Playwright

class DashboardPage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self) -> None:
        self.page.goto("https://vod.film/filmy/the-pickup-caly-film")

    def terms_accept(self) -> None:
        agree_btn: Locator = self.page.get_by_role("button", name="Zgadzam się", exact=True)
        agree_btn.click()

    def search_for_title(self, title: str) -> None:
        search_mag_glass: Locator = self.page.get_by_role("img", name="search icon")
        search_mag_glass.click()

        search_input_field: Locator = self.page.locator("#search")
        search_input_field.fill(title)

    def choose_title(self, title: str) -> Locator:
        chosen_title: Locator = self.page.get_by_text(title)
        return chosen_title
    
    def enter_title(self, title: str) -> None:
        try:
            from utils.pages.moviePage import MoviePage
        except ImportError as e:
            print(f"Error occurred while importing module {e}")
        
        chosen_title = self.choose_title(title)
        chosen_title.click()

        return MoviePage(self.page)