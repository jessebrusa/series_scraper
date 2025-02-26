from src.data_manager import DataManager
from src.ask_input import AskInput
from src.playwright_manager import PlaywrightManager

SKIP_MEDIA_TYPE = 'Anime'
HEADLESS = True

class Main:
    def __init__(self):
        self.data_manager = DataManager()
        self.ask_input = AskInput(self.data_manager)
        self.playwright_manager = PlaywrightManager(self.data_manager, HEADLESS)

    def run(self):
        if not self.define_media(skip=True):
            self.exit_program()
            return 
             
        self.search_title()

        self.exit_program()
        
    def exit_program(self):
        print('Thanks for using the program!')
        self.playwright_manager.close_browser()

    def define_media(self, skip=False):
        if skip:
            self.data_manager.set_media_type(SKIP_MEDIA_TYPE)
            return SKIP_MEDIA_TYPE
        return self.ask_input.ask_media_type()

    def search_title(self, skip=False):
        self.playwright_manager.nav_to_media_type_url()
        self.playwright_manager.search_title(self.ask_input.ask_title())
        self.playwright_manager.collect_titles()
        print(self.data_manager.searched_titles)


if __name__ == '__main__':
    main = Main()
    main.run()