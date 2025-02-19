from playwright.sync_api import sync_playwright
from .playwright_modules.playwright_super import PlaywrightSuper
from .playwright_modules.compile_series_data import Compile_Series_Data
from .playwright_modules.extract_video_url import ExtractVideoUrl

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
            result = 1  
            selected_series = series_list[result]
            return selected_series
        
        compile_series_data = Compile_Series_Data(self.page)
        test_title = 'Naruto'
        series_list = compile_series_data.search_for_series(test_title)
        selected_series = choose_series(series_list)
        self.go_to(f'https://www.wcostream.tv{selected_series["href"]}')
        self.episodes = compile_series_data.get_episode_titles()
        self.episode_data = compile_series_data.get_episode_data()

    def download_episodes(self):   
        for i in range(120, 121):
            print(self.episodes[i]['title'])
            self.go_to(self.episodes[i]['href'])
            if self.episode_data[i][0] is None:
                season_number = '01'
            else:
                season_number = self.episode_data[i][0]
            if self.episode_data[i][1] is None:
                continue
            else:
                episode_number = self.episode_data[i][1]
            
            output_file_name = f's{season_number}e{episode_number}.mp4'
            print(output_file_name)

            extracted_video_url = ExtractVideoUrl(self.page).extract()
            print(extracted_video_url)