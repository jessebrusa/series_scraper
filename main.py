from src.data_manager import DataManager
from src.ask_input import AskInput
from src.playwright_manager import PlaywrightManager

HEADLESS = False

SKIP_MEDIA_TYPE = 'Anime'
SKIP_SERIES_TITLES = [{'title': 'Black Clover English Subbed', 'href': '/anime/black-clover-english-subbed'}, {'title': 'Black Clover', 'href': '/anime/black-clover'}, {'title': 'Mugyutto! Black Clover English Subbed', 'href': '/anime/mugyutto-black-clover-english-subbed'}]
SKIP_SERIES_TITLE = {'title': 'Black Clover', 'href': '/anime/black-clover'}

class Main:
    def __init__(self):
        self.data_manager = DataManager()
        self.ask_input = AskInput(self.data_manager)
        self.playwright_manager = PlaywrightManager(self.data_manager, HEADLESS)

    def run(self):
        if not self.define_media(skip=True):
            self.exit_program()
            return 
        
        if not self.search_title(skip=True):
            self.exit_program()
            return
        
        if not self.select_title():
            self.exit_program()
            return

        self.exit_program()
        
    def exit_program(self):
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
            return True
        self.ask_input.ask_series_title()
        self.playwright_manager.nav_to_series_url()
        return True


if __name__ == '__main__':
    main = Main()
    main.run()