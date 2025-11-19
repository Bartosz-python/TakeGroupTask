from playwright.sync_api import Page, Locator

class MoviePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def locate_header(self) -> Locator:
        header: Locator = self.page.locator("h1")
        return header
    
    def locate_player(self) -> Locator:
        player: Locator = self.page.locator(".plyr__poster")
        player.scroll_into_view_if_needed()
        return player
    
    def locate_popup(self) -> Locator:
        popup_register: Locator = self.page.locator("#register-now")
        return popup_register