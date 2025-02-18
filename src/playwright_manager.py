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
        def chose_series(title_dict):
            for i, key in enumerate(title_dict.keys()):
                print(f'{i+1}: {key}')
            result = 1  # You can change this to get user input if needed
            selected_key = list(title_dict.keys())[result]
            selected_series = title_dict[selected_key]
            return selected_series
        
        compile_series_data = Compile_Series_Data(self.page)
        test_title = 'Naruto'
        title_dict = compile_series_data.search_for_series(test_title)
        selected_series = chose_series(title_dict)
        self.go_to(f'https://www.wcostream.tv{selected_series}')
        compile_series_data.get_episode_titles()
