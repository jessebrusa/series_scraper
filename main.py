from src.data_manager import DataManager  
from src.playwright_manager import PlaywrightManager

class Main:
    def __init__(self):
        self.data_manager = DataManager()
        self.playwright_manager = PlaywrightManager()

    def run(self):
        self.playwright_manager.start_browser(headless=False)
        self.page = self.playwright_manager.get_page()

        self.page.goto('https://www.wcostream.tv/')

        self.playwright_manager.compile_series_data()
        self.playwright_manager.download_episodes()

        self.playwright_manager.close_browser()


if __name__ == "__main__":
    main = Main()
    main.run()