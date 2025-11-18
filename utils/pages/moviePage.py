from playwright.sync_api import Page, Locator
import re

class MoviePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def locate_header(self) -> Locator:
        header: Locator = self.page.locator("h1")
        return header
    
    def locate_player(self) -> Locator:
        player: Locator = self.page.locator(".plyr__poster")
        return player

    def press_play(self) -> None:
        play_btn: Locator = self.page.locator("#player-container button").filter(has_text=re.compile(r"^Play$"))
        play_btn.click()
    
    def locate_popup(self) -> Locator:
        popup_register: Locator = self.page.locator("#register-now")
        return popup_register