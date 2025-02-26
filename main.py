from src.data_manager import DataManager
from src.define_media import DefineMedia

SKIP_MEDIA_TYPE = 'Anime'

class Main:
    def __init__(self):
        self.data_manager = DataManager()

    def run(self):
        if not self.define_media(skip=False):
            self.exit_program()
            return
        
    def exit_program(self):
        print('Thanks for using the program!')

    def define_media(self, skip=False):
        if skip:
            self.data_manager.set_media_type(SKIP_MEDIA_TYPE)
            return SKIP_MEDIA_TYPE
        return DefineMedia(self.data_manager).ask_media_type()

    def nav_to_search(self):
        pass

    
if __name__ == '__main__':
    main = Main()
    main.run()