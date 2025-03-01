from src.data_manager import DataManager
from src.ask_input import AskInput
from src.playwright_manager import PlaywrightManager
from src.file_manager import FileManager
from src.video_downloader import VideoDownloader
from src.scan_library import ScanLibrary

HEADLESS = True
WORK_DIRECTORY = None

ANIME_TEST_DATA = './data/anime/Digimon Adventure.json'

SKIP_LOAD_TEST_DATA = True
SKIP_DEFINE_MEDIA = True
SKIP_SEARCH_TITLE = True
SKIP_SELECT_TITLE = True
SKIP_COMPILE_EPISODE_DATA = True
SKIP_EXTRACT_VIDEO_LINKS = True
SKIP_DOWNLOAD_VIDEOS = True

class Main:
    def __init__(self):
        self.data_manager = DataManager()
        self.ask_input = AskInput(self.data_manager)
        self.playwright_manager = PlaywrightManager(self.data_manager, HEADLESS)
        self.file_manager = FileManager(directory=WORK_DIRECTORY)

    def run(self):
        if not self.load_test_data(skip=SKIP_LOAD_TEST_DATA, load='anime'):
            print('Failed to load test data. Exiting program...')
            self.playwright_manager.close_browser()
            return

        if not self.define_media(skip=SKIP_DEFINE_MEDIA):
            print('No media type selected. Exiting program...')
            self.playwright_manager.close_browser()
            return 

        if not self.search_title(skip=SKIP_SEARCH_TITLE):
            print('No titles found. Exiting program...')
            self.playwright_manager.close_browser()
            return

        if not self.select_title(skip=SKIP_SELECT_TITLE):
            print('No title selected. Exiting program...')
            self.playwright_manager.close_browser()
            return
        
        if not self.compile_episode_data(skip=SKIP_COMPILE_EPISODE_DATA):
            print('No episodes found. Exiting program...')
            self.playwright_manager.close_browser()
            return

        if not self.extract_video_links(skip=SKIP_EXTRACT_VIDEO_LINKS):
            print('Failed to extract video links. Exiting.')
            self.playwright_manager.close_browser()
            return

        self.create_file_structure()
        self.download_videos(skip=SKIP_DOWNLOAD_VIDEOS)
        
        self.scan_library()

        print('Thanks for using the program!')
        self.playwright_manager.close_browser()

    def load_test_data(self, skip=False, load=False):
        if load == 'anime':
            self.data_manager.load_data(ANIME_TEST_DATA)
            if self.data_manager.get_media_type() is not None:
                return True
        
    def define_media(self, skip=False):
        if not skip:
            return self.ask_input.ask_media_type()
        else:
            return self.data_manager.get_media_type()   

    def search_title(self, skip=False):
        if not skip:
            self.playwright_manager.nav_to_media_type_url()
            self.playwright_manager.search_title(self.ask_input.ask_title())
            self.playwright_manager.collect_titles()
            return self.data_manager.get_searched_titles()
        else:
            return self.data_manager.get_searched_titles()

    def select_title(self, skip=False):
        if not skip:
            self.ask_input.ask_series_title()
            self.playwright_manager.nav_to_series_url()
            return True
        else:
            self.playwright_manager.nav_to_series_url()
            return True

    def compile_episode_data(self, skip=False):
        if not skip:
            self.playwright_manager.collect_episode_data()
            self.data_manager.write_data()
            return True
        else:
            return self.data_manager.get_episodes() 
          
    def create_file_structure(self):
        self.file_manager.create_series_directory(self.data_manager.get_series_title())
        self.file_manager.create_seasons_directories(self.data_manager.get_num_seasons())

    def extract_video_links(self, skip=False):
        if not skip:
            self.playwright_manager.extract_video_links()
            self.data_manager.write_data()
        return self.data_manager.get_episodes()

    def download_videos(self, skip=False):
        if not skip:
            VideoDownloader(self.file_manager, self.data_manager).download_videos()


    def scan_library(self, skip=False):
        if self.data_manager.get_media_type() == 'anime':
            library_id = '5'
        ScanLibrary().scan_library(library_id)

if __name__ == '__main__':
    main = Main()
    main.run()