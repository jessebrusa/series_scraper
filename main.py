from src.data_manager import DataManager
from src.ask_input import AskInput
from src.playwright_manager import PlaywrightManager
from src.file_manager import FileManager

HEADLESS = True
WORK_DIRECTORY = 'E:/Anime'

ANIME_TEST_DATA = './data/anime/Eve no Jikan English Subbed.json'

class Main:
    def __init__(self):
        self.data_manager = DataManager()
        self.ask_input = AskInput(self.data_manager)
        self.playwright_manager = PlaywrightManager(self.data_manager, HEADLESS)
        self.file_manager = FileManager(directory=WORK_DIRECTORY)

    def run(self):
        if not self.load_test_data(load='anime'):
            print('Failed to load test data. Exiting program...')
            self.playwright_manager.close_browser()
            return

        if not self.define_media(skip=True):
            print('No media type selected. Exiting program...')
            self.playwright_manager.close_browser()
            return 
        
        if not self.search_title(skip=True):
            print('No titles found. Exiting program...')
            self.playwright_manager.close_browser()
            return
        
        if not self.select_title(skip=True):
            print('No title selected. Exiting program...')
            self.playwright_manager.close_browser()
            return
        
        if not self.compile_episode_data(skip=True):
            print('No episodes found. Exiting program...')
            self.playwright_manager.close_browser()
            return

        if not self.create_file_structure(skip=True):
            print('Failed to create file structure. Exiting program...')
            self.playwright_manager.close_browser()
            return
        
        if not self.extract_video_links(skip=True):
            print('Failed to extract video links. Exiting.')
            self.playwright_manager.close_browser()
            return

        print(self.data_manager.get_data())

        print('Thanks for using the program!')
        self.playwright_manager.close_browser()

    def load_test_data(self, load=False):
        if load == 'anime':
            self.data_manager.load_data(ANIME_TEST_DATA)
            if self.data_manager.get_media_type() is not None:
                return True
        
    def define_media(self, skip=False):
        if not skip:
            return self.ask_input.ask_media_type()

    def search_title(self, skip=False):
        if not skip:
            self.playwright_manager.nav_to_media_type_url()
            self.playwright_manager.search_title(self.ask_input.ask_title())
            self.playwright_manager.collect_titles()
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
            return self.playwright_manager.collect_episode_data()
        else:
            self.playwright_manager.collect_episode_data()
            return True
          
    def create_file_structure(self, skip=False):
        if not skip:
            self.file_manager.create_series_directory(self.data_manager.get_series_title())
            self.file_manager.create_seasons_directories(self.data_manager.get_num_seasons())

    def extract_video_links(self, skip=False):
        if not skip:
            self.playwright_manager.extract_video_links()
            self.data_manager.write_data()
            return True


if __name__ == '__main__':
    main = Main()
    main.run()