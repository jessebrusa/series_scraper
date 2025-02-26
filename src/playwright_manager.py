from playwright.sync_api import sync_playwright
from .playwright_modules import PlaywrightSuper

class PlaywrightManager(PlaywrightSuper):
    def __init__(self, data_manager, headless=True):
        super().__init__()
        self.data_manager = data_manager
        self.headless = headless
        self.page = None
        self.open_browser()

    def open_browser(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        self.page.route("**/*", self.route_intercept)

    def nav_to_media_type_url(self):
        self.page.goto(self.data_manager.get_media_type_url())

    def search_title(self, title):
        input_selector = '#searchbox'
        self.page.wait_for_selector(input_selector)
        self.page.fill(input_selector, title)

        submit_button = '#konuara > div > input[type=submit]'
        self.page.wait_for_selector(submit_button)
        self.page.click(submit_button)
        self.page.pause()

    def collect_titles(self):
        title_selector = '.aramadabaslik a'
        self.page.wait_for_selector(title_selector)

        title_selector_list = self.page.query_selector_all(title_selector)

        searched_titles = []
        for title in title_selector_list:
            searched_titles.append({
                'title': title.text_content().strip(),
                'href': title.get_attribute('href')
            })

        self.data_manager.set_searched_titles(searched_titles)

    def close_browser(self):    
        self.page.close()
        self.browser.close()
        self.playwright.stop()
