from src.data_manager import DataManager
from src.file_manager import FileManager
from src.playwright_manager import PlaywrightManager
from src.video_downloader import VideoDownloader

class Main:
    def __init__(self):
        self.data_manager = DataManager('https://www.wcostream.tv/')
        self.file_manager = FileManager()
        self.playwright_manager = PlaywrightManager(self.data_manager)

    def nav_to_site(self):
        self.playwright_manager.start_browser(headless=False)
        self.page = self.playwright_manager.get_page()

        self.page.goto(self.data_manager.base_url)

    def search_anime(self, debug=False):
        if debug:
            title = 'Naruto'
        else:
            title = input('Enter the title of the anime you want to download: ')

        self.playwright_manager.search_for_series(title)
        self.playwright_manager.collect_series_titles()

    def choose_anime(self, debug=False):
        print('Enter the number of the anime you want to download: ')

        for i, anime in enumerate(self.data_manager.get_series_title_options()):
            print(f'{i+1}. {anime["title"]}')
        if debug:
            anime_number = 2
        else:
            anime_number = int(input('Enter the number: '))

        selected_anime = self.data_manager.get_series_title_options()[anime_number-1]
        self.data_manager.set_series_title(selected_anime)

        print(f'You have selected {selected_anime["title"]}')

    def navigate_to_anime_page(self):
        self.page.goto(self.data_manager.get_series_title_href())

    def collect_content_links(self):
        pass

    def filter_non_episodes(self):
        pass

    def format_output_file_name(self):
        pass

    def format_data(self):
        pass

    def extract_video_urls(self):
        pass

    def download_videos(self):
        pass

    def run(self):
        self.nav_to_site()
        self.search_anime(True)
        self.choose_anime(True)
        self.navigate_to_anime_page()

        # self.playwright_manager.compile_series_data()
        # name_video = self.playwright_manager.extract_video_urls()
        # with open('name_video.txt', 'w') as file:
        #     for name in name_video:
        #         file.write(f'{name}\n')

        # self.playwright_manager.close_browser()

        # with open('name_video.txt', 'r') as file:
        #     lines = file.readlines()
        #     name_video = [[lines[i].strip(), lines[i+1].strip()] for i in range(0, len(lines), 2)]

        # if name_video:
        #     downloader = VideoDownloader(name_video, max_workers=10)
        #     try:
        #         downloader.download_videos()
        #     except KeyboardInterrupt:
        #         print("Main process interrupted. Exiting...")

if __name__ == "__main__":
    main = Main()
    main.run()
