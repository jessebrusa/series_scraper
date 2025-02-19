from playwright.sync_api import sync_playwright
from .playwright_modules.playwright_super import PlaywrightSuper
from .playwright_modules.compile_series_data import CompileSeriesData
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
        
        compile_series_data = CompileSeriesData(self.page)
        test_title = 'Naruto'
        series_list = compile_series_data.search_for_series(test_title)
        selected_series = choose_series(series_list)
        self.go_to(f'https://www.wcostream.tv{selected_series["href"]}')
        self.episodes = compile_series_data.get_episode_titles()
        self.episode_data = compile_series_data.get_episode_data()

    def download_episodes(self):   
        for i in range(345, 346):  
            episode_index = i - 1  
            print(self.episodes[episode_index]['title'])
            self.go_to(self.episodes[episode_index]['href'])
            if self.episode_data[episode_index][0] is None:
                season_number = '01'
            else:
                season_number = self.episode_data[episode_index][0]
            if self.episode_data[episode_index][1] is None:
                continue
            else:
                episode_number = self.episode_data[episode_index][1]
            
            output_file_name = f's{season_number}e{episode_number}.mp4'
            print(output_file_name)
    
            extracted_video_url = ExtractVideoUrl(self.page).extract()
            print(extracted_video_url)