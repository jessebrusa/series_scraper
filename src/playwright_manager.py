from playwright.sync_api import sync_playwright
from .playwright_modules.playwright_super import PlaywrightSuper
from .playwright_modules.compile_series_data import Compile_Series_Data

class PlaywrightManager(PlaywrightSuper):
    def __init__(self):
        super().__init__()
        self.playwright = sync_playwright().start()
        self.browser = None
        self.page = None

    def start_browser(self, headless=True):
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()

    def compile_series_data(self):
        def choose_series(series_list):
            for i, series in enumerate(series_list):
                print(f'{i+1}: {series["title"]}')
            result = 1  
            selected_series = series_list[result]
            return selected_series
        
        compile_series_data = Compile_Series_Data(self.page)
        test_title = 'Naruto'
        series_list = compile_series_data.search_for_series(test_title)
        selected_series = choose_series(series_list)
        self.go_to(f'https://www.wcostream.tv{selected_series["href"]}')
        episodes = compile_series_data.get_episode_titles()
        for episode in episodes:
            print(episode['title'])
            self.go_to(episode['href'])
            video_play_button_selector = '#video-js > button'
            self.click(video_play_button_selector)
