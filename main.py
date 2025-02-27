from src.data_manager import DataManager
from src.ask_input import AskInput
from src.playwright_manager import PlaywrightManager
from src.file_manager import FileManager

HEADLESS = True
WORK_DIRECTORY = 'E:/Anime'

SKIP_MEDIA_TYPE = 'Anime'
SKIP_SERIES_TITLES = [{'title': 'Black Clover English Subbed', 'href': '/anime/black-clover-english-subbed'}, {'title': 'Black Clover', 'href': '/anime/black-clover'}, {'title': 'Mugyutto! Black Clover English Subbed', 'href': '/anime/mugyutto-black-clover-english-subbed'}]
SKIP_SERIES_TITLE = {'title': 'Black Clover', 'href': '/anime/black-clover'}

class Main:
    def __init__(self):
        self.data_manager = DataManager()
        self.ask_input = AskInput(self.data_manager)
        self.playwright_manager = PlaywrightManager(self.data_manager, HEADLESS)
        self.file_manager = FileManager(directory=WORK_DIRECTORY)

    def run(self):
        if not self.define_media(skip=True):
            print('No media type selected. Exiting program...')
            return 
        
        if not self.search_title(skip=True):
            print('No titles found. Exiting program...')
            return
        
        if not self.select_title(skip=True):
            print('No title selected. Exiting program...')
            return
        
        if not self.compile_episode_data(skip=True):
            print('No episodes found. Exiting program...')
            return

        if not self.create_file_structure():
            print('Failed to create file structure. Exiting program...')
            return
        


        print('Thanks for using the program!')
        self.playwright_manager.close_browser()
        
    def define_media(self, skip=False):
        if skip:
            self.data_manager.set_media_type(SKIP_MEDIA_TYPE)
            return True
        return self.ask_input.ask_media_type()

    def search_title(self, skip=False):
        if skip:
            self.data_manager.set_searched_titles(SKIP_SERIES_TITLES)
            return True
        self.playwright_manager.nav_to_media_type_url()
        self.playwright_manager.search_title(self.ask_input.ask_title())
        self.playwright_manager.collect_titles()
        return self.data_manager.get_searched_titles()

    def select_title(self, skip=False):
        if skip:
            self.data_manager.set_series_title(SKIP_SERIES_TITLE['title'])
            self.data_manager.set_series_url(SKIP_SERIES_TITLE['href'])
            self.playwright_manager.nav_to_series_url()
            return True
        self.ask_input.ask_series_title()
        self.playwright_manager.nav_to_series_url()
        return True

    def compile_episode_data(self, skip=False):
        if skip:
            self.data_manager.set_episodes([{'episode_title': '1', 'href': '/black-clover-episode-1-english-subbed'}, {'episode_title': '2', 'href': '/black-clover-episode-2-english-subbed'}, {'episode_title': '3', 'href': '/black-clover-episode-3-english-subbed'}])
            self.playwright_manager.collect_episode_data()
            return True
        return self.playwright_manager.collect_episode_data()
    
    def create_file_structure(self):
        self.file_manager.create_series_directory(self.data_manager.get_series_title())
        self.file_manager.create_seasons_directories(self.data_manager.get_num_seasons())
        return True

    def extract_video_links(self):
        pass


if __name__ == '__main__':
    main = Main()
    main.run()