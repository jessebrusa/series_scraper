from src.data_manager import DataManager
from src.file_manager import FileManager
from src.playwright_manager import PlaywrightManager
from src.video_downloader import VideoDownloader

class Main:
    def __init__(self):
        self.data_manager = DataManager()
        self.file_manager = FileManager()
        self.playwright_manager = PlaywrightManager(self.data_manager)

    def nav_to_site(self, headless=True):
        self.playwright_manager.start_browser(headless=headless)
        self.page = self.playwright_manager.get_page()
        self.page.goto(self.data_manager.base_url)

    def search_anime(self, debug=False):
        if debug:
            title = 'Attack on Titan'
        else:
            title = input('Enter the title of the anime you want to download: ')
        self.playwright_manager.search_for_series(title)
        self.playwright_manager.collect_series_titles()

    def choose_anime(self, debug=False):
        if debug:
            anime_number = 1
        else:
            print('Enter the number of the anime you want to download:')
            for i, anime in enumerate(self.data_manager.get_series_title_options()):
                print(f'{i+1}. {anime["title"]}')
            anime_number = int(input('Enter the number: '))
        selected_anime = self.data_manager.get_series_title_options()[anime_number-1]
        self.data_manager.set_series_title(selected_anime)
        self.data_manager.write_series_title()

    def navigate_to_anime_page(self):
        self.page.goto(self.data_manager.get_series_title_href())

    def collect_episode_links(self, write_to_file=False, open_from_file=False):
        if open_from_file:
            self.data_manager.read_episodes()
        self.playwright_manager.collect_episode_titles()
        if write_to_file:
            self.data_manager.write_episodes()

    def filter_episodes(self, open_from_file=False, write_to_file=False):
        if open_from_file:
            self.data_manager.read_episodes()
        self.data_manager.filter_episodes()
        if write_to_file:
            self.data_manager.write_processed_episodes()

    def create_file_structure(self):
        self.file_manager.create_series_directory(self.data_manager.get_series_title())
        self.file_manager.create_seasons_directories(self.data_manager.num_seasons())

    def extract_video_urls(self, open_from_file=False, write_to_file=False):
        if open_from_file:
            self.data_manager.read_processed_episodes()
        self.playwright_manager.extract_video_urls()
        if write_to_file:
            self.data_manager.write_finished_episodes()

    def download_videos(self, read_from_file=False):
        if read_from_file:
            self.data_manager.read_finished_episodes()
        self.create_file_structure() 
        VideoDownloader(self.file_manager, self.data_manager, max_workers=20).download_videos()

    def run(self):
        # self.data_manager.read_series_title()
        self.nav_to_site(headless=True)
        self.search_anime(debug=False)
        self.choose_anime(debug=False)
        self.navigate_to_anime_page()
        self.collect_episode_links(write_to_file=True, open_from_file=False)
        self.filter_episodes(write_to_file=True, open_from_file=False)   
        self.create_file_structure()
        self.extract_video_urls(write_to_file=True, open_from_file=False)
        self.download_videos(read_from_file=False)

if __name__ == "__main__":
    main = Main()
    main.run()