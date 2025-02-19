from src.playwright_manager import PlaywrightManager

class Main:
    def __init__(self):
        self.playwright_manager = PlaywrightManager()

    def run(self):
        # self.playwright_manager.start_browser(headless=False)
        # self.page = self.playwright_manager.get_page()

        # self.page.goto('https://www.wcostream.tv/')

        # self.playwright_manager.compile_series_data()
        # name_video = self.playwright_manager.extract_video_urls()
        # with open('name_video.txt', 'w') as file:
        #     for name in name_video:
        #         file.write(f'{name}\n')

        # self.playwright_manager.close_browser()

        with open('name_video.txt', 'r') as file:
            name_video = file.read()
        print(name_video)


if __name__ == "__main__":
    main = Main()
    main.run()