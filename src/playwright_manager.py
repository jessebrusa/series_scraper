from playwright.sync_api import sync_playwright
from .playwright_modules import PlaywrightSuper
from .playwright_modules import TitleAnime
from .playwright_modules import CompileEpisodeAnimeData

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
        if self.data_manager.get_media_type() == 'anime':
            TitleAnime(self.page).search_title(title)
        else:
            print('Media type not supported.')

    def collect_titles(self):
        if self.data_manager.get_media_type() == 'anime':
            self.data_manager.set_searched_titles(TitleAnime(self.page).collect_titles())
        else:
            print('Media type not supported.')

    def nav_to_series_url(self):
        self.page.goto(self.data_manager.get_series_url())

    def collect_episode_data(self):
        episodes = None
        if self.data_manager.get_media_type() == 'anime':
            episodes = CompileEpisodeAnimeData(self.page).get_episodes()
        self.data_manager.set_episodes(episodes)
        return self.data_manager.get_episodes()

    def close_browser(self):    
        self.page.close()
        self.browser.close()
        self.playwright.stop()
