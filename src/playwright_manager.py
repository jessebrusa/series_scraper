from playwright.sync_api import sync_playwright
from .playwright_modules import PlaywrightSuper
from .playwright_modules import TitleAnime
from .playwright_modules.compile_anime import CompileEpisodeAnimeData
from .playwright_modules.extract_video_link_anime import ExtractVideoLinkAnime

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

    def extract_video_links(self):
        if self.data_manager.get_media_type() == 'anime':
            self.page.close()
            for index, episode in enumerate(self.data_manager.get_episodes()):
                print(f'Extracting video src: {index + 1}/{len(self.data_manager.get_episodes())}...')
                self.page = self.browser.new_page()
                self.page.goto(episode['href'])
                video_link = ExtractVideoLinkAnime(self.page).extract_video_link()
                self.data_manager.add_video_src(index, video_link)
                self.page.close()
            self.close_browser()
    
    def close_browser(self):    
        self.page.close()
        self.browser.close()
        self.playwright.stop()
